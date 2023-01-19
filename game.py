import time
import numpy as np
import pygame
import random


class Game:
    
    def __init__(self, cell_size: int, x_cells: int, y_cells: int) -> None:
        
        before_time = time.time_ns()
        
        self.cell_size: int = cell_size
        self.x_cells: int = x_cells
        self.y_cells: int = y_cells
        self.nr_cells: int = self.x_cells * self.y_cells
        self.next_board: np.ndarray = np.zeros(self.nr_cells, dtype=int)
        self.living_cells: np.ndarray = np.random.randint(0, self.nr_cells, int(self.nr_cells/10))
        self.dying_cells: np.ndarray = np.empty(0, dtype=int)
        self.running: bool = True
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.x_cells*self.cell_size, self.y_cells*self.cell_size))
        self.current_board: np.ndarray = self.generate_first_board(int(self.nr_cells/10))

        print(f"Game init took {(time.time_ns() - before_time)/1000000} ms")

    def start_game_loop(self) -> None:
        frames = 0
        draw_time = 0
        update_time = 0
        total_time = 0

        while self.running:
            before_time = time.time_ns()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.QUIT:
                    self.running = False

            before_draw = time.time_ns()

            self.screen.fill((0,0,0))
            self.screen.blit(self.draw_board(),(0,0))

            pygame.display.flip()

            after_draw = time.time_ns()

            self.update_board()
            
            frames += 1
            after_time = time.time_ns()
            draw_time = draw_time + (after_draw - before_draw)/1000000
            update_time = update_time + (after_time - after_draw)/1000000
            total_time = total_time + (after_time - before_time)/1000000
            if(frames == 10):
                print(f"Draw time: {'{:.2f}'.format(draw_time/frames)} ms | Update time: {'{:.2f}'.format(update_time/frames)} ms | Total time: {'{:.2f}'.format(total_time/frames)} ms")
                total_time = 0
                draw_time = 0
                update_time = 0
                frames = 0
            

    def draw_board(self) -> pygame.Surface:

        board = pygame.Surface((self.x_cells*self.cell_size, self.y_cells*self.cell_size))
        cell = pygame.Surface((self.cell_size, self.cell_size))

        cell.fill((255,255,255))

        for cell_nr in range(0, self.nr_cells):
            if self.current_board[cell_nr] == 1:
                board.blit(cell, ((cell_nr%(self.x_cells))*self.cell_size, int(cell_nr / (self.y_cells))*self.cell_size))

        return board        

        pass

    def update_board(self) -> np.ndarray:
        """
        Rules:
        1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        2. Any live cell with two or three live neighbours lives on to the next generation.
        3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        5. Edges loop around to the other side of the board.
        """
        board = self.current_board
        next_board = self.calculate_neighbors(board)
        for cell in range(0, self.nr_cells):
            if board[cell] == 1:
                if next_board[cell] < 2 or next_board[cell] > 3:
                    board[cell] = 0
            else:
                if next_board[cell] == 3:
                    board[cell] = 1

        return board

    def generate_first_board(self, nr_starting_cells: int) -> np.ndarray: 
        
        starting_cells = np.zeros(nr_starting_cells, dtype=int)
        starting_board = np.zeros(self.nr_cells, dtype=int)

        # Generate random starting cells
        for i in range(0, nr_starting_cells):
            starting_cells[i] = np.random.randint(0, self.nr_cells)

        # Set starting cells to 1 and the rest to 0
        for cell in range(0, nr_starting_cells):
            starting_board[starting_cells[cell]] = 1
        
        return starting_board


    def calculate_neighbors(self,board: np.ndarray) -> np.ndarray:
        
        next_board = np.zeros(self.nr_cells, dtype=int)

        for count in range(0, self.nr_cells):
            cell = count

            top_left,top,top_right,left,right,bottom_left,bottom, bottom_right = self.calculate_neighbor_positions(cell)

            next_board[cell] = board[top_left] + board[top] + board[top_right] + board[left] + board[right] + board[bottom_left] + board[bottom] + board[bottom_right]
            

        return next_board

    def calculate_neighbor_positions(self, cell) -> tuple[int,int,int,int,int,int,int,int]:
        
        top_left = cell - (self.x_cells+1)
        top = cell - self.x_cells
        top_right = cell - (self.x_cells-1)
        left = cell - 1
        right = cell + 1

        if(right >= self.nr_cells):
            right = right - self.nr_cells
        bottom_left = cell + (self.x_cells-1)
        if(bottom_left >= self.nr_cells):
            bottom_left = bottom_left - self.nr_cells
        bottom = cell + self.x_cells
        if(bottom >= self.nr_cells):
            bottom = bottom - self.nr_cells
        bottom_right = cell + (self.x_cells+1)
        if(bottom_right >= self.nr_cells):
            bottom_right = bottom_right - self.nr_cells
        
        return top_left, top, top_right, left, right, bottom_left, bottom, bottom_right
        

"""
1 2 3
4 5 6
7 8 9

1 2 3 4 5 6 7 8 9
"""