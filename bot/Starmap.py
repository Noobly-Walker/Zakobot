import sys, pygame, math
pygame.init()

size = width, height = 1200, 700
black = 0, 0, 0
scale = 'full' #full or half
tpf = 20

if scale == 'full':
    subfolder = '100_scale\\'
    mag = 1
elif scale == 'half':
    subfolder = '50_scale\\'
    mag = 0.5
elif scale == 'double':
    subfolder = '200_scale\\'
    mag = 2

screen = pygame.display.set_mode(size)

class GameObject:
    def __init__(self, image, height, speed):
        image = pygame.image.load('starmap_textures\\'+subfolder+image)
        self.imgwidth = image.get_width()
        self.speed = speed
        self.image = image
        self.half = self.imgwidth//2
        self.pos = image.get_rect().move(height[0]-self.half, height[1]-self.half)
        self.center = (height[0], height[1])
        
    def move(self):
        #self.pos = self.pos.move(self.speed)
        self.center = (self.pos[0]+self.half, self.pos[1]+self.half)
        
    def orbit(self, radius, center:tuple, location:tuple, speed):
        a = center[0]
        b = center[1]
        x = location[0]-a
        y = location[1]-b
        r = radius
        s = speed

        theta = math.atan2(y,x) + s
        return (r * math.cos(theta)+a, r * math.sin(theta)+b)
    
    def orbit_obj(self, obj, dist, spd):
        if type(obj) is tuple:
            x1, y1 = obj[0].center
            x2, y2 = obj[1].center
            anchor = ((x1+x2)/2, (y1+y2)/2)
            a1, b1 = obj[0].speed
            a2, b2 = obj[1].speed
            objspeed = ((a1+a2)/2, (b1+b2)/2)
        else:
            anchor = obj.center
            objspeed = obj.speed
        pos_offset = (self.pos[0]+self.half, self.pos[1]+self.half)
        new_pos = self.orbit(dist, anchor, pos_offset, spd)
        self.pos = (new_pos[0]-self.half+objspeed[0], new_pos[1]-self.half+objspeed[1])
        self.center = (self.pos[0]+self.half, self.pos[1]+self.half)

def orbital_speed(dist):
    try:
        return min(0.4, 1234/dist**2.5)
    except Exception:
        return 0
bodyclass = {'MS':'M-star.png', 'KS':'K-star.png', 'GS':'G-star.png',
             'FS':'F-star.png', 'AS':'A-star.png', 'BS':'B-star.png',
             'OS':'O-star.png',
             'BP':'B-planet.png', 'DP':'D-planet.png', 'HP':'H-planet.png', 'JP':'J-planet.png',
             'MP':'M-planet.png', 'NP':'N-planet.png', 'PP':'P-planet.png',
             'YP':'Y-planet.png'}

