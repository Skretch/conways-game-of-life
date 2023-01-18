import pygame


class Game:
    
    def __init__(self, board_size: tuple[int, int], cell_size: int):

        self.cell_size: int = cell_size
        self.board_size: tuple[int,int] = board_size
        self.next_board: list[list[int]]
        self.running: bool = True
        
        pygame.init()
        self.screen = pygame.display.set_mode(self.board_size)
        self.current_board: list[list[int]] = self.generate_first_board(50)
        self.game_loop()

    def game_loop(self) -> None:

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

    def update_board(self) -> list[list[int]]:
        """
        Rules:
        1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        2. Any live cell with two or three live neighbours lives on to the next generation.
        3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        5. Edges loop around to the other side of the board.
        """
        pass

    def generate_first_board(self, nr_starting_cells: int) -> list[list[int]]:
        pass