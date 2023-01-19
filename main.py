from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    
    game = Game(5, 150, 150)
    game.start_game_loop()


if __name__ == "__main__":
    main()