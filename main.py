import pygame
import random
import sys
import math
import neat
from enum import Enum


# Configurations
width = 1280
height = 720
background_color = (255, 255, 255)
    
score = 0
max_score = 0
score_speedup = 100
generation = 0

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
    name = ""
    jump_height = 12 # Jump height (d: 12)
    cur_jump_height = jump_height
    sprites = {"run": [], "jump": []}
    run_anim = [0, 5]
    state = DinoAnimState.RUN

    def __init__(self, x, y, name = None):
        if name is not None:
            self.name = name
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

    def draw(self, screen, tag = None):
        screen.blit(self.spriteimage, (self.hitbox.x, self.hitbox.y))

        if tag is not None: # Draw tag over the dino
            tag_label = tag.render(self.name, True, (200, 200, 200))
            tag_label_rect = tag_label.get_rect()
            tag_label_rect.center = (self.hitbox.x + self.hitbox.width / 2, self.hitbox.y - 20)
            screen.blit(tag_label, tag_label_rect)


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

# Day and Night cycle class
class DayNightCycle:
    def __init__(self):
        self.time = 0
        self.day_length = 1200
        self.night_length = 1000
        self.transition_length = 100
        self.day_color = (255, 255, 255)
        self.night_color = (20, 20, 20)
        self.text_day_color = (0, 0, 0)
        self.text_night_color = (255, 255, 255)

        self.state = "day"

        self.background_color = self.day_color
        self.text_color = self.text_day_color

    def update(self):
        if self.state == "day":
            if self.time < self.day_length:
                self.time += 1
            else:
                self.state = "transition_night"
                self.time = 0
            
        elif self.state == "night":
            if self.time < self.night_length:
                self.time += 1
            else:
                self.state = "transition_day"
                self.time = 0

        elif self.state == "transition_night" or self.state == "transition_day":
            if self.time < self.transition_length:
                self.time += 1
                transition = self.time / self.transition_length

                if self.state == "transition_night":
                    self.background_color = [int(self.day_color[i] * (1 - transition) + self.night_color[i] * transition) for i in range(3)]

                    self.text_color = [int(self.text_day_color[i] * (1 - transition) + self.text_night_color[i] * transition) for i in range(3)]

                elif self.state == "transition_day":
                    self.background_color = [int(self.night_color[i] * (1 - transition) + self.day_color[i] * transition) for i in range(3)]

                    self.text_color = [int(self.text_night_color[i] * (1 - transition) + self.text_day_color[i] * transition) for i in range(3)]

            else:
                if self.state == "transition_night":
                    self.state = "night"
                else:
                    self.state = "day"
                
                self.time = 0

                if self.state == "night":
                    self.current_background_color = self.night_color
                else:
                    self.current_background_color = self.day_color

                if self.state == "night":
                    self.current_text_color = self.text_night_color
                else:
                    self.current_text_color = self.text_day_color
        
        return self.background_color, self.text_color


