import pygame, sys, random
from pygame.math import Vector2
import time
import os

# Define as cores
NIGHT_GREEN = (0, 50, 0)
BLOOD_RED = (139, 0, 0)
DARK_GRAY = (80, 80, 80)
BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = (220, 220, 220)
WHITE = (200, 200, 200)
GOLD = (255, 215, 0)

# Define o tamanho da célula e o número de células
cell_size = 30
cell_number = 20

# Inicializa o Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Cria a tela
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
apple = pygame.image.load('img/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # Velocidade inicial


# Carrega a imagem do obstáculo
obstaculo_image_path = os.path.join(os.path.dirname(__file__), 'img', 'obstaculo.png')
obstaculo_image = pygame.image.load(obstaculo_image_path).convert_alpha()  # Converte para um formato mais eficiente
obstaculo_image = pygame.transform.scale(obstaculo_image, (cell_size, cell_size))  # Redimensiona a imagem para o tamanho do obstáculo

# Função para gerar uma posição aleatória para os obstáculos
def gera_pos_aleatoria(obstaculo_pos, snake_body):
    """Gera uma posição aleatória para um obstáculo, evitando a cobra."""
    x = random.randint(0, cell_number - 1)
    y = random.randint(0, cell_number - 1)
    pos = Vector2(x, y)
    while pos in obstaculo_pos or pos in snake_body:  # Evita colocar obstáculos em cima da cobra
        x = random.randint(0, cell_number - 1)
        y = random.randint(0, cell_number - 1)
        pos = Vector2(x, y)
    return pos

# Função para verificar colisão entre duas posições (Vector2)
def colisao(pos1, pos2):
    """Verifica se duas posições (Vector2) são iguais."""
    return pos1 == pos2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False
        self.load_assets()  # Carrega as imagens
        self.crunch_sound = pygame.mixer.Sound('som/crunch.wav')

    def load_assets(self):
        """Carrega todos os recursos de imagem da cobra."""
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

    def draw_snake(self):
        """Desenha a cobra na tela."""
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        """Atualiza a imagem da cabeça da cobra com base na direção."""
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        """Atualiza a imagem da cauda da cobra com base na direção."""
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        """Move a cobra."""
        if self.direction == Vector2(0, 0):  # Não move se a direção for zero
            return

        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        """Adiciona um bloco ao corpo da cobra."""
        self.new_block = True

    def play_crunch_sound(self):
        """Toca o som de crunch."""
        self.crunch_sound.play()

    def reset(self):
        """Reseta a cobra para a posição inicial."""
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self, snake_body):
        self.snake_body = snake_body
        self.randomize()
        self.is_special = False

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        """Gera uma posição aleatória para a fruta, evitando a cobra."""
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

        while self.pos in self.snake_body:  # Garante que a fruta não apareça na cobra
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            self.pos = Vector2(self.x, self.y)

        self.is_special = False

    def make_special(self):
        self.is_special = True

class OBSTACLE:
    def __init__(self, snake_body, existing_obstacles):
        self.snake_body = snake_body
        self.existing_obstacles = existing_obstacles
        self.randomize()

    def draw_obstacle(self):
        obstacle_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(obstaculo_image, obstacle_rect)  # Desenha a imagem do obstáculo

    def randomize(self):
        """Gera uma posição aleatória para o obstáculo, evitando a cobra e outros obstáculos."""
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

        while self.pos in self.snake_body or self.pos in self.existing_obstacles:
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self, selected_level):
        self.snake = SNAKE()
        self.fruit = FRUIT(self.snake.body)
        self.lives = 3
        self.score = 0
        self.has_moved = False
        self.apples_collected = 0
        self.apples_to_win = 5
        self.xp = 0
        self.level = selected_level
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
        self.obstacles = []  # Lista para armazenar os obstáculos

    def define_level_goals(self):
        """Define o número de maçãs necessárias para vencer cada nível."""
        if self.level == 1:
            self.apples_to_win = 5
        elif self.level == 2:
            self.apples_to_win = 10
        elif self.level == 3:
            self.apples_to_win = 15
        elif self.level == 4:
            self.apples_to_win = 20

    def increase_speed(self):
        """Aumenta a velocidade da cobra a cada nível, limitando a velocidade máxima."""
        self.speed = max(50, self.speed - 15)
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)  # Atualiza o timer
        print(f"Snake speed increased to: {self.speed}")

    def next_level(self):
        """Avança para o próximo nível."""
        self.level += 1
        if self.level > 4:
            self.level = 1  # Volta para o nível 1 se passar do nível 4

        self.current_background_color = self.background_colors[self.level - 1]
        self.apples_collected = 0
        self.fruit = FRUIT(self.snake.body)
        self.define_level_goals()
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()
        self.increase_speed()
        self.level_complete = False
        self.obstacles = []  # Limpa os obstáculos para o novo nível

        # Redirecionar para a tela inicial
        selected_level = main_menu(screen)
        self.level = selected_level
        self.define_level_goals()
        self.increase_speed()

    def update(self):
        """Atualiza o estado do jogo."""
        if not self.game_over() and self.has_moved and not self.show_objective and not self.level_complete:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        """Desenha todos os elementos do jogo na tela."""
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_lives()
        for obstacle in self.obstacles:  # Desenha todos os obstáculos
            obstacle.draw_obstacle()
        if self.show_objective:
            self.draw_objective()

    def check_collision(self):
        """Verifica a colisão com a fruta."""
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1
            self.apples_collected += 1

            if self.apples_collected >= self.apples_to_win:
                self.level_complete = True
                self.level_complete_timer = pygame.time.get_ticks()
            else:
                self.fruit.randomize()

            # Garante que a nova fruta não apareça em cima da cobra
            while self.fruit.pos in self.snake.body:
                self.fruit.randomize()

    def check_fail(self):
        """Verifica se a cobra bateu na parede ou em si mesma."""
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.lose_life()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.lose_life()
        for obstacle in self.obstacles:
            if self.snake.body[0] == obstacle.pos:
                self.lose_life()

    def lose_life(self):
        """Diminui o número de vidas e reinicia a cobra."""
        self.lives -= 1
        if not self.game_over():
            self.reset_snake()

    def game_over(self):
        """Verifica se o jogo acabou."""
        return self.lives <= 0

    def draw_grass(self):
        """Desenha o fundo do jogo."""
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
        """Desenha a pontuação na tela."""
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
        """Desenha o número de vidas na tela."""
        lives_text = str(self.lives)
        lives_surface = game_font.render(f"Lives: {lives_text} XP: {self.xp}", True, TEXT_COLOR)
        lives_rect = lives_surface.get_rect(topleft=(10, 10))
        screen.blit(lives_surface, lives_rect)

    def draw_objective(self):
        """Desenha o objetivo do nível na tela."""
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        objective_text = f"Level {self.level}: Eat {self.apples_collected}/{self.apples_to_win} apples!"
        objective_surface = font.render(objective_text, True, TEXT_COLOR)
        objective_rect = objective_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(objective_surface, objective_rect)

    def draw_level_complete(self):
        """Desenha a mensagem de nível completo na tela."""
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 60)
        level_complete_text = f"Level {self.level} Complete!"
        level_complete_surface = font.render(level_complete_text, True, WHITE)
        level_complete_rect = level_complete_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(level_complete_surface, level_complete_rect)

    def reset_game(self):
        """Reseta o jogo para o estado inicial."""
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
        self.current_background_color = self.background_colors[0]
        self.level_complete = False
        self.obstacles = []  # Limpa os obstáculos quando o jogo é resetado

    def reset_snake(self):
        """Reseta a cobra para a posição inicial."""
        self.snake.reset()
        self.has_moved = False
        self.snake.direction = Vector2(0, 0)

    def spawn_obstacle(self):
        """Cria um novo obstáculo aleatoriamente."""
        if random.random() < self.obstacle_chance:  # Adiciona obstáculo com certa probabilidade
            new_obstacle = OBSTACLE(self.snake.body, [o.pos for o in self.obstacles])  # Evita sobreposição
            self.obstacles.append(new_obstacle)

