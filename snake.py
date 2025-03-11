import pygame, sys, random
from pygame.math import Vector2
import time
import os

NIGHT_GREEN = (0, 50, 0)
BLOOD_RED = (139, 0, 0)
DARK_GRAY = (80, 80, 80)
BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = (220, 220, 220)
WHITE = (200, 200, 200)
GOLD = (255, 215, 0)

cell_size = 30
cell_number = 20
import os

# Carrega a imagem do obstáculo
obstaculo_image_path = os.path.join(os.path.dirname(__file__), 'img', 'obstaculo.png')
obstaculo_image = pygame.image.load(obstaculo_image_path)
obstaculo_image = pygame.transform.scale(obstaculo_image, (cell_size, cell_size))  # Redimensiona a imagem para o tamanho do obstáculo
# Função para gerar uma posição aleatória para os obstáculos
def gera_pos_aleatoria(obstaculo_pos):
    x = random.randint(0, cell_number - 1) * cell_size
    y = random.randint(0, cell_number - 1) * cell_size

    if (x, y) in obstaculo_pos:
        return gera_pos_aleatoria(obstaculo_pos)

    return x, y
obstaculo_pos = [gera_pos_aleatoria([]) for _ in range(5)]  # Gera 5 obstáculos aleatórios
def colisao(pos1, pos2):
    return pos1 == pos2
class SNAKE:
    def __init__(self):
        # Inicializa o corpo da cobra como uma lista de vetores 2D.
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        # Define a direção inicial da cobra (parada).
        self.direction = Vector2(0, 0)
        # Flag para indicar se um novo bloco deve ser adicionado ao corpo da cobra.
        self.new_block = False
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
                # Determina a orientação do segmento do corpo com base nos segmentos vizinhos.
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
    def __init__(self, snake_body):
        self.snake_body = snake_body
        self.randomize()
        self.is_special = False

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

        # GARANTE QUE A FRUTA NÃO APAREÇA NA COBRA
        while self.pos in self.snake_body:
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            self.pos = Vector2(self.x, self.y)
        self.is_special = False

    def make_special(self):
        self.is_special = True

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
        self.fruit = FRUIT(self.snake.body)
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
        self.level_complete = False
        self.speed = 150
        self.background_colors = [BACKGROUND_COLOR, NIGHT_GREEN, BLOOD_RED, DARK_GRAY]
        self.current_background_color = self.background_colors[0]
        self.show_objective = True
        self.objective_timer = 2000
        self.objective_start_time = 0
        self.define_level_goals()
        self.increase_speed()
        self.obstaculo_pos = [gera_pos_aleatoria([]) for _ in range(5)]  # Gera 5 obstáculos aleatórios

    # Outras funções da classe MAIN...

    def define_level_goals(self):
        if self.level == 1:
            self.apples_to_win = 10
        elif self.level == 2:
            self.apples_to_win = 15
        elif self.level == 3:
            self.apples_to_win = 20
        elif self.level == 4:
            self.apples_to_win = 25
        if self.level == 1:
            self.apples_to_win = 10
        elif self.level == 2:
            self.apples_to_win = 15
        elif self.level == 3:
            self.apples_to_win = 20
        elif self.level == 4:
            self.apples_to_win = 25
    
    def increase_speed(self):
        self.speed = max(50, self.speed - 15)
        print(f"Snake speed increased to: {self.speed}")
    
    def next_level(self):
        self.level += 1
        if self.level > 4:
            self.level = 1  # Wrap around to level 1 if we exceed the number of levels
    
        self.current_background_color = self.background_colors[self.level - 1]
        self.apples_collected = 0
        self.fruit = FRUIT(self.snake.body)  # Passa o corpo da cobra atualizado
        self.define_level_goals()
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()
        self.increase_speed()  # Aumenta a velocidade da cobra
        self.level_complete = False
        self.level_complete_timer = None
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)
    
        # Redirecionar para a tela inicial
        selected_level = main_menu(screen)
        self.level = selected_level
        self.define_level_goals()
        self.increase_speed()

    def update(self):
        if not self.game_over() and self.has_moved and not self.show_objective and not self.level_complete:
            self.snake.move_snake() # Move a cobra.
            self.check_collision() # Verifica se houve colisão com a fruta.
            self.check_fail() # Verifica se a cobra bateu em algo.

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

    # Outras funções da classe MAIN...

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1  # Aumenta a pontuação em 1 por maçã
            self.apples_collected += 1

            # Se o número de maçãs coletadas for maior ou igual ao número de maçãs necessárias para vencer.
            if self.apples_collected >= self.apples_to_win:
                self.level_complete = True # Define a flag de nível completo como True.
                self.level_complete_timer = pygame.time.get_ticks() # Define o tempo em que o nível foi completado.
            else:
                self.fruit.randomize()


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
            for col in range(cell_number):
                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, (30, 30, 30), grass_rect) # Desenha um retângulo cinza escuro.
                else:
                    pygame.draw.rect(screen, (10, 10, 10), grass_rect) # Desenha um retângulo cinza muito escuro.
        border_rect = pygame.Rect(0, 0, CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE)
        pygame.draw.rect(screen, BLOOD_RED, border_rect, 3)

    def draw_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, TEXT_COLOR)
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
        pygame.draw.rect(screen, NIGHT_GREEN, bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, NIGHT_GREEN, bg_rect, 2)

    def draw_lives(self):
        lives_text = str(self.lives)
        lives_surface = game_font.render(f"Lives: {lives_text} XP: {self.xp}", True, TEXT_COLOR)
        lives_rect = lives_surface.get_rect(topleft=(10, 10))
        screen.blit(lives_surface, lives_rect)

    def draw_objective(self):
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        objective_text = f"Level {self.level}: Eat {self.apples_collected}/{self.apples_to_win} apples!"
        objective_surface = font.render(objective_text, True, TEXT_COLOR)
        objective_rect = objective_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(objective_surface, objective_rect)
    
    def draw_level_complete(self):
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 60)
        level_complete_text = f"Level {self.level} Complete!"
        level_complete_surface = font.render(level_complete_text, True, WHITE)
        level_complete_rect = level_complete_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(level_complete_surface, level_complete_rect)


    def reset_game(self):
        self.reset_snake()
        self.fruit = FRUIT(self.snake.body)
        self.lives = 3
        self.score = 0
        self.has_moved = False
        self.apples_collected = 0
        self.xp = 0
        self.level = 1
        self.level_up = False
        self.obstacle = None
        self.obstacle_chance = 0.2
        self.speed = 150
        self.define_level_goals()
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()
        self.current_background_color = self.background_colors[0]  # Reset background color
        self.level_complete = False
        self.level_complete_timer = None


    def reset_snake(self):
        self.snake.reset()
        self.has_moved = False
        self.snake.direction = Vector2(0, 0)
