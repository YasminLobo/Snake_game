import pygame, sys, random
from pygame.math import Vector2
import time
import os

# --- CONSTANTES ---
# Definição de cores usando tuplas RGB (Red, Green, Blue).
NIGHT_GREEN = (0, 50, 0)
BLOOD_RED = (139, 0, 0)
DARK_GRAY = (80, 80, 80)
BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = (220, 220, 220)
WHITE = (200, 200, 200)
GOLD = (255, 215, 0)

# Define o tamanho de cada célula da grade do jogo e o número de células.
CELL_SIZE = 30
CELL_NUMBER = 20

# --- FUNÇÕES AUXILIARES ---

def generate_random_position(occupied_positions):
    """Gera uma posição aleatória para um objeto, garantindo que não esteja em posições ocupadas."""
    # Gera coordenadas x e y aleatórias dentro da grade do jogo.
    x = random.randint(0, CELL_NUMBER - 1)
    y = random.randint(0, CELL_NUMBER - 1)
    pos = Vector2(x, y) # Cria um vetor 2D para representar a posição.

    # Se a posição gerada já estiver ocupada (por exemplo, pela cobra ou outro objeto).
    if pos in occupied_positions:
        return generate_random_position(occupied_positions)  # Chamada recursiva para gerar outra posição.

    return pos # Retorna a posição gerada se ela não estiver ocupada.

def check_collision(pos1, pos2):
    """Verifica se duas posições são as mesmas, indicando uma colisão."""
    return pos1 == pos2 # Retorna True se as posições forem iguais, False caso contrário.

# --- OBJETOS DO JOGO ---

class Snake:
    """Representa a cobra no jogo."""
    def __init__(self):
        # Inicializa o corpo da cobra como uma lista de vetores 2D.
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        # Define a direção inicial da cobra (parada).
        self.direction = Vector2(0, 0)
        # Flag para indicar se um novo bloco deve ser adicionado ao corpo da cobra.
        self.new_block = False

        # Carrega imagens das partes do corpo da cobra.
        self.head_up = pygame.image.load('img/JA/j_head_up.png').convert_alpha()
        self.head_down = pygame.image.load('img/JA/j_head_down.png').convert_alpha()
        self.head_right = pygame.image.load('img/JA/j_head_right.png').convert_alpha()
        self.head_left = pygame.image.load('img/JA/j_head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('img/JA/j_tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('img/JA/j_tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('img/JA/j_tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('img/JA/j_tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('img/JA/j_body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('img/JA/j_body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('img/JA/j_body_tr.png').convert_alpha()  # canto superior direito
        self.body_tl = pygame.image.load('img/JA/j_body_tl.png').convert_alpha()  # canto superior esquerdo
        self.body_br = pygame.image.load('img/JA/j_body_br.png').convert_alpha()  # canto inferior direito
        self.body_bl = pygame.image.load('img/JA/j_body_bl.png').convert_alpha()  # canto inferior esquerdo

        # Carrega som de mastigação.
        self.crunch_sound = pygame.mixer.Sound('som/crunch.wav')


    def draw_snake(self):
        """Desenha a cobra na tela, usando as imagens corretas para cabeça, cauda e segmentos do corpo."""
        self.update_head_graphics() # Atualiza a imagem da cabeça.
        self.update_tail_graphics() # Atualiza a imagem da cauda.

        # Itera sobre cada bloco do corpo da cobra.
        for index, block in enumerate(self.body):
            # Calcula a posição x e y do bloco na tela.
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            # Cria um retângulo para representar o bloco na tela.
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            # Se este for o primeiro bloco (cabeça).
            if index == 0:
                screen.blit(self.head, block_rect) # Desenha a imagem da cabeça.
            # Se este for o último bloco (cauda).
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect) # Desenha a imagem da cauda.
            else:
                # Determina a orientação do segmento do corpo com base nos segmentos vizinhos.
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                # Se os blocos vizinhos estão na mesma coluna (corpo vertical).
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect) # Desenha a imagem do corpo vertical.
                # Se os blocos vizinhos estão na mesma linha (corpo horizontal).
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect) # Desenha a imagem do corpo horizontal.
                else:  # Peças de canto.
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect) # Desenha a imagem do canto superior esquerdo.
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect) # Desenha a imagem do canto inferior esquerdo.
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect) # Desenha a imagem do canto superior direito.
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect) # Desenha a imagem do canto inferior direito.

    def update_head_graphics(self):
        """Atualiza a imagem da cabeça da cobra com base em sua direção de movimento."""
        # Calcula a relação entre o primeiro e o segundo bloco do corpo (direção).
        head_relation = self.body[1] - self.body[0]
        # Define a imagem da cabeça com base na direção.
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
        # Calcula a relação entre o penúltimo e o último bloco do corpo (direção).
        tail_relation = self.body[-2] - self.body[-1]
        # Define a imagem da cauda com base na direção.
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
        # Se um novo bloco deve ser adicionado.
        if self.new_block:
            body_copy = self.body[:] # Cria uma cópia do corpo da cobra.
            body_copy.insert(0, body_copy[0] + self.direction)  # Adiciona nova cabeça na direção atual.
            self.body = body_copy[:] # Atualiza o corpo da cobra.
            self.new_block = False # Reseta a flag.
        else:
            body_copy = self.body[:-1]  # Remove a cauda.
            body_copy.insert(0, body_copy[0] + self.direction)  # Adiciona nova cabeça na direção atual.
            self.body = body_copy[:] # Atualiza o corpo da cobra.

    def add_block(self):
        """Define a flag para adicionar um novo bloco à cobra no próximo movimento."""
        self.new_block = True # Define a flag como True.

    def play_crunch_sound(self):
        """Toca o efeito sonoro de mastigação."""
        self.crunch_sound.play() # Toca o som.

    def reset(self):
        """Redefine a cobra para seu estado inicial."""
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] # Redefine o corpo.
        self.direction = Vector2(0, 0) # Redefine a direção.


