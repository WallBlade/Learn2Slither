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
    
    # AI settings
    parser.add_argument('-model-path',
                       type=str,
                       help='Path to load/save AI model')
    
    parser.add_argument('-training',
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

def main():
    args = parse_arguments()
    game = Game(args)
    game.run_game()

if __name__ == "__main__":
    main()