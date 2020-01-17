'''
Tests the determine win function.
'''
import grandcontroller
import time


class CheckWin:
    def __init__(self, adelay=0):
        '''
        Initializes a game
        '''
        self.controller = grandcontroller.GrandControl()
        self.controller.board.playerA = 'A'
        self.controller.playon.who_is_playing = self.controller.board.playerA
        self.sleep = time.sleep
        self.delay = adelay

    def print_results(self, lastpiece=None):
        '''
        prints the board and if there is a winner.
        '''
        self.controller.board.print_board()
        self.controller.playon.determine_win()
        self.sleep(self.delay)
        self.controller.board.initialize_board()

    '''code below check directions_coords'''

    def print_directions(self):
        directions_coords = {
            'uldr': ((-1, 1), (1, -1)),
            'urdl': ((1, 1), (-1, -1)),
            'lr': ((-1, 0), (1, 0)),
            'ud': ((0, -1), (0, 1))
        }
        for key in directions_coords:
            for x, y in directions_coords[key]:
                self.controller.board.add_piece(x + 3, y + 2, key, False)
        self.controller.board.print_board()

    def check_4(self):
        '''checking winning positions'''
        '''straight cases, in the corner and the middle'''

        for y in range(4):
            self.controller.board.add_piece(0, y, None, False)
        self.print_results()
        for y in range(4):
            self.controller.board.add_piece(0, y, None, False)
        self.controller.board.add_piece(0, y - 1, None, False)
        self.print_results()

        for y in range(4):
            self.controller.board.add_piece(3, y, None, False)
        self.print_results()
        for y in range(4):
            self.controller.board.add_piece(3, y, None, False)
        self.controller.board.add_piece(3, y - 1, None, False)
        self.print_results()
        '''horizontal cases, in the corner and the middle'''

        for x in range(4):
            self.controller.board.add_piece(x, 0, None, False)
        self.print_results()
        for x in range(4):
            self.controller.board.add_piece(x, 0, None, False)
        self.controller.board.add_piece(x - 1, 0, None, False)
        self.print_results()

        for x in range(4):
            self.controller.board.add_piece(x, 3, None, False)
        self.print_results()
        for x in range(4):
            self.controller.board.add_piece(x, 3, None, False)
        self.controller.board.add_piece(x - 1, 3, None, False)
        self.print_results()
        '''diagonal cases, in the corner and the middle, uldr, urdl'''

        for x in range(4):
            self.controller.board.add_piece(x, x, None, False)
        self.print_results()
        for x in range(4):
            self.controller.board.add_piece(x, x, None, False)
        self.controller.board.add_piece(x - 1, x - 1, None, False)
        self.print_results()

        for x in range(2, 6):
            self.controller.board.add_piece(x, x, None, False)
        self.print_results()
        for x in range(2, 6):
            self.controller.board.add_piece(x, x, None, False)
        self.controller.board.add_piece(x - 1, x - 1, None, False)
        self.print_results()

        for x in range(4):
            self.controller.board.add_piece(x, 5 - x, None, False)
        self.print_results()
        for x in range(4):
            self.controller.board.add_piece(x, 5 - x, None, False)
        self.controller.board.add_piece(x - 1, 5 - (x - 1), None, False)
        self.print_results()

        for x in range(1, 5):
            self.controller.board.add_piece(x, 5 - x, None, False)
        self.print_results()
        for x in range(1, 5):
            self.controller.board.add_piece(x, 5 - x, None, False)
        self.controller.board.add_piece(x - 1, 5 - (x - 1), None, False)
        self.print_results()

    def check_3(self):
        '''check non winning positions'''
        '''star-shaped, criss-cross, and square'''

        for x, y in ((2, 3), (3, 3), (4, 3), (3, 4), (3, 2), (3, 3)):
            self.controller.board.add_piece(x, y, None, False)
        self.print_results()

        for x, y in ((2, 2), (3, 3), (4, 4), (2, 4), (4, 2), (3, 3)):
            self.controller.board.add_piece(x, y, None, False)
        self.print_results()

        for x in range(2, 5):
            for y in range(2, 5):
                self.controller.board.add_piece(x, y, None, False)
        self.controller.board.add_piece(3, 3, None, False)
        self.print_results()
        '''square with one-gap l boundary'''
        for x in range(2, 5):
            for y in range(2, 5):
                self.controller.board.add_piece(x, y, None, False)
        for y in range(6):
            self.controller.board.add_piece(0, y, None, False)
        for x in range(7):
            self.controller.board.add_piece(x, 0, None, False)
        self.controller.board.add_piece(2, 2, None, False)
        self.print_results()


def main():
    checkwin = CheckWin()
    checkwin.print_directions()
    checkwin.check_4()
    checkwin.check_3()


if __name__ == "__main__":
    main()
