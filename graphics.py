"""
This creates graphics using the gui interface, Tkinter. It will create the drawing objects and place them in the cavas
that you dictate. The x coordinates are go from the left to right and the y coordinates go from top to bottom.
left_x, top_y, right_x, bottom_y

This was created by Sam W. Section Leader for Code in Place 2023. This is to mirror as closley as possible the Canvas
ghapics.py import that is used by the students of Code in Place 2023.
"""

# If the following line fails, "Tkinter" needs to be installed
import tkinter as tk

# If the following line fails, "Pillow" needs to be installed
from PIL import Image, ImageTk

# I noticed that the circles was off the edge at (0, 0), offset is to move it into the screen.
OFFSET = 2

# Text at x = 0 is slightly off of the screen, this fixes that
TEXT_X_OFFSET = 1
TEXT_Y_OFFSET = 0

# If canvas.wait_for_click() is added into the function that repeats, the one that is passed into canvas.show(function),
# it will continuously add to the wait queue. This prevents the limit from getting way too high and cause memory issue.
# This is the limit number of function that will be stored in the wait queue, the can go over because it will grab
# all of the functions within the function that is passed into this from the other code.
WAIT_QUEUE_LIMIT = 1000

# For the repeated function, the one passed in by self.show(function). This is will create a delay, may turn into an
# argument/parameter to give the user more control.
DELAY = 1  # each 1000 is a second


class Canvas:
    # Initiates the canvas object
    def __init__(self, width, height, color='white', title=''):
        # creates main window
        self.root = tk.Tk()
        self.root.title(title)

        # creates the canvas and places it inside the main window
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=color)

        # This is the list of images that are being uploaded
        self.img = []

        # This is the arguments for the function that is being uploaded that will constantly loop while the program
        # is running
        self.arguments = []
        # This is the function that is uploaded with canvas.show()
        self.user_function = None

        # The (x, y) mouses movement coordinates that is stored when the user requests it.
        self.x = 0
        self.y = 0
        # This binds motion to the canvas so that action can be performed like tracking the mouses (x, y) coordinate
        self.canvas.bind('<Motion>', self.__motion__)

        # This is to correspond with the self.wait_for_click() function. If true other actions will not be proformed
        # until the mouse is clicked.
        self.waiting = False
        # This is a list of actions (functions) that are waiting for the mouse to be clicked
        self.wait_queue = []

        # This binds motion to the canvas so that action can be performed like getting the mouses (x, y) coordinates
        # when the mouse is clicked
        self.x_clicked = 0
        self.y_clicked = 0


        # This binds the mouse button to the canvas so that the user can pero
        self.canvas.bind("<Button-1>", self.__canvas_click__)

        # Puts the canvas on the window
        self.canvas.pack(padx=0, pady=0)

    # Clears the canvas
    def clear(self):
        if self.waiting:
            self.__add_to_wait_list__([self.clear, []])
            return
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
        # if waiting to click then will add the function to the queue instead of running it.
        if self.waiting:
            # adding to the wait queue
            self.__add_to_wait_list__([self.create_oval, [left_x, top_y, right_x, bottom_y, color, outline]])
            return
        self.canvas.create_oval(left_x + OFFSET, top_y + OFFSET, right_x, bottom_y, fill=color, outline=outline)

    # Draws a rectangle or square
    def create_rectangle(self, left_x, top_y, right_x, bottom_y, color='black', outline=''):
        # if waiting to click then will add the function to the queue instead of running it.
        if self.waiting:
            # adding to the wait queue
            self.__add_to_wait_list__([self.create_rectangle, [left_x, top_y, right_x, bottom_y, color, outline]])
            return
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

    # This returns the y value
    def get_mouse_y(self):
        return self.y

    # This returns the x value
    def get_mouse_x(self):
        return self.x

    # shows the canvas window (could not figure out how to do it otherwise)
    # This will lock up the code and nothing else can bed done.
    def show(self, passed_function=None):
        if passed_function:
            self.user_function = passed_function
            self.root.after(DELAY, self.__repeat_code__)
        self.root.mainloop()

    # This stops the all actions until the user clicks on the canvas
    def wait_for_click(self):
        self.waiting = True
        if len(self.wait_queue) > 0:
            self.wait_queue.append(['wait', 'wait'])

    # This ends the program, it is added if the user wants to add a stop button.
    def end(self):
        self.root.destroy()

    def argument_list(self, arguments_list):
        self.arguments = arguments_list

    # This adds functions and other options to the wait list.
    def __add_to_wait_list__(self, function, resume=False):
        print('len to wait list = ', len(self.wait_queue))
        if resume:
            self.waiting = False
        else:
            self.wait_queue.append(function)

    # This gets the  (x, y) coordinates of the mouse when clicked.
    def __canvas_click__(self, event):
        self.x_clicked = event.x
        self.y_clicked = event.y
        self.waiting = False
        self.__resume__()

    # This resumes the program after it has been clicked
    def __resume__(self):
        if len(self.wait_queue) < 1:
            return

        function_pair = self.wait_queue.pop(0)
        while function_pair[0] != 'wait':
            function_pair[0](*function_pair[1])
            if len(self.wait_queue) > 0:
                function_pair = self.wait_queue.pop(0)
            else:
                break

    # This gets the (x y) coordinates of the mouse as it moves on the canvas
    def __motion__(self, event):
        self.x = event.x
        self.y = event.y

    # this will perform the wait list actions until the next wait list is called
    def __perform_wait_list_actions__(self):
        for element in self.wait_queue:
            print(element)

    def __repeat_code__(self):
        if len(self.wait_queue) < WAIT_QUEUE_LIMIT:
            self.user_function(*self.arguments)
        self.root.after(DELAY, self.__repeat_code__)
