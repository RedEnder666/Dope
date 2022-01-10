import pygame
import os
import sys
import time
from math import sin, cos, pi
tile_images = {
    'wall': 'box.png',
    'wall2': 'grass.png'
    }
MAP2 = []
WALLWIDTH = 30
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
hud_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
MAP = []
tile_width = tile_height = 30

def move_by_vec(x, y, r, s):
    return x + s * sin(r), y + s * cos(r)
        
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


    
def load_map(file):
    MAP = []
    f = open(file).read().split('\n')
    for i in f:
        MAP.append(list(i))
    return MAP




                
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        if '.' not in tile_type:
            self.image = load_image(tile_images[tile_type])
        else:
            self.image = load_image(tile_type)
        self.image = pygame.transform.scale(self.image, (tile_width, tile_width))
        self.rect = self.image.get_rect().move(
        tile_width * pos_x, tile_height * pos_y)


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, texture):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = load_image(texture + '.png')
        self.image = pygame.transform.scale(self.image, (tile_width, tile_width))
        self.rect = self.image.get_rect().move(x, y)

    def move(self, x, y):
        self.x += x
        self.y += y


    
        
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__(player_group)
        self.image = load_image('player.png')
        self.w = width
        self.rect = self.image.get_rect().move(x, y)
        self.image = pygame.transform.scale(self.image, (width, width))


    def pos(self):
        playerpos = self.rect[:2]
        playerpos[0] += self.w / 2
        playerpos[1] += self.w / 2
        return playerpos
    
    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def move_vec(self, r, s):
        r += 5
        self.move(s * sin(r), s * cos(r))
        
    def collide(self, r, s):
        if (self.pos()[0] // tile_width * tile_width, self.pos()[1] // tile_width * tile_width) in MAP2:
            self.move_vec(r, -(s + 5))


class HUD(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(hud_group)
        self.image = image
        self.rect = self.image.get_rect()

        
class Weapon(pygame.sprite.Sprite):
    def __init__(self, images, w):
        super().__init__(all_sprites)
        self.images = images
        self.i = len(images) // 2 + 1
        self.image = images[self.i]
        self.rect = self.image.get_rect()
        self.waiting = w
        
        
    def shoot(self, i):
        self.i = (self.i + i) % len(self.images)
        self.image = self.images[int(self.i)]


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, i, w=WALLWIDTH):
        width = w
        super().__init__(all_sprites)
        self.image = i
        self.rect = [[x - width, y - width], [x + width, y + width]]


''' 
camera = Camera()
pygame.init()
player = Player(5, 2, 2)
print(player.pos)
player.move_by_vec(0, 1)
print([int(i) for i in player.pos])
'''
