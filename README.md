# Dino-AI

**Dino-AI** is a Python game inspired by the classic Chrome Dino game, featuring both a single-player mode and an AI mode. The AI mode uses the `NEAT` (NeuroEvolution of Augmenting Topologies) algorithm to evolve a neural network capable of playing the game autonomously. The game uses the `Pygame` library for graphics and sound.

## Features

- **Single Player Mode**: Manual mode where Player control the dinosaur’s jump to avoid obstacles.
- **AI Mode:** Autonomous gameplay with a neural network powered by NEAT, allowing the AI to evolve over generations to improve its performance.
- **Dynamic Gameplay Elements:**
  - Day and night cycle for visual variation.
  - The game speed gradually increases as the score goes up, adding complexity to the gameplay.
- **Scoring System:** Tracks current score and maximum score in single-player mode and supports fitness scoring for AI training.

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
   ├── main.py
   ├── config-feedforward.txt
   ├── icon.ico
   ├── requirements.txt
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
    - `1` to start the AI Mode. `NEAT` will simulate multiple generations of Dinos, with the best-performing neural networks selected to continue learning and improving.
    - `2` to start Single Player Mode. Use the `spacebar` to make the dinosaur jump and avoid obstacles.

## Configuration

To adjust the AI’s behavior, you can modify parameters in `config-feedforward.txt` as needed. This file contains settings for mutation rates, population size, and other NEAT-specific options. Also some configurations are contained in the `main.py` file.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes** and test them.
4. **Submit** a pull request describing your changes.
