#! /usr/bin/env python

import Tkinter as tk
import sokoban as sk
from sys import exit
from PIL import Image, ImageTk

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
    def __init__(self, level_name):
        tk.Tk.__init__(self)

        # set up game
        level = sk.load_level(level_name)
        self.history = [('init', level)]
        self.undo = 0

        # set up tk widgets
        frame = tk.Frame(self)
        frame.pack()

        self.score_label = tk.Label(frame, text= "Welcome!")
        self.score_label.pack()

        row = len(level)
        col = len(level[0])
        self.width= col * CASE
        self.height = row * CASE

        c = tk.Canvas(frame, width=self.width, height=self.height, background='lightgrey')
        c.pack()
        c.focus_set()
        c.bind("<Key>", self.key_press)
        self.c = c

        wframe = tk.Frame(frame)
        wframe.pack()
        label = tk.Label(wframe, text=
                         'Push the boxes on the white cases to win.\n'
                         'Enter your move (W, S, A, D), u to undo or q to exit ')
        label.pack(side=tk.LEFT)

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


        self.display()


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
        elif cmd == 'u':
            self.do_undo()
        else:
            print ' ==== Unkown command'
        self.display()

if __name__ == '__main__':
    import sys
    level = sys.argv[1] if len(sys.argv) > 1 else 'level00'
    app = App(level)
    app.mainloop()
