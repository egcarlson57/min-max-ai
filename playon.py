import random


class PlayOn:
    '''Control interaction between players and determine scrore'''

    def __init__(self, acontroller):
        '''
        Player attributes:
        playerX = [name, AI or Human, smart or random AI, recursive depth]
        '''
        self.controller = acontroller
        self.playerA = ['A', None, 'smart', 5]
        self.playerB = ['B', None, 'smart', 5]
        self.who_is_playing = None
        self.winner = None
        self.no_input = False

    def get_who_is_playing(self):
        '''
        Returns the current player
        '''
        return self.who_is_playing[0]

    def get_winner(self):
        '''
        Returns the winner.
        '''
        return self.winner

    def set_players(self, x, y):
        '''
        determine whether player is AI or Human depending on input
        randomly selects a player to start
        '''

        if y == 2:
            self.controller.playon.players = ('Human', "Human")
        elif y == 1:
            self.controller.playon.players = ('Human', 'AI')
        else:
            self.controller.playon.players = ('AI', 'AI')
        self.playerA[1], self.playerB[1] = self.controller.playon.players
        print('Player A is {}, Player B is {}. Players set!\n'.format(
            self.playerA, self.playerB))
        if self.who_is_playing == None:
            self.who_is_playing = random.choice((self.playerA, self.playerB))
            print("Player {}'s turn".format(self.get_who_is_playing()).center(
                50, '-'), '\n')

    def human_play(self, x, y):
        '''
        Human: get input, and check whether is valid
        Valid: add to board and display on graphics

        Then determine whether player wins
        Win: change end_game state or else switches player
        '''
        if self.controller.board.add_piece(x, y) == True:
            self.controller.graphics.add_piece(x, y)
            if self.determine_win() == False and self.check_tie() == False:
                self.switch_players()
                self.controller.graphics.during_game()
            else:
                return True
        else:
            self.controller.graphics.display_bottom('Invalid Piece!')

    def ai_play(self):
        '''
        AI: get move, add to board and display on graphics
        Then determine whether player wins
        Win: change end_game state or else switches player
        '''
        while self.who_is_playing[1] == 'AI':
            print('AI Thinking...')
            self.controller.graphics.display_bottom('AI Thinking...')
            self.no_input = True  #prevent input when ai is thinking
            if self.who_is_playing[2] == 'smart':
                x, y = self.controller.ai.make_decision_smart(
                    self.who_is_playing[3])
            else:  #ai is random
                x, y = self.controller.ai.make_decision_random()
            self.no_input = False
            print("AI's move is {}, {}.\n".format(x, y))
            self.controller.board.add_piece(x, y)
            self.controller.graphics.add_piece(x, y)
            if self.determine_win() == False and self.check_tie() == False:
                self.switch_players()
                self.controller.graphics.during_game()
            else:
                return True

    def switch_players(self):
        '''
        Switches who is playing.
        '''
        if self.who_is_playing == self.playerA:
            self.who_is_playing = self.playerB
        else:
            self.who_is_playing = self.playerA
        print("Player switched! Player {}'s turn".format(
            self.get_who_is_playing()).center(50, '-'), '\n')

    def check_tie(self, aboard=None):
        '''Checks if the game is over due to a tie (all pieces filled up)'''
        if aboard == None:
            aboard = self.controller.board
        board_size = aboard.get_width() * aboard.get_height()

        if aboard.get_num_pieces() < board_size:
            return False
        else:
            return True

    def determine_win(self,
                      aplayer=None,
                      apiece=None,
                      actual=True,
                      aboard=None):
        '''Uses accumulators for each direction that a connection can be in,
        and uses a matrix to determine what directions to check in. This checks
        each new piece that has been placed and returns True when the new piece
        results in connections >= 4

        uldr, ud, urdl
        lr, piece,  lr
        urdl, ud, uldr

        uldr = connections to the up, left / down, right
        urdl = connections to up, right / down, left
        ud = connections to up / down
        lr = connections to left / right

        More examples in testing_win.py
        '''

        if aplayer == None:
            aplayer = self.get_who_is_playing()
        if apiece == None:
            apiece = self.controller.board.get_new_piece()
        if aboard == None:
            aboard == self.controller.board

        self.connections_dirtn = {'uldr': 0, 'urdl': 0, 'lr': 0, 'ud': 0}
        self.directions_coords = {
            'uldr': ((-1, 1), (1, -1)),
            'urdl': ((1, 1), (-1, -1)),
            'lr': ((-1, 0), (1, 0)),
            'ud': ((0, -1), (0, 1))
        }

        for dirtns in self.directions_coords:
            for a_dirtn in self.directions_coords[dirtns]:
                self.connections_dirtn[dirtns] += self.connection_in_a_dirctn(
                    a_dirtn, aplayer, apiece, aboard)
            '''return True aligns inside'''
            if self.connections_dirtn[dirtns] >= 3:
                if actual == True:
                    print('Player {} wins'.format(
                        self.get_who_is_playing()).center(50, '*'))
                self.winner = self.get_who_is_playing()
                return True
                '''return False aligns at the start'''
        else:
            return False

    def connection_in_a_dirctn(self, adirection, aplayer, apiece, aboard=None):
        '''
        Recursively sums how many pieces of a player's are in a certain direction.
        If recursion is disabled, it only checks if the piece directed to by the
        vector inputted as adirection is the same as the player inputted as aplayer.
        '''
        if aboard == None:
            aboard = self.controller.board
        new_piece = (apiece[0] + adirection[0], apiece[1] + adirection[1])
        new_x, new_y = new_piece[0], new_piece[1]

        if new_x >= aboard.get_width() or new_y >= aboard.get_height(
        ) or new_x < 0 or new_y < 0:
            return 0
        elif aboard.get_pieces()[new_x][new_y] != aplayer:
            return 0
        else:
            return 1 + self.connection_in_a_dirctn(adirection, aplayer,
                                                   new_piece, aboard)
