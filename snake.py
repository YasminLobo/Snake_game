import pygame, sys, random
from pygame.math import Vector2
import time
import os

# --- CONSTANTS ---
NIGHT_GREEN = (0, 50, 0)
BLOOD_RED = (139, 0, 0)
DARK_GRAY = (80, 80, 80)
BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = (220, 220, 220)
WHITE = (200, 200, 200)
GOLD = (255, 215, 0)

CELL_SIZE = 30
CELL_NUMBER = 20

# --- HELPER FUNCTIONS ---

def generate_random_position(occupied_positions):
    """Generates a random position for an object, ensuring it's not in occupied positions."""
    x = random.randint(0, CELL_NUMBER - 1)
    y = random.randint(0, CELL_NUMBER - 1)
    pos = Vector2(x, y)

    if pos in occupied_positions:
        return generate_random_position(occupied_positions)  # Recursive call if position is occupied

    return pos

def check_collision(pos1, pos2):
    """Checks if two positions are the same, indicating a collision."""
    return pos1 == pos2

# --- GAME OBJECTS ---

class Snake:
    """Represents the snake in the game."""
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False  # Flag to indicate if a new block should be added

        # Load snake body part images
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

        self.body_tr = pygame.image.load('img/body_tr.png').convert_alpha()  # top-right corner
        self.body_tl = pygame.image.load('img/body_tl.png').convert_alpha()  # top-left corner
        self.body_br = pygame.image.load('img/body_br.png').convert_alpha()  # bottom-right corner
        self.body_bl = pygame.image.load('img/body_bl.png').convert_alpha()  # bottom-left corner

        # Load crunch sound
        self.crunch_sound = pygame.mixer.Sound('som/crunch.wav')


    def draw_snake(self):
        """Draws the snake on the screen, using the correct images for head, tail, and body segments."""
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
                # Determine body segment orientation based on neighboring segments
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:  # Corner pieces
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        """Updates the snake's head image based on its movement direction."""
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
        """Updates the snake's tail image based on its movement direction."""
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
        """Moves the snake by adding a new head and removing the tail (unless a block is added)."""
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)  # Add new head
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]  # Remove tail
            body_copy.insert(0, body_copy[0] + self.direction)  # Add new head
            self.body = body_copy[:]

    def add_block(self):
        """Sets the flag to add a new block to the snake on the next move."""
        self.new_block = True

    def play_crunch_sound(self):
        """Plays the crunch sound effect."""
        self.crunch_sound.play()

    def reset(self):
        """Resets the snake to its initial state."""
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    """Represents the fruit that the snake eats."""
    def __init__(self, snake_body, obstacle_positions):
        self.snake_body = snake_body
        self.obstacle_positions = obstacle_positions  # Store obstacle positions as Vector2
        self.is_special = False
        self.randomize()

    def draw_fruit(self):
        """Draws the fruit on the screen."""
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(apple, fruit_rect)  # Assuming 'apple' is a loaded image

    def randomize(self):
        """Generates a random position for the fruit, ensuring it's not on the snake or obstacles."""
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

        # Ensure fruit is not on snake or obstacles
        while self.pos in self.snake_body or self.pos in self.obstacle_positions:
            self.x = random.randint(0, CELL_NUMBER - 1)
            self.y = random.randint(0, CELL_NUMBER - 1)
            self.pos = Vector2(self.x, self.y)
        self.is_special = False

    def make_special(self):
        """Marks the fruit as a special fruit (for future implementation)."""
        self.is_special = True


class Obstacle:
    """Represents an obstacle that the snake must avoid."""

    def __init__(self):
        self.pos = generate_random_position([])  # Initial random position
        self.rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)


    def draw_obstacle(self):
        """Draws the obstacle on the screen."""
        self.rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(obstaculo_image, self.rect)  # Draw the obstacle image

    def randomize(self, occupied_positions):
        """Generates a random position for the obstacle, avoiding occupied positions."""
        self.pos = generate_random_position(occupied_positions)
        self.rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)


# --- GAME LOGIC ---