def next_level(self):
    self.level += 1
    if self.level > 4:
        self.level = 1  # Wrap around to level 1 if we exceed the number of levels

    self.current_background_color = self.background_colors[self.level - 1]
    self.apples_collected = 0
    self.fruit = FRUIT(self.snake.body)  # Passa o corpo da cobra atualizado
    self.define_level_goals()
    self.show_objective = True
    self.objective_start_time = pygame.time.get_ticks()
    self.increase_speed()  # Aumenta a velocidade da cobra
    self.level_complete = False
    self.level_complete_timer = None
    pygame.time.set_timer(SCREEN_UPDATE, self.speed)

    # Redirecionar para a tela inicial
    selected_level = main_menu(screen)
    self.level = selected_level
    self.define_level_goals()
    self.increase_speed()

    def define_level_goals(self):
        if self.level == 1:
            self.apples_to_win = 10
        elif self.level == 2:
            self.apples_to_win = 15
        elif self.level == 3:
            self.apples_to_win = 20
        elif self.level == 4:
            self.apples_to_win = 25

    def increase_speed(self):
        # Aumenta a velocidade da cobra a cada nível
        self.speed = max(50, self.speed - 15)  # Diminui o intervalo, aumentando a velocidade
        print(f"Snake speed increased to: {self.speed}")
