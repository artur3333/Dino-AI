import pygame
import random
import sys
import math
from enum import Enum

# Configurations
width = 1280
height = 720
background_color = (255, 255, 255)

score = 0
max_score = 0
score_speedup = 100

# Sounds
pygame.init()
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("sounds/jump.wav")
death_sound = pygame.mixer.Sound("sounds/death.wav")


# Animation states class
class DinoAnimState(Enum):
    RUN = 1
    JUMP = 2


# Dino class
class Dino:
    jump_height = 12 # Jump height (d: 12)
    cur_jump_height = jump_height
    sprites = {"run": [], "jump": []}
    run_anim = [0, 5]
    state = DinoAnimState.RUN

    def __init__(self, x, y):
        self.load_sprites()
        self.spriteimage = self.sprites["run"][0]
        self.hitbox = pygame.Rect(x, y, self.sprites["run"][0].get_width(), self.sprites["run"][0].get_height())

    def load_sprites(self):
        self.sprites["run"].append(pygame.image.load("sprites/dino/dino_run1.png"))
        self.sprites["run"].append(pygame.image.load("sprites/dino/dino_run2.png"))
        self.sprites["jump"].append(pygame.image.load("sprites/dino/dino.png"))

    def animation(self):
        if self.state == DinoAnimState.RUN:
            self.run()
        elif self.state == DinoAnimState.JUMP:
            self.jump()

    def run(self):
        self.sprites["run"][0] = pygame.image.load("sprites/dino/dino_run1.png")
        self.sprites["run"][1] = pygame.image.load("sprites/dino/dino_run2.png")
        self.spriteimage = self.sprites["run"][self.run_anim[0] // self.run_anim[1]]

        self.run_anim[0] += 1
        if self.run_anim[0] >= self.run_anim[1] * 2:
            self.run_anim[0] = 0

    def jump(self):
        if self.state == DinoAnimState.JUMP: 
            self.hitbox.y -= self.cur_jump_height * ((game_speed / 8) * 2) # Jump speed
            self.cur_jump_height -= 1 * (game_speed / 16) # Gravity

            if self.hitbox.y >= height - 170: # Ground level
                self.hitbox.y = height - 170 # Ground level (d: 170)
                self.cur_jump_height = self.jump_height
                self.state = DinoAnimState.RUN
        else:
            self.state = DinoAnimState.JUMP
            pygame.mixer.Sound.play(jump_sound)
            self.spriteimage = self.sprites["jump"][0]

    def draw(self, screen):
        screen.blit(self.spriteimage, (self.hitbox.x, self.hitbox.y))


# Cactus class
class Cactus:
    active = True
    all = ["1", "2", "3", "4", "5", "6"]
    cactustype = None

    def __init__(self, x, y):
        self.load_sprites()
        self.hitbox.x = x
        self.hitbox.y = y - self.hitbox.height

    def load_sprites(self):
        if self.cactustype is None:
            self.random_cactus()
        self.spriteimage = pygame.image.load("sprites/cactus/" + self.cactustype + ".png")
        self.hitbox = self.spriteimage.get_rect()
    
    def random_cactus(self):
        self.cactustype = random.choice(self.all)

    def animation(self):
        self.hitbox.x -= game_speed
        if self.hitbox.x < -self.hitbox.width:
            self.active = False
        
    def draw(self, screen):
        screen.blit(self.spriteimage, (self.hitbox.x, self.hitbox.y))


# Main menu
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dino Game - Main Menu")
    pygame.display.set_icon(pygame.image.load('icon.ico'))

    font = pygame.font.SysFont("Artifakt Element Heavy", 50)

    while True:
        screen.fill(background_color)
        title_text = font.render("Select Game Mode", True, (0, 0, 0))
        AI_text = font.render("1. AI Mode (not working yet)", True, (0, 0, 0))
        single_player_text = font.render("2. Manual Mode", True, (0, 0, 0))

        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4))
        screen.blit(AI_text, (width // 2 - AI_text.get_width() // 2, height // 2))
        screen.blit(single_player_text, (width // 2 - single_player_text.get_width() // 2, height // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pass
                elif event.key == pygame.K_2:
                    run_single_player()


# Game over screen (only for single player)
def game_over_screen_single_player():
    global max_score
    max_score = max(max_score, score)

    pygame.mixer.Sound.play(death_sound)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dino Game - Game Over")
    pygame.display.set_icon(pygame.image.load('icon.ico'))

    font = pygame.font.SysFont("Artifakt Element Heavy", 50)
    score_font = pygame.font.SysFont("Verdana", 30)

    while True:
        screen.fill(background_color)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        score_text = score_font.render("Score: " + str(math.floor(score)), True, (0, 0, 0))
        max_score_text = score_font.render("Max Score: " + str(math.floor(max_score)), True, (0, 0, 0))
        play_again_text = font.render("Press Enter to play again", True, (0, 0, 0))
        return_menu_text = font.render("Press Escape to return to main menu", True, (0, 0, 0))

        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
        screen.blit(max_score_text, (width // 2 - max_score_text.get_width() // 2, height // 2 + 50))
        screen.blit(play_again_text, (width // 2 - play_again_text.get_width() // 2, height // 2 + 200))
        screen.blit(return_menu_text, (width // 2 - return_menu_text.get_width() // 2, height // 2 + 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print ("MAX score: " + str(max_score))
                    run_single_player()
                elif event.key == pygame.K_ESCAPE:
                    main_menu()


# Run single player mode
def run_single_player():
    global game_speed, score
    game_speed = 4 # Game speed (d: 4)
    score = 0
    score_speedup = 100

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dino Game - Single Player")
    pygame.display.set_icon(pygame.image.load('icon.ico'))
    clock = pygame.time.Clock()
    road = [[pygame.image.load("sprites/road.png"), [0, height - 100]], [pygame.image.load("sprites/road.png"), [2400, height - 100]]]
    
    score_font = pygame.font.SysFont("Verdana", 20)

    player = Dino(30, height - 170)
    enemies = [Cactus(width + 300, height - 85), Cactus(width * 2, height - 85)]

    while True: # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        press_key = pygame.key.get_pressed()
        if press_key[pygame.K_SPACE] and player.state == DinoAnimState.RUN:
            player.jump()

        screen.fill(background_color)

        # Road animation
        for chunk in road:
            if chunk[1][0] < -2400:
                chunk[1][0] = road[len(road) - 1][1][0] + 2400

                road[0], road[1] = road[1], road[0]
                break

            chunk[1][0] -= game_speed
            screen.blit(chunk[0], chunk[1])

        player.animation()
        player.draw(screen)

        # Draw enemies
        if len(enemies) < 3:
            enemies.append(Cactus(enemies[len(enemies) - 1].hitbox.x + width / random.uniform(0.8, 3), height - 90))

        remove_enemies = []
        for item, enemy in enumerate(enemies):
            enemy.animation()
            enemy.draw(screen)

            if not enemy.active:
                remove_enemies.append(item)
                continue

            if player.hitbox.colliderect(enemy.hitbox):
                game_over_screen_single_player()
                return
        
        for item in remove_enemies:
            enemies.pop(item)

        score += 1 * (game_speed / 8)
        if score >= score_speedup:
            game_speed += 1
            score_speedup += 100 * (game_speed / 4)
        
        # Score label
        score_label = score_font.render("Score: " + str(math.floor(score)), True, (0, 0, 0))
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (width / 2, 50)
        screen.blit(score_label, score_label_rect)

        # Speed label
        score_label = score_font.render("Speed: " + str(game_speed / 4) + "x", True, (0, 0, 0))
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (width - 100, 50)
        screen.blit(score_label, score_label_rect)

        pygame.display.flip()
        clock.tick(60)


# Main
if __name__ == "__main__":
    main_menu()
