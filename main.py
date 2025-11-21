import pygame
import time
import os
import random




WIDTH, HEIGHT = 1000, 800

FPS = 60

LEFT_PADDLE_WIDTH = 20
LEFT_PADDLE_HEIGHT = 100

RIGHT_PADDLE_WIDTH = 20
RIGHT_PADDLE_HEIGHT = 100

BALL_RADIUS = 10

PADDLE_VEL = 15


def draw(WIN, left_paddle, right_paddle, ball_x, ball_y, left_score_text, left_score, right_score_text, right_score):
    WIN.fill((0, 0, 0))

    # Draw paddles
    pygame.draw.rect(WIN, (255, 255, 255), left_paddle)
    pygame.draw.rect(WIN, (255, 255, 255), right_paddle)

    # Draw ball
    pygame.draw.circle(WIN, (255, 255, 255), (int(ball_x), int(ball_y)), BALL_RADIUS)


    # Draw scores
    left_score_surface = left_score_text.render(str(left_score), True, (255, 255, 255))
    WIN.blit(left_score_surface, (WIDTH // 4, 20))

    right_score_surface = right_score_text.render(str(right_score), True, (255, 255, 255))
    WIN.blit(right_score_surface, (WIDTH * 3 // 4 - right_score_surface.get_width(), 20))


    pygame.display.update()

def reset_ball():
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

    ball_vel_x = random.choice([-5, 5])
    ball_vel_y = random.choice([-5, 5])
    return ball_x, ball_y, ball_vel_x, ball_vel_y

def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("placeholder")

    Clock = pygame.time.Clock()
    pygame.mixer.init()

    paddle_sound_path = os.path.join("Assets", "paddle_hit.wav")
    wall_sound_path = os.path.join("Assets", "wall_hit.wav")
    score_sound_path = os.path.join("Assets", "player_score.wav")

    paddle_sound = pygame.mixer.Sound(paddle_sound_path)
    wall_sound = pygame.mixer.Sound(wall_sound_path)
    score_sound = pygame.mixer.Sound(score_sound_path)

    run = True

    left_score_text = pygame.font.SysFont("Arial", 70, bold=True)
    right_score_text = pygame.font.SysFont("Arial", 70, bold=True)

    left_paddle = pygame.Rect(20, HEIGHT // 2, LEFT_PADDLE_WIDTH, LEFT_PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 20 - RIGHT_PADDLE_WIDTH, HEIGHT // 2, RIGHT_PADDLE_WIDTH, RIGHT_PADDLE_HEIGHT)

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

    ball_vel_x = 5
    ball_vel_y = 5

    left_score = 0
    right_score = 0

    while run:

        Clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    left_score = 0
                    right_score = 0
                    left_paddle.y = HEIGHT // 2 - LEFT_PADDLE_HEIGHT // 2
                    right_paddle.y = HEIGHT // 2 - RIGHT_PADDLE_HEIGHT // 2
                    ball_x, ball_y, ball_vel_x, ball_vel_y = reset_ball()
                    pygame.time.delay(500)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and left_paddle.y - PADDLE_VEL > 0: # UP - left paddle
            left_paddle.y -= PADDLE_VEL
        if keys[pygame.K_s] and left_paddle.y + LEFT_PADDLE_HEIGHT + PADDLE_VEL < HEIGHT: # DOWN - left paddle
            left_paddle.y += PADDLE_VEL
        
        if keys[pygame.K_UP] and right_paddle.y - PADDLE_VEL > 0: # UP - right paddle
            right_paddle.y -= PADDLE_VEL
        if keys[pygame.K_DOWN] and right_paddle.y + RIGHT_PADDLE_HEIGHT + PADDLE_VEL < HEIGHT: # DOWN - right paddle
            right_paddle.y += PADDLE_VEL
        

        
        ball_x += ball_vel_x
        ball_y += ball_vel_y

        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
            ball_vel_y *= -1
            wall_sound.play()

        
        ball_rect = pygame.Rect(int(ball_x - BALL_RADIUS), int(ball_y - BALL_RADIUS), BALL_RADIUS * 2, BALL_RADIUS * 2)


        if ball_rect.colliderect(left_paddle):
            ball_vel_x *= -1
            ball_x = left_paddle.right + BALL_RADIUS
            paddle_sound.play()

        if ball_rect.colliderect(right_paddle):
            ball_vel_x *= -1
            ball_x = right_paddle.left - BALL_RADIUS
            paddle_sound.play()
        

        if ball_x - BALL_RADIUS <= 0:
            right_score += 1
            ball_x, ball_y, ball_vel_x, ball_vel_y = reset_ball()
            score_sound.play()

        if ball_x + BALL_RADIUS >= WIDTH:
            left_score += 1
            ball_x, ball_y, ball_vel_x, ball_vel_y = reset_ball()
            score_sound.play()
            


        draw(WIN, left_paddle, right_paddle, ball_x, ball_y, left_score_text, left_score, right_score_text, right_score)
    pygame.quit()


if __name__ == '__main__':
    main()