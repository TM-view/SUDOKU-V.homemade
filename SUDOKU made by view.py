import sys, random, pygame as pg
from collections import defaultdict
from time import time

pg.init()
screen_size = (740, 790)
screen = pg.display.set_mode(screen_size)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BOARDER = (10, 10, 720, 720)
ANS = [[0]*9 for _ in range(9)]
SHOW = [[None]*9 for _ in range(9)]
KEEP = [[None]*9 for _ in range(9)]
CLICK = [pg.Rect(75*x + 60, 740, 40, 100) for x in range(9)]
INSTEAD = [pg.Rect(80*x + 10, 80*y + 10, 90, 90) for x in range(9) for y in range(9)]
CHOOSE = 0
SAME = 0
COMPLETE = set()
WIN = False
INCORRECT_POS = defaultdict(float)
WRONG = False
X = 0

def set_background():
    screen.fill(BLACK)
    pg.draw.rect(screen, WHITE, BOARDER)
    for x in range(1, 9):
        if x % 3 == 0:
            pg.draw.line(screen, BLACK, (80*x+10, 10), (80*x+10, 730), 7)
        pg.draw.line(screen, BLACK, (80*x+10, 10), (80*x+10, 730), 3)
    for y in range(1, 9):
        if y % 3 == 0:
            pg.draw.line(screen, BLACK, (10, 80*y+10), (730, 80*y+10), 7)
        pg.draw.line(screen, BLACK, (10, 80*y+10), (730, 80*y+10), 3)

def is_valid(ANS, row, col, num):
    for i in range(9):
        if ANS[row][i] == num or ANS[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if ANS[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board():
    for row in range(9):
        for col in range(9):
            if ANS[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(ANS, row, col, num):
                        ANS[row][col] = num
                        if fill_board():
                            return True
                        ANS[row][col] = 0
                return False
    return True

def initialize_show():
    for i in range(9):
        for j in range(9):
            if random.random() < 0.4:  # 0-1 more = easy, less = hard 
                SHOW[i][j] = ANS[i][j]
                KEEP[i][j] = ANS[i][j]
            else:
                SHOW[i][j] = 0
                KEEP[i][j] = 0

def draw_numbers():
    global WIN
    font = pg.font.Font(None, 48)
    for list in range(9):
        for row in range(3):
            for col in range(3):
                if SHOW[(list//3)*3 + row][(list%3)*3 + col] != 0 and not WIN:
                    if SHOW[(list//3)*3 + row][(list%3)*3 + col] != ANS[(list//3)*3 + row][(list%3)*3 + col]:
                        text = font.render(str(SHOW[(list//3)*3 + row][(list%3)*3 + col]), True, RED)
                    elif SHOW[(list//3)*3 + row][(list%3)*3 + col] == SAME and SAME != 0 and SHOW[(list//3)*3 + row][(list%3)*3 + col] == ANS[(list//3)*3 + row][(list%3)*3 + col]:
                        text = font.render(str(SHOW[(list//3)*3 + row][(list%3)*3 + col]), True, GREEN)
                    else:    
                        text = font.render(str(SHOW[(list//3)*3 + row][(list%3)*3 + col]), True, BLACK)
                    text_direction = text.get_rect(center=(((list%3) * 240) + (col*80) + 50, ((list//3) * 240) + (row*80) + 50))
                    screen.blit(text, text_direction)

    for num in range(1, 10): 
        if num in COMPLETE: 
            continue
        else:
            if num == CHOOSE:
                select_number = font.render(str(num), True, BLUE)            
            else:
                select_number = font.render(str(num), True, WHITE)
            select_direction = select_number.get_rect(center=(num*75, 760))
            screen.blit(select_number, select_direction)
    
    winFont = pg.font.Font(None, 80)
    if WIN:
        message = winFont.render("NAH U'D WIN", True, RED)
        message_direction = message.get_rect(center=(370,370))
        screen.blit(message, message_direction)

def detect_pos(posX):
    global CHOOSE
    if CHOOSE == 0:
        positions = [(1, 0, 100), (2, 134, 175), (3, 209, 250), 
                     (4, 284, 325), (5, 359, 400), (6, 424, 465), 
                     (7, 499, 540), (8, 574, 615), (9, 649, 690)]
        
        for position, start, end in positions:
            if start < posX <= end and position not in COMPLETE:
                CHOOSE = position
                break
        
        if SAME in COMPLETE:
            CHOOSE = 0
    else:
        CHOOSE = 0

def find_index(pos):
    x, y = pos[0] // 80, pos[1] // 80
    return y, x

def detect_complete(SHOW):
    lst = [element for list in SHOW for element in list]
    for i in range(1,10):
        if lst.count(i) == 9:
            COMPLETE.add(i)

def game_run():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for rect in CLICK:
                if rect.collidepoint(mouse_pos):
                    detect_pos(mouse_pos[0])
            
            global CHOOSE
            for rect in INSTEAD:
                if rect.collidepoint(mouse_pos):
                    row, col = find_index(mouse_pos)
                    if CHOOSE != 0 and KEEP[row][col] == 0 and SHOW[row][col] != ANS[row][col]:
                        SHOW[row][col] = CHOOSE
                        
                        if SHOW[row][col] != ANS[row][col]:
                            global WRONG
                            global X
                            WRONG = True
                            X += 1
                            INCORRECT_POS[(row, col)] = time()
                    
                    global SAME
                    if SAME == 0:
                        SAME = SHOW[row][col]
                    elif SAME != 0 and SAME not in COMPLETE:
                        if SAME != CHOOSE:
                            SAME = 0
                    elif CHOOSE in COMPLETE and SAME != 0:
                        SAME = 0

        if SAME in COMPLETE:
            SAME = 0
        if CHOOSE in COMPLETE:
            CHOOSE = 0
        
        global WIN
        if ANS == SHOW:
            for i in range(9):
                for j in range(9):
                    SHOW[i][j] == 0
            WIN = True
    
    current_time = time()
    for pos, timestamp in list(INCORRECT_POS.items()):
        if current_time - timestamp > 3:
            row, col = pos
            SHOW[row][col] = 0
            del INCORRECT_POS[pos]
            WRONG = False
    
    if X > 2 :
        sys.exit()
    
    if not WRONG :
        detect_complete(SHOW)
    set_background()
    draw_numbers()
    pg.display.flip()

fill_board()
initialize_show()

while True:
    game_run()