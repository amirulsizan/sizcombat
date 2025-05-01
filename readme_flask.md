# Simple Web Combat Game (Flask Version)

This is a web-based version of the simple turn-based combat game, built using the Flask web framework in Python for the backend and HTML, CSS, and JavaScript for the frontend.

Unlike the Pygame version, this game runs in a web browser. The Python Flask application manages the game logic and state on the server, and the browser interacts with it via HTTP requests.

## Features

* Web-based interface running in a browser.

* Turn-based combat system managed by the Flask backend.

* Player and Enemy characters with HP, Attack, and Defense stats.

* Player actions (Attack, Heal) sent to the backend via JavaScript.

* Game state (HP, messages, turn) updated dynamically in the browser.

* Game Over state and Reset functionality.

## Requirements

* Python 3.6 or higher

* `Flask` library

## Installation

1. Clone this repository to your local machine:

git clone <repository_url>
cd <repository_name>


(Replace `<repository_url>` and `<repository_name>` with the actual URL and name of your GitHub repository once you create it and upload the code).

2. Install the required library (`Flask`):

pip install -r requirements.txt


## How to Run

1. Make sure you have installed the requirements as described above.

2. Set the `FLASK_APP` environment variable to your main application file (`app.py`):

export FLASK_APP=app.py  # On Linux/macOS

set FLASK_APP=app.py # On Windows

3. Run the Flask development server:

flask run


4. Open your web browser and go to the address provided by Flask (usually `http://127.0.0.1:5000/`).

## Project Structure

* `app.py`: The main Flask application file containing the game logic and routes.

* `templates/`:

* `index.html`: The main HTML file for the game interface.

* `static/`:

* `style.css`: CSS file for styling the game interface.

* `script.js`: JavaScript file for handling frontend interactions and communication with the Flask backend.

* `requirements.txt`: Lists the necessary Python libraries (`Flask`).

## How to Play

1. Open the game in your web browser by running the Flask application and navigating to the provided URL.

2. The game state (character HP, messages) will be displayed.

3. Click the "Attack" or "Heal" buttons to perform actions when it's your turn.

4. The game will update automatically after each turn.

5. Click "Play Again" on the game over screen to restart.

## Extending the Game

This provides a basic web framework for the game. Here are some ideas for expansion:

* Implement more sophisticated UI elements and animations using CSS and JavaScript.

* Add more enemy types and player abilities.

* Integrate a database to save game progress or player stats.

* Implement user accounts and multiplayer functionality.

* Improve the enemy AI.

* Add more game states (e.g., character selection, world map).

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License