def main_menu(screen):
    """Mostra o menu principal e permite selecionar um nível."""
    background_image = pygame.image.load('img/Capa_Prancheta 1.png').convert()
    background_image = pygame.transform.scale(background_image, screen.get_size())
    start_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
    phrase = "Welcome to Snake Game!"
    typed_text = ""

    def draw_screen():
        """Desenha a tela do menu."""
        screen.blit(background_image, (0, 0))
        level_buttons = []
        for i in range(1, 5):
            button_surface = start_font.render(f"Level {i}", True, TEXT_COLOR)
            button_rect = button_surface.get_rect(center=(screen.get_width() // 2 + (i - 2.5) * 150, screen.get_height() // 2 + 150))  # Mais para baixo
            pygame.draw.rect(screen, BLOOD_RED, button_rect.inflate(30, 10), border_radius=15)
            pygame.draw.rect(screen, WHITE, button_rect.inflate(30, 10), 4, border_radius=15)
            screen.blit(button_surface, button_rect)
            level_buttons.append((button_rect, i))
        pygame.display.update()
        return level_buttons

    running = True
    for i in range(len(phrase)):
        typed_text += phrase[i]
        draw_screen()
        time.sleep(0.05)

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
                return 1  # Seleciona o nível 1 por padrão se alguma tecla for pressionada
        clock.tick(60)
    return 1  # Retorna 1 por padrão

# Inicia o jogo
selected_level = main_menu(screen)
main_game = MAIN(selected_level)  # Passa o nível selecionado para o jogo

# Loop principal do jogo
game_running = True
pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)

while True:
    if game_running:
        current_time = pygame.time.get_ticks()

        # Remove a tela de objetivo após um tempo
        if main_game.show_objective and current_time - main_game.objective_start_time >= main_game.objective_timer:
            main_game.show_objective = False

        # Desenha os elementos do jogo
        screen.fill(main_game.current_background_color)
        main_game.draw_elements()
        # Spawna os obstáculos
        if random.random() < 0.005: #Chance de 0,5% de um obstáculo aparecer por frame
            main_game.spawn_obstacle()

        # Lógica quando o nível é completo
        if main_game.level_complete:
            main_game.draw_level_complete()
            if main_game.level_complete_timer is not None and current_time - main_game.level_complete_timer > 2000:
                main_game.next_level()  # Avança para o próximo nível após 2 segundos

    # Tela de Game Over
    else:
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
        game_over_text = font.render("Game Over! Click or press any key to return to the main menu.", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(game_over_text, game_over_rect)

    # Manipulação de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and game_running:
            main_game.update()
        if event.type == pygame.KEYDOWN and game_running:
            if not main_game.has_moved:
                main_game.has_moved = True  # Permite movimento após a primeira tecla
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

        if not game_running and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
            selected_level = main_menu(screen)  # Volta para o menu principal
            main_game = MAIN(selected_level)  # Reinicia o jogo
            game_running = True
            pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)  # Reinicia o timer

    # Verifica Game Over
    if game_running and main_game.game_over():
        game_running = False  # Vai para a tela de Game Over

    pygame.display.update()
    clock.tick(60)