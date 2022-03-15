import numpy as np
import pygame

class MAIN:
    def __init__(self):      
        self.main_Board_Obj = BOARD()
        self.main_Player_Obj = PLAYER()
        
    def drop_piece(self, board, row, col):
        board[row][col] = self.main_Player_Obj.get_name()
    
    def is_valid_position(self, board, col):
        return board[ROW_COUNT-1][col] == 0
            
    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r
            
    def winning_move(self, board, piece):
        # checking horizontally
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True
                
        # checking vertically
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True
                
        # checking positively sloped diagonals
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True
                
        # checking negatively sloped diagonals
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def player_won_lable(self):
        lable = game_font.render('Player ' + str(self.main_Player_Obj.get_name()) + ' won! Restart (y | n)?', True, 'black')
        screen.blit(lable, (20, 37))
        pygame.display.flip()

    def update_ui(self):
        self.main_Board_Obj.flip_zeros(board)
        self.main_Board_Obj.draw_board(board)            
        self.main_Player_Obj.switch_player()

    def restart(self):
        self.main_Board_Obj.clear()
        self.update_ui()
        self.main_Board_Obj.current_player = 0

class BOARD:
    def flip_zeros(self, board):
        print(np.flip(board, 0))
        print('\n')
    
    def draw_board(self, board):        
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                board_rect = pygame.Rect(int(c*SQUARE_SIZE), int(r*SQUARE_SIZE)+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, (50, 109, 255), board_rect)
                pygame.draw.circle(screen, 'white', (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS-10)
                pygame.draw.circle(screen, 'black', (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS-10, 2)
        
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, 'red', (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS-9)
                    pygame.draw.circle(screen, 'black', (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS-9, 2)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, 'yellow', (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS-9)
                    pygame.draw.circle(screen, 'black', (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS-9, 2)
        pygame.display.update()

    def clear(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                board[r][c] = 0
        
class PLAYER:
    def __init__(self):
        self.current_player = 0

    def get_name(self):
        if self.current_player == 0:
            return 1
        else:
            return 2
    
    def setting_player_color(self):
        pygame.draw.rect(screen, 'white', (0, 0, width, SQUARE_SIZE))
        posx = event.pos[0]
        if self.current_player == 0:
            pygame.draw.circle(screen, 'red', (posx, int(SQUARE_SIZE/2)), RADIUS-10)
        else:
            pygame.draw.circle(screen, 'yellow', (posx, int(SQUARE_SIZE/2)), RADIUS-10)
            
    def deciding_the_position(self):
        pygame.draw.rect(screen, 'white', (0, 0, width, SQUARE_SIZE))
        posx = event.pos[0]
        col = int(posx//SQUARE_SIZE)
        row = main_game.get_next_open_row(board, col)
        if main_game.is_valid_position(board, col):
            main_game.drop_piece(board, row, col)

    def switch_player(self):
        self.current_player += 1
        self.current_player = self.current_player % 2
            
COLUMN_COUNT = 7
ROW_COUNT = 6
SQUARE_SIZE = 95
RADIUS = int(SQUARE_SIZE/2)
board = np.zeros((ROW_COUNT, COLUMN_COUNT))
player_won = False
game_over = False

main_game = MAIN()
main_game.main_Board_Obj.flip_zeros(board)

pygame.init()
game_font = pygame.font.SysFont('Calibri', 25)

width = int(COLUMN_COUNT * SQUARE_SIZE)
height = int((ROW_COUNT+1) * SQUARE_SIZE)
size = (width, height)
screen = pygame.display.set_mode(size)
icon = pygame.image.load('Icons/icon_1.jpg')
pygame.display.set_icon(icon)
pygame.display.set_caption('Connect Four by @Victor_Azariah')
screen.fill('white')
main_game.main_Board_Obj.draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        elif player_won == False:
            if event.type == pygame.MOUSEMOTION:
                main_game.main_Player_Obj.setting_player_color()
                pygame.display.update()
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_game.main_Player_Obj.deciding_the_position()
                if main_game.winning_move(board, main_game.main_Player_Obj.get_name()):
                    main_game.player_won_lable()
                    player_won = True
                main_game.update_ui()

        elif player_won:
            if event.type == pygame.KEYUP:                             
                if event.key == pygame.K_y:    # yes key              
                    player_won = False
                    main_game.restart()
                elif event.key == pygame.K_n:    # no key
                    game_over = True
