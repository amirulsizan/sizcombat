import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Combat Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# --- Game States ---
MENU = 0
COMBAT = 1
GAME_OVER = 2

current_state = MENU

# --- Game Variables ---
message = ""
turn = "player" # "player" or "enemy"

# --- Character Classes ---
class Character:
    def __init__(self, name, max_hp, attack, defense):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        # Simple damage calculation: damage - defense (with a minimum of 1 damage)
        actual_damage = max(1, damage - self.defense)
        self.current_hp -= actual_damage
        if self.current_hp < 0:
            self.current_hp = 0
        return actual_damage

    def is_alive(self):
        return self.current_hp > 0

# --- Game Objects ---
player = Character("Hero", 100, 20, 5)
enemy = Character("Goblin", 75, 15, 3)

# --- UI Elements (Buttons) ---
class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()
                        return True # Indicate button was clicked
        return False

# --- Buttons for Combat ---
attack_button = Button(50, 500, 150, 50, "Attack", BLUE, WHITE)
heal_button = Button(250, 500, 150, 50, "Heal", GREEN, WHITE)

# --- Button for Menu ---
start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, "Start Game", BLUE, WHITE)

# --- Game Functions ---
def draw_text(surface, text, color, x, y, font_size=36):
    if font_size == 36:
        text_surface = font.render(text, True, color)
    else:
        text_surface = small_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_health_bar(surface, current_hp, max_hp, x, y, width, height, color):
    fill = (current_hp / max_hp) * width
    outline_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, BLACK, outline_rect, 2)

def player_attack():
    global message, turn
    if turn == "player" and player.is_alive():
        damage = random.randint(player.attack - 5, player.attack + 5) # Add some randomness
        actual_damage = enemy.take_damage(damage)
        message = f"{player.name} attacks {enemy.name} for {actual_damage} damage!"
        turn = "enemy" # Switch turn

def player_heal():
    global message, turn
    if turn == "player" and player.is_alive():
        heal_amount = random.randint(10, 20) # Heal a random amount
        player.current_hp += heal_amount
        if player.current_hp > player.max_hp:
            player.current_hp = player.max_hp
        message = f"{player.name} heals for {heal_amount} HP!"
        turn = "enemy" # Switch turn

def enemy_turn():
    global message, turn, current_state
    if turn == "enemy" and enemy.is_alive():
        # Simple enemy AI: 70% chance to attack, 30% chance to do nothing (or future ability)
        action_choice = random.choices(["attack", "wait"], weights=[70, 30], k=1)[0]

        if action_choice == "attack":
            damage = random.randint(enemy.attack - 3, enemy.attack + 3) # Add some randomness
            actual_damage = player.take_damage(damage)
            message = f"{enemy.name} attacks {player.name} for {actual_damage} damage!"
        else:
             message = f"{enemy.name} waits..." # Or implement a different enemy action

        turn = "player" # Switch turn

    # Check for game over after enemy turn
    if not player.is_alive() or not enemy.is_alive():
        current_state = GAME_OVER

def reset_game():
    global player, enemy, current_state, message, turn
    player = Character("Hero", 100, 20, 5)
    enemy = Character("Goblin", 75, 15, 3)
    current_state = MENU
    message = ""
    turn = "player"

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == MENU:
            if start_button.handle_event(event):
                current_state = COMBAT
                message = "The battle begins!"
                turn = "player" # Ensure player starts
        elif current_state == COMBAT:
            if turn == "player":
                attack_button.handle_event(event)
                heal_button.handle_event(event)
            # Enemy turn is handled automatically after player action
        elif current_state == GAME_OVER:
             # In a more complex game, you'd have a restart button here
             pass


    # --- Update Game State ---
    if current_state == COMBAT:
        if turn == "enemy" and player.is_alive() and enemy.is_alive():
            # Add a small delay before enemy attacks for better flow
            pygame.time.delay(1000) # 1 second delay
            enemy_turn()
        elif not player.is_alive():
            current_state = GAME_OVER
            message = "You have been defeated!"
        elif not enemy.is_alive():
            current_state = GAME_OVER
            message = "You defeated the enemy!"


    # --- Drawing ---
    screen.fill(WHITE)

    if current_state == MENU:
        draw_text(screen, "Simple Combat Game", BLACK, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 3)
        start_button.draw(screen)
    elif current_state == COMBAT:
        # Draw characters (simple rectangles for now)
        pygame.draw.rect(screen, BLUE, (100, 200, 50, 100)) # Player
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 150, 200, 50, 100)) # Enemy

        # Draw health bars
        draw_health_bar(screen, player.current_hp, player.max_hp, 100, 180, 150, 20, GREEN)
        draw_health_bar(screen, enemy.current_hp, enemy.max_hp, SCREEN_WIDTH - 250, 180, 150, 20, GREEN)

        # Draw names and HP text
        draw_text(screen, player.name, BLACK, 100, 150, font_size=28)
        draw_text(screen, f"HP: {player.current_hp}/{player.max_hp}", BLACK, 100, 290, font_size=28)

        draw_text(screen, enemy.name, BLACK, SCREEN_WIDTH - 250, 150, font_size=28)
        draw_text(screen, f"HP: {enemy.current_hp}/{enemy.max_hp}", BLACK, SCREEN_WIDTH - 250, 290, font_size=28)


        # Draw message area
        pygame.draw.rect(screen, YELLOW, (50, 400, SCREEN_WIDTH - 100, 80))
        draw_text(screen, message, BLACK, 60, 410, font_size=28)

        # Draw buttons if it's player's turn and player is alive
        if turn == "player" and player.is_alive():
            attack_button.draw(screen)
            heal_button.draw(screen)

    elif current_state == GAME_OVER:
        game_over_text = ""
        if player.is_alive():
            game_over_text = "You Win!"
        else:
            game_over_text = "Game Over!"

        draw_text(screen, game_over_text, BLACK, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20)
        draw_text(screen, "Press ESC to Quit", BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, font_size=28)
        # In a real game, you'd add a restart button here. For now, press ESC to quit.


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
