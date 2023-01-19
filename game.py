import pygame
import random


class Game:
    
    def __init__(self, cell_size: int, x_cells: int, y_cells: int) -> None:

        self.cell_size: int = cell_size
        self.x_cells: int = x_cells
        self.y_cells: int = y_cells
        self.nr_cells: int = self.x_cells * self.y_cells
        self.next_board: list[list[int]]
        self.running: bool = True
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.x_cells*self.cell_size, self.y_cells*self.cell_size))
        self.current_board: list[int] = self.generate_first_board(50)

    def start_game_loop(self) -> None:

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.QUIT:
                    self.running = False
                
            self.screen.fill((0,0,0))
            #self.screen.blit(self.draw_board(),(0,0))

            pygame.display.flip()

    def draw_board(self) -> pygame.Surface:
        pass

    def update_board(self) -> list[int]:
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

    def generate_first_board(self, nr_starting_cells: int) -> list[int]: 
        
        starting_cells = []
        starting_board = []

        # Generate random starting cells
        for i in range(0, nr_starting_cells):
            starting_cells.append(random.randint(0, self.nr_cells))

        # Set starting cells to 1 and the rest to 0
        for cell in range(0, self.nr_cells):
            if cell in starting_cells:
                starting_board.append(1)
            else:
                starting_board.append(0)
        
        return starting_board


    def calculate_neighbors(self,board: list[int]) -> list[int]:
        
        next_board = []

        for cell in range(0, self.nr_cells):
            
            next_board.append(0)

            if(board[cell-(self.y_cells+1)] == 1):
                next_board[cell] += 1
            if(board[cell-(self.y_cells)] == 1):
                next_board[cell] += 1
            if(board[cell-(self.y_cells-1)] == 1):
                next_board[cell] += 1
            if(board[cell-1] == 1):
                next_board[cell] += 1
                if(next_board[cell] > 3):
                    continue 
            if(board[cell+1] == 1):
                next_board[cell] += 1
                if(next_board[cell] > 3):
                    continue 
            if(board[cell+(self.y_cells-1)] == 1):
                next_board[cell] += 1
                if(next_board[cell] > 3):
                    continue 
            if(board[cell+(self.y_cells)] == 1):
                next_board[cell] += 1
                if(next_board[cell] > 3):
                    continue
            if(board[cell+(self.y_cells+1)] == 1):
                next_board[cell] += 1

        return next_board