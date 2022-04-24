import sys
from battlecity import *
from concurrent import futures
import grpc
import consul
from proto import battlecity_pb2
from proto import battlecity_pb2_grpc


steel_image = pygame.image.load('./img/wall/steels.gif')
wall_image = pygame.image.load('./img/wall/walls.gif')
water_image = pygame.image.load('./img/wall/water.gif')
bullet_image = pygame.image.load("./img/tankmissile.gif")
bg = (0, 0, 0)

screen = pygame.display.set_mode((1200, 900))

class node(battlecity_pb2_grpc.battlecityServiceServicer):
    def __init__(self, name = "p1tank", HOST = '127.0.0.1', PORT = 50051): 
        # Self information
        self.name = name
        self.HOST = HOST
        self.PORT=PORT
        self.consul = consul.Consul()

        self.Clients = {}
        self.Client_tanks = {}


        self.LocalOperations = []

        self.LocalTimestamp = 0

        self.game = game()

        self.wall = []
        self.steel = []
        self.water = []
        self.bullet = []
        self.tid = []
        self.tf = []
        self.tr = []




    def SendTank(self, request, context):
        # self.LocalTimestamp = max(request.timestamp, self.LocalTimestamp) + 1
        tank1 = tank(self.game, eval(request.tank_rect), request.node)
        self.game.add_tank(tank1)
        self.Client_tanks[tank1.id] = tank1
        return battlecity_pb2.AckReply(flag=1, timestamp=self.LocalTimestamp, node=self.name)
    
    def GetMap(self, request, context):
        # print(request)
        # self.LocalTimestamp = max(request.timestamp, self.LocalTimestamp) + 1

        wl = []
        s = [] 
        wr = []
        b = []
        t_id = []
        t_facing = []
        t_rect = []
        for k in self.game.map.wall_group:
            wl.append(str(k.rect))
        for k in self.game.map.steel_group:
            s.append(str(k.rect))
        for k in self.game.map.water_group:
            wr.append(str(k.rect))    
        for bullet in self.game.bullet_group:
            b.append(str(bullet.rect))
        if len(self.game.tanklist) > 0:
            for tank in self.game.tanklist:

                t_id.append(str(tank.id))
                t_facing.append(str(tank.facing))
                t_rect.append(str(tank.rect))

        return battlecity_pb2.MapReply(wall_rect=wl, steel_rect=s, water_rect=wr, bullet_rect=b, tank_id=t_id, tank_facing=t_facing, tank_rect=t_rect, timestamp=self.LocalTimestamp, node=self.name)

    def GetOp(self, request, context):
        self.LocalTimestamp = max(request.timestamp, self.LocalTimestamp)
        op = operation({pygame.K_DOWN:request.down, pygame.K_UP:request.up, pygame.K_LEFT:request.left, pygame.K_RIGHT:request.right, pygame.K_SPACE:request.space}, request.KEYDOWN)
        # print(self.Client_tanks)
        self.Client_tanks[request.node].move_tank(op)
        return battlecity_pb2.AckReply(flag=1, timestamp=self.LocalTimestamp, node=self.name)



    def register(self):
        check = consul.Check.tcp(self.HOST, self.PORT, "10s")
        self.consul.agent.service.register("battlecity", f"{self.name}",address=self.HOST, port=self.PORT, check=check)

    def deregister(self):
        self.consul.agent.service.deregister(f"{self.name}")

    def load_server(self):
        found_service = self.consul.agent.services()
        # print(found_service)
        for name in found_service:
            host = found_service[name]["Address"]
            port = found_service[name]["Port"]
            channel = grpc.insecure_channel(host + ':' + str(port))
            stub = battlecity_pb2_grpc.battlecityServiceStub(channel)
                       
            self.Clients[name] = stub
            # c[name] = stub

    def init_game(self,position=(1000,700),is_server=False):

        main_node = self.name
        for name in self.Clients:
            response = self.Clients[name].SendTank(battlecity_pb2.TankRequest(tank_rect=position, timestamp=self.LocalTimestamp, node=self.name))
            main_node = name
            # print(main_node > name)
            # if main_node > name: main_node = name
        time.sleep(5)

        if is_server:    
            self.game.new_map(load=False)
            time.sleep(5)
        else:
            time.sleep(5)
            map_elements = self.Clients[main_node].GetMap(battlecity_pb2.AckRequest(flag=1, timestamp=self.LocalTimestamp, node=self.name))
            print(map_elements.wall_rect)
            for str_rect in map_elements.wall_rect:
                self.wall.append(str_rect)
            for str_rect in map_elements.steel_rect:
                self.steel.append(str_rect)
            for str_rect in map_elements.water_rect:
                self.water.append(str_rect)
            

    def render(self):
        for rect in self.wall:
            rect = rect.replace("<rect", "")
            rect = rect.replace(">", "")
            screen.blit(wall_image, eval(rect))
        for rect in self.steel:
            rect = rect.replace("<rect", "")
            rect = rect.replace(">", "")
            screen.blit(steel_image, eval(rect))
        for rect in self.water:
            rect = rect.replace("<rect", "")
            rect = rect.replace(">", "")
            screen.blit(water_image, eval(rect))
        for rect in self.bullet:
            rect = rect.replace("<rect", "")
            rect = rect.replace(">", "")
            screen.blit(bullet_image, eval(rect))
        for i in range(0, len(self.tid)):
            f = 'U'
            if self.tf[i] == '1':
                f = 'R'
            if self.tf[i] == '2':
                f = 'D'
            if self.tf[i] == '3':
                f = 'L'
            r = self.tr[i].replace("<rect", "")
            r = r.replace(">", "")
            screen.blit(pygame.image.load("./img/" + str(self.tid[i])+str(f) +".gif"), eval(r))



