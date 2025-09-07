# PONG by JM V1.0

import pygame
import math

pygame.init()
pygame.mixer.init()
screen_width, screen_height = 480,270
scale_factor = 2
display_width, display_height = screen_width * scale_factor,\
     screen_height * scale_factor
display= pygame.display.set_mode((display_width, display_height))
screen = pygame.Surface((screen_width, screen_height))
clock = pygame.time.Clock()
FPS = 70

# game states
pause = False
menu = True
game_over = False
level_up = False
levelup_time = 0
game_over_time = 0
game_over_duration = 5000

# init sounds
score1_sound = pygame.mixer.Sound('score1.wav')
score2_sound = pygame.mixer.Sound('score2.wav')
paddle1_sound = pygame.mixer.Sound('paddle1_hit.wav')
paddle2_sound = pygame.mixer.Sound('paddle2_hit.wav')
score1_sound.set_volume(0.5)
score2_sound.set_volume(0.5)
paddle1_sound.set_volume(0.5)
paddle2_sound.set_volume(0.5)

BG_COLOR = (0,50,0)
BORDER_COLOR = NET_COLOR = BALL_COLOR = PADDLE_COLOR = (255,255,255)
TEXT_COLOR = (68,255,30)
BALL_INIT_SPEED = 150
PADDLE1_INIT_SPEED = 0
MAX_BALL_SPEED = 600
font = pygame.font.Font("pong_font.ttf", 16)
screen_ctrx, screen_ctry = screen_width//2,screen_height//2
score1 = 0
score2 = 0
level_data = {1:(100,0.5,44),
              2:(150,0.5,44),
              3:(200,0.25,44),
              4:(250,0.25,44),
              5: (300,0,44),
              6: (300,0,34),
              7: (300,0,24),
              8: (300,0,14),
              9: (300,0,6),
              }
current_level = 1
leveled_paddle2_speed, leveled_player2_lookahead, leveled_paddle1_height = level_data[current_level]

