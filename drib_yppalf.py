import pygame
pygame.init()
WIDTH=800
HEIGHT=900
screen=pygame.display.set_mode((WIDTH,HEIGHT))
fps = 60
pygame.display.set_caption("drib yppalf")
scroll_ground=0
scroll_speed=4
#load images
bg=pygame.image.load("flappybord-assets-main/bg.png")
ground=pygame.image.load("flappybord-assets-main/ground.png")



run=True
while run:
    screen.blit(bg,(0,0))
    screen.blit(ground,(scroll_ground,HEIGHT-200))
    scroll_ground=scroll_ground-scroll_speed
    if scroll_ground<-35:
        scroll_ground=0
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            run=False 
            pygame.quit()
    pygame.display.update()