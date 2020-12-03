from maze.MazeUtils import *
from maze.Grid import Grid
from values.Constants import *
import time


class Testing:
    __solutionStartX = MAZE_WIDTH
    __solutionStartY = MAZE_HEIGHT

    def __init__(self, screen: Union[Surface, SurfaceType], grid_instance: Grid):
        self.__screen = screen
        self.__grid = grid_instance.grid
    # init()

    # ---------- General Solution Functions ---------- #

    def solve_maze(self):
        self.__mark_start_exit()
        self.__recursive_solution()

    def __mark_start_exit(self):
        """
        Convenience function for drawing the solution's start and exit positions as red and green cells, respectively.
        """

        draw_maze_cell(self.__solutionStartX, self.__solutionStartY, self.__screen, None, Colour.RED)
        draw_maze_cell(ROOT_X, ROOT_Y, self.__screen, None, Colour.GREEN)
    # mark_start_exit()

    def __draw_solution_cell(self, x, y) -> None:
        """
        Draws a red circle in the center of the cell at position (x, y).
        Used to draw individual steps in the solution path.

        :param x: x-coordinate to draw circle on
        :param y: x-coordinate to draw circle on
        """

        # Add an offset to place the circle in the center of the cell
        x += CELL_SIZE / 2
        y += CELL_SIZE / 2
        pygame.draw.circle(self.__screen, Colour.RED.value, (x, y), 3)
        pygame.display.update()

    # draw_solution_cell()

    # ---------- Recursive Solution Functions ---------- #

    def __recursive_solution(self, x = MAZE_WIDTH, y = MAZE_HEIGHT) -> bool:

        if ANIMATIONS_ENABLED:
            time.sleep(.05)

        print(x, y)

        if (x, y) == (ROOT_X, ROOT_Y):
            print("EXIT FOUND")
            return True
        elif self.__grid[x, y].visited_while_solving:
            print(f"Already visited cell at ({x},{y})")
            return False

        self.__grid[x, y].visited_while_solving = True
        print(self.__grid[x, y].walls)

        if (not self.__grid[x, y].walls[Direction.LEFT] and x - CELL_SIZE > 0 and self.__recursive_solution(x - CELL_SIZE, y)) or (
            not self.__grid[x, y].walls[Direction.RIGHT] and x + CELL_SIZE <= MAZE_WIDTH and self.__recursive_solution(x + CELL_SIZE, y)) or (
            not self.__grid[x, y].walls[Direction.UP] and y - CELL_SIZE > 0 and self.__recursive_solution(x, y - CELL_SIZE)) or (
            not self.__grid[x, y].walls[Direction.DOWN] and y + CELL_SIZE <= MAZE_HEIGHT and self.__recursive_solution(x, y + CELL_SIZE)):
            self.__draw_solution_cell(x, y)
            return True

        return False
