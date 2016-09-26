#! /usr/bin/env python

import Tkinter as tk
import sokoban as sk
from sys import exit
from PIL import Image, ImageTk
from itertools import cycle

# will determine the size of the display
ICON_SIZE = 100
PAD = 3
CASE = ICON_SIZE + PAD

def box(i,j):
    x1 = j * CASE
    y1 = i * CASE
    x2 = j * CASE + ICON_SIZE
    y2 = i * CASE + ICON_SIZE
    return x1, y1, x2, y2

def center(i,j):
    x = j * CASE + ICON_SIZE / 2
    y = i * CASE + ICON_SIZE / 2
    return x, y

COLORS = {
    sk.FREE: 'black',
    sk.WALL: 'grey',
    sk.PLAYER: 'lightblue',
    sk.CRATE: '#9B2501',
    sk.CRATE_ON_OBJECTIVE: 'lightyellow',
    sk.OBJECTIVE: 'white',
    sk.PLAYER_ON_OBJECTIVE: 'lightblue',
}

# lets be a bit more natural with keys
MOVES = {
    'w': (-1, 0),
    'd': (0, 1),
    's': (1, 0),
    'a': (0, -1),
}

class App(tk.Tk):
    help_text = """Push the boxes on the white cases to win
    Enter your move (W, S, A, D), u to undo or q to exit """

    def __init__(self, level_names):
        tk.Tk.__init__(self)
        self.level_names = cycle(level_names)

        # set up tk widgets
        frame = tk.Frame(self)
        frame.pack()

        self.score_label = tk.Label(frame, text= "Welcome!")
        self.score_label.pack()

        c = tk.Canvas(frame, background='lightgrey')
        c.pack()
        c.focus_set()
        c.bind("<Key>", self.key_press)
        self.c = c

        wframe = tk.Frame(frame)
        wframe.pack()
        self.help = tk.Label(wframe, text= self.help_text)
        self.help.pack(side=tk.LEFT)

        self.undo_button = tk.Button(wframe, text='Undo', command=self.do_undo)
        self.undo_button.pack(side=tk.RIGHT)

        # set up img display
        img_size = (int(ICON_SIZE * 0.95),int(ICON_SIZE *0.95))

        player_image = Image.open("res/people-delivery.png").resize(img_size)
        crate_image = Image.open("res/crate.png").resize(img_size)
        objective_image = Image.open("res/unknown.png").convert("RGBA").resize(img_size)
        objective_player_image = Image.blend(player_image, objective_image, 0.20)
        objective_crate_image = Image.blend(crate_image, objective_image, 0.20)

        self.IMAGES = {
            sk.PLAYER: ImageTk.PhotoImage(player_image),
            sk.CRATE: ImageTk.PhotoImage(crate_image),
            sk.CRATE_ON_OBJECTIVE: ImageTk.PhotoImage(objective_crate_image),
            sk.OBJECTIVE: ImageTk.PhotoImage(objective_image),
            sk.PLAYER_ON_OBJECTIVE: ImageTk.PhotoImage(objective_player_image),
        }

        self.load_next_level()
        self.display()

    def load_next_level(self):
        level_name = self.level_names.next()
        level = sk.load_level(level_name)
        self.history = [('init', level)]
        self.undo = 0

        row = len(level)
        col = len(level[0])
        self.width= col * CASE
        self.height = row * CASE

        self.c.config(width=self.width, height=self.height)
        self.help.config(text=self.help_text)


    def display(self):
        """Display the level on the canvas in self.c"""
        # remove everything on canvas
        self.c.delete(tk.ALL)
        level = self.history[-1][1]

        for i, row in enumerate(level):
            for j, case in enumerate(row):
                if case in COLORS:
                    self.c.create_rectangle(*box(i,j), fill=COLORS[case])
                if case in self.IMAGES:
                    self.c.create_image(*center(i,j), image=self.IMAGES[case])

        self.undo_button.config(state = tk.DISABLED if len(self.history) == 1 else tk.NORMAL)
        if sk.has_won(level):
            self.c.create_text((self.width/2, self.height/2),
                               text="You have won!", fill='red',
                              font=("Purisa Bold", 55))
            self.undo_button.config(state = tk.DISABLED)
            self.help.config(text="Press n for next level, q to quit")

        text = '{0} moves done'.format(len(self.history) -1) if self.history > 1\
                else '1 move done'
        if self.undo:
            text += ' and {} undo'.format(self.undo)
        self.score_label.config(text=text)


    def do_undo(self):
        print ' ====  Undoing last move.'
        if len(self.history) > 1:
            self.history.pop()
            self.undo += 1
        else:
            print 'Initial level'
        self.display()

    def key_press(self, event):
        cmd = event.char
        history = self.history

        if cmd  == 'q':
            exit()

        if sk.has_won(history[-1][1]):
            return

        elif cmd in MOVES.keys():
            dx, dy = MOVES[cmd]
            r =  sk.move(history[-1][1], dx, dy)
            if r is False:
                print '!!!! Invalid move'
            else:
                history.append((cmd, r))
        elif cmd == 'n':
            self.load_next_level()
        elif cmd == 'u':
            self.do_undo()
        else:
            print ' ==== Unkown command'
        self.display()

if __name__ == '__main__':
    import sys, glob
    levels = sys.argv[1:] if len(sys.argv) > 1 else sorted(glob.glob('*.sok'))
    app = App(levels)
    app.mainloop()
