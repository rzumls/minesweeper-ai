import pygame

pygame.init() 

WIDTH = 300
HEIGHT = 300

ROWS = 8
COLS = 8

GRAY = (200, 200, 200) 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Minesweeper") 

cell_width = WIDTH // COLS
cell_height = HEIGHT // ROWS

clicked_tiles = [[False for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid(rows, cols): 
    for row in range(rows): 
        for col in range(cols): 
            x = col * cell_width
            y = row * cell_height
            rect = pygame.Rect(x, y, cell_width, cell_height)
            
            if clicked_tiles[row][col]:
                pygame.draw.rect(screen, RED, rect)  
            else:
                pygame.draw.rect(screen, GRAY, rect) 


            pygame.draw.rect(screen, WHITE, rect, 1)

def handle_tile_click(pos):

    mouse_x, mouse_y = pos
    col = mouse_x // cell_width
    row = mouse_y // cell_height
    
    clicked_tiles[row][col] = not clicked_tiles[row][col]
    print(f"Tile clicked: Row {row}, Column {col}")

# Main loop
run = True
while run: 
    screen.fill(WHITE)  
    draw_grid(ROWS, COLS)  

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(f' Here {event.button}') # 
            mouse_pos = pygame.mouse.get_pos()  
            handle_tile_click(mouse_pos)  


    pygame.display.flip()

pygame.quit()
