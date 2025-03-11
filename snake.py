import pygame, sys, random
from pygame.math import Vector2
import time
import os

# --- CONSTANTES ---
NIGHT_GREEN = (0, 50, 0)
BLOOD_RED = (139, 0, 0)
DARK_GRAY = (80, 80, 80)
BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = (220, 220, 220)
WHITE = (200, 200, 200)
GOLD = (255, 215, 0)

CELL_SIZE = 30
CELL_NUMBER = 20

JUMP_SCARE_DURATION = 2000  # Milissegundos para exibir o jump scare
JUMP_SCARE_FADE_DURATION = 500  # Milissegundos para fade-in e fade-out do jump scare

# --- FUNÇÕES AUXILIARES ---

def generate_random_position(occupied_positions):
    """Gera uma posição aleatória para um objeto, garantindo que não esteja em posições ocupadas."""
    x = random.randint(0, CELL_NUMBER - 1)
    y = random.randint(0, CELL_NUMBER - 1)
    pos = Vector2(x, y)

    if pos in occupied_positions:
        return generate_random_position(occupied_positions)  # Chamada recursiva se a posição estiver ocupada

    return pos

def check_collision(pos1, pos2):
    """Verifica se duas posições são as mesmas, indicando uma colisão."""
    return pos1 == pos2

# --- OBJETOS DO JOGO ---

class Snake:
    """Representa a cobra no jogo."""
    def __init__(self):  # Remova o parâmetro level
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False  # Flag para indicar se um novo bloco deve ser adicionado
        self.load_images() # nao passa parametro

        # Carrega som de mastigação
        self.crunch_sound = pygame.mixer.Sound('som/crunch.wav')

    def load_images(self): # Remova o parâmetro level
        """Carrega imagens das partes do corpo da cobra."""
        base_path = 'img/JA' # Caminho base para as imagens

        try:
            self.head_up = pygame.image.load(f'{base_path}/j_head_up.png').convert_alpha()
            self.head_down = pygame.image.load(f'{base_path}/j_head_down.png').convert_alpha()
            self.head_right = pygame.image.load(f'{base_path}/j_head_right.png').convert_alpha()
            self.head_left = pygame.image.load(f'{base_path}/j_head_left.png').convert_alpha()

            self.tail_up = pygame.image.load(f'{base_path}/j_tail_up.png').convert_alpha()
            self.tail_down = pygame.image.load(f'{base_path}/j_tail_down.png').convert_alpha()
            self.tail_right = pygame.image.load(f'{base_path}/j_tail_right.png').convert_alpha()
            self.tail_left = pygame.image.load(f'{base_path}/j_tail_left.png').convert_alpha()

            self.body_vertical = pygame.image.load(f'{base_path}/j_body_vertical.png').convert_alpha()
            self.body_horizontal = pygame.image.load(f'{base_path}/j_body_horizontal.png').convert_alpha()

            self.body_tr = pygame.image.load(f'{base_path}/j_body_tr.png').convert_alpha()  # canto superior direito
            self.body_tl = pygame.image.load(f'{base_path}/j_body_tl.png').convert_alpha()  # canto superior esquerdo
            self.body_br = pygame.image.load(f'{base_path}/j_body_br.png').convert_alpha()  # canto inferior direito
            self.body_bl = pygame.image.load(f'{base_path}/j_body_bl.png').convert_alpha()  # canto inferior esquerdo

        except FileNotFoundError as e:
            print(f"Erro ao carregar imagens da cobra: {e}.  Certifique-se de que os nomes das imagens estejam corretos (por exemplo, `j_head_up.png` em todos os diretórios) e que as pastas existam.")
            pygame.quit()
            sys.exit()

    def draw_snake(self):
        """Desenha a cobra na tela, usando as imagens corretas para cabeça, cauda e segmentos do corpo."""
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                # Determina a orientação do segmento do corpo com base nos segmentos vizinhos
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:  # Peças de canto
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        """Atualiza a imagem da cabeça da cobra com base em sua direção de movimento."""
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
        """Atualiza a imagem da cauda da cobra com base em sua direção de movimento."""
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
        """Move a cobra adicionando uma nova cabeça e removendo a cauda (a menos que um bloco seja adicionado)."""
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)  # Adiciona nova cabeça
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]  # Remove a cauda
            body_copy.insert(0, body_copy[0] + self.direction)  # Adiciona nova cabeça
            self.body = body_copy[:]

    def add_block(self):
        """Define a flag para adicionar um novo bloco à cobra no próximo movimento."""
        self.new_block = True

    def play_crunch_sound(self):
        """Toca o efeito sonoro de mastigação."""
        self.crunch_sound.play()

    def reset(self):
        """Redefine a cobra para seu estado inicial."""
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class Fruit:
    """Representa a fruta que a cobra come."""
    def __init__(self, snake_body, obstacle_positions):
        self.snake_body = snake_body
        self.obstacle_positions = obstacle_positions  # Armazena as posições dos obstáculos como Vector2
        self.is_special = False
        self.randomize()

    def draw_fruit(self):
        """Desenha a fruta na tela."""
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(apple, fruit_rect)  # Supondo que 'apple' seja uma imagem carregada

    def randomize(self):
        """Gera uma posição aleatória para a fruta, garantindo que não esteja na cobra ou nos obstáculos."""
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

        # Garante que a fruta não esteja na cobra ou nos obstáculos
        while self.pos in self.snake_body or self.pos in self.obstacle_positions:
            self.x = random.randint(0, CELL_NUMBER - 1)
            self.y = random.randint(0, CELL_NUMBER - 1)
            self.pos = Vector2(self.x, self.y)
        self.is_special = False

    def make_special(self):
        """Marca a fruta como uma fruta especial (para implementação futura)."""
        self.is_special = True

