import curses 
from random import randint
from threading import Thread
import logging
import time


logging.basicConfig(
    format="[%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)s()] %(message)s",
    level=logging.DEBUG,
)
#constants

class conf:
        
    WINDOW_WIDTH = 20  # number of columns of window box  20
    WINDOW_HEIGHT = 10 # number of rows of window box     10

    ESC=27
    inGame = True
    snake = [(4,1),(4,2),(4,3)]
    food = (6,6)
    score =0
    pause = False
    '''
    Number of blocks in window per line = WINDOW_WIDTH -2. 
    Block x index ranges from 1 to WINDOW_WIDTH -2.
    Number of blocks in window per column = WINDOW_HEIGHT -2. 
    Block y index ranges from 1 to WINDOW_HEIGHT -2.
    '''

    def __init__(self):
        # setup window
        curses.initscr()
        win = curses.newwin(self.WINDOW_HEIGHT, self.WINDOW_WIDTH, 0, 0) # rows, columns
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        win.border(0)
        win.nodelay(1) # -1
        self.win = win
        
        # return win
    def returnWin(self):
        return self.win


def onKeyPress(key):
    prevKey = key
    event = win.getch()
    key = event if event != -1 else prevKey

    x, y =0,0
    if key == curses.KEY_UP and prevKey!= curses.KEY_DOWN:
        y -=1
    if key == curses.KEY_DOWN and prevKey!= curses.KEY_UP:
        y += 1
    if key == curses.KEY_LEFT and prevKey!= curses.KEY_RIGHT:
        x -=1
    if key == curses.KEY_RIGHT and prevKey!= curses.KEY_LEFT:
        x += 1
    if key == conf.ESC:
        conf.inGame = False
    if key == ' ':
        conf.pause = True

    return key, y ,x

class Snake:
    def __init__(self, win):
        for coords in conf.snake:
            y, x = coords
            win.addch(y,x,'*')
        self.segments = conf.snake
        self.win = win
        # return self
    
    def checkCollision(self):
        if self.segments[0] in self.segments[1:]:
            conf.inGame = False
            logging.info("Snake eat snake")
        if self.segments[0][0] <= 0 or self.segments[0][0] >= conf.WINDOW_HEIGHT-1 or self.segments[0][1]<= 0 or self.segments[0][1]>=conf.WINDOW_WIDTH -1:
            conf.inGame = False
            logging.info("Snake hit wall")

    def move(self, y , x):
        new_segment = (self.segments[0][0] + y , self.segments[0][1] + x)
        self.segments.insert(0, new_segment)
        
        self.win.addch(self.segments[0][0], self.segments[0][1], '*')

        self.checkCollision()


    def checkApple(self, apple):
        if self.segments[0] == apple.coords:
            return 1
        
    def tailShrink(self):
        tail = self.segments.pop()
        self.win.addch(tail[0],tail[1], ' ')

       
class Food:
    def __init__(self, win):
        y ,x =  randint(1, conf.WINDOW_HEIGHT-2,) , randint(1, conf.WINDOW_WIDTH-2 )
        win.addch(y,x, '&')
        self.coords = (y,x)
        self.win = win
        # return self
    def newFood(self):
        return Food(self.win)       

if __name__ == '__main__':
    conf = conf()
    win = conf.returnWin()
    snake = Snake(win)
    food  = Food(win)
    
    prevKey = curses.KEY_DOWN

    # win.addch(food[0],food[1],'$')  

    while(conf.inGame):
        if conf.pause:
            while(win.getch() != ' '):
                time.sleep(1)
            conf.pause = False
            

        win.addstr(0,2, "Score" + str(conf.score) + ' ')
        win.timeout(150 - (len(snake.segments)) // 5 + len(snake.segments)//10 % 120) 

        #onKeypress
        prevKey, y , x = onKeyPress(prevKey)
        snake.move( y,x)
        if snake.checkApple(food):
            food = food.newFood()
            conf.score +=1
        else:
            snake.tailShrink()
        
        #update snake move, food move, collision detection
    curses.endwin()
    print(f"Final score = {conf.score}")