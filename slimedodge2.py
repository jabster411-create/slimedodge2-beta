import pygame
import time
import math
import pygame.font


pygame.init()

WIDTH = 2000
HEIGHT = 800
BG = (135, 206, 235)
FPS = 60

GRAVITY = 0.8
JUMP_STRENGTH = -20
ENEMY_SPEED = 4
y_velocity = 0
is_jumping = False
FLOOR_Y = HEIGHT - 100

WALK_SPEED = 5
SPRINT_SPEED = 10

sprint_timer = 0
cooldown_end_time = 0
MAX_SPRINT_FRAMES = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("slime dodge2")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
ENEMY_SIZE = 65
player = pygame.Rect(100, HEIGHT - PLAYER_HEIGHT - 100, PLAYER_WIDTH, PLAYER_HEIGHT)
player_image = pygame.image.load("player1.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

enemy_image = pygame.transform.scale(pygame.image.load("slime1.png").convert_alpha(), (ENEMY_SIZE, ENEMY_SIZE))
enemy = pygame.Rect(WIDTH - ENEMY_SIZE - 100, 100, ENEMY_SIZE, ENEMY_SIZE)

enemy_hitbox = enemy.inflate(-45, -45)




start_time = time.time()
FONT = pygame.font.SysFont("timesnewroman", 30)
  
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    current_speed = WALK_SPEED
    on_cooldown = current_time < cooldown_end_time

    if not on_cooldown:
        if keys[pygame.K_LSHIFT] and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            current_speed = SPRINT_SPEED
            sprint_timer  += 1

            if sprint_timer >= MAX_SPRINT_FRAMES:
               cooldown_end_time = current_time + 1000
        
        else:       
             if sprint_timer > 0:
                  sprint_timer -= 1

    else:
        
        if sprint_timer == 0:
            sprint_timer -= 2
        if sprint_timer < 0:
            sprint_timer = 0


    if keys[pygame.K_LEFT] and player.x - current_speed > 0:
        player.x -= current_speed
    if keys[pygame.K_RIGHT] and player.x + current_speed + player.width < WIDTH:
        player.x += current_speed
    

    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             running = False
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and not is_jumping:
                y_velocity = JUMP_STRENGTH
                is_jumping = True


    direction_x = player.centerx - enemy.centerx
    direction_y = player.centery - enemy.centery
    distance = math.hypot(direction_x, direction_y)       
        
    if distance > 0:
        enemy.x += round(direction_x / distance * ENEMY_SPEED)
        enemy.y += round(direction_y / distance * ENEMY_SPEED)

        enemy_hitbox.center = enemy.center

        if enemy_hitbox.colliderect(player):
            print("HIT!")
            running = False


  
    y_velocity += GRAVITY
    player.y += y_velocity

     
    

    if player.bottom >= FLOOR_Y:
        player.bottom = FLOOR_Y
        y_velocity = 0
        is_jumping = False



            


    screen.fill(BG)
    pygame.draw.line(screen, (144, 238, 144), (0, FLOOR_Y), (WIDTH,  FLOOR_Y), 80)

    

    screen.blit(player_image, (player.x, player.y))
    screen.blit(enemy_image, enemy)
    
    elapsed = int(time.time() - start_time)
    time_text = FONT.render(f"clock: {elapsed}s", True, "red")
    screen.blit(time_text, (10, 10))
    pygame.display.flip()


pygame.quit()