def start():
    arg = sys.argv
    is_server = arg[3]
    position = arg[1]
    name = arg[2]
    if not (name =='p1tank' or name == 'p2tank' or name == 'p3tank' or name == 'p4tank'):
        print('Unknown tank style')
    if is_server and len(arg) > 5:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        local_node = node(name = name, HOST = arg[4], PORT = int(arg[5]))
        battlecity_pb2_grpc.add_battlecityServiceServicer_to_server(local_node, server)
        server.add_insecure_port('[::]:'+str(local_node.PORT))
        local_node.register()
        time.sleep(20)

        server.start()
    else:
        
        local_node = node(name = name)
        time.sleep(1)

    local_node.load_server()
    local_node.init_game(position, is_server)


    local_node.deregister()
    if is_server:
        local_node.game.run()
    run(local_node)
    while(len(local_node.tid) > 1):
        if is_server:
            local_node.game.run()
        run(local_node)
    if is_server:
        local_node.game.run()
    run(local_node)
    over = pygame.image.load('./img/over.gif')
    over = pygame.transform.scale(over, (1200,900))
    screen.blit(over, over.get_rect())
    pygame.display.flip()
    time.sleep(5)
def run(local_node):
    time.sleep(0.001)


    screen.fill(bg)
    local_node.render()
    # time.sleep(0.005)
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        # for name in c:
            # stub = local_node.Clients[name]
        # print(keys)
        for name in local_node.Clients:

            response = local_node.Clients[name].GetOp(battlecity_pb2.OpRequest(left=keys[pygame.K_LEFT], right=keys[pygame.K_RIGHT], up=keys[pygame.K_UP], 
            down=keys[pygame.K_DOWN], space=keys[pygame.K_SPACE], KEYDOWN=(event.type ==771), timestamp=local_node.LocalTimestamp, node=local_node.name))
    for name in local_node.Clients:
        render_element = local_node.Clients[name].GetMap(battlecity_pb2.AckRequest())
    local_node.wall = render_element.wall_rect
    local_node.steel = render_element.steel_rect
    local_node.water = render_element.water_rect
    local_node.bullet = render_element.bullet_rect
    local_node.tid = render_element.tank_id
    local_node.tf = render_element.tank_facing
    local_node.tr = render_element.tank_rect
    pygame.display.flip()


         
         
if __name__ == '__main__':
    start()