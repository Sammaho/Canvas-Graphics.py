"""
This creates graphics using the gui interface, Tkinter. It will create the drawing objects and place them in the cavas
that you dictate. The x coordinates are go from the left to right and the y coordinates go from top to bottom.
left_x, top_y, right_x, bottom_y
"""

# If the following line fails, "Tkinter" needs to be installed
import tkinter as tk
from tkinter import font
#f = font.nametofont('TkDefaultFont')
# If the following line fails, "Pillow" needs to be installed
from PIL import Image, ImageTk

# I noticed that the circles was off the edge at (0, 0), offset is to move it into the screen.
OFFSET = 2

# Text at x = 0 is slightly off of the screen, this fixes that
TEXT_X_OFFSET = 1
TEXT_Y_OFFSET = 0

# This is for the get x and get y functions to work properly. This is will  create a delay
DELAY = 1  # each 1000 is a second


class Canvas:
    # Initiates the canvas object
    def __init__(self, width, height, color='white', title=''):
        # creates main window
        self.root = tk.Tk()
        self.root.title(title)
        self.img = []
        self.arguments = []
        self.user_function = None
        # creates the canvas and places it inside the main window
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=color)

        self.x = 0
        self.y = 0
        self.canvas.bind('<Motion>', self.__motion__)

        self.waiting = False
        self.x_clicked = 0
        self.y_clicked = 0
        self.canvas.bind("<Button-1>", self.__canvas_click__)

        self.canvas.pack(padx=0, pady=0)

    # Clears the canvas
    def clear(self):
        self.canvas.delete('all')

    # Draws a line
    def create_line(self, left_x, top_y, right_x, bottom_y, color='black'):
        self.canvas.create_line(left_x, top_y, right_x, bottom_y, fill=color)

    # Creates an image
    def create_image(self, left_x, top_y, filename):
        self.img.append(ImageTk.PhotoImage(Image.open(filename)))
        self.canvas.create_image(left_x, top_y, anchor='nw', image=self.img[-1])

    # Draws an oval or circle
    def create_oval(self, left_x, top_y, right_x, bottom_y, color='black', outline=""):
        self.canvas.create_oval(left_x + OFFSET, top_y + OFFSET, right_x, bottom_y, fill=color, outline=outline)

    # Draws a rectangle or square
    def create_rectangle(self, left_x, top_y, right_x, bottom_y, color='black', outline=''):
        self.canvas.create_rectangle(left_x + OFFSET, top_y + OFFSET, right_x, bottom_y, fill=color, outline=outline)

    # Adds text in the canvas
    def create_text(self, left_x, top_y, text, color="black", font='Calibri', font_size=10, italic=False, bold=False,
                    underline=False):
        font_bold_underline_italic = ''
        if italic:
            font_bold_underline_italic = font_bold_underline_italic + ' italic'
        if bold:
            font_bold_underline_italic = font_bold_underline_italic + ' bold'
        if underline:
            font_bold_underline_italic = font_bold_underline_italic + ' underline'

        self.canvas.create_text(left_x + TEXT_X_OFFSET, top_y + TEXT_Y_OFFSET, fill=color,
                                font=(font, font_size, font_bold_underline_italic), anchor='nw', text=text)

    # This gets the (x y) coordinates of the mouse as it moves on the canvas
    def __motion__(self, event):
        self.x = event.x
        self.y = event.y

    # This gets the  (x, y) coordinates of the mouse when clicked.
    def __canvas_click__(self, event):
        self.x_clicked = event.x
        self.y_clicked = event.y

    # This returns the y value
    def get_mouse_y(self):
        return self.y

    # This returns the x value
    def get_mouse_x(self):
        return self.x

    def wait_for_click(self):
        if self.waiting == False:
            print('waiting')
            self.waiting = True
            self.show()
        else:
            print('not waiting')
            self.waiting = False
            self.canvas.destroy()

    def argument_list(self, arguments_list):
        self.arguments = arguments_list

    def __repeat_code__(self):
        self.user_function(*self.arguments)
        self.root.after(DELAY, self.__repeat_code__)

    # shows the canvas window (could not figure out how to do it otherwise)
    # This will lock up the code and nothing else can bed done.
    def show(self, passed_function=None):
        if passed_function:
            self.user_function = passed_function
            self.root.after(DELAY, self.__repeat_code__)
        self.root.mainloop()

