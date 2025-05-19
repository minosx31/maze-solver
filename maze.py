from cell import Cell
import time, random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        if seed: random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def get_cells(self):
        return self._cells

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _draw_cell(self, i, j):
        if not self.win: return

        x1 = self.x1 + ( i * self.cell_size_x )
        y1 = self.y1 + ( j * self.cell_size_y )
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        # Draw cell
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _create_cells(self):
        # Create x * y cells
        for x in range(self.num_cols):
            column = []
            for y in range(self.num_rows):
                column.append(Cell(self.win))
            self._cells.append(column)
        # Draw each cell
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                self._draw_cell(x, y)
    
    def _break_entrance_and_exit(self):
        # Entrance
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        # Exit
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        self._draw_cell(self.num_cols-1,self.num_rows-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_visit = []
            for r,c in [[-1,0], [1,0], [0,-1], [0,1]]:
                ni, nj = i+r, j+c
                if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and not self._cells[ni][nj].visited:
                    to_visit.append((ni, nj))

            if not to_visit:
                self._draw_cell(i, j)
                break

            randDir = random.randint(0, len(to_visit)-1)
            visiting_cell = to_visit[randDir]

            if i < visiting_cell[0]:
                self._cells[i][j].has_right_wall = False
                self._cells[visiting_cell[0]][j].has_left_wall = False
            elif i > visiting_cell[0]:
                self._cells[i][j].has_left_wall = False
                self._cells[visiting_cell[0]][j].has_right_wall = False
            elif j < visiting_cell[1]:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][visiting_cell[1]].has_top_wall = False
            else:
                self._cells[i][j].has_top_wall = False
                self._cells[i][visiting_cell[1]].has_bottom_wall = False


            self._break_walls_r(visiting_cell[0], visiting_cell[1])

    def _reset_cells_visited(self):
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                self._cells[x][y].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows:
            return True

        for r,c in [[-1,0], [1,0], [0,-1], [0,1]]:
            ni, nj = i+r, j+c
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and not self._cells[ni][nj].visited:
                if i < ni:
                    if not self._cells[i][j].has_right_wall and not self._cells[ni][j].has_left_wall:
                        self._cells[i][j].draw_move(self._cells[ni][j])
                        if self._solve_r(ni, j):
                            return True
                        else:
                            self._cells[i][j].draw_move(self._cells[ni][j], True)
                elif i > ni:
                    if not self._cells[i][j].has_left_wall and not self._cells[ni][j].has_right_wall:
                        self._cells[i][j].draw_move(self._cells[ni][j])
                        if self._solve_r(ni, j):
                            return True
                        else:
                            self._cells[i][j].draw_move(self._cells[ni][j], True)
                elif j < nj:
                    if not self._cells[i][j].has_bottom_wall and not self._cells[i][nj].has_top_wall:
                        self._cells[i][j].draw_move(self._cells[i][nj])
                        if self._solve_r(i, nj):
                            return True
                        else:
                            self._cells[i][j].draw_move(self._cells[i][nj], True)
                else:
                    if not self._cells[i][j].has_top_wall and not self._cells[i][nj].has_bottom_wall:
                        self._cells[i][j].draw_move(self._cells[i][nj])
                        if self._solve_r(i, nj):
                            return True
                        else:
                            self._cells[i][j].draw_move(self._cells[i][nj], True)
        return False