# Object Name: [Class, (Spawn Coords), (Speed), Orbiting, Orbit Dist]
KEG051 = {'KEG051':['GS', (width//2, height//2), (0, 0), 'KEG051', 0],
          'KEG051-1':['BP', (500, 300), (0, 0), 'KEG051', 50],
          'KEG051-2':['NP', (500, 300), (0, 0), 'KEG051', 70],
          'KEG051-3':['MP', (500, 300), (0, 0), 'KEG051', 110],
          'KEG051-4':['MP', (500, 300), (0, 0), 'KEG051', 150],
          'KEG051-5':['MP', (500, 300), (0, 0), 'KEG051', 210],
          'KEG051-6':['JP', (500, 300), (0, 0), 'KEG051', 330],
          'KEG051-7':['JP', (500, 300), (0, 0), 'KEG051', 470],
          'KEG051-3a':['DP', (500, 300), (0, 0), 'KEG051-3', 20],
          'KEG051-4a':['DP', (500, 300), (0, 0), 'KEG051-4', 20],
          'KEG051-5a':['DP', (500, 300), (0, 0), 'KEG051-5', 20],
          'KEG051-5b':['DP', (500, 300), (0, 0), 'KEG051-5', 30],
          'KEG051-6a':['DP', (500, 300), (0, 0), 'KEG051-6', 30],
          'KEG051-6b':['DP', (500, 300), (0, 0), 'KEG051-6', 40],
          'KEG051-6c':['DP', (500, 300), (0, 0), 'KEG051-6', 50],
          'KEG051-7a':['DP', (500, 300), (0, 0), 'KEG051-7', 30],
          'KEG051-7b':['DP', (500, 300), (0, 0), 'KEG051-7', 40]}

KEG045 = {'KEG045':['GS', (width//2-(600*mag), height//2), (0, 0), 'KEB045', 1200],
          'KEB045':['BS', (width//2+(600*mag), height//2), (0, 0), 'KEG045', 1200],
          'KEG045-1':['BP', (500, 300), (0, 0), 'KEG045', 50],
          'KEG045-2':['BP', (500, 300), (0, 0), 'KEG045', 80],
          'KEG045-3':['MP', (500, 300), (0, 0), 'KEG045', 110],
          'KEG045-4':['MP', (500, 300), (0, 0), 'KEG045', 190],
          'KEG045-6':['PP', (500, 300), (0, 0), 'KEG045', 290],
          'KEG045-7':['JP', (500, 300), (0, 0), 'KEG045', 400],
          'KEB045-1':['BP', (500, 300), (0, 0), 'KEB045', 50],
          'KEB045-2':['BP', (500, 300), (0, 0), 'KEB045', 100],
          'KEB045-3':['HP', (500, 300), (0, 0), 'KEB045', 140],
          'KEB045-4':['MP', (500, 300), (0, 0), 'KEB045', 210],
          'KEG045-3a':['DP', (500, 300), (0, 0), 'KEG045-3', 20],
          'KEG045-4a':['DP', (500, 300), (0, 0), 'KEG045-4', 20],
          'KEG045-6a':['DP', (500, 300), (0, 0), 'KEG045-6', 20],
          'KEG045-6b':['DP', (500, 300), (0, 0), 'KEG045-6', 30],
          'KEG045-7a':['DP', (500, 300), (0, 0), 'KEG045-7', 30],
          'KEG045-7b':['DP', (500, 300), (0, 0), 'KEG045-7', 40],
          'KEG045-7c':['DP', (500, 300), (0, 0), 'KEG045-7', 50],
          'KEB045-2a':['DP', (500, 300), (0, 0), 'KEB045-2', 20],
          'KEB045-3a':['DP', (500, 300), (0, 0), 'KEB045-3', 20],
          'KEB045-4a':['DP', (500, 300), (0, 0), 'KEB045-4', 20],
          'KEB045-4b':['DP', (500, 300), (0, 0), 'KEB045-4', 30]}

test = {'stara':['GS', (width//2-(50*mag), height//2), (0, 0), 'starb', 100],
        'starb':['GS', (width//2+(50*mag), height//2), (0, 0), 'stara', 100],
        'planet':['MP', (width//2+(100*mag), height//2), (0, 0), ('stara', 'starb'), 150]}

active = test
objects = {}

for i in active:
    objects[i] = GameObject(bodyclass[active[i][0]], active[i][1], active[i][2])

framebuffer = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #Slow the animation down
    if framebuffer == tpf:
        for i in objects:
            objects[i].move()
            if type(active[i][3]) is tuple:
                objects[i].orbit_obj((objects[active[i][3][0]], objects[active[i][3][1]]), active[i][4]*mag, orbital_speed(active[i][4]))
            else:
                objects[i].orbit_obj(objects[active[i][3]], active[i][4]*mag, orbital_speed(active[i][4]))
        
        framebuffer = 0
    framebuffer += 1
    
    screen.fill(black)
    for i in objects:
        screen.blit(objects[i].image, objects[i].pos)
    
    pygame.display.flip()
