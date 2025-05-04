from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
# In a real application, use a strong, randomly generated secret key
# and store it securely (e.g., environment variable).
# For this example, a simple key is used.
app.secret_key = 'your_secret_key_here'

# --- Character Class (Same as before, but used by Flask) ---
class Character:
    def __init__(self, name, max_hp, attack, defense):
        self.name = name self
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.current_hp -= actual_damage
        if self.current_hp < 0:
            self.current_hp = 0
        return actual_damage

    def is_alive(self):
        return self.current_hp > 0

    # Helper to get character state for JSON response
    def get_state(self):
        return {
            'name': self.name,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
            'attack': self.attack,
            'defense': self.defense,
            'is_alive': self.is_alive()
        }

# --- Game State Management ---
def initialize_game():
    """Initializes or resets the game state in the session."""
    session['player'] = Character("Hero", 100, 20, 5).get_state()
    session['enemy'] = Character("Goblin", 75, 15, 3).get_state()
    session['message'] = "The battle begins!"
    session['turn'] = "player" # "player" or "enemy"
    session['game_over'] = False

def get_game_state():
    """Retrieves the current game state from the session."""
    return {
        'player': session.get('player'),
        'enemy': session.get('enemy'),
        'message': session.get('message'),
        'turn': session.get('turn'),
        'game_over': session.get('game_over')
    }

def update_character_state(character_key, updated_character):
    """Updates a character's state in the session."""
    session[character_key] = updated_character.get_state()

# --- Game Logic Functions (Called by Flask routes) ---
def player_attack_logic():
    """Handles the player's attack action."""
    game_state = get_game_state()
    player_state = game_state['player']
    enemy_state = game_state['enemy']

    # Recreate Character objects from session state for logic
    player_char = Character(player_state['name'], player_state['max_hp'], player_state['attack'], player_state['defense'])
    player_char.current_hp = player_state['current_hp']

    enemy_char = Character(enemy_state['name'], enemy_state['max_hp'], enemy_state['attack'], enemy_state['defense'])
    enemy_char.current_hp = enemy_state['current_hp']

    message = ""
    if game_state['turn'] == "player" and player_char.is_alive() and not game_state['game_over']:
        damage = random.randint(player_char.attack - 5, player_char.attack + 5)
        actual_damage = enemy_char.take_damage(damage)
        message = f"{player_char.name} attacks {enemy_char.name} for {actual_damage} damage!"

        # Update session state
        update_character_state('enemy', enemy_char)
        session['message'] = message
        session['turn'] = "enemy" # Switch turn

        # Check for game over
        if not enemy_char.is_alive():
            session['game_over'] = True
            session['message'] = f"{enemy_char.name} has been defeated! You win!"

    return get_game_state()

def player_heal_logic():
    """Handles the player's heal action."""
    game_state = get_game_state()
    player_state = game_state['player']

    player_char = Character(player_state['name'], player_state['max_hp'], player_state['attack'], player_state['defense'])
    player_char.current_hp = player_state['current_hp']

    message = ""
    if game_state['turn'] == "player" and player_char.is_alive() and not game_state['game_over']:
        heal_amount = random.randint(10, 20)
        player_char.current_hp += heal_amount
        if player_char.current_hp > player_char.max_hp:
            player_char.current_hp = player_char.max_hp
        message = f"{player_char.name} heals for {heal_amount} HP!"

        # Update session state
        update_character_state('player', player_char)
        session['message'] = message
        session['turn'] = "enemy" # Switch turn

    return get_game_state()


def enemy_turn_logic():
    """Handles the enemy's turn."""
    game_state = get_game_state()
    player_state = game_state['player']
    enemy_state = game_state['enemy']

    player_char = Character(player_state['name'], player_state['max_hp'], player_state['attack'], player_state['defense'])
    player_char.current_hp = player_state['current_hp']

    enemy_char = Character(enemy_state['name'], enemy_state['max_hp'], enemy_state['attack'], enemy_state['defense'])
    enemy_char.current_hp = enemy_state['current_hp']

    message = ""
    if game_state['turn'] == "enemy" and enemy_char.is_alive() and not game_state['game_over']:
        # Simple enemy AI: 70% chance to attack, 30% chance to do nothing
        action_choice = random.choices(["attack", "wait"], weights=[70, 30], k=1)[0]

        if action_choice == "attack" and player_char.is_alive():
            damage = random.randint(enemy_char.attack - 3, enemy_char.attack + 3)
            actual_damage = player_char.take_damage(damage)
            message = f"{enemy_char.name} attacks {player_char.name} for {actual_damage} damage!"
            update_character_state('player', player_char)
        else:
            message = f"{enemy_char.name} waits..."

        session['message'] = message
        session['turn'] = "player" # Switch turn

        # Check for game over
        if not player_char.is_alive():
            session['game_over'] = True
            session['message'] = f"You have been defeated by {enemy_char.name}!"

    return get_game_state()


# --- Flask Routes ---
@app.route('/')
def index():
    """Renders the main game page."""
    # Initialize game state if not already in session
    if 'player' not in session:
        initialize_game()
    return render_template('index.html')

@app.route('/game_state', methods=['GET'])
def game_state():
    """Returns the current game state as JSON."""
    return jsonify(get_game_state())

@app.route('/player_action', methods=['POST'])
def player_action():
    """Handles player actions (attack/heal)."""
    action = request.json.get('action')
    game_state = get_game_state()

    if game_state['turn'] == "player" and not game_state['game_over']:
        if action == 'attack':
            updated_state = player_attack_logic()
        elif action == 'heal':
            updated_state = player_heal_logic()
        else:
            return jsonify({'error': 'Invalid action'}), 400 # Bad request

        # After player action, immediately process enemy turn if game is not over
        if not session.get('game_over'):
             # Simulate a small delay before enemy turn for better UX
             # In a real app, this might involve more sophisticated async handling
             # For simplicity here, we'll just run the logic immediately
             updated_state = enemy_turn_logic()


        return jsonify(updated_state)
    else:
        return jsonify({'message': 'It is not your turn or game is over.'}), 400

@app.route('/reset_game', methods=['POST'])
def reset_game_route():
    """Resets the game state."""
    initialize_game()
    return jsonify(get_game_state())

if __name__ == '__main__':
    # Use debug=True for development. Set to False for production.
    app.run(debug=True)
