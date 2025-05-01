# Simple Turn-Based Combat Game

This is a simple turn-based combat game built using the `pygame` library in Python.

## Features

* Turn-based combat system.
* Player and Enemy characters with HP, Attack, and Defense stats.
* Basic player actions: Attack and Heal.
* Simple enemy AI.
* Basic graphical interface using `pygame`.
* Game states: Menu, Combat, Game Over.

## Requirements

* Python 3.6 or higher
* `pygame` library

## Installation

1.  Clone this repository to your local machine:

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

    (Replace `<repository_url>` and `<repository_name>` with the actual URL and name of your GitHub repository once you create it and upload the code).

2.  Install the required library (`pygame`):

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  Make sure you have installed the requirements as described above.
2.  Run the `main.py` file from your terminal:

    ```bash
    python main.py
    ```

## How to Play

1.  When the game starts, you will see a menu screen. Click the "Start Game" button to begin the combat.
2.  In the combat screen, you will see your character ("Hero") and the enemy ("Goblin").
3.  It's your turn first. Click the "Attack" button to attack the enemy or the "Heal" button to restore some of your HP.
4.  After your action, it will be the enemy's turn. The enemy will automatically perform an action.
5.  The game continues in turns until either your HP or the enemy's HP reaches zero.
6.  The game over screen will display the result. Press the ESC key to quit the game.

## Project Structure

* `main.py`: Contains the main game logic, character classes, UI elements, and the game loop.
* `requirements.txt`: Lists the necessary Python libraries (`pygame`).

## Extending the Game

This is a basic framework. Here are some ideas to make it more complex:

* Add more enemy types with different stats and abilities.
* Implement more player abilities (e.g., special attacks, defense buffs).
* Introduce an inventory system for items (potions, weapons, armor).
* Add a leveling system for the player.
* Create different combat encounters or levels.
* Improve the graphics with sprites and backgrounds.
* Add sound effects and music.
* Implement a more sophisticated enemy AI.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details (You would add a LICENSE file to your GitHub repo).
