import pygame, os
pygame.font.init()
pygame.mixer.init()

# Game settings
WIDTH, HEIGHT = 800, 550
VEL = 3
BULLET_VEL = 6
SW, SH = 50, 50
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Fonts
health_font = pygame.font.SysFont("Pixelify Sans", 60)
winner_font = pygame.font.SysFont("Pixelify Sans", 100)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nebula")

# Assets
border = pygame.Rect(1, 290, WIDTH, 15)
yellow_spaceimg = pygame.image.load("yellow.png")
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceimg, (SW, SH)), 180)
red_spaceimg = pygame.image.load("red.png")
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceimg, (SW, SH)), 0)
bg = pygame.transform.scale(pygame.image.load("orange_space_bg.jpg"), (WIDTH, HEIGHT))

# Bullet handler
def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets[:]:
        bullet.y += BULLET_VEL  # Red bullets go down
        if bullet.colliderect(yellow):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets[:]:
        bullet.y -= BULLET_VEL  # Yellow bullets go up
        if bullet.colliderect(red):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.y < 0:
            yellow_bullets.remove(bullet)

# Ship movement
def yellow_movement(keypressed,yellow):
    if keypressed[pygame.K_a] and yellow.x>10:
        yellow.x-=VEL
    if keypressed[pygame.K_d] and yellow.x+yellow.width<WIDTH:
        yellow.x+=VEL
    if keypressed[pygame.K_w] and yellow.y>border.y+border.height:
        yellow.y-=VEL
    if keypressed[pygame.K_s] and yellow.y+yellow.height<HEIGHT:
        yellow.y+=VEL

def red_movement(keys, red):
    if keys[pygame.K_LEFT] and red.x > 10:
        red.x -= VEL
    if keys[pygame.K_RIGHT] and red.x + red.width < WIDTH:
        red.x += VEL
    if keys[pygame.K_UP] and red.y > 10:
        red.y -= VEL
    if keys[pygame.K_DOWN] and red.y+red.height< border.y:
        red.y += VEL

# Drawing
def draw_screen(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, winner):
    screen.blit(bg, (0, 0))
    
    if winner == "":
        pygame.draw.rect(screen,"white",border)
        screen.blit(yellow_spaceship, (yellow.x, yellow.y))
        screen.blit(red_spaceship, (red.x, red.y))
        
        for bullet in red_bullets:
            pygame.draw.rect(screen, "white", bullet)
        for bullet in yellow_bullets:
            pygame.draw.rect(screen, "white", bullet)
        
        red_health_text = health_font.render("health: " + str(red_health), 1, "white")
        yellow_health_text = health_font.render("health: " + str(yellow_health), 1, "white")
        screen.blit(red_health_text, (WIDTH - 200, 20))
        screen.blit(yellow_health_text, (20, 20))
    else:
        winner_text = winner_font.render(winner, 1, "orange")
        screen.blit(winner_text, (100, HEIGHT / 2 - 50))

    pygame.display.update()

# Main game loop
def main():
    red = pygame.Rect(WIDTH/2, 200, SW, SH)
    yellow = pygame.Rect(WIDTH/2, HEIGHT-200, SW, SH)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LSHIFT:
                    bullet = pygame.Rect(yellow.centerx - 5, yellow.top - 10, 10, 5)
                    yellow_bullets.append(bullet)
                if e.key == pygame.K_RSHIFT:
                    bullet = pygame.Rect(red.centerx - 5, red.bottom + 5, 10, 5)
                    red_bullets.append(bullet)

            if e.type == RED_HIT:
                red_health -= 1
            if e.type == YELLOW_HIT:
                yellow_health -= 1

        winner = ""
        if red_health <= 0:
            winner = "GG yellow WINS U SUCK RED"
        elif yellow_health <= 0:
            winner = "GG red WINS U SUCK YELLOW"

        keys = pygame.key.get_pressed()
        yellow_movement(keys, yellow)
        red_movement(keys, red)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)
        draw_screen(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, winner)

main()
