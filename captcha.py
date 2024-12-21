import pygame
from random import randint
from typing import *

pygame.init()
screen = pygame.display.set_mode((500,500))
running = True
captcha_show = False
grid_width = 3
grid_height = 3
num_captchas = grid_width
idxs = [x for x in range(randint(1,9))]
humanity_proven = False
rects = []

def font_renderer(color, font_size=20, **texts: Tuple[str, Tuple[int,  int]]):
    font_objs = []
    for _ , value in texts.items():
        font = pygame.font.Font(None, font_size)
        font_surface = font.render(value[0], True, color)
        font_rect = font_surface.get_rect(topleft = value[1])
        font_objs.append((font_surface, font_rect))
    return font_objs

def screen_blitter(list_of_objs):
    for surface, rect in list_of_objs:
        screen.blit(surface, rect)

def start_screen():
    text = "Hey! I'm not so sure you're not a robot. Prove you're a human!"
    continue_to_captcha = "Press [Enter] to prove your humanity!"
    
    objs = font_renderer('white', font_size=20, a=(text, (0,0)), b=(continue_to_captcha, (0,100)))
    screen_blitter(objs)

def proved_humanity_screen():
    text = "Humanity proven! I no longer believe you are an android!"
    
    objs = font_renderer('white', font_size=24, a=(text, (0,0)))
    screen_blitter(objs)

def grid(x, y, s):
    for row in range(x):
        for col in range(y):
            rects.append(pygame.Rect((s * row) + (screen.width // 2 - (x * s // 2)), s * col 
                                     + (screen.height // 2 - (y * s // 2)), s, s,))

def setup():
    grid(3,3,100)

def random_color():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    return color

def capthcha_colors():
    c_color = random_color()
    return c_color

captcha_color = capthcha_colors()

def captcha_screen(rect_color, border_color, border_size, captcha_color= captcha_color):
    screen.fill('orange')
    objs = font_renderer('white', font_size=24, t1=("Click all the sqaures that aren't:", (100,0)))
    pygame.draw.rect(screen, rect_color, pygame.Rect(350, 2,  15, 15))
    screen_blitter(objs)

    for r in rects:
        if rects.index(r) not in idxs:
            pygame.draw.rect(screen, rect_color, r)
            pygame.draw.rect(screen, border_color, r, border_size)
        else:
            pygame.draw.rect(screen, captcha_color, r)
            pygame.draw.rect(screen, border_color, r, border_size)

def valid_selection():
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for r in rects:
        if mouse_pos_x in range(r.x, r.x + r.width) and mouse_pos_y in range(r.y, r.y + r.height):
              if pygame.mouse.get_pressed()[0]:
                  return [True, rects.index(r)]
setup()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not humanity_proven:
                    captcha_show = not captcha_show
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                b, r = valid_selection()
                if b:
                    if r in idxs:
                        idxs.pop(idxs.index(r))
                        if len(idxs) == 0:
                            humanity_proven = True
                            captcha_show = False #this whole thing ugly and could probably be cleaned, but this was just for fun.
                            #and it work.
            except:
                pass
            

    screen.fill('black')
    
    if not captcha_show and not humanity_proven:
        start_screen()
    if captcha_show and not humanity_proven:
        captcha_screen('blue', 'black', 2)
    if not captcha_show and humanity_proven:
        proved_humanity_screen()
        
    pygame.display.update()
pygame.quit()