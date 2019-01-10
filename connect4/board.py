class Board:
    '''
    Provides basic board methods

    Pieces are stored as matrix and accessed as where_pieces[x][y]
    '0' is no pieces, 'A' is player A's pieces and 'B' is player B's pieces

    Initialize_game initializes board as empty '0', with x = 7 and y = 6
    with the origin as where_pieces[0][0]:

        [
            [    [    [    [    [    [    [
            '0', '0', '0', '0', '0', '0', '0',
        y   '0', '0', '0', '0', '0', '0', '0',
        =   '0', '0', '0', '0', '0', '0', '0',
        6   '0', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '0',
               ]    ]    ]    ]    ]    ]    ]

                        x = 7                    ]

    Add_piece checks whether piece is valid
    (within range, empty spot and pieces below),
    adds the player's piece onto the board and updates the new_piece

    Print_board transposes the matrix with zip() to print row by row,
    reverses the transposed matrix to ensure the origin is at the bottom left,
    then prints the reversed matrix to the terminal with row and col coordinates

    zip usage at: https://docs.python.org/3/tutorial/datastructures.html
    '''

    def __init__(self, acontroller, aheight=6, awidth=7):
        '''
        Sets default height and width for board. We did not implement any way for the user
        to change the standard values for these, but all code in this program is designed so that
        you could change it and it should work. Essentially, we coded for a general case.
        '''
        self.controller = acontroller

        self.height = aheight
        self.width = awidth

        self.where_pieces = None
        self.new_piece = None
        self.previous_piece = None
        self.num_pieces = 0

    def get_height(self):
        '''
        Returns the height of the board.
        '''
        return self.height

    def get_width(self):
        '''
        Returns the width of the board.
        '''
        return self.width

    def get_pieces(self):
        '''
        Returns a matrix containing all pieces.
        '''
        return self.where_pieces

    def get_new_piece(self):
        '''
        Returns the newest piece.
        '''
        return self.new_piece

    def get_previous_piece(self):
        '''
        Returns the 2nd last piece played.
        '''
        return self.previous_piece

    def get_num_pieces(self):
        '''
        Returns number of pieces on the board.
        '''
        return self.num_pieces

    def initialize_board(self):
        '''
        Creates the initial matrix that maps all pieces and puts '0' for each piece
        representing that the board starts empty.
        '''
        self.where_pieces = [['0'] * self.get_height()
                             for i in range(self.get_width())]
        self.num_pieces = 0
        self.previous_piece = None

    def add_piece(self, x, y, player=None, no_invalid=True):
        '''
        Adds a piece at the specified place. Returns true if a piece was added.
        Returns false if the piece could not be added and tells the user as such.
        '''
        if player == None:
            player = self.controller.playon.get_who_is_playing()
        if no_invalid == True:
            if x < self.get_width() and y < self.get_height(
            ) and self.where_pieces[x][y] == '0' and (
                    y == 0 or self.where_pieces[x][y - 1] != '0'):
                self.previous_piece = self.get_new_piece()
                self.where_pieces[x][y] = player
                self.new_piece = (x, y)
                self.num_pieces += 1
                return True
            else:
                print('Invalid piece!\n')
                return False
        else:
            self.previous_piece = self.get_new_piece()
            self.where_pieces[x][y] = player
            self.new_piece = (x, y)
            self.num_pieces += 1

    def print_board(self):
        '''
        Prints the board to the terminal.
        '''
        print('Printing board...\n')
        row_num = self.get_height()
        for y in list(reversed(list(zip(*self.get_pieces())))):
            row_num -= 1
            print(row_num, y, '\n')
        for col_num in range(self.get_width()):
            print(' ' * 3, col_num, end='')
        print('\n')

    def add_where_pieces(self, awhere_pieces):
        '''
        Sets the board equal to a board that is passed in as a parameter.
        '''
        self.where_pieces = awhere_pieces

    def remove_piece(self, x, y):
        '''
        Removes a piece from a specific position.
        '''
        self.where_pieces[x][y] = '0'
        self.num_pieces -= 1
