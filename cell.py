from graphics import Point, Line

class Cell:
    def __init__(self, win):
        self._win = win
        self._x1 = -1
        self._x2 = -1
        self._y1 = -1
        self._y2 = -1
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black" if self.has_left_wall else "white")
        self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black" if self.has_right_wall else "white")
        self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black" if self.has_top_wall else "white")
        self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black" if self.has_bottom_wall else "white")

    def draw_move(self, to_cell, undo=False):
        start_point = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)

        end_point = Point((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)

        self._win.draw_line(Line(start_point, end_point), "gray" if undo else "red")
            