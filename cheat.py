import pygame
import random

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Runner")

# Couleurs
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 20, 147)
WHITE = (255, 255, 255)

# Joueur
player_size = 50
player_x = 100
player_y = HEIGHT // 2

# Obstacles
obstacle_width = 20
obstacle_height = 100
obstacle_speed = 6

# Score
score = 0
font = pygame.font.SysFont("consolas", 30)
big_font = pygame.font.SysFont("consolas", 60)

# Horloge
clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.rect(win, NEON_BLUE, (x, y, player_size, player_size), border_radius=8)

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(win, NEON_PINK, obs)

def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    win.blit(text, (10, 10))

def game_over_screen():
    while True:
        win.fill(BLACK)
        over_text = big_font.render("GAME OVER", True, NEON_PINK)
        retry_text = font.render("Appuyez sur R pour Réessayer", True, WHITE)
        quit_text = font.render("Appuyez sur Q pour Quitter", True, WHITE)

        win.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3))
        win.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, HEIGHT//2))
        win.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

def main():
    global player_y, score
    run = True
    gravity = 0.5
    velocity = 0
    obstacles = []
    player_y = HEIGHT // 2
    score = 0

    while run:
        clock.tick(60)
        win.fill(BLACK)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Contrôles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            velocity = -7

        velocity += gravity
        player_y += velocity

        # Bordures
        if player_y < 0:
            player_y = 0
            velocity = 0
        if player_y + player_size > HEIGHT:
            player_y = HEIGHT - player_size
            velocity = 0

        # Obstacles
        if random.randint(1, 30) == 1:
            y_pos = random.randint(0, HEIGHT - obstacle_height)
            obstacles.append(pygame.Rect(WIDTH, y_pos, obstacle_width, obstacle_height))

        for obs in obstacles[:]:
            obs.x -= obstacle_speed
            if obs.colliderect(pygame.Rect(player_x, player_y, player_size, player_size)):
                # Game Over
                if game_over_screen():
                    # Réessayer
                    main()
                else:
                    run = False
            if obs.x + obstacle_width < 0:
                obstacles.remove(obs)
                score += 1

        # Dessin
        draw_player(player_x, player_y)
        draw_obstacles(obstacles)
        show_score(score)

        pygame.display.update()

    pygame.quit()

main()