class Main:
    """Manages the main game logic, including levels, score, collisions, and game state."""
    def __init__(self):
        self.snake = Snake()
        self.obstacles = [Obstacle() for _ in range(5)]  # Create 5 obstacle objects
        self.obstacle_positions = [obstacle.pos for obstacle in self.obstacles]  # Store obstacle positions as Vector2
        self.fruit = Fruit(self.snake.body, self.obstacle_positions)
        self.lives = 3
        self.score = 0
        self.has_moved = False  # Flag to prevent movement before a key is pressed
        self.apples_collected = 0
        self.apples_to_win = 5 # Initial value, might be changed in define_level_goals
        self.xp = 0
        self.level = 1
        self.level_up = False # flag to identify level up
        self.obstacle_chance = 0.2
        self.level_complete = False
        self.speed = 150 # milliseconds between screen updates
        self.background_colors = [BACKGROUND_COLOR, NIGHT_GREEN, BLOOD_RED, DARK_GRAY]
        self.current_background_color = self.background_colors[0] # set initial background color
        self.show_objective = True
        self.objective_timer = 2000 # milliseconds to show objective
        self.objective_start_time = 0
        self.define_level_goals()
        self.increase_speed()

    def define_level_goals(self):
        """Defines how many apples the snake must eat to complete the current level."""
        if self.level == 1:
            self.apples_to_win = 10
        elif self.level == 2:
            self.apples_to_win = 15
        elif self.level == 3:
            self.apples_to_win = 20
        elif self.level == 4:
            self.apples_to_win = 25

    def increase_speed(self):
        """Increases the snake's speed, making the game harder."""
        self.speed = max(50, self.speed - 15)
        print(f"Snake speed increased to: {self.speed}")

    def next_level(self):
        """Advances the game to the next level."""
        self.level += 1
        if self.level > 4:
            self.level = 1  # Wrap around to level 1 if we exceed the number of levels

        self.current_background_color = self.background_colors[self.level - 1]
        self.apples_collected = 0
        # Reset obstacle positions on level transition.
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

        # Redirecionar para a tela inicial
        selected_level = main_menu(screen)
        self.level = selected_level
        self.define_level_goals()
        self.increase_speed()

    def update(self):
        """Updates the game state, moving the snake, checking for collisions, and handling game over conditions."""
        if not self.game_over() and self.has_moved and not self.show_objective and not self.level_complete:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        """Draws all game elements on the screen."""
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_lives()
        for obstacle in self.obstacles:
            obstacle.draw_obstacle()

    def check_collision(self):
        """Checks if the snake has collided with the fruit."""
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1  # Aumenta a pontuação em 1 por maçã
            self.apples_collected += 1

            if self.apples_collected >= self.apples_to_win:
                self.level_complete = True
                self.level_complete_timer = pygame.time.get_ticks()
            else:
                # Ensure new fruit doesn't overlap with obstacles
                occupied_positions = self.snake.body + [o.pos for o in self.obstacles]
                self.fruit = Fruit(self.snake.body, [o.pos for o in self.obstacles])  # Pass the Vector2 positions now

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                # Ensure new fruit doesn't overlap with obstacles
                occupied_positions = self.snake.body + [o.pos for o in self.obstacles]
                self.fruit = Fruit(self.snake.body,  [o.pos for o in self.obstacles]) # Pass Vector2 positions

    def check_fail(self):
        """Checks if the snake has hit a wall, itself, or an obstacle."""
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.lose_life()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.lose_life()
        # Check obstacle collision: compare Vector2 positions directly.
        for obstacle in self.obstacles:
            if self.snake.body[0] == obstacle.pos:
                self.lose_life()

    def lose_life(self):
        """Handles the loss of a life, resetting the snake if lives remain."""
        self.lives -= 1
        if not self.game_over():
            self.reset_snake()

    def game_over(self):
        """Checks if the game is over (no lives remaining)."""
        return self.lives <= 0

    def draw_grass(self):
        """Draws the grass background."""
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
        """Draws the score on the screen."""
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
        """Draws the number of lives remaining on the screen."""
        lives_text = str(self.lives)
        lives_surface = game_font.render(f"Lives: {lives_text} XP: {self.xp}", True, TEXT_COLOR)
        lives_rect = lives_surface.get_rect(topleft=(10, 10))
        screen.blit(lives_surface, lives_rect)

    def draw_objective(self):
        """Draws the current level's objective on the screen."""
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        objective_text = f"Level {self.level}: Eat {self.apples_collected}/{self.apples_to_win} apples!"
        objective_surface = font.render(objective_text, True, TEXT_COLOR)
        objective_rect = objective_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(objective_surface, objective_rect)

    def draw_level_complete(self):
        """Draws the level complete message on the screen."""
        font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 60)
        level_complete_text = f"Level {self.level} Complete!"
        level_complete_surface = font.render(level_complete_text, True, WHITE)
        level_complete_rect = level_complete_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(level_complete_surface, level_complete_rect)

    def reset_game(self):
        """Resets the entire game to its initial state."""
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
        self.level_up = False
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
        """Resets the snake to its initial position and direction."""
        self.snake.reset()
        self.has_moved = False
        self.snake.direction = Vector2(0, 0)

# --- MENU ---

def main_menu(screen):
    """Displays the main menu and allows the player to select a level."""
    pygame.init()
    background_image = pygame.image.load('img/Capa_Prancheta 1.png').convert()
    background_image = pygame.transform.scale(background_image, screen.get_size())
    start_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
    phrase = "Welcome to Snake Game!"
    typed_text = ""

    def draw_screen():
        """Draws the menu screen with level selection buttons."""
        screen.blit(background_image, (0, 0))
        level_buttons = []
        for i in range(1, 5):
            button_surface = start_font.render(f"Level {i}", True, TEXT_COLOR)
            button_rect = button_surface.get_rect(
                center=(screen.get_width() // 2 + (i - 2.5) * 150, screen.get_height() // 2 + 150))  # Mais para baixo
            pygame.draw.rect(screen, BLOOD_RED, button_rect.inflate(30, 10), border_radius=15)
            pygame.draw.rect(screen, WHITE, button_rect.inflate(30, 10), 4, border_radius=15)
            screen.blit(button_surface, button_rect)
            level_buttons.append((button_rect, i))
        pygame.display.update()
        return level_buttons

    # Initial typing animation
    for i in range(len(phrase)):
        typed_text += phrase[i]
        draw_screen()
        time.sleep(0.05)

    # Main menu loop
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
                return 1  # Default to level 1 if any key is pressed
        clock.tick(60)
    return 1  # Default to level 1

# --- INITIALIZATION ---
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
apple = pygame.image.load('img/apple.png').convert_alpha()  # Load apple image here
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT  # Custom event for updating the screen

# Load obstacle image
obstaculo_image_path = os.path.join(os.path.dirname(__file__), 'img', 'obstaculo.png')
obstaculo_image = pygame.image.load(obstaculo_image_path)
obstaculo_image = pygame.transform.scale(obstaculo_image, (CELL_SIZE, CELL_SIZE))  # Redimensiona a imagem para o tamanho do obstáculo

# Show main menu and get selected level
selected_level = main_menu(screen)

# Create the main game instance
main_game = Main()
main_game.level = selected_level
main_game.define_level_goals()
main_game.increase_speed()

# --- GAME LOOP ---
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
                main_game = Main()
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