class Fruit:
    """Representa a fruta que a cobra come."""
    def __init__(self, snake_body, obstacle_positions):
        self.snake_body = snake_body # Armazena o corpo da cobra.
        self.obstacle_positions = obstacle_positions  # Armazena as posições dos obstáculos como Vector2
        self.is_special = False # Flag para indicar se a fruta é especial.
        self.randomize() # Gera uma posição aleatória para a fruta.

    def draw_fruit(self):
        """Desenha a fruta na tela."""
        # Cria um retângulo para representar a fruta na tela.
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(apple, fruit_rect)  # Desenha a imagem da maçã.

    def randomize(self):
        """Gera uma posição aleatória para a fruta, garantindo que não esteja na cobra ou nos obstáculos."""
        self.x = random.randint(0, CELL_NUMBER - 1) # Gera uma coordenada x aleatória.
        self.y = random.randint(0, CELL_NUMBER - 1) # Gera uma coordenada y aleatória.
        self.pos = Vector2(self.x, self.y) # Cria um vetor 2D para representar a posição.

        # Garante que a fruta não esteja na cobra ou nos obstáculos.
        while self.pos in self.snake_body or self.pos in self.obstacle_positions:
            self.x = random.randint(0, CELL_NUMBER - 1) # Gera uma nova coordenada x.
            self.y = random.randint(0, CELL_NUMBER - 1) # Gera uma nova coordenada y.
            self.pos = Vector2(self.x, self.y) # Cria um novo vetor 2D para representar a posição.
        self.is_special = False # Reseta a flag de fruta especial.

    def make_special(self):
        """Marca a fruta como uma fruta especial (para implementação futura)."""
        self.is_special = True # Define a flag como True.


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
        self.snake = Snake() # Cria uma instância da cobra.
        self.obstacles = [Obstacle() for _ in range(5)]  # Cria 5 objetos de obstáculo
        self.obstacle_positions = [obstacle.pos for obstacle in self.obstacles]  # Armazena as posições dos obstáculos como Vector2
        self.fruit = Fruit(self.snake.body, self.obstacle_positions) # Cria uma instância da fruta.
        self.lives = 3 # Define o número inicial de vidas.
        self.score = 0 # Define a pontuação inicial.
        self.has_moved = False  # Flag para impedir o movimento antes que uma tecla seja pressionada
        self.apples_collected = 0 # Inicializa o contador de maçãs coletadas.
        self.apples_to_win = 5 # Valor inicial, pode ser alterado em define_level_goals
        self.xp = 0 # Inicializa a experiência.
        self.level = 1 # Define o nível inicial.
        self.level_up = False # Flag para identificar o aumento de nível
        self.obstacle_chance = 0.2 # Chance de um obstáculo aparecer.
        self.level_complete = False # Flag para indicar se o nível foi completado.
        self.speed = 150 # Milissegundos entre as atualizações da tela
        self.background_colors = [BACKGROUND_COLOR, NIGHT_GREEN, BLOOD_RED, DARK_GRAY]
        self.current_background_color = self.background_colors[0] # Define a cor de fundo inicial
        self.show_objective = True # Flag para exibir o objetivo do nível.
        self.objective_timer = 2000 # Milissegundos para mostrar o objetivo
        self.objective_start_time = 0 # Tempo em que o objetivo começou a ser exibido.
        self.define_level_goals() # Define o número de maçãs necessárias para vencer o nível.
        self.increase_speed() # Aumenta a velocidade do jogo.

        # Carrega a imagem de vida
        self.life_image = pygame.image.load('img/coracao.png').convert_alpha()  # Substitua 'img/coracao.png' pelo caminho da sua imagem
        self.life_image = pygame.transform.scale(self.life_image, (25, 25))  # Ajusta o tamanho conforme necessário

        # Carrega a imagem de Game Over
        self.game_over_image = pygame.image.load('img/game-over_Prancheta 1.jpg').convert_alpha() # substitua pelo nome correto
        self.game_over_image = pygame.transform.scale(self.game_over_image, (600, 600))  # Ajuste conforme necessário

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
        self.level += 1 # Incrementa o nível.
        if self.level > 4:
            self.level = 1  # Volta ao nível 1 se excedermos o número de níveis

        self.current_background_color = self.background_colors[self.level - 1]
        self.apples_collected = 0 # Reseta o contador de maçãs.
        # Redefine as posições dos obstáculos na transição de nível.
        for obstacle in self.obstacles:
            occupied_positions = self.snake.body + [o.pos for o in self.obstacles if o != obstacle]
            obstacle.randomize(occupied_positions)
        self.obstacle_positions = [obstacle.pos for obstacle in self.obstacles]

        self.fruit = Fruit(self.snake.body, self.obstacle_positions) # Cria uma nova fruta.
        self.define_level_goals() # Define as metas do novo nível.
        self.show_objective = True # Exibe o objetivo do novo nível.
        self.objective_start_time = pygame.time.get_ticks() # Define o tempo de início da exibição do objetivo.
        self.increase_speed() # Aumenta a velocidade.
        self.level_complete = False # Reseta a flag de nível completo.
        self.level_complete_timer = None # Reseta o timer de nível completo.
        pygame.time.set_timer(SCREEN_UPDATE, self.speed) # Define o timer para atualizar a tela.

        # Redireciona para a tela inicial
        selected_level = main_menu(screen)
        self.level = selected_level
        self.define_level_goals()
        self.increase_speed()

    def update(self):
        """Atualiza o estado do jogo, movendo a cobra, verificando colisões e lidando com as condições de Game Over."""
        # Se o jogo não acabou, a cobra se moveu, o objetivo não está sendo exibido e o nível não foi completado.
        if not self.game_over() and self.has_moved and not self.show_objective and not self.level_complete:
            self.snake.move_snake() # Move a cobra.
            self.check_collision() # Verifica se houve colisão com a fruta.
            self.check_fail() # Verifica se a cobra bateu em algo.

    def draw_elements(self):
        """Desenha todos os elementos do jogo na tela."""
        self.draw_grass() # Desenha o fundo.
        self.fruit.draw_fruit() # Desenha a fruta.
        self.snake.draw_snake() # Desenha a cobra.
        self.draw_score() # Desenha a pontuação.
        self.draw_lives() # Desenha as vidas.
        for obstacle in self.obstacles:
            obstacle.draw_obstacle()

    def check_collision(self):
        """Verifica se a cobra colidiu com a fruta."""
        # Se a posição da fruta é igual à posição da cabeça da cobra.
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block() # Adiciona um bloco à cobra.
            self.snake.play_crunch_sound() # Toca o som de mastigação.
            self.score += 1  # Aumenta a pontuação em 1 por maçã
            self.apples_collected += 1 # Incrementa o contador de maçãs.

            # Se o número de maçãs coletadas for maior ou igual ao número de maçãs necessárias para vencer.
            if self.apples_collected >= self.apples_to_win:
                self.level_complete = True # Define a flag de nível completo como True.
                self.level_complete_timer = pygame.time.get_ticks() # Define o tempo em que o nível foi completado.
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
        # Se a cobra saiu da tela.
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.lose_life() # Perde uma vida.
        # Se a cobra bateu em si mesma.
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.lose_life() # Perde uma vida.
        # Verifica a colisão com o obstáculo: compara as posições do Vector2 diretamente.
        for obstacle in self.obstacles:
            if self.snake.body[0] == obstacle.pos:
                self.lose_life()

    def lose_life(self):
        """Lida com a perda de uma vida, redefinindo a cobra se as vidas restantes."""
        self.lives -= 1 # Decrementa o número de vidas.
        if not self.game_over(): # Se o jogo não acabou.
            self.reset_snake() # Reseta a cobra.

    def game_over(self):
        """Verifica se o jogo acabou (sem vidas restantes)."""
        return self.lives <= 0 # Retorna True se o número de vidas for menor ou igual a zero, False caso contrário.

    def draw_grass(self):
        """Desenha o fundo de grama."""
        # Itera sobre cada célula da grade.
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBER):
                # Cria um retângulo para representar a célula.
                grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                # Se a soma da linha e da coluna for par.
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, (30, 30, 30), grass_rect) # Desenha um retângulo cinza escuro.
                else:
                    pygame.draw.rect(screen, (10, 10, 10), grass_rect) # Desenha um retângulo cinza muito escuro.
        border_rect = pygame.Rect(0, 0, CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE)
        pygame.draw.rect(screen, BLOOD_RED, border_rect, 3)

    def draw_score(self):
        """Desenha a pontuação na tela."""
        score_text = str(self.score) # Converte a pontuação para string.
        score_surface = game_font.render(score_text, True, TEXT_COLOR) # Renderiza o texto da pontuação.
        score_x = int(CELL_SIZE * CELL_NUMBER - 60) # Calcula a posição x da pontuação.
        score_y = int(CELL_SIZE * CELL_NUMBER - 40) # Calcula a posição y da pontuação.
        score_rect = score_surface.get_rect(center=(score_x, score_y)) # Cria um retângulo para a pontuação.
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery)) # Cria um retângulo para a maçã.
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                               apple_rect.height) # Cria um retângulo para o fundo da pontuação.
        pygame.draw.rect(screen, NIGHT_GREEN, bg_rect) # Desenha o fundo da pontuação.
        screen.blit(score_surface, score_rect) # Desenha a pontuação.
        screen.blit(apple, apple_rect) # Desenha a maçã.
        pygame.draw.rect(screen, NIGHT_GREEN, bg_rect, 2) # Desenha a borda do fundo da pontuação.

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
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40) # Define a fonte.
        objective_text = f"Nível {self.level}: Coma {self.apples_collected}/{self.apples_to_win} maçãs!" # Define o texto do objetivo.
        objective_surface = font.render(objective_text, True, TEXT_COLOR) # Renderiza o texto do objetivo.
        objective_rect = objective_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)) # Cria um retângulo para o texto do objetivo.
        screen.blit(objective_surface, objective_rect) # Desenha o texto do objetivo.

    def draw_level_complete(self):
        """Desenha a mensagem de nível completo na tela."""
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 60) # Define a fonte.
        level_complete_text = f"Nível {self.level} Completo!" # Define o texto de nível completo.
        level_complete_surface = font.render(level_complete_text, True, WHITE) # Renderiza o texto.
        level_complete_rect = level_complete_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)) # Cria um retângulo para o texto.
        screen.blit(level_complete_surface, level_complete_rect) # Desenha o texto.

    def reset_game(self):
        """Redefine todo o jogo para seu estado inicial."""
        self.reset_snake() # Reseta a cobra.
        self.obstacles = [Obstacle() for _ in range(5)] # Cria novos obstáculos.
        self.obstacle_positions = [obstacle.pos for obstacle in self.obstacles]
        self.fruit = Fruit(self.snake.body, self.obstacle_positions) # Cria uma nova fruta.
        self.lives = 3 # Redefine o número de vidas.
        self.score = 0 # Redefine a pontuação.
        self.has_moved = False
        self.apples_collected = 0 # Reseta o contador de maçãs.
        self.xp = 0 # Reseta a experiência.
        self.level = 1 # Redefine o nível.
        self.level_up = False # Reseta a flag de level up.
        self.obstacle_chance = 0.2 # Redefine a chance de obstáculo.
        self.speed = 150 # Redefine a velocidade.
        self.define_level_goals() # Redefine as metas do nível.
        pygame.time.set_timer(SCREEN_UPDATE, self.speed) # Define o timer para atualizar a tela.
        self.show_objective = True # Define para mostrar o objetivo.
        self.objective_start_time = pygame.time.get_ticks() # Define o tempo de início da exibição do objetivo.
        self.current_background_color = self.background_colors[0]  # Redefine a cor de fundo
        self.level_complete = False # Reseta a flag de nível completo.
        self.level_complete_timer = None # Reseta o timer de nível completo.

    def reset_snake(self):
        """Redefine a cobra para sua posição e direção inicial."""
        self.snake.reset() # Reseta a cobra.
        self.has_moved = False
        self.snake.direction = Vector2(0, 0) # Redefine a direção.

    def draw_game_over(self):
        """Desenha a imagem de Game Over e o botão para retornar ao menu principal."""
        screen.blit(self.game_over_image, (0, 0))  # Desenha a imagem de Game Over

        # Propriedades do botão
        button_width = 200
        button_height = 50
        button_color = BLOOD_RED
        button_text_color = WHITE
        button_x = screen.get_width() // 2 - button_width // 2
        button_y = screen.get_height() // 2 + 100 # Posição do botão

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

        return button_rect # Retorna o retângulo do botão para verificar cliques

# --- MENU ---

def main_menu(screen):
    """Exibe o menu principal e permite que o jogador selecione um nível."""
    pygame.init()
    background_image = pygame.image.load('img/Capa_Prancheta 1.png').convert()
    background_image = pygame.transform.scale(background_image, screen.get_size())
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