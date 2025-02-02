# Snake Game with Q-Learning AI

This project is a Snake game that can be played in either **human mode** or **AI mode** using a **Q-learning agent**. The AI learns to play the game through reinforcement learning.

## Features
- Play as a human or let the AI control the snake.
- Train the AI using Q-learning.
- Adjustable game settings including board size, speed, and visualization.

## Installation & Setup
Follow these steps to set up the project:

```sh
# Clone the repository
git clone <repo-url>
cd <repo-directory>

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

Usage

Run the program with different modes and settings using command-line arguments:

python main.py -mode ai -board-size 10 -speed 50 -training -sessions 100

Available Arguments

Argument

Type

Default

Description

-mode

str

human

Game mode: human or ai

-w

int

600

Window width

-board-size

int

10

Size of the game board

-speed

int

50

Game speed (FPS)

-model-path

str

None

Path to load/save AI model

-training

flag

False

Enable AI training mode

-sessions

int

100

Number of training episodes

-visual

str

on

AI training visualization: on or off