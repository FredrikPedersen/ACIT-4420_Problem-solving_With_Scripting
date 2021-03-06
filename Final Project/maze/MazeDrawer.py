import random
from typing import Dict, List, Set, Tuple

from maze.Cell import Cell
from maze.Grid import Grid
from utilities.DrawUtills import *


class MazeDrawer:

    """
    Class used to draw a maze upon the grid by colouring cells and walls in different colours.
    """

    def __init__(self, screen: Union[Surface, SurfaceType]):
        grid_instance: Grid = Grid.get_instance()

        self.__screen = screen
        self.__grid: Dict[Tuple[int, int], Cell] = grid_instance.generate_grid()
    # __init__()

    def draw(self):
        """
        Public facing convenience function for performing all drawing tasks of this class
        """

        self.__draw_grid()
        self.__draw_maze()
    # draw()

    def __draw_grid(self) -> None:
        """
        Draws black lines around each cell in the grid, which will represent walls in the graphical output.
        Starts in the left-most corner of the cell and draws lines at the top, bottom, right and left-egdes, respectively.
        """

        for coordinates in self.__grid:
            x: int = coordinates[0]
            y: int = coordinates[1]

            pygame.draw.line(self.__screen, Colour.BLACK.value, [x, y], [x + Constants.CELL_SIZE, y])
            pygame.draw.line(self.__screen, Colour.BLACK.value, [x + Constants.CELL_SIZE, y + Constants.CELL_SIZE], [x, y + Constants.CELL_SIZE])
            pygame.draw.line(self.__screen, Colour.BLACK.value, [x + Constants.CELL_SIZE, y], [x + Constants.CELL_SIZE, y + Constants.CELL_SIZE])
            pygame.draw.line(self.__screen, Colour.BLACK.value, [x, y + Constants.CELL_SIZE], [x, y])
            pygame.display.update()
    # draw_grid()

    def __draw_maze(self) -> None:
        """
        Iterative randomized depth-first search to create a maze on a grid of cells.
        For each step of the algorithm:
            1. Mark the current cell as visited
            2. While the current cell has any unvisited neighbour cells:
                 - Choose one of the unvisited neighbours.
                 - Remove the wall between the current cell and the chosen neighbouring cell.
                 - Invoke the routine for the chosen neighbouring cell.
        """

        x = Constants.ROOT_X
        y = Constants.ROOT_Y

        # Mark the starting location as visited, add it to the stack and draw it.
        visited: Set[Tuple[int, int]] = {(x, y)}
        stack: List[Tuple[int, int]] = [(x, y)]

        while len(stack) > 0:

            neighbouring_cells: List[Direction] = self.__find_unvisited_neighbours(x, y, visited)

            if len(neighbouring_cells) > 0:

                # Select a neighbour at random
                chosen_neighbour: Direction = (random.choice(neighbouring_cells))

                if chosen_neighbour == Direction.RIGHT:
                    self.__grid[(x, y)].toggle_wall(Direction.RIGHT)
                    self.__grid[x + Constants.CELL_SIZE, y].toggle_wall(Direction.LEFT)

                    draw_maze_cell(x, y, self.__screen, Direction.RIGHT)

                    x = x + Constants.CELL_SIZE
                    visited.add((x, y))
                    stack.append((x, y))

                elif chosen_neighbour == Direction.LEFT:
                    self.__grid[(x, y)].toggle_wall(Direction.LEFT)
                    self.__grid[x - Constants.CELL_SIZE, y].toggle_wall(Direction.RIGHT)

                    draw_maze_cell(x, y, self.__screen, Direction.LEFT)

                    x = x - Constants.CELL_SIZE
                    visited.add((x, y))
                    stack.append((x, y))

                elif chosen_neighbour == Direction.DOWN:
                    self.__grid[(x, y)].toggle_wall(Direction.DOWN)
                    self.__grid[x, y + Constants.CELL_SIZE].toggle_wall(Direction.UP)

                    draw_maze_cell(x, y, self.__screen, Direction.DOWN)

                    y = y + Constants.CELL_SIZE
                    visited.add((x, y))
                    stack.append((x, y))

                elif chosen_neighbour == Direction.UP:
                    self.__grid[(x, y)].toggle_wall(Direction.UP)
                    self.__grid[x, y - Constants.CELL_SIZE].toggle_wall(Direction.DOWN)

                    draw_maze_cell(x, y, self.__screen, Direction.UP)

                    y = y - Constants.CELL_SIZE
                    visited.add((x, y))
                    stack.append((x, y))

            else:

                # If all neighbouring cells are visited, remove the current one from the stack
                x, y = stack.pop()
                self.__draw_backtracking_cell(x, y)
    # draw_maze()

    def __find_unvisited_neighbours(self, x: int, y: int, visited: Set[Tuple[int, int]]) -> List[Direction]:
        """
        Finds all the existing unvisited neighbour for the current cell (x, y).

        :param x: x-coordinate of current cell.
        :param y: y-coordinate of current cell.
        :param visited: List of all visited cells in the current maze.
        :return: List of the direction of all unvisited neighbours of the current cell (x, y).
        """

        neighbouring_cells: List[Direction] = []

        # Check if right, left, bottom and top cells are already visited and exists, respectively.
        if (x + Constants.CELL_SIZE, y) not in visited and (x + Constants.CELL_SIZE, y) in self.__grid:
            neighbouring_cells.append(Direction.RIGHT)

        if (x - Constants.CELL_SIZE, y) not in visited and (x - Constants.CELL_SIZE, y) in self.__grid:
            neighbouring_cells.append(Direction.LEFT)

        if (x, y + Constants.CELL_SIZE) not in visited and (x, y + Constants.CELL_SIZE) in self.__grid:
            neighbouring_cells.append(Direction.DOWN)

        if (x, y - Constants.CELL_SIZE) not in visited and (x, y - Constants.CELL_SIZE) in self.__grid:
            neighbouring_cells.append(Direction.UP)

        return neighbouring_cells
    # find_unvisited_neighbours()

    def __draw_backtracking_cell(self, x, y) -> None:
        """
        Draws a red square at position (x, y), then changes the colour back to default after .05 seconds.
        This creates a blinking red cell, used for displaying how the maze-algorithm backtracks through the stack.

        :param x: x-coordinate to draw red cell at
        :param y: y-coordinate to draw red cell at
        """

        # Offsets to make sure the maze's tile colour does not fill over the wall colour.
        rectangle_size: int = Constants.CELL_SIZE - 1

        pygame.draw.rect(self.__screen, Colour.RED.value, (x + 1, y + 1, rectangle_size, rectangle_size), 0)
        pygame.display.update()

        sleep_if_animation()

        # Change colour back after the backtracking has been displayed
        draw_maze_cell(x, y, self.__screen)
        pygame.display.update()
    # draw_backtracking_cell()