class Obstacle:
    """Representa um obstáculo que a cobra deve evitar."""
    def __init__(self):
        self.pos = generate_random_position([])  # Posição aleatória inicial
        self.rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)

    def draw_obstacle(self):
        """Desenha o obstáculo na tela."""
        self.rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(obstaculo_image, self.rect)  # Desenha a imagem do obstáculo

    def randomize(self, occupied_positions):
        """Gera uma posição aleatória para o obstáculo, evitando posições ocupadas."""
        self.pos = generate_random_position(occupied_positions)
        self.rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)

# --- LÓGICA DO JOGO ---

class Main:
    """Gerencia a lógica principal do jogo, incluindo níveis, pontuação, colisões e estado do jogo."""
    def __init__(self):
        self.level = 1
        self.snake = Snake()  # Não passe o nível aqui!
        self.obstacles = [Obstacle() for _ in range(5)]  # Cria 5 objetos de obstáculo
        self.obstacle_positions = [obstacle.pos for obstacle in self.obstacles]  # Armazena as posições dos obstáculos como Vector2
        self.fruit = Fruit(self.snake.body, self.obstacle_positions)

        self.lives = 3
        self.score = 0
        self.has_moved = False  # Flag para impedir o movimento antes que uma tecla seja pressionada
        self.apples_collected = 0
        self.apples_to_win = 5  # Valor inicial, pode ser alterado em define_level_goals
        self.xp = 0
        self.level_up = False  # Flag para identificar o aumento de nível
        self.obstacle_chance = 0.2
        self.level_complete = False
        self.speed = 150  # Milissegundos entre as atualizações da tela
        self.background_colors = [BACKGROUND_COLOR, NIGHT_GREEN, BLOOD_RED, DARK_GRAY]
        self.current_background_color = self.background_colors[0]  # Define a cor de fundo inicial
        self.show_objective = True
        self.objective_timer = 2000  # Milissegundos para mostrar o objetivo
        self.objective_start_time = 0
        self.define_level_goals()
        self.increase_speed()

        # Carrega a imagem de vida
        try:
            self.life_image = pygame.image.load('img/coracao.png').convert_alpha()  # Substitua 'img/coracao.png' pelo caminho da sua imagem
            self.life_image = pygame.transform.scale(self.life_image, (25, 25))  # Ajusta o tamanho conforme necessário

            # Carrega a imagem de Game Over
            self.game_over_image = pygame.image.load('img/game-over_Prancheta 1.jpg').convert_alpha()  # substitua pelo nome correto
            self.game_over_image = pygame.transform.scale(self.game_over_image, (600, 600))  # Ajuste conforme necessário
        except FileNotFoundError as e:
            print(f"Erro ao carregar imagens: {e}. Verifique os arquivos de imagem (coracao.png, game-over_Prancheta 1.jpg).")
            pygame.quit()
            sys.exit()

        # Carrega a imagem do jump scare
        try:
            self.jump_scare_image = pygame.image.load('img/jumpscare.jpg').convert_alpha()  # Substitua 'img/jumpscare.png' pelo caminho da sua imagem
            self.jump_scare_image = pygame.transform.scale(self.jump_scare_image, screen.get_size())  # Ajusta para o tamanho da tela
        except FileNotFoundError as e:
            print(f"Erro ao carregar a imagem do jump scare: {e}. Verifique o arquivo 'img/jumpscare.png'.")
            self.jump_scare_image = None  # Desativa o jump scare se a imagem não for encontrada

        # Carrega o som do jump scare
        try:
            self.jump_scare_sound = pygame.mixer.Sound('som/jumpscare.mp3')  # Substitua 'som/jumpscare.wav' pelo caminho do seu som
        except FileNotFoundError:
            print("Aviso: Arquivo de som do jump scare não encontrado. O jogo continuará sem o som.")
            self.jump_scare_sound = None

        self.show_jump_scare = False
        self.jump_scare_start_time = 0
        self.jump_scare_alpha = 0

    def define_level_goals(self):
        """Define quantas maçãs a cobra deve comer para completar o nível atual."""
        if self.level == 1:
            self.apples_to_win = 10
        elif self.level == 2:
            self.apples_to_win = 15
        elif self.level == 3:
            self.apples_to_win = 20
        elif self.level == 4:
            self.apples_to_win = 25

    def increase_speed(self):
        """Aumenta a velocidade da cobra, tornando o jogo mais difícil."""
        self.speed = max(50, self.speed - 15)
        print(f"Velocidade da cobra aumentada para: {self.speed}")

    def next_level(self):
        """Avança o jogo para o próximo nível."""
        self.level += 1
        if self.level > 4:
            self.level = 1  # Volta ao nível 1 se excedermos o número de níveis

        self.current_background_color = self.background_colors[self.level - 1]
        self.apples_collected = 0
        # Redefine as posições dos obstáculos na transição de nível.
        for obstacle in self.obstacles:
            occupied_positions = self.snake.body + [o.pos for o in self.obstacles if o != obstacle]
            obstacle.randomize(occupied_positions)
        self.obstacle_positions = [obstacle.pos for obstacle in self.obstacles]

        self.fruit = Fruit(self.snake.body, self.obstacle_positions)
        self.define_level_goals()
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()
        self.increase_speed()
        self.level_complete = False
        self.level_complete_timer = None
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)

        # Redireciona para a tela inicial
        selected_level = main_menu(screen)
        self.level = selected_level
        # self.snake = Snake(self.level)  # Cria uma nova cobra com a skin do novo nível (removido)
        self.define_level_goals()
        self.increase_speed()

    def update(self):
        """Atualiza o estado do jogo, movendo a cobra, verificando colisões e lidando com as condições de Game Over."""
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
        for obstacle in self.obstacles:
            obstacle.draw_obstacle()

    def check_collision(self):
        """Verifica se a cobra colidiu com a fruta."""
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1  # Aumenta a pontuação em 1 por maçã
            self.apples_collected += 1

            if self.apples_collected >= self.apples_to_win:
                self.level_complete = True
                self.level_complete_timer = pygame.time.get_ticks()
            else:
                # Garante que a nova fruta não se sobreponha aos obstáculos
                occupied_positions = self.snake.body + [o.pos for o in self.obstacles]
                self.fruit = Fruit(self.snake.body, [o.pos for o in self.obstacles])  # Passa as posições do Vector2 agora

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                # Garante que a nova fruta não se sobreponha aos obstáculos
                occupied_positions = self.snake.body + [o.pos for o in self.obstacles]
                self.fruit = Fruit(self.snake.body,  [o.pos for o in self.obstacles]) # Passa as posições do Vector2

    def check_fail(self):
        """Verifica se a cobra bateu em uma parede, em si mesma ou em um obstáculo."""
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.lose_life()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.lose_life()
        # Verifica a colisão com o obstáculo: compara as posições do Vector2 diretamente.
        for obstacle in self.obstacles:
            if self.snake.body[0] == obstacle.pos:
                self.lose_life()

    def lose_life(self):
        """Lida com a perda de uma vida, redefinindo a cobra se as vidas restantes."""
        self.lives -= 1
        if not self.game_over():
            self.reset_snake()

    def game_over(self):
        """Verifica se o jogo acabou (sem vidas restantes)."""
        return self.lives <= 0

    def draw_grass(self):
        """Desenha o fundo de grama."""
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBER):
                grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, (30, 30, 30), grass_rect)
                else:
                    pygame.draw.rect(screen, (10, 10, 10), grass_rect)
        border_rect = pygame.Rect(0, 0, CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE)
        pygame.draw.rect(screen, BLOOD_RED, border_rect, 3)

    def draw_score(self):
        """Desenha a pontuação na tela."""
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, TEXT_COLOR)
        score_x = int(CELL_SIZE * CELL_NUMBER - 60)
        score_y = int(CELL_SIZE * CELL_NUMBER - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                               apple_rect.height)
        pygame.draw.rect(screen, NIGHT_GREEN, bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, NIGHT_GREEN, bg_rect, 2)

    def draw_lives(self):
        """Desenha o número de vidas restantes na tela."""
        start_x = 10  # Posição X inicial para a primeira imagem de vida
        for i in range(self.lives):
            life_rect = self.life_image.get_rect(topleft=(start_x + i * 30, 10))  # Ajusta espaçamento
            screen.blit(self.life_image, life_rect)
        # Desenha o texto de XP ao lado das vidas
        xp_text = game_font.render(f"XP: {self.xp}", True, TEXT_COLOR)
        xp_rect = xp_text.get_rect(topleft=(start_x + self.lives * 30 + 10, 10))  # Ajusta a posição do texto XP
        screen.blit(xp_text, xp_rect)

    def draw_objective(self):
        """Desenha o objetivo do nível atual na tela."""
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        objective_text = f"Nível {self.level}: Coma {self.apples_collected}/{self.apples_to_win} maçãs!"
        objective_surface = font.render(objective_text, True, TEXT_COLOR)
        objective_rect = objective_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(objective_surface, objective_rect)

    def draw_level_complete(self):
        """Desenha a mensagem de nível completo na tela."""
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 60)
        level_complete_text = f"Nível {self.level} Completo!"
        level_complete_surface = font.render(level_complete_text, True, WHITE)
        level_complete_rect = level_complete_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(level_complete_surface, level_complete_rect)

    def reset_game(self):
        """Redefine todo o jogo para seu estado inicial."""
        self.reset_snake()
        self.obstacles = [Obstacle() for _ in range(5)]
        self.obstacle_positions = [obstacle.pos for obstacle in self.obstacles]
        self.fruit = Fruit(self.snake.body, self.obstacle_positions)
        self.lives = 3
        self.score = 0
        self.has_moved = False
        self.apples_collected = 0
        self.xp = 0
        self.level = 1
        # self.snake = Snake(self.level) # Define a cobra do nível 1 novamente (removido)
        self.level_up = False
        self.obstacle_chance = 0.2
        self.speed = 150
        self.define_level_goals()
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)
        self.show_objective = True
        self.objective_start_time = pygame.time.get_ticks()
        self.current_background_color = self.background_colors[0]  # Redefine a cor de fundo
        self.level_complete = False
        self.level_complete_timer = None
        self.show_jump_scare = False
        self.jump_scare_alpha = 0

    def reset_snake(self):
        """Redefine a cobra para sua posição e direção inicial."""
        self.snake.reset()
        self.has_moved = False
        self.snake.direction = Vector2(0, 0)

    def draw_game_over(self):
        """Desenha a imagem de Game Over e o botão para retornar ao menu principal."""
        screen.blit(self.game_over_image, (0, 0))  # Desenha a imagem de Game Over

        # Propriedades do botão
        button_width = 200
        button_height = 50
        button_color = BLOOD_RED
        button_text_color = WHITE
        button_x = screen.get_width() // 2 - button_width // 2
        button_y = screen.get_height() // 2 + 100  # Posição do botão

        # Cria o retângulo do botão
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Desenha o botão
        pygame.draw.rect(screen, button_color, button_rect)

        # Renderiza o texto do botão
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
        text_surface = font.render("Voltar ao Menu", True, button_text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)

        # Desenha o texto no botão
        screen.blit(text_surface, text_rect)

        return button_rect  # Retorna o retângulo do botão para verificar cliques

    def trigger_jump_scare(self):
        """Inicia a sequência do jump scare."""
        if self.jump_scare_image:
            self.show_jump_scare = True
            self.jump_scare_start_time = pygame.time.get_ticks()
            self.jump_scare_alpha = 0  # Reinicia o alpha para o fade-in começar corretamente
            if self.jump_scare_sound:
                self.jump_scare_sound.play()  # Toca o som do jump scare

    def draw_jump_scare(self):
        """Desenha o jump scare com um efeito de fade-in e fade-out."""
        if self.show_jump_scare and self.jump_scare_image:
            elapsed_time = pygame.time.get_ticks() - self.jump_scare_start_time

            if elapsed_time < JUMP_SCARE_FADE_DURATION:
                # Fade-in
                alpha = int((elapsed_time / JUMP_SCARE_FADE_DURATION) * 255)
            elif elapsed_time > JUMP_SCARE_DURATION - JUMP_SCARE_FADE_DURATION:
                # Fade-out
                fade_out_time = elapsed_time - (JUMP_SCARE_DURATION - JUMP_SCARE_FADE_DURATION)
                alpha = int(((JUMP_SCARE_FADE_DURATION - fade_out_time) / JUMP_SCARE_FADE_DURATION) * 255)
            else:
                # Totalmente visível
                alpha = 255

            # Garante que o alpha esteja dentro do intervalo válido
            alpha = max(0, min(alpha, 255))

            # Cria uma cópia da imagem do jump scare e define sua transparência
            temp_surface = self.jump_scare_image.copy()
            temp_surface.set_alpha(alpha)

            # Desenha a imagem com transparência
            screen.blit(temp_surface, (0, 0))

            # Se o tempo total exceder a duração, oculta o jump scare
            if elapsed_time > JUMP_SCARE_DURATION:
                self.show_jump_scare = False

