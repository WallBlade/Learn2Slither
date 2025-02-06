import os
import argparse as ap
from game import Game

def parse_arguments():
    parser = ap.ArgumentParser(description='Snake Game with AI and Human modes')
    
    # Mode selection
    parser.add_argument('-mode', 
                       choices=['human', 'ai'],
                       default='human',
                       help='Game mode: human player or AI agent')

    # Window settings
    parser.add_argument('-w',
                       type=int,
                       default=600,
                       help='Window width')
    
    # Game settings
    parser.add_argument('-board-size',
                       type=int,
                       default=10,
                       help='Size of the game board')
    
    parser.add_argument('-speed',
                       type=int,
                       default=50,
                       help='Game speed (FPS)')

    parser.add_argument('-step-by-step',
                          action='store_true',
                          help='Enable step-by-step mode for human player')
    
    # AI settings
    parser.add_argument('-save',
                       type=str,
                       help='Path to save AI model')

    parser.add_argument('-load',
                       type=str,
                       help='Path to load AI model')
    
    parser.add_argument('-dontlearn',
                       action='store_true',
                       help='Enable training mode for AI')
    
    parser.add_argument('-sessions',
                       type=int,
                       default=100,
                       help='Number of episodes for AI training')
    
    parser.add_argument('-visual',
                       choices=['on', 'off'],
                       default='on',
                       help='Enable visualisation of AI training: on or off')
    
    return parser.parse_args()

def create_models_folder():
    directory_name = 'models'

    try:
        os.makedirs('models')
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    args = parse_arguments()
    if args.save or args.load:
        create_models_folder()
    game = Game(args)
    game.run_game()

if __name__ == "__main__":
    main()