# Init ball1
ball_size= 6
ball_speed= BALL_INIT_SPEED
ball_x, ball_y = screen_ctrx, screen_ctry
ball_dirx= 1
ball_diry= 1
ball_angle = 35
ball1_rect = pygame.rect.FRect(screen_ctrx - ball_size //2,screen_ctry - 
                              ball_size //2,ball_size, ball_size)

# Init Paddles
paddle_offset = 4
paddle_width = 6
paddle_height = leveled_paddle1_height
paddle1_speed = PADDLE1_INIT_SPEED
paddle2_speed = leveled_paddle2_speed
paddle_accel = 35
player1_auto = False
paddle1_rect = pygame.rect.FRect(paddle_offset,screen_ctry-
                                (paddle_height//2),paddle_width,paddle_height)
paddle2_rect = pygame.rect.FRect(screen_width-paddle_width-paddle_offset,
                                screen_ctry-(paddle_height//2),
                                paddle_width,paddle_height)

running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # Time since last frame in seconds
# process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWMOVED:
            pause = True  # Set flag when window is moved
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and not menu:
                pause = not pause
            if event.key == pygame.K_RETURN and menu:
                menu = not menu
            
    if not player1_auto and not pause and not game_over and not level_up and not menu:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddle1_rect.top>0:
            paddle1_speed += paddle_accel
            paddle1_rect.centery -= paddle1_speed*dt
           
        if keys[pygame.K_DOWN] and paddle1_rect.bottom < screen_height:
            paddle1_speed += paddle_accel
            paddle1_rect.centery += paddle1_speed*dt
           
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            paddle1_speed = 0
            
        if paddle1_speed > 300:
            paddle1_speed = 300

    if not pause and not menu and not game_over and not level_up:         
# move AI paddle
        if player1_auto:
            if ball1_rect.centerx < screen_ctrx:
                if paddle1_rect.centery> ball1_rect.centery and \
                    paddle1_rect.top>0:
                    paddle1_rect.centery -= paddle1_speed*dt
                if paddle1_rect.centery<ball1_rect.centery and \
                    paddle1_rect.bottom<screen_height:
                    paddle1_rect.centery += paddle1_speed*dt
        if ball1_rect.centerx > screen_width * leveled_player2_lookahead:
            if paddle2_rect.centery>ball1_rect.centery and \
                    paddle2_rect.top>0:
                paddle2_rect.centery -= paddle2_speed*dt
            if paddle2_rect.centery<ball1_rect.centery and \
                    paddle2_rect.bottom<screen_height:
                paddle2_rect.centery += paddle2_speed*dt
                
# handle ball wall bounce
        if ball1_rect.top <=0: 
            ball1_rect.top = 1
            ball_diry *=-1
        if ball1_rect.bottom>=screen_height:
            ball1_rect.bottom = screen_height-1
            ball_diry *=-1

# handle ball and paddle collisions
        if ball1_rect.colliderect(paddle1_rect):
            paddle1_sound.play()
            if ball1_rect.bottom <= paddle1_rect.top + 2 or ball1_rect.top >= paddle1_rect.bottom - 2:
                ball_diry *= -1
            else:
                
                ball_x = paddle1_rect.right+ball_size/2 + 1
                ball_angle = (abs(paddle1_rect.centery - 
                              ball1_rect.centery) /0.5) + 5
                ball_dirx *=-1
                ball_speed *=1.05
                if ball_speed > MAX_BALL_SPEED:
                    ball_speed = MAX_BALL_SPEED
        if ball1_rect.colliderect(paddle2_rect):
            paddle2_sound.play()
            if ball1_rect.bottom <= paddle2_rect.top + 2 or ball1_rect.top >= paddle2_rect.bottom - 2:
                ball_diry *= -1
            else:
                ball_x = paddle2_rect.left-ball_size/2 - 1
                ball_angle = (abs(paddle2_rect.centery - 
                                ball1_rect.centery) /0.5) + 5
                ball_dirx *=-1
                ball_speed *=1.05
                if ball_speed > MAX_BALL_SPEED:
                    ball_speed = MAX_BALL_SPEED
# score/reset ball
        if ball1_rect.centerx > screen_width:
            #reset ball
            score1_sound.play()
            score1+=1
            ball_speed = BALL_INIT_SPEED
            ball_dirx *=-1
            ball_angle = 35
            ball_x = screen_ctrx
            ball_y = screen_ctry
        if ball1_rect.centerx < 0:
            #reset ball
            score2_sound.play()
            score2+=1
            ball_speed = BALL_INIT_SPEED
            ball_dirx *=-1
            ball_angle = 35
            ball_x = screen_ctrx
            ball_y = screen_ctry
# check for win
        if score1 ==11 or score1-score2==3:
            level_up = True
            levelup_time = pygame.time.get_ticks()  # Record time of game over

        if score2 ==11 or score2-score1==3:
            game_over = True
            game_over_time = pygame.time.get_ticks()  # Record time of game over

# calculate dx,dy - the ball incremental move per frame
        '''ball x increment = cos( angle) * speed *  x direction
        ball y increment = sin( angle) * speed * x direction
        COS(angle) * ball speed keeps the ball speed the same at any angle
        Ball direction is - or + depending on up/down/left/right
        This setting makes it easy to change the ball direction 
        after IF statement'''
        ball_dx = math.cos(ball_angle/180*math.pi)*(ball_speed*dt)*ball_dirx
        ball_dy = math.sin(ball_angle/180*math.pi)*(ball_speed*dt)*ball_diry 
        ball_x +=ball_dx
        ball_y +=ball_dy
# move the ball in x,y
        ball1_rect.centerx = ball_x
        ball1_rect.centery = ball_y
# draw objects
    screen.fill((BG_COLOR))
    score1_text = font.render(str(score1), False, TEXT_COLOR)  
    score1_text_rect = score1_text.get_rect(center=(screen_width//4, 15))  
    score2_text = font.render(str(score2), False, TEXT_COLOR)
    score2_text_rect = score2_text.get_rect(center=(screen_width*3//4, 15))   
    screen.blit(score1_text, score1_text_rect)
    screen.blit(score2_text, score2_text_rect)
    pygame.draw.rect(screen,BORDER_COLOR,(0,0,480,270),1)
    for netlines in range(8):
        pygame.draw.line(screen,NET_COLOR,(screen_width//2,netlines * 35 + 5),(screen_width//2,netlines*35 + 20))
    pygame.draw.rect(screen,BALL_COLOR,ball1_rect)
    pygame.draw.rect(screen,BALL_COLOR,paddle1_rect)
    pygame.draw.rect(screen,BALL_COLOR,paddle2_rect)

# Game State logic
    if menu:
        menu_text = font.render("Pong by JM", False, 
                                 TEXT_COLOR)  
        menu_text2 = font.render("Press ENTER to start", False, 
                                 TEXT_COLOR)  
        menu_text3 = font.render("Press ESC anytime to QUIT. W and S move the paddle", False, 
                                 TEXT_COLOR)         
        menu_text_rect = menu_text.get_rect(center=(screen_width//2, 30))    
        menu_text_rect2 = menu_text2.get_rect(center=(screen_width//2, 67))
        menu_text_rect3 = menu_text3.get_rect(center=(screen_width//2, 102))    
        screen.blit(menu_text, menu_text_rect)
        screen.blit(menu_text2, menu_text_rect2)
        screen.blit(menu_text3, menu_text_rect3)



    if pause:
        pause_text = font.render("PAUSED - Press SPACE to resume", False, 
                                 TEXT_COLOR)  
        pause_text_rect = pause_text.get_rect(center=(screen_width//2, 67))    
        screen.blit(pause_text, pause_text_rect)
    
    if game_over:
        game_over_text = font.render("GAME OVER", False, 
                                     TEXT_COLOR)  
        game_over_text_rect = game_over_text.get_rect(center=(screen_width//2, 99))    
        screen.blit(game_over_text, game_over_text_rect)
        if pygame.time.get_ticks() - game_over_time >= game_over_duration:
            game_over = False
            menu = True
            score1 = 0
            score2 = 0
            current_level = 1
            leveled_paddle2_speed, leveled_player2_lookahead, leveled_paddle1_height = level_data[current_level]
            paddle2_speed = leveled_paddle2_speed
            paddle1_rect.height = leveled_paddle1_height
            paddle1_rect.centery = screen_height//2
            paddle2_rect.centery = screen_height//2

    if level_up:
        level_up_text = font.render(f"Leveling up to level {current_level+1}...", False, 
                                     TEXT_COLOR)  
        level_up_text_rect = level_up_text.get_rect(center=(screen_width//2, 99))    
        screen.blit(level_up_text, level_up_text_rect)
        paddle1_rect.centery = screen_height//2
        paddle2_rect.centery = screen_height//2
        if pygame.time.get_ticks() - levelup_time >= game_over_duration:
            
            score1 = 0
            score2 = 0
            current_level +=1
            if current_level >9:
                current_level = 9
            leveled_paddle2_speed, leveled_player2_lookahead, leveled_paddle1_height = level_data[current_level]
            paddle2_speed = leveled_paddle2_speed
            paddle1_rect.height = leveled_paddle1_height
            paddle1_rect.centery = screen_height//2
            paddle2_rect.centery = screen_height//2
            level_up = False
            
    scaled_screen = pygame.transform.scale(screen, (display_width, 
                                                    display_height))
    display.blit(scaled_screen, (0, 0))

    pygame.display.flip()
     
pygame.quit()
