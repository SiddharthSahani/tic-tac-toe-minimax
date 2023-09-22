
import pygame as pg
pg.init()


cell_size = 100
border = 1
total_cell_size = cell_size + 2*border


screen = pg.display.set_mode((total_cell_size*3, total_cell_size*3))
pg.display.set_caption("Tic Tac Toe")
clock = pg.time.Clock()
font = pg.font.SysFont("Consolas", cell_size, True)


background_color = pg.Color("#020D36")
symbol_color = pg.Color("#E4E6EB")


empty_cell_surf = pg.Surface((cell_size, cell_size))
empty_cell_surf.fill(background_color)

cross_cell_surf = empty_cell_surf.copy()
pg.draw.line(cross_cell_surf, symbol_color, (0.2*cell_size, 0.2*cell_size), (0.8*cell_size, 0.8*cell_size), 5)
pg.draw.line(cross_cell_surf, symbol_color, (0.2*cell_size, 0.8*cell_size), (0.8*cell_size, 0.2*cell_size), 5)

zero_cell_surf = empty_cell_surf.copy()
pg.draw.circle(zero_cell_surf, symbol_color, (cell_size/2, cell_size/2), 0.4*cell_size, 4)


Board = list[str]

AI = 'O'
PLAYER = 'X'


def draw_board(board: Board) -> None:
    for i in range(3):
        for j in range(3):
            pos = i*3 + j

            match board[pos]:
                case 'X': surf = cross_cell_surf
                case 'O': surf = zero_cell_surf
                case _:   surf = empty_cell_surf

            screen.blit(surf, (j*total_cell_size + border, i*total_cell_size + border))


def evaluate_board(board: Board) -> int:
    # +10 for O winning
    # -10 for X winning
    # else 0

    # rows
    for i in range(3):
        if board[i*3+0] == board[i*3+1] == board[i*3+2]:
            if board[i*3] == 'O':
                return +10
            if board[i*3] == 'X':
                return -10
    
    # cols
    for i in range(3):
        if board[i+3*0] == board[i+3*1] == board[i+3*2]:
            if board[i] == 'O':
                return +10
            if board[i] == 'X':
                return -10
    
    # diags
    if board[0] == board[4] == board[8]:
        if board[0] == 'O':
            return +10
        if board[0] == 'X':
            return -10
    if board[2] == board[4] == board[6]:
        if board[2] == 'O':
            return +10
        if board[2] == 'X':
            return -10
    
    return 0


def get_empty_positions(board: Board) -> list[int]:
    return [i for i in range(9) if board[i] == '.']


def minimax(board: Board, maximizing: bool) -> int:
    evaluation = evaluate_board(board)
    if evaluation != 0:
        return evaluation

    possible_positions = get_empty_positions(board)

    if not possible_positions:
        return 0

    if maximizing:
        best_score = -1000
        for pos in possible_positions:
            board[pos] = 'O'
            score = minimax(board, False)
            board[pos] = '.'
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for pos in possible_positions:
            board[pos] = 'X'
            score = minimax(board, True)
            board[pos] = '.'
            best_score = min(score, best_score)
        return best_score


def find_best_move(board: Board) -> int:
    maximizing = True if AI == 'O' else False
    best_move = -1
    best_score = 1000 * (-1 if maximizing else +1)

    for pos in get_empty_positions(board):

        board[pos] = AI
        score = minimax(board, not maximizing)
        board[pos] = '.'
        
        if maximizing:
            if score > best_score:
                best_score = score
                best_move = pos
        else:
            if score < best_score:
                best_score = score
                best_move = pos

    return best_move


def play_best_move(board: Board) -> None:
    best = find_best_move(board)
    if best != -1:
        board[best] = AI


def main():
    running = True
    game_over = False

    board = ['.'] * 9
    if AI == 'O':
        play_best_move(board)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONUP and not game_over:
                mouse_pos = pg.mouse.get_pos()
                col = mouse_pos[0] // total_cell_size
                row = mouse_pos[1] // total_cell_size
                pos = row*3 + col

                if board[pos] == '.':
                    board[pos] = PLAYER
                    play_best_move(board)

        clock.tick(30)
        screen.fill("green")

        draw_board(board)
        
        pg.display.update()


if __name__ == '__main__':
    main()
