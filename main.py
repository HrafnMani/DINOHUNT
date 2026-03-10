from game import Game
from state import State

def main():
    state = State()     # Universal variable tracker
    game = Game(state)  # Actual game machine
    
    while not game.isOver():
        game.tick()
        
    game.exit()

if __name__ == "__main__":
    main()