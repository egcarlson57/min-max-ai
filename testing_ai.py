'''
This function tests that the ai makes the correct decision in given situations.
'''

import ai
import grandcontroller


class CheckAI:
    def __init__(self):
        '''
        Initializes an object of type CheckAI.
        '''
        self.controller = grandcontroller.GrandControl()
        self.ai = ai.AI(self.controller)
        self.ai.player = 'A'
        self.player = 'A'
        self.enemy = 'B'
        self.ai.board.initialize_board()

    def eval_row(self):
        '''
        Check direction connections

        Check whether eval_score method in ai class
        gives right answer

        1 piece with all directions empty will give 16
        as 1 direction with both sides empty will give 4
        4+4+4+4=16

        Add another piece on the right will give
        4+4+4+16 = 28
        Add another piece on the right will give
        4+4+4+64 = 76
        Add another piece on the right will give
        4+4+4+256 = 268
        '''
        for x in range(1, 5):
            self.ai.board.add_piece(x, 3, self.player, False)
            self.ai.board.print_board()
            print(
                self.ai.eval_score(self.player, self.ai.board.get_new_piece(),
                                   False))
        self.ai.board.initialize_board()

    def eval_gaps(self):
        '''
        Check gaps

        Add a piece to an empty board will give 16

        Add another piece beyond the zero will give
        4+4+4+8 = 20

        Add another piece at (3,3) will still give
        4+4+4+8 = 20, as the piece on (1,3) is discounted
        with two zero in between the new piece and (1,3)

        Add another piece beyond the zero and
        putting the center piece as new piece will give
        4+4+4+16 = 28

        '''

        for x in range(1, 6, 2):
            self.ai.board.add_piece(x, 3, self.player, False)
            self.ai.board.print_board()
            print(
                self.ai.eval_score(self.player, self.ai.board.get_new_piece(),
                                   False))
        self.ai.board.add_piece(3, 3, self.player, False)
        print(
            self.ai.eval_score(self.player, self.ai.board.get_new_piece(),
                               False))
        self.ai.board.initialize_board()

    def eval_possible_win(self):
        '''
        Check possible wins

        An 'A' at the center with 'B's a gap away vertically
        should give
        4+4+4+1 = 13

        An 'A' at the center with a 'B's no gap away and another 'B'
        two gaps away vertically should give
        4+4+4+1 = 13

        A 'B','A','O','A','B' with everywhere else as empty should give
        4+4+4+1=13
        '''

        self.ai.board.add_piece(3, 5, self.enemy, False)
        self.ai.board.add_piece(3, 1, self.enemy, False)
        self.ai.board.add_piece(3, 3, self.player, False)
        self.ai.board.print_board()
        print(
            self.ai.eval_score(self.player, self.ai.board.get_new_piece(),
                               False))
        self.ai.board.initialize_board()

        self.ai.board.add_piece(3, 4, self.enemy, False)
        self.ai.board.add_piece(3, 0, self.enemy, False)
        self.ai.board.add_piece(3, 3, self.player, False)
        self.ai.board.print_board()
        print(
            self.ai.eval_score(self.player, self.ai.board.get_new_piece(),
                               False))
        self.ai.board.initialize_board()

        self.ai.board.add_piece(3, 5, self.enemy, False)
        self.ai.board.add_piece(3, 1, self.enemy, False)
        self.ai.board.add_piece(3, 2, self.player, False)
        self.ai.board.add_piece(3, 4, self.player, False)
        self.ai.board.print_board()
        print(
            self.ai.eval_score(self.player, self.ai.board.get_new_piece(),
                               False))
        self.ai.board.initialize_board()


def main():
    check_ai = CheckAI()
    check_ai.eval_row()
    check_ai.eval_gaps()
    check_ai.eval_possible_win()


if __name__ == '__main__':
    main()
