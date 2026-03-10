from game import Game

def main():
    game = Game()
    while not game.isOver():
        game.tick()
    game.exit()

if __name__ == "__main__":
    main()