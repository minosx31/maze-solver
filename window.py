from tkinter import Tk, BOTH, Canvas
from graphics import Point, Line

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Create root widget
        self.__root = Tk()
        self.__root.title = "Maze"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        # Canvas widget
        self.canvas = Canvas(self.__root, height=self.height, width=self.width)
        self.canvas.pack()
        
        # Set isRunning
        self.isRunning = False

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self):
        self.isRunning = True
        while self.isRunning:
            self.redraw()

    def close(self):
        self.isRunning = False

    def draw_line(self, line: Line, fill_color="black"):
        line.draw(self.canvas, fill_color)