# Main menu
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dino Game - Main Menu")
    pygame.display.set_icon(pygame.image.load('icon.ico'))

    font = pygame.font.SysFont("Artifakt Element Heavy", 40)

    while True:
        screen.fill(background_color)
        title_text = font.render("Select Game Mode", True, (0, 0, 0))
        AI_text = font.render("1. AI (NeuroEvolution) Mode", True, (0, 0, 0))
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
                    # run the AI mode
                    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "config-feedforward.txt")
                    population = neat.Population(config)
                    population.run(run_AI_mode, 1000)

                elif event.key == pygame.K_2:
                    # run the single player mode
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
    act_label_font = pygame.font.SysFont("Georgia", 40)

    while True:
        screen.fill(background_color)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        score_text = score_font.render("Score: " + str(math.floor(score)), True, (0, 0, 0))
        max_score_text = score_font.render("Max Score: " + str(math.floor(max_score)), True, (0, 0, 0))
        play_again_text = act_label_font.render("Press Enter to play again", True, (0, 0, 0))
        return_menu_text = act_label_font.render("Press Escape to return to main menu", True, (0, 0, 0))

        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
        screen.blit(max_score_text, (width // 2 - max_score_text.get_width() // 2, height // 2 + 50))
        screen.blit(play_again_text, (width // 2 - play_again_text.get_width() // 2, height // 2 + 240))
        screen.blit(return_menu_text, (width // 2 - return_menu_text.get_width() // 2, height // 2 + 290))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print ("MAX score: " + str(max_score))
                    run_single_player() # Restart the game
                elif event.key == pygame.K_ESCAPE:
                    main_menu() # Return to main menu


# Run single player mode
def run_single_player():
    global score
    global game_speed
    game_speed = 4 # Game speed (d: 4)
    score = 0
    score_speedup = 100

    day_night_cycle = DayNightCycle()

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dino Game - Single Player")
    pygame.display.set_icon(pygame.image.load('icon.ico'))
    clock = pygame.time.Clock()
    road = [[pygame.image.load("sprites/road.png"), [0, height - 100]], [pygame.image.load("sprites/road.png"), [2400, height - 100]]]
    
    font = pygame.font.SysFont("Verdana", 20)

    player = Dino(30, height - 170, name="")
    enemies = [Cactus(width + 300, height - 85), Cactus(width * 2, height - 85)]

    while True: # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        press_key = pygame.key.get_pressed()
        if press_key[pygame.K_SPACE] and player.state == DinoAnimState.RUN:
            player.jump()

        background_color, text_color = day_night_cycle.update() # Day/Night cycle
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

        # Score update
        score += 1 * (game_speed / 8)
        if score >= score_speedup:
            game_speed += 1
            score_speedup += 100 * (game_speed / 4)
        
        # Score label
        score_label = font.render("Score: " + str(math.floor(score)), True, text_color)
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (width / 2, 50)
        screen.blit(score_label, score_label_rect)

        # Speed label
        score_label = font.render("Speed: " + str(game_speed / 4) + "x", True, text_color)
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (width - 100, 50)
        screen.blit(score_label, score_label_rect)

        pygame.display.flip()
        clock.tick(60)


def distance(pos1, pos2): # Distance between two points (needed for AI mode)
    distance_X = pos1[0] - pos2[0]
    distance_Y = pos1[1] - pos2[1]
    return math.sqrt(distance_X**2 + distance_Y**2)


# Run AI mode
def run_AI_mode(genomes, config):
    global score
    global game_speed
    global score_speedup
    global generation

    game_speed = 4 # Game speed (d: 4)
    score = 0
    generation += 1
    score_speedup = 100

    day_night_cycle = DayNightCycle()

    enemies = [Cactus(width + 300, height - 85), Cactus(width * 2, height - 85)]
    dinosaurs = []
    nets = []
    names = ["Dino1", "Dino2", "Dino3", "Dino4", "Dino5", "Dino6", "Dino7", "Dino8", "Dino9", "Dino10",
             "Dino11", "Dino12", "Dino13", "Dino14", "Dino15", "Dino16", "Dino17", "Dino18", "Dino19", "Dino20"]

    for item, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

        name = "Dino"

        if len(names):
            name = names.pop()

        dinosaurs.append(Dino(30, height - 170, name))
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dino Game - AI (NeuroEvolution) Mode")
    pygame.display.set_icon(pygame.image.load('icon.ico'))
    clock = pygame.time.Clock()
    road = [[pygame.image.load("sprites/road.png"), [0, height - 100]], [pygame.image.load("sprites/road.png"), [2400, height - 100]]]

    font = pygame.font.SysFont("Verdana", 20)
    gen_font = pygame.font.SysFont("Verdana", 40)

    while True: # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        background_color, text_color = day_night_cycle.update() # Day/Night cycle
        screen.fill(background_color)

        # Road animation
        for chunk in road:
            if chunk[1][0] < -2400:
                chunk[1][0] = road[len(road) - 1][1][0] + 2400

                road[0], road[1] = road[1], road[0]
                break

            chunk[1][0] -= game_speed
            screen.blit(chunk[0], chunk[1])
        
        # Dinosaurs
        for dino in dinosaurs:
            dino.animation()
            dino.draw(screen, tag=font)

        if len(dinosaurs) == 0:
            break

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

            for item, dino in enumerate(dinosaurs):
                if dino.hitbox.colliderect(enemy.hitbox):
                    genomes[item][1].fitness -= 10 # Collision penalty
                    dinosaurs.pop(item)
                    genomes.pop(item)
                    nets.pop(item)
        
        for item in remove_enemies:
            enemies.pop(item)

            for item, dino in enumerate(dinosaurs):
                genomes[item][1].fitness += 5 # Passing reward

        # AI jump
        for item, dino in enumerate(dinosaurs):
            output = nets[item].activate((dino.hitbox.y, distance((dino.hitbox.x, dino.hitbox.y), enemies[0].hitbox.midtop), enemies[0].hitbox.width, game_speed))

            if output[0] > 0.5 and dino.state == DinoAnimState.RUN:
                dino.jump()
                genomes[item][1].fitness -= 1 # Jumping penalty
        
        # Score update
        score += 1 * (game_speed / 8)
        if score > score_speedup:
            score_speedup += 100 * (game_speed / 2)
            game_speed += 1
        
        # Score label
        score_label = font.render("Score: " + str(math.floor(score)), True, text_color)
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (width / 2, 100)
        screen.blit(score_label, score_label_rect)

        # Speed label
        score_label = font.render("Speed: " + str(game_speed / 4) + "x", True, text_color)
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (width - 100, 50)
        screen.blit(score_label, score_label_rect)

        # Generation label
        gen_label = gen_font.render("Generation: " + str(generation), True, (255, 0, 0))
        gen_label_rect = gen_label.get_rect()
        gen_label_rect.center = (width / 2, 50)
        screen.blit(gen_label, gen_label_rect)

        # Main menu label
        return_menu_text = font.render("Press Escape to return to main menu", True, text_color)
        return_menu_text_rect = return_menu_text.get_rect()
        return_menu_text_rect.center = (width / 2, height - 25)
        screen.blit(return_menu_text, return_menu_text_rect)

        # display dinosaurs names
        for i, dinosaur in enumerate(dinosaurs):
            dname_label = font.render(dinosaur.name, True, text_color)
            dname_label_rect = dname_label.get_rect()
            dname_label_rect.center = (width - 100, 100 + (i * 25))
            screen.blit(dname_label, dname_label_rect)

        pygame.display.flip()
        clock.tick(60)


# Main
if __name__ == "__main__":
    main_menu()
