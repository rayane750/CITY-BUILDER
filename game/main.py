from game.view.menu import *
from game.model.settings import *
from game.controller.game import Game


def main():

    running = True
    playing = False

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((900, 700))
    clock = pg.time.Clock()

    # implement menus
    menu = Menu(text_buttons, L_center, H_center, delta_H)
    menu.set()

    # implement game
    game = Game(screen, clock)

    while running:

        # start menu goes here
        menu.display()
        choice = menu.check_state()
        match choice:
            case "Exit":
                running = exit_function(menu.DISPLAY)
            case "Start new career":
                playing = True
        while playing:
            # game loop here
            game.run()

if __name__ == "__main__":
    main()
