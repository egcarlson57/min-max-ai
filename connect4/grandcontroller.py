#!/usr/bin/env python3
'''run game directly in terminal'''

import board
import graphics
import playon
import ai
import turtle


class GrandControl:
    '''
    Enables interaction between all the underlying modules

    Call the Graphics to listen to mouse click

    Branching determines the appropriate response to the mouse click,
    depending on which state the game is in. Three states are possible:


    0. Initialize the game by calling the Graphics method
    to get input on selecting the players (Human or AI)
    One players are selected, the Board is initialized,
    Graph#!/usr/bin/env python3ics print board to screen, and the state goes to 1


    1. Graphics print board, and call Playon to
    start playing and switches between players

    Human's turn: Get input on new piece, add new piece to board,
    display new piece on screen
    AI's turn: Get input by calling AI, add new piece to board,
    display new piece on screen

    Determine win with every move. Upon win, Graphics print win result,
    screen exit on click and change state to 2

    2. Game ended, no input
    '''

    def __init__(self):
        '''
        Initizlizes the game and creates objects of the classes we defined in other
        documents.
        '''
        self.state = 0
        self.board = board.Board(self)
        self.graphics = graphics.Graphics(self)
        self.playon = playon.PlayOn(self)
        self.ai = ai.AI(self)

        self.graphics.initialize_game()
        self.board.initialize_board()
        print('\nGame initialized\n')

    def branch(self, x, y):
        '''
        Creates different game states which control what the turtle does.
        '''
        x = int(x)
        y = int(y)
        #self.state = 1
        if self.playon.no_input == False:
            if self.state == 0:
                self.playon.set_players(x, y)
                self.board.initialize_board()
                self.graphics.create_board()
                self.graphics.during_game()
                if self.playon.ai_play() == True:
                    self.graphics.end_game()
                    self.state = 2
                else:
                    self.state = 1
            elif self.state == 1:
                if self.playon.human_play(x, y) == True:
                    self.graphics.end_game()
                    self.state = 2
                else:
                    if self.playon.ai_play() == True:
                        self.graphics.end_game()
                        self.state = 2
            else:
                self.graphics.initialize_game()
                self.board.initialize_board()
                print('\nGame initialized\n')
                self.state = 0


def main():
    '''
    This is the main function of our program. Here we initialize our GrandControl
    aka our event-driven programming which controls our turtle loop
    '''
    controller = GrandControl()  #run the game!
    print('Game started!\n')
    '''
    Testing using keyboard input
    while True:
        x = input('x: ')
        y = input('y: ')
        print('\n')
        controller.branch(x, y)
        '''


if __name__ == "__main__":
    main()
    turtle.mainloop()