# --- MENU ---

def main_menu(screen):
    """Exibe o menu principal e permite que o jogador selecione um nível."""
    pygame.init()
    try:
        background_image = pygame.image.load('img/Capa_Prancheta 1.png').convert()
        background_image = pygame.transform.scale(background_image, screen.get_size())
    except FileNotFoundError as e:
        print(f"Erro ao carregar imagem do menu: {e}. Verifique o arquivo 'img/Capa_Prancheta 1.png'.")
        pygame.quit()
        sys.exit()

    start_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
    phrase = "Bem-vindo ao Jogo da Cobra!"
    typed_text = ""

    def draw_screen():
        """Desenha a tela do menu com botões de seleção de nível."""
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
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button_rect, level in level_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        return level
            elif event.type == pygame.KEYDOWN:
                return 1  # Volta ao nível 1 por padrão se qualquer tecla for pressionada
        clock.tick(60)
    return 1  # Volta ao nível 1 por padrão

# --- INICIALIZAÇÃO ---
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

try:
    apple = pygame.image.load('img/apple.png').convert_alpha()  # Carrega a imagem # Carrega a imagem da maçã aqui
except FileNotFoundError as e:
    print(f"Erro ao carregar imagem da maçã: {e}. Verifique o arquivo 'img/apple.png'.")
    pygame.quit()
    sys.exit()

