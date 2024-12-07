#author: Lasoie Maloney
#Description: Python Flood Model
#Requirements: Pygame, Numpy, 
#Last update: 19/11/24
import pygame
import numpy as np
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

#Set up screen
pygame.init()
screen = pygame.display.set_mode((1520,900), pygame.RESIZABLE) # update on 19/11/24 to enable manually resizing of Pygame window
#win = pygame.display.set_mode((400, 280))
pygame.display.set_caption("Laoise's Flood Model")  

#Set up grid
width, height = 70, 70
cell_size = 10 
old_grid = np.zeros((height, width), dtype=float)
grid = np.zeros((height, width), dtype=float)
de_grid = np.zeros((height, width), dtype=float) # grid for elevation map
#grid[10][9]= 1
cx,cy= width/2, height/2   #location of mountain peak
lx, ly = width/4, height/4  #location of lake
l = 0 #distance from mountain peak
c = width/4  # standard deviation, steepness of mountain 
a = 1 #max. height of mountain
#de_grid[10][9] = 1
#Create mountain 3/12/24
for y in range(height):
        for x in range(width):
            l = np.sqrt(((cx-x) * (cx-x)) + ((cy-y) * (cy-y))) # distance x, y is from mountain peak
            f = 1 * np.exp(-0.5*((l/c)*(l/c))) # height of mountain at x, y
            de_grid[x][y] = f
#Create lake 3/12/24
for y in range(height-100):
        for x in range(width-100):
            l = np.sqrt(((cx-x) * (cx-x)) + ((cy-y) * (cy-y))) # distance x, y is from mountain peak
            f = 1 * (1 - np.exp(-0.5*((l/c)*(l/c)))) # height of mountain at x, y
            de_grid[x][y] = f + 10


dropdown = Dropdown(
    screen, 150, 750, 108, 50, name='Select Location',
    choices=[
        'Cork City',
        'Whitegate',
        'Cobh',
        'Youghal',
    ],
    borderRadius=3, colour=pygame.Color('green'), values=[1, 2, 3, 'true'], direction='down', textHAlign='left'
)


def print_value():
    print(dropdown.getSelected())
    

# Print Value Button
button = Button(
    screen, 450, 750, 100, 50, text='Print Value', fontSize=30,
    margin=20, inactiveColour=(0, 0, 255), pressedColour=(0, 0, 0),
    radius=5, onClick=print_value, font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom'
)

#Run Button properties for Flood Model
font = pygame.font.Font(None, 50)
button_surface = pygame.Surface((100, 100))
text = font.render("Run", True, (0,0,255))
text_rect = text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))
button_rect = pygame.Rect(300, 750, 200, 200)

#Run Button properties for Elevation Map   19/11/24 
font = pygame.font.Font(None, 50)
button_surface_el = pygame.Surface((100, 100))
text_el = font.render("Run", True, (0,200,255))
text_rect_el = text_el.get_rect(center=(button_surface_el.get_width()/2, button_surface_el.get_height()/2))
button_rect_el = pygame.Rect(1100, 750, 200, 200)

fr = 2#f/s
#Start game loop
running = True
clock = pygame.time.Clock()
while running:
    #Event manager
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: #ON QUIT
            running = False
    #If mouse is clicked, call the on_mouse_button_down() function
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if button_rect.collidepoint(event.pos):
         print("Button clicked!")
        elif button_rect_el.collidepoint(event.pos):
         print("Button clicked!")
    #Update flood grid
    screen.fill(pygame.Color(255,255,255,255)) 
    for y in range(height):
        for x in range(width):
            gs = int ((grid[x][y]) * 255)
            color = pygame.Color(0, 0, gs, 255)

            pygame.draw.rect(screen, color, (20+(x * cell_size), 20+(y * cell_size), cell_size, cell_size))

    #Update de_grid
    for y in range(height):
        for x in range(width):
                    if x and y != 0:
                        if lx/x == 1 and ly/y ==1: #if we are in the region of the lake, outline it with white to make it apparent
                        # gs = int ((de_grid[x][y]) * 255)
                         de_grid[x][y] = 0
                
                    gs = int ((de_grid[x][y]) * 255)
                    color = pygame.Color(gs, gs, gs,55) 

                    pygame.draw.rect(screen, color, (800+(x * cell_size), 20+(y * cell_size), cell_size, cell_size))


    #Display button text
    button_surface.blit(text, text_rect)
    screen.blit(button_surface, (button_rect.x, button_rect.y))

    button_surface_el.blit(text_el, text_rect_el)
    screen.blit(button_surface_el, (button_rect_el.x, button_rect_el.y))
    pygame_widgets.update(events)
    pygame.display.flip() #Double buffer reveal updated screen

    #Save the current grid
    for y in range(height):
        for x in range(width):

            old_grid[x][y] = grid[x][y]

            
    #Create new grid using old grid 
    #Move water around 
    for y in range(height-1):
        for x in range(width-1):
            grid[x+1][y-1] = 0.25 * (old_grid[x][y])
            grid[x][y] = 0.75 * (old_grid[x][y]) #Share the water from old grid to new cells

            #grid[x+1][y] = 1

    #Create rain effect
    #Add new water

    grid[10][5] = 0.1 + old_grid[10][5]
    clock.tick(fr) #framerate


pygame.quit()
