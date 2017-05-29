# Just to show how an AI is implemented


#where the computer is going to Choose its winning step by itself



from tkinter import Tk, Button,messagebox
from tkinter.font import Font

from copy import deepcopy
 
class Board:
 
  def __init__(self,other=None):
    self.player = '-'
    self.opponent = 'o'
    self.empty = ' '
    self.size = 3
    self.fields = {}
    for y in range(self.size):
      for x in range(self.size):
        self.fields[x,y] = self.empty
    # copy constructor
    if other:
      self.__dict__ = deepcopy(other.__dict__)
 
  def move(self,x,y):
    board = Board(self)
    board.fields[x,y] = board.player
    (board.player,board.opponent) = (board.opponent,board.player)
    return board

  #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
 #dont get confused , This is our graph
    #(0,0)(0,1)(0,2)
    #(1,0)(1,1)(1,2)
    #(2,0)(2,1)(2,2)
  
  def __minimax(self, player):
    if self.won():
      if player:
        return (-1,None) # negative unit is assigned on the move if player has wining move
      else:
        return (+1,None) # Positive unit is assigned on the move if i as computer have wining move
    elif self.tied():
      return (0,None)    # If the draw condition is move priority has 0
    elif player:
      best = (-2,None)
      for x,y in self.fields:
        if self.fields[x,y]==self.empty:
          value = self.move(x,y).__minimax(not player)[0]
          if value>best[0]:
            best = (value,(x,y))
      return best
    else:
      best = (+2,None)
      for x,y in self.fields:
        if self.fields[x,y]==self.empty:
          value = self.move(x,y).__minimax(not player)[0]
          if value<best[0]:
            best = (value,(x,y))
      return best
 
  def best(self):
    return self.__minimax(True)[1]
 
  def tied(self):
    for (x,y) in self.fields:  #To check on the cells
      if self.fields[x,y]==self.empty:  # if not full:  game is still on 
        return False 
    return True    # if full : Game is Tied and over
 
  def won(self):
    # horizontal
    
    #->(0,0)(0,1)(0,2)
    #->(1,0)(1,1)(1,2)
    #->(2,0)(2,1)(2,2)
    
    #a condition to check for y's length to be 3 if there is no oponent in x's of y's
    for y in range(self.size):
      winning = []
      for x in range(self.size):
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
      if len(winning) == self.size:
        return winning

    # vertical
    #a condition to check for x's length to be 3 if there is no oponent in y's of x's
    
    for x in range(self.size):
      winning = []
      for y in range(self.size):
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
      if len(winning) == self.size:
        return winning
      
    # diagonal (0,0)|(1,1)|(2,2)
    winning = []
    for y in range(self.size):
      x = y
      if self.fields[x,y] == self.opponent:
        winning.append((x,y))
    if len(winning) == self.size:
      return winning
    
    # another diagonal  (2,0)(1,1)(0,2)
    winning = []
    for y in range(self.size):
      x = self.size-1-y
      if self.fields[x,y] == self.opponent:
        winning.append((x,y))
    if len(winning) == self.size:
      return winning

    # default
    return None
 
  def __str__(self): # search its meaning
    string = ''
    for y in range(self.size):
      for x in range(self.size):
        string+=self.fields[x,y]  # search its meaning
      string+="\n"
    return string

 
class GUI:
 
  def __init__(self):
    self.app = Tk()
    self.app.title('Dot line AI')
    self.app.resizable(width=False, height=False)
    self.board = Board()
    self.font = Font(family="Elephant", size=40)
    self.buttons = {}
    for x,y in self.board.fields:
      handler = lambda x=x,y=y: self.move(x,y)
      button = Button(self.app, command=handler, font=self.font, width=4, height=2)
      button.grid(row=y, column=x)
      self.buttons[x,y] = button
    handler = lambda: self.reset()
    button = Button(self.app, text='Start Again', command=handler)
    button.grid(row=self.board.size+1, column=0, columnspan=self.board.size, sticky="WE")
    self.update()
 
  def reset(self):
    self.board = Board()
    self.update()

  def move(self,x,y):
    self.app.config(cursor="watch")
    self.app.update()
    self.board = self.board.move(x,y)
    self.update()
    move = self.board.best()
    if move:
      self.board = self.board.move(*move)
      self.update()
    self.app.config(cursor="")
 
  def update(self):
    for (x,y) in self.board.fields:
      text = self.board.fields[x,y]
      self.buttons[x,y]['text'] = text
      self.buttons[x,y]['disabledforeground'] = 'black'
#to get texts coloured when win
      if text==self.board.empty:
        self.buttons[x,y]['state'] = 'normal'
      else:
        self.buttons[x,y]['state'] = 'disabled'
    winning = self.board.won()

    if winning:
      for x,y in winning:
        self.buttons[x,y]['disabledforeground'] = 'red'
      for x,y in self.buttons:
        self.buttons[x,y]['state'] = 'disabled'
    for (x,y) in self.board.fields:
      self.buttons[x,y].update()

 
  def Draw(self):
      return self.draw
      
  def mainloop(self):
    self.app.mainloop()
 
if __name__ == '__main__':
  GUI().mainloop()