game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT # Evento personalizado para atualizar a tela

# Carrega a imagem do obstáculo
try:
    obstaculo_image_path = os.path.join(os.path.dirname(__file__), 'img', 'obstaculo.png')
    obstaculo_image = pygame.image.load(obstaculo_image_path)
    obstaculo_image = pygame.transform.scale(obstaculo_image, (CELL_SIZE, CELL_SIZE))  # Redimensiona a imagem para o tamanho do obstáculo
except FileNotFoundError as e:
    print(f"Erro ao carregar imagem do obstáculo: {e}. Verifique o arquivo 'img/obstaculo.png'.")
    pygame.quit()
    sys.exit()

# Inicia a música de fundo
try:
    pygame.mixer.music.load('som/musica_de_fundo.mp3')  # Substitua 'som/musica_de_fundo.mp3' pelo caminho da sua música
    pygame.mixer.music.set_volume(0.5)  # Define o volume da música (opcional)
    pygame.mixer.music.play(-1)  # Toca a música em loop (-1 significa loop infinito)
except pygame.error as e:
    print(f"Erro ao carregar música de fundo: {e}. Verifique o arquivo 'som/musica_de_fundo.mp3'.")
    pygame.quit()
    sys.exit()

# Mostra o menu principal e obtém o nível selecionado
selected_level = main_menu(screen)

# Cria a instância principal do jogo
main_game = Main()
main_game.level = selected_level
main_game.define_level_goals()
main_game.increase_speed()

# --- LOOP DO JOGO ---
game_running = True
pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)
while True:
    if game_running:
        current_time = pygame.time.get_ticks()
        if main_game.show_objective:
            if current_time - main_game.objective_start_time >= main_game.objective_timer:
                main_game.show_objective = False

        screen.fill(main_game.current_background_color)  # Define a cor de fundo
        main_game.draw_elements()

        if main_game.level_complete:
            main_game.draw_level_complete()
            if current_time - main_game.level_complete_timer > 2000:
                main_game.next_level()

    else:
        # Lógica da tela de Game Over
        screen.fill(BACKGROUND_COLOR)  # Preenche com a cor de fundo padrão quando o jogo acaba
        button_rect = main_game.draw_game_over() # Desenha a imagem de Game Over e o botão na tela

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Verifica se o clique foi no botão
                if button_rect.collidepoint(mouse_pos):
                    selected_level = main_menu(screen)
                    main_game = Main()
                    main_game.level = selected_level
                    main_game.define_level_goals()
                    main_game.increase_speed()
                    game_running = True
                    pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)
                    break # Inicia um novo jogo
            elif event.type == pygame.KEYDOWN: # Se o jogador pressionar qualquer tecla
                selected_level = main_menu(screen)
                main_game = Main()
                main_game.level = selected_level
                main_game.define_level_goals()
                main_game.increase_speed()
                game_running = True
                pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)
                break # Inicia um novo jogo
    if game_running: # Eventos do jogo
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
            game_running = False # Define o game running como falso para pará-lo até que o jogador clique no botão

    pygame.display.update()
    clock.tick(60)