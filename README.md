# Dino-AI

A dinosaur game (like the Google Chrome Dino game) built with Python and Pygame. The player controls a dinosaur that can run and jump to avoid incoming obstacles. The game speed increases as the score rises.

## Features

- **Single Player Mode**: Manual mode is currently the only playable mode. Players control the dinosaur’s jump to avoid obstacles.
- **Increasing Difficulty**: The game speed gradually increases as the score goes up, adding complexity to the gameplay.

## Requirements

- Python 3.x
- Dependencies specified in `requirements.txt`

## Installation

1. Clone this repository:

```bash
   git clone https://github.com/artur3333/Dino-AI.git
   cd Dino-AI
   ```

2. Install the required dependencies:

```bash
   pip install -r requirements.txt
   ```

## Directory Tree

```plaintext
   Dino-AI/
   ├── icon.ico
   ├── sprites/
       ├── dino/
           ├── dino_run1.png
           ├── dino_run2.png
           └── dino.png
       ├── cactus/
           ├── 1.png
           ├── 2.png
           ├── 3.png
           ├── 4.png
           ├── 5.png
           └── 6.png
       └── road.png
   └── sounds/
       ├── death.wav
       └── jump.wav
   ```

## Usage
1. Run the game by executing:

```bash
   python main.py
   ```

2. In the main menu, press:
    - 2 to start Single Player Mode

3. Use the spacebar to make the dinosaur jump and avoid obstacles.

## Future Improvements

- **AI Mode**: Placeholder for an AI mode to be implemented in the future.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes** and test them.
4. **Submit** a pull request describing your changes.
