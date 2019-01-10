'''
add piece to the screen
'''
self.thescreen.tracer(0, 0)
for i in range(3):
    '''
    erases the message saying whos turn it is
    self.theturtle.undo()
    #erases the message saying whos turn it is
self.theturtle.undo()  #same purpose as last undo.
self.theturtle.undo()  #erases the outline around the last piece
'''
if player == None:
    player = self.controller.playon.get_who_is_playing()
self.theturtle.up()
if self.controller.playon.get_who_is_playing() == 'A':
    self.theturtle.fillcolor('red')
else:
    self.theturtle.fillcolor('yellow')
self.theturtle.pencolor('black')
self.theturtle.goto(x + 0.9, y + 0.5)
self.theturtle.begin_fill()
self.theturtle.width(5)
self.theturtle.setheading(90)
self.theturtle.circle(0.4)
self.theturtle.end_fill()
self.theturtle.pendown()
self.theturtle.width(10)
self.theturtle.setheading(90)
self.theturtle.circle(0.4)
self.theturtle.penup()
self.thescreen.update()
