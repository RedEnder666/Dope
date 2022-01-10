import pygame
if __name__ == '__main__':
    from main import *
from player import *

def render(p, screen):
    global rotation
    tile = tile_width
    for i in range(FOV + 3):
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
                if MAP[int(end[0] // tile)][int(end[1] // tile)] != '?':
                    pygame.draw.rect(screen, color, (i * SCALE, point - pheight // 2, SCALE, pheight))
                else:
                    Entity((i * SCALE, point - pheight // 2), ['0', '1'])
                break
        #pygame.draw.line(screen, (0,255,0), ray, end, depth // 10)
