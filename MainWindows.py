import pygame
from pygame.locals import *

pygame.init()
size = (1460,800)
size2 = (1000,600)
width, height = size
screen = pygame.display.set_mode(size,0,0,0,0)
screen2 = pygame.display.set_caption('oulala')
running = True
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
key_dict = {K_k:BLACK, K_r:RED, K_g:GREEN, K_b:BLUE,
K_y:YELLOW, K_c:CYAN, K_m:MAGENTA, K_w:WHITE, KMOD_LSHIFT+K_r: GRAY}
print(key_dict)
background = MAGENTA
screen.fill(background)
pygame.display.update()
ball = pygame.image.load("ball.gif")
speed = [2, 2]
rect = ball.get_rect()
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in key_dict:
                background = key_dict[event.key]
                caption = 'background color = ' + str(background)
                pygame.display.set_caption(caption)

            #if event.key == K_g:
             #   background = GREEN
            #if event.key == K_y:
             #   background = YELLOW
        if event.type == pygame.QUIT:
            running = False
    rect = rect.move(speed)
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]
    screen.fill(background)
    polyg = pygame.draw.polygon(screen, RED, [(120,324),(32,65)], width)
    pygame.draw.rect(screen, BLUE, rect, width)
    pygame.draw.circle(screen, RED, (120, 324), 60, width)
    pygame.draw.circle(screen, RED, (200, 324), 60, width)
    pygame.draw.rect(screen, RED, (130, 200, 62,300), width)
    pygame.draw.circle(screen, RED, (150, 470), 35, width)
    screen.blit(ball,rect)
    pygame.display.update()
pygame.quit()