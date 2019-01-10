import turtle
'''turtle docs at https://docs.python.org/3/library/turtle.html'''


class Graphics:
    def __init__(self, acontroller):
        '''
        Creates a turtle and screen object to be used for the graphical display.
        '''
        self.controller = acontroller
        self.theturtle = turtle.Turtle(visible=False)
        self.thescreen = turtle.Screen()

    def initialize_game(self):
        '''
        Print three options,
        'Human versus Human', 'Human versus AI', 'AI versus AI'
        to the screen
        '''

        self.thescreen.setup(
            width=(self.controller.board.get_width() + 1) * 100,
            height=(self.controller.board.get_height() + 1) * 100)

        self.thescreen.setworldcoordinates(0, 0, 1, 3)
        self.rectangle_with_string((0, 3), (1, 2), 'Human versus Human', 20,
                                   'green')
        self.rectangle_with_string((0, 2), (1, 1), 'Human versus AI', 20,
                                   'yellow')
        self.rectangle_with_string((0, 1), (1, 0), 'AI versus AI', 20,
                                   'orange')

        self.thescreen.onscreenclick(self.controller.branch)

    def rectangle_with_string(self,
                              top_left_coords,
                              bottom_right_coords,
                              string,
                              textsize=12,
                              color='white'):
        '''
        Print rectangle to the screen with texts at the center
        to the screen
        '''
        self.thescreen.tracer(0, 0)
        self.theturtle.up()
        self.theturtle.fillcolor(color)
        self.theturtle.goto(top_left_coords)
        self.theturtle.begin_fill()
        self.theturtle.goto(top_left_coords[0], bottom_right_coords[1])
        self.theturtle.goto(bottom_right_coords)
        self.theturtle.goto(bottom_right_coords[0], top_left_coords[1])
        self.theturtle.goto(top_left_coords)
        self.theturtle.end_fill()
        self.theturtle.goto((top_left_coords[0] + bottom_right_coords[0]) / 2,
                            (top_left_coords[1] + bottom_right_coords[1]) / 2)
        self.theturtle.write(
            string, align="center", font=("Times", textsize, "normal"))
        self.thescreen.update()

    def create_board(self):
        '''
        print empty board to the screen
        '''
        self.thescreen.tracer(0, 0)
        self.thescreen.setworldcoordinates(
            -1, -1,
            self.controller.board.get_width() + 1,
            self.controller.board.get_height() + 1)
        self.theturtle.clear()
        self.theturtle.up()
        self.theturtle.fillcolor('blue')
        self.theturtle.goto(0, 0)
        self.theturtle.down()
        self.theturtle.begin_fill()
        self.theturtle.goto(self.controller.board.get_width(), 0)
        self.theturtle.goto(self.controller.board.get_width(),
                            self.controller.board.get_height())
        self.theturtle.goto(0, self.controller.board.get_height())
        self.theturtle.goto(0, 0)
        self.theturtle.end_fill()
        self.theturtle.up()
        self.theturtle.setheading(90)
        for x in range(self.controller.board.get_width()):
            for y in range(self.controller.board.get_height()):
                self.theturtle.fillcolor('white')
                self.theturtle.up()
                self.theturtle.goto(x + 0.9, y + 0.5)
                self.theturtle.down()
                self.theturtle.begin_fill()
                self.theturtle.circle(0.4)
                self.theturtle.end_fill()
        self.during_game()
        self.thescreen.update()
        print('Board created\n')

    def add_piece(self, x, y, player=None):
        '''
        add piece to the screen
        '''
        self.thescreen.tracer(0, 0)
        '''
        #Draw over the previous piece to remove inner circle outline
        For whatever reason doesn't work properly
        if self.controller.board.get_previous_piece() != None:
            if self.controller.playon.get_who_is_playing() == 'A':
                self.theturtle.fillcolor('yellow')
            else:
                self.theturtle.fillcolor('red')
            previous_x, previous_y = self.controller.board.get_previous_piece()
            self.theturtle.up()
            self.theturtle.goto(previous_x + 0.9, previous_y + 0.5)
            self.theturtle.begin_fill()
            self.theturtle.width(5)
            self.theturtle.setheading(90)
            self.theturtle.circle(0.4)
            self.theturtle.end_fill()
        '''
        if player == None:
            player = self.controller.playon.get_who_is_playing()

        if self.controller.playon.get_who_is_playing() == 'A':
            self.theturtle.fillcolor('red')
        else:
            self.theturtle.fillcolor('yellow')
        # Draw outer circle
        self.theturtle.up()
        self.theturtle.goto(x + 0.9, y + 0.5)
        self.theturtle.begin_fill()
        self.theturtle.width(5)
        self.theturtle.setheading(90)
        self.theturtle.circle(0.4)
        self.theturtle.end_fill()

        #Draw inner circle outline
        self.theturtle.up()
        self.theturtle.goto(x + 0.8, y + 0.5)
        self.theturtle.pencolor('black')
        self.theturtle.pendown()
        self.theturtle.setheading(90)
        self.theturtle.circle(0.3)
        self.theturtle.penup()
        self.thescreen.update()
        print('Graphics added piece at x:{}, y:{}.\n'.format(int(x), int(y)))

    def display_bottom(self, string):
        self.thescreen.tracer(0, 0)
        self.rectangle_with_string(
            (-1, 0), (self.controller.board.get_width() + 1, -1), string)
        self.thescreen.update()

    def display_top(self, string):
        self.thescreen.tracer(0, 0)
        self.rectangle_with_string(
            (-1, self.controller.board.get_height() + 1),
            (self.controller.board.get_width() + 1,
             self.controller.board.get_height()), string)
        self.thescreen.update()

    def during_game(self):
        player_a = self.controller.playon.playerA[1]
        player_b = self.controller.playon.playerB[1]
        self.display_top(
            'Player A: ' + player_a + '        Player B: ' + player_b)
        current_player = self.controller.playon.get_who_is_playing()
        self.display_bottom('It is Player ' + current_player + "'s turn.")

    def end_game(self, winner=None):
        '''
        prints end game results to the screen
        '''
        if winner == None:
            winner = self.controller.playon.get_winner()
        if winner == None:
            self.display_top("It's a tie!")
        else:
            self.display_top('Player ' + winner + ' is the winner')
        self.display_bottom('Click anywhere to play again')
        self.controller.board.previous_piece = None