def main_menu(screen):
    pygame.init()
    background_image = pygame.image.load('img/Capa_Prancheta 1.png').convert()
    background_image = pygame.transform.scale(background_image, screen.get_size())
    start_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
    phrase = "Bem-vindo ao Jogo da Cobra!"
    typed_text = ""

    def draw_screen():
        screen.blit(background_image, (0, 0))
        level_buttons = []
        for i in range(1, 5):
            button_surface = start_font.render(f"Nível {i}", True, TEXT_COLOR)
            button_rect = button_surface.get_rect(
                center=(screen.get_width() // 2 + (i - 2.5) * 150, screen.get_height() // 2 + 150))  # Mais para baixo
            pygame.draw.rect(screen, BLOOD_RED, button_rect.inflate(30, 10), border_radius=15)
            pygame.draw.rect(screen, WHITE, button_rect.inflate(30, 10), 4, border_radius=15)
            screen.blit(button_surface, button_rect)
            level_buttons.append((button_rect, i))
        pygame.display.update()
        return level_buttons

    # Animação de digitação inicial
    for i in range(len(phrase)):
        typed_text += phrase[i]
        draw_screen()
        time.sleep(0.05)

    # Loop do menu principal
    running = True
    while running:
        level_buttons = draw_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button_rect, level in level_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        return level
            elif event.type == pygame.KEYDOWN:
                return 1
        clock.tick(60)
    return 1
    pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
apple = pygame.image.load('img/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT

selected_level = main_menu(screen)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT(self.snake.body)
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
        self.level_complete = False
        self.speed = 150
        self.background_colors = [BACKGROUND_COLOR, NIGHT_GREEN, BLOOD_RED, DARK_GRAY]
        self.current_background_color = self.background_colors[0]
        self.show_objective = True
        self.objective_timer = 2000
        self.objective_start_time = 0
        self.define_level_goals()
        self.increase_speed()
        self.obstaculo_pos = [gera_pos_aleatoria([]) for _ in range(5)]  # Gera 5 obstáculos aleatórios

    # Outras funções da classe MAIN...

    def define_level_goals(self):
        if self.level == 1:
            self.apples_to_win = 10
        elif self.level == 2:
            self.apples_to_win = 15
        elif self.level == 3:
            self.apples_to_win = 20
        elif self.level == 4:
            self.apples_to_win = 25
        if self.level == 1:
            self.apples_to_win = 10
        elif self.level == 2:
            self.apples_to_win = 15
        elif self.level == 3:
            self.apples_to_win = 20
        elif self.level == 4:
            self.apples_to_win = 25
    
    def increase_speed(self):
        self.speed = max(50, self.speed - 15)
        print(f"Snake speed increased to: {self.speed}")
    
    def next_level(self):
        self.level += 1
        if self.level > 4:
            self.level = 1  # Wrap around to level 1 if we exceed the number of levels
    
        self.current_background_color = self.background_colors[self.level - 1]
        self.apples_collected = 0
        self.fruit = FRUIT(self.snake.body)  # Passa o corpo da cobra atualizado
        self.define_level_goals()
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()
        self.increase_speed()  # Aumenta a velocidade da cobra
        self.level_complete = False
        self.level_complete_timer = None
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)
    
        # Redirecionar para a tela inicial
        selected_level = main_menu(screen)
        self.level = selected_level
        self.define_level_goals()
        self.increase_speed()
    def update(self):
        if not self.game_over() and self.has_moved and not self.show_objective and not self.level_complete:
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

    # Outras funções da classe MAIN...

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1  # Aumenta a pontuação em 1 por maçã
            self.apples_collected += 1

            if self.apples_collected >= self.apples_to_win:
                self.level_complete = True
                self.level_complete_timer = pygame.time.get_ticks()
            else:
                self.fruit.randomize()


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
            for col in range(cell_number):
                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, (30, 30, 30), grass_rect)
                else:
                    pygame.draw.rect(screen, (10, 10, 10), grass_rect)
        border_rect = pygame.Rect(0, 0, cell_number * cell_size, cell_number * cell_size)
        pygame.draw.rect(screen, BLOOD_RED, border_rect, 3)

    def draw_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, TEXT_COLOR)
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
        pygame.draw.rect(screen, NIGHT_GREEN, bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, NIGHT_GREEN, bg_rect, 2)

    def draw_lives(self):
        lives_text = str(self.lives)
        lives_surface = game_font.render(f"Lives: {lives_text} XP: {self.xp}", True, TEXT_COLOR)
        lives_rect = lives_surface.get_rect(topleft=(10, 10))
        screen.blit(lives_surface, lives_rect)

    def draw_objective(self):
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        objective_text = f"Level {self.level}: Eat {self.apples_collected}/{self.apples_to_win} apples!"
        objective_surface = font.render(objective_text, True, TEXT_COLOR)
        objective_rect = objective_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(objective_surface, objective_rect)
    
    def draw_level_complete(self):
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 60)
        level_complete_text = f"Level {self.level} Complete!"
        level_complete_surface = font.render(level_complete_text, True, WHITE)
        level_complete_rect = level_complete_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(level_complete_surface, level_complete_rect)


    def reset_game(self):
        self.reset_snake()
        self.fruit = FRUIT(self.snake.body)
        self.lives = 3
        self.score = 0
        self.has_moved = False
        self.apples_collected = 0
        self.xp = 0
        self.level = 1
        self.level_up = False
        self.obstacle = None
        self.obstacle_chance = 0.2
        self.speed = 150
        self.define_level_goals()
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()
        self.current_background_color = self.background_colors[0]  # Reset background color
        self.level_complete = False
        self.level_complete_timer = None


    def reset_snake(self):
        self.snake.reset()
        self.has_moved = False
        self.snake.direction = Vector2(0, 0)

main_game = MAIN()
main_game.level = selected_level
main_game.define_level_goals()
main_game.increase_speed()

game_running = True
pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)

while True:
    if game_running:
        current_time = pygame.time.get_ticks()
        if main_game.show_objective:
            if current_time - main_game.objective_start_time >= main_game.objective_timer:
                main_game.show_objective = False

        screen.fill(main_game.current_background_color)  # Setting the background color
        main_game.draw_elements()

        # Desenha os obstáculos e verifica colisão
        for pos in obstaculo_pos:
            if colisao((main_game.snake.body[0].x * cell_size, main_game.snake.body[0].y * cell_size), pos):
                main_game.lose_life()
            screen.blit(obstaculo_image, pos)

        if main_game.level_complete:
            main_game.draw_level_complete()
            if current_time - main_game.level_complete_timer > 2000:
                main_game.next_level()
        
    else:
        screen.fill(BACKGROUND_COLOR)  # Fill with default background color when game is over

    if not game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                selected_level = main_menu(screen)
                main_game = MAIN()
                main_game.level = selected_level
                main_game.define_level_goals()
                main_game.increase_speed()
                game_running = True
                pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)
                break
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if not main_game.game_over() and not main_game.level_complete:
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

        if main_game.game_over():
            main_game.reset_game()
            game_running = False

    pygame.display.update()
    clock.tick(60)