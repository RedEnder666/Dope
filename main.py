#импорт
from player import *
from tkinter import messagebox as mb
# Переменные
clock = pygame.time.Clock()
SKY_COLOR = 75, 187, 253
FLOOR_COLOR = 20, 20, 20
point = 300
shoot = 0
ticks = 0
rotation = 100
FOV = 60
HUD_IMAGE = "HUD.png"
MAX_DEPTH = 300
mx, my = 0, 0
MAP2 = []
PROJ_C = 7000
SCALE = 800 // FOV
SPEED = 3
collisions = []
CENTRE = False
time = 0
FOV_g = pi
world_map = set()

def mapping(a, b):
    return (a // tile_width) * tile_width, (b // tile_width) * tile_width

def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            world_map.add((x * tile_width, y * tile_width))
            if level[y][x] == ' ':
                pass
                #Tile('empty', x, y)
            elif level[y][x] == '*':
                Tile('wall', x, y)
                MAP2.append((x * tile_width, y * tile_width))
                #collisions.append(pygame.Rect((x * tile_width - 25, y * tile_width - 25), (x * tile_width + 25, y * tile_width + 25)))
            elif level[y][x] == ':':
                Tile('wall2', x, y)
                MAP2.append((x * tile_width, y * tile_width))
                #collisions.append(pygame.Rect((x * tile_width - 25, y * tile_width - 25), (x * tile_width + 25, y * tile_width + 25)))
            elif level[y][x] == '?':
                MAP2.append((x * (tile_width // 2), y * (tile_width // 2)))



def render(p):
    global rotation
    tile = tile_width
    for i in range(0, int(FOV * 1.2)):
        ray = p.rect[:2]
        ray[0] += p.w / 2
        ray[1] += p.w / 2
        for depth in range(MAX_DEPTH):
            end = move_by_vec(*ray, rotation + i / FOV, depth)
            if (end[0] // tile * tile, end[1] // tile * tile) in MAP2:
                pheight = min(PROJ_C / (depth + 0.0000000000000000000000000000000000001), 800)
                color = [max(255 - depth, 0)] * 3
                try:
                    if MAP[int(end[0] // tile)][int(end[1] // tile)] == ':':
                        color = [0] * 2 + [max(255 - depth, 0)]
                    else:
                        color = [0] + [max(255 - depth, 0)] * 2
                except:
                    color = [max(255 - depth, 0)] * 3
                pygame.draw.rect(screen, color, (i * SCALE, point - pheight // 2, SCALE, pheight))
                break
        #pygame.draw.line(screen, (0,255,0), ray, end, depth // 10)
        
        
def collide(x, y):
    tile = tile_width
    return (x // tile * tile, y // tile * tile) in MAP2


def col(p):
    points = [(p.pos()[0] - p.w, p.pos()[1]),
              (p.pos()[0] + p.w, p.pos()[1]),
              (p.pos()[0], p.pos()[1] - p.w),
              (p.pos()[0], p.pos()[1] + p.w)]
    if collide(*points[0]):
        p.rect = p.rect.move(SPEED, 0)
    if collide(*points[1]):
        p.rect = p.rect.move(SPEED, 0)
    if collide(*points[2]):
        p.rect = p.rect.move(0, SPEED)
    if collide(*points[3]):
        p.rect = p.rect.move(0, -SPEED)
        
# код
if __name__ == '__main__':
    pygame.init()
    all_sprites.update()
    size = width, height = 800, point  * 2
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    
    mx, my  = 0, 300
    x = [load_image(f"weaps/{i}.png") for i in range(1, 7)] + [load_image(f"weaps/{i}.png") for i in range(6, 1, -1)]
    weapon = Weapon(x, 1)
    weapon.rect.x = width // 2 - 150
    weapon.rect.y = point - 100
    HUD_IMAGE = load_image(HUD_IMAGE, colorkey=-1)
    HUD_IMAGE = pygame.transform.scale(HUD_IMAGE, (width, width // 10))
    HUD = HUD(HUD_IMAGE)
    HUD.rect.x = 0
    HUD.rect.y =520
    player = Player(100, 100, 10)
    
    MAP = load_map("Map.txt")
    
    
    

                    
    generate_level(MAP)
    
    
    while True:
        time += 1
        clock.tick(25)
        keys = pygame.key.get_pressed()
        ticks += 1
        
        #tiles_group.draw(screen)
        render(player)
        all_sprites.draw(screen)
        if shoot != 0 and ticks % weapon.waiting == 0:
            shoot -= 1
            weapon.shoot(1)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shoot == 0:
                    all_sprites.draw(screen)
                    shoot = len(weapon.images)
            
                           
                
            if event.type == pygame.MOUSEMOTION:
                rotation += -(width / 2 - mx) / 500
                mx, my = event.pos
                if CENTRE:
                    pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos((400, my))
                else:
                    pygame.mouse.set_visible(True)
                
                my = height - my
        
            
        playerpos = player.rect[:2]
        playerpos[0] += player.w / 2
        playerpos[1] += player.w / 2
        if playerpos[0] // tile_width > len(MAP) or playerpos[0] // tile_width < 0 or \
        playerpos[1] // tile_width > len(MAP) or playerpos[1] // tile_width < 0:
            mb.showinfo("Вы выбрались из лабиринта!")
            os.startfile('menu.py')
            pygame.quit()
            quit()
        if time >= 4000:
            mb.showinfo("Вы не смогли выбраться из лабиринта!")
            os.startfile('menu.py')
            pygame.quit()
            quit()
        pygame.display.set_caption('Время прошло: ' + str(time))
        # Движение
        
        if keys[pygame.K_a]:
            col(player)
            player.move_vec(rotation, SPEED)
            
        elif keys[pygame.K_d]:
            col(player)
            player.move_vec(rotation, -SPEED)
            
        if keys[pygame.K_s]:
            col(player)
            player.move_vec(rotation + 90, -SPEED)
            
        elif keys[pygame.K_w]:
            col(player)
            player.move_vec(rotation + 90, SPEED)
            
        if keys[pygame.K_c]:
            CENTRE = bool(int(CENTRE + 1) % 2)
            

            
           
        point = my
        
        #tiles_group.draw(screen)
        #player_group.draw(screen)
        hud_group.draw(screen)
        pygame.display.flip()
        screen.fill(SKY_COLOR)
        screen.fill(FLOOR_COLOR, pygame.Rect(0, point, width, height))
        continue
    
    
