import pygame, random, sys

pygame.init()
pygame.font.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
BROWN = (205, 124,69)

WIDTH, HEIGHT = 400,400
BOARDWIDTH, BOARDHEIGHT = 3,3
SQUARESIZE = 100
XMARGIN = int((WIDTH - (SQUARESIZE * BOARDWIDTH + (BOARDWIDTH - 1)))/2)
YMARGIN = int((HEIGHT - (SQUARESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1)))/2)

BACKGROUND = pygame.transform.scale(pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\wood_background.png"), (WIDTH, HEIGHT))

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Tic Tac Toe')

def print_board(b, a): # b = board , a = available 
    print('Here is the board\n\n')
    print('          '+a[7] +'|'+ a[8] +'|'+ a[9]+'        '+b[7]+'|'+b[8]+'|'+b[9])
    print('          '+'-----        -----')
    print('          '+a[4] +'|'+ a[5] +'|'+ a[6]+'        '+b[4]+'|'+b[5]+'|'+b[6])
    print('          '+'-----        -----')
    print('          '+a[1] +'|'+ a[2] +'|'+ a[3]+'        '+b[1]+'|'+b[2]+'|'+b[3]+'\n')

def draw_board(screen):
    playx = WIDTH - 2*XMARGIN
    playy = HEIGHT - 2*YMARGIN
    pygame.draw.line(screen, WHITE, (int(playx//3) + XMARGIN, YMARGIN), (int(playx//3) +XMARGIN, HEIGHT-YMARGIN), 4)
    pygame.draw.line(screen, WHITE, (int(playx//3)*2+XMARGIN, YMARGIN), (int(playx//3)*2 + XMARGIN, HEIGHT-YMARGIN), 4)
    pygame.draw.line(screen, WHITE, (XMARGIN, int(playy//3)+ YMARGIN), (WIDTH-XMARGIN, int(playy//3)+YMARGIN), 4)
    pygame.draw.line(screen, WHITE, (XMARGIN, int(playy//3)*2+YMARGIN), (WIDTH-XMARGIN, int(playy//3)*2 + YMARGIN), 4)

def win_check(board, mark):
    for x in range(BOARDWIDTH): # checking horizontals
        for y in range(BOARDHEIGHT-2):
            if board[x][y]==board[x][y+1]==board[x][y+2]==mark:
                return True
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH-2):
            if board[x][y] == board[x+1][y] == board[x+2][y] == mark:
                return True
    for x in range(BOARDWIDTH-2):
        for y in range(BOARDHEIGHT-2):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == mark:
                return True
    board.reverse()
    for x in range(BOARDWIDTH-2):
        for y in range(BOARDHEIGHT-2):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == mark:
                return True
    return False
    
def handle_moves(board,x,y, human,ai):
    board[x][y] = human
    if not win_check(board,human):
        x, y = ai_move(board, ai, human)
        if x != None and y != None:
            board[x][y] = ai

def ai_move(board,ai,human):
    possible_moves = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == 0:
                possible_moves.append((x,y))
    move = (None,None)
    
    for letter in [ai,human]:
        for possible in possible_moves:
            board_copy = board[:] # lists are mutable and to avoid altering the board we make a copy
            x, y = possible
            board_copy[x][y] = letter
            if win_check(board_copy, letter):
                return possible
    
    open_corners = [x for x in possible_moves if x in [(0,0),(0,2),(2,0),(2,2)]]
    if len(open_corners) > 0:
        move = random.choice(open_corners)
        return move 

    if (1,1) in possible_moves:
        move = (1,1)
        return move
    
    edges_open = [x for x in possible_moves if x in [(0,1),(1,0),(1,2),(2,1)]]
    if len(edges_open) > 0:
        move = random.choice(edges_open)
    
    return move

def get_board():
    board = []
    for _ in range(BOARDWIDTH):
        column = [] 
        for _ in range(BOARDHEIGHT):
            column.append(0)
        board.append(column)
    return board

def full_board(board):
    for row in board:
        if 0 in row:
            return False
    return True

def getLeftTopSquare(squarex, squarey):
    left = XMARGIN + (squarex * SQUARESIZE) + (squarex - 1)
    top = YMARGIN + (squarey* SQUARESIZE) + (squarey - 1)
    return (left, top)

def getSpotClicked(board, x, y, mark):
    for squarex in range(len(board)):
        for squarey in range(len(board[0])):
            left, top = getLeftTopSquare(squarex, squarey)
            squareRect = pygame.Rect(left, top, SQUARESIZE, SQUARESIZE)
            if squareRect.collidepoint(x,y):
                board[squarex][squarey] = mark

def main():

    
    board = [' ' for _ in range(10)]
    available = [str(x) for x in range(10)] # available postions that are shown to the user

    toggle = random.choice((1,-1))
    players = [0, 'X', 'O']
    human = players[toggle]
    ai = players[toggle *-1]
    print(f'Your mark is {human} human and you will go first!')

    while False:
        print_board(board,available)
        
        if not (win_check(board, ai)):
           handle_moves(board,human, available)
        else:
            print(f'Sorry {ai}\'s won this time!')
            break
           
        if not (win_check(board, human)):
            
            move = ai_move(board, ai, human)
            if move == 0:
               print_board(board,available)
               print('Tie game!')
            else:
                insert_letter(board, ai, move, available)
                print(f'Computer placed an \'{ai}\' in position {move}')
                
            
        else:
            print_board(board, available)
            print('You won this game! Great job!')
            break
        
def new_main():
    FPSCLOCK = pygame.time.Clock()
    Board = get_board()
    
    toggle = random.choice((1,-1))
    PLAYERS = [0, 'X', 'O']
    human = PLAYERS[toggle]
    Ai = PLAYERS[toggle *-1]

    while not full_board(Board):
        #SCREEN.fill(WHITE)
        
        print(human, Ai)
        SCREEN.blit(BACKGROUND, (0,0))
        draw_board(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:#(event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP7:
                    handle_moves(Board, 0,0,human,Ai)
                if event.key == pygame.K_KP8:
                    handle_moves(Board, 0,1,human,Ai)
                if event.key == pygame.K_KP9:
                    handle_moves(Board,0,2,human,Ai)
                if event.key == pygame.K_KP4:
                    handle_moves(Board, 1,0,human,Ai)
                if event.key == pygame.K_KP5:
                    handle_moves(Board, 1,1,human,Ai)
                if event.key == pygame.K_KP6:
                    handle_moves(Board, 1,2,human,Ai)
                if event.key == pygame.K_KP1:
                    handle_moves(Board, 2,0,human,Ai)
                if event.key == pygame.K_KP2:
                    handle_moves(Board, 2,1,human,Ai)
                if event.key == pygame.K_KP3:
                    handle_moves(Board, 2,2,human,Ai)
                
            
            elif event.type == pygame.MOUSEBUTTONUP:
                getSpotClicked(Board, event.pos[0], event.pos[1], human)
            
        if win_check(Board, human):
            print('You won!')
            break
        print(Board)
        if win_check(Board, Ai):
            print('Congrats you coded!')
            break

        FPSCLOCK.tick(1)
        pygame.display.update()



if __name__ == '__main__':
    new_main()
    
    # if input('Do you want to play again? (Y/N)').upper().startswith('Y'):
    #     continue
    # else:
    #     pygame.quit()
    #     sys.exit()

