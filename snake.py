import pygame, sys, random
from pygame.math import Vector2
import time

# Define cores com tema de terror
NIGHT_GREEN = (0, 50, 0)  # Verde escuro para a grama
BLOOD_RED = (139, 0, 0)  # Vermelho sangue
DARK_GRAY = (80, 80, 80)  # Cinza escuro para obstáculos
BACKGROUND_COLOR = (20, 20, 20)  # Preto para o fundo
TEXT_COLOR = (220, 220, 220)  # Cinza claro para o texto
WHITE = (200, 200, 200) # Cinza claro para alguns textos

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        # Carrega imagens padrões
        self.head_up = pygame.image.load('img/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('img/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('img/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('img/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('img/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('img/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('img/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('img/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('img/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('img/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('img/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('img/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('img/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('img/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('som/crunch.wav')
    
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class OBSTACLE: 
    def __init__(self):
        self.randomize()

    def draw_obstacle(self):
        obstacle_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, DARK_GRAY, obstacle_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.lives = 3
        self.score = 0
        self.has_moved = False
        self.apples_collected = 0
        self.apples_to_win = 5
        self.xp = 0
        self.level = 1
        self.level_up = False
        self.obstacle = None
        self.obstacle_chance = 0.2
        self.speed = 150
        self.define_level_goals()
        self.show_objective = True
        self.objective_timer = 2000
        self.objective_start_time = 0

    def update(self):
        if not self.game_over() and self.has_moved and not self.show_objective:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_lives()
        if self.obstacle:
            self.obstacle.draw_obstacle()
        
        if self.show_objective:
            self.draw_objective()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1
            self.apples_collected += 1

            if self.apples_collected >= self.apples_to_win:
                self.xp += 10
                self.apples_collected = 0
                self.level_up = True

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.lose_life()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.lose_life()

        if self.obstacle and self.snake.body[0] == self.obstacle.pos:
            self.lose_life()

    def lose_life(self):
        self.lives -= 1
        if not self.game_over():
            self.reset_snake()

    def game_over(self):
        return self.lives <= 0

    def draw_grass(self):
        for row in range(cell_number):
            if row % 2 == 0: 
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, NIGHT_GREEN, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, NIGHT_GREEN, grass_rect)

    def draw_score(self):
        score_text = str(self.score) 
        score_surface = game_font.render(score_text,True,TEXT_COLOR)
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen,NIGHT_GREEN,bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,NIGHT_GREEN,bg_rect,2)

    def draw_lives(self):
        lives_text = str(self.lives)
        lives_surface = game_font.render(f"Lives: {lives_text} XP: {self.xp}", True, TEXT_COLOR)
        lives_rect = lives_surface.get_rect(topleft=(10, 10))
        screen.blit(lives_surface, lives_rect)
    
    def draw_objective(self):
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        objective_text = f"Level {self.level}: Eat {self.apples_to_win} apples!"
        objective_surface = font.render(objective_text, True, TEXT_COLOR)
        objective_rect = objective_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(objective_surface, objective_rect)
    
    def reset_game(self):
        self.reset_snake()
        self.fruit.randomize()
        self.lives = 3
        self.score = 0
        self.has_moved = False
        self.apples_collected = 0
        self.xp = 0
        self.level = 1
        self.level_up = False
        self.obstacle = None
        self.speed = 150
        self.define_level_goals()
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()

    def reset_snake(self):
        self.snake.reset()
        self.has_moved = False
        self.snake.direction = Vector2(0, 0)

    def next_level(self):
        self.level += 1
        self.apples_collected = 0
        self.reset_snake()
        self.fruit.randomize()
        self.define_level_goals()
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()

        if self.level == 2:
            self.speed = 120
        elif self.level == 3:
            self.speed = 100
            if random.random() < self.obstacle_chance:
                self.obstacle = OBSTACLE()
                while self.obstacle.pos in self.snake.body or self.obstacle.pos == self.fruit.pos:
                    self.obstacle.randomize()
        elif self.level == 4:
            self.speed = 80
            if random.random() < self.obstacle_chance:
                self.obstacle = OBSTACLE()
                while self.obstacle.pos in self.snake.body or self.obstacle.pos == self.fruit.pos:
                    self.obstacle.randomize()
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)
    
    def define_level_goals(self):
        if self.level == 1:
            self.apples_to_win = 10
        elif self.level == 2:
            self.apples_to_win = 15
        elif self.level == 3:
            self.apples_to_win = 20
        elif self.level == 4:
            self.apples_to_win = 25

# ----- Funções da Interface -----
def main_menu(screen):
    pygame.init()

    title_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 80)
    text_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 28)
    start_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)

    phrase = "A fome da criatura é insaciável..."
    typed_text = ""

    def draw_screen():
        screen.fill(BACKGROUND_COLOR)

        title_surface = title_font.render("SNAKE GAME", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 5))
        screen.blit(title_surface, title_rect)

        phrase_surface = text_font.render(typed_text, True, WHITE)
        phrase_rect = phrase_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2.5))
        screen.blit(phrase_surface, phrase_rect)

        start_surface = start_font.render("▶ START", True, TEXT_COLOR)
        start_rect = start_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 1.8))

        pygame.draw.rect(screen, DARK_GRAY, start_rect.inflate(50, 20), border_radius=15)
        pygame.draw.rect(screen, WHITE, start_rect.inflate(50, 20), 4, border_radius=15)
        screen.blit(start_surface, start_rect)

        pygame.display.update()
        return start_rect

    for i in range(len(phrase)):
        typed_text += phrase[i]
        draw_screen()
        time.sleep(0.05) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if draw_screen().collidepoint(mouse_pos):
                    return True
            elif event.type == pygame.KEYDOWN:
                return True
        clock.tick(60)
    return False

def level_up_screen(screen, level):
    font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 35)
    text_surface = font.render(f"Level {level} Completed! Continue...", True, WHITE)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(text_surface, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        clock.tick(60)

# ----- Inicialização do Pygame -----
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('img/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT

main_game = MAIN()

# ----- Loop Principal -----
game_running = main_menu(screen)
pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)

while True:
    if game_running:
        current_time = pygame.time.get_ticks()

        if main_game.show_objective:
            if current_time - main_game.objective_start_time >= main_game.objective_timer:
                main_game.show_objective = False

        if main_game.level_up:
            level_up_screen(screen, main_game.level)
            main_game.next_level()
            main_game.level_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if not main_game.game_over():
                    if not main_game.has_moved:
                        main_game.has_moved = True

                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)
                    elif event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    elif event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)

        screen.fill(BACKGROUND_COLOR)

        if main_game.game_over():
            main_game.reset_game()
            game_running = False

        main_game.draw_elements()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if main_menu(screen):
                    game_running = True
                    main_game.reset_game()
                    pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)
                    break
        screen.fill(BACKGROUND_COLOR)
    pygame.display.update()
    clock.tick(60)