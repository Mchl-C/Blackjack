import pygame, sys, os
import translator
import randomly
from display_spritesheet import get_frames
from calculator import Calculator
from font_system import *
from win32 import win32api, win32con, win32gui

#-----------------------------------------------------------------------
# Find assets loc
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Set up
pygame.init()
pygame.font.init()

pygame.display.set_caption("Desktop Pet")

screen_info = pygame.display.Info()
WIDTH  = screen_info.current_w
HEIGHT = screen_info.current_h

print(WIDTH, HEIGHT)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME, pygame.FULLSCREEN)
clock = pygame.time.Clock()

SPRITESHEET_PATH = [['CatPack/Cat-1/Cat-1-Idle.png',
                    'CatPack/Cat-1/Cat-1-Itch.png',
                    'CatPack/Cat-1/Cat-1-Laying.png',
                    'CatPack/Cat-1/Cat-1-Licking.png',
                    'CatPack/Cat-1/Cat-1-Meow.png',
                    'CatPack/Cat-1/Cat-1-Run.png',
                    'CatPack/Cat-1/Cat-1-Sitting.png',
                    'CatPack/Cat-1/Cat-1-Sleeping1.png',
                    'CatPack/Cat-1/Cat-1-Sleeping2.png',
                    'CatPack/Cat-1/Cat-1-Stretching.png',
                    'CatPack/Cat-1/Cat-1-Walk.png'],
                    ['CatPack/Cat-2/Cat-2-Idle.png',
                    'CatPack/Cat-2/Cat-2-Itch.png',
                    'CatPack/Cat-2/Cat-2-Laying.png',
                    'CatPack/Cat-2/Cat-2-Licking.png',
                    'CatPack/Cat-2/Cat-2-Meow.png',
                    'CatPack/Cat-2/Cat-2-Run.png',
                    'CatPack/Cat-2/Cat-2-Sitting.png',
                    'CatPack/Cat-2/Cat-2-Sleeping1.png',
                    'CatPack/Cat-2/Cat-2-Sleeping2.png',
                    'CatPack/Cat-2/Cat-2-Stretching.png',
                    'CatPack/Cat-2/Cat-2-Walk.png'],
                    ['CatPack/Cat-3/Cat-3-Idle.png',
                    'CatPack/Cat-3/Cat-3-Itch.png',
                    'CatPack/Cat-3/Cat-3-Laying.png',
                    'CatPack/Cat-3/Cat-3-Licking.png',
                    'CatPack/Cat-3/Cat-3-Meow.png',
                    'CatPack/Cat-3/Cat-3-Run.png',
                    'CatPack/Cat-3/Cat-3-Sitting.png',
                    'CatPack/Cat-3/Cat-3-Sleeping1.png',
                    'CatPack/Cat-3/Cat-3-Sleeping2.png',
                    'CatPack/Cat-3/Cat-3-Stretching.png',
                    'CatPack/Cat-3/Cat-3-Walk.png'],
                    ['CatPack/Cat-4/Cat-4-Idle.png',
                    'CatPack/Cat-4/Cat-4-Itch.png',
                    'CatPack/Cat-4/Cat-4-Laying.png',
                    'CatPack/Cat-4/Cat-4-Licking.png',
                    'CatPack/Cat-4/Cat-4-Meow.png',
                    'CatPack/Cat-4/Cat-4-Run.png',
                    'CatPack/Cat-4/Cat-4-Sitting.png',
                    'CatPack/Cat-4/Cat-4-Sleeping1.png',
                    'CatPack/Cat-4/Cat-4-Sleeping2.png',
                    'CatPack/Cat-4/Cat-4-Stretching.png',
                    'CatPack/Cat-4/Cat-4-Walk.png'],
                    ['CatPack/Cat-5/Cat-5-Idle.png',
                    'CatPack/Cat-5/Cat-5-Itch.png',
                    'CatPack/Cat-5/Cat-5-Laying.png',
                    'CatPack/Cat-5/Cat-5-Licking.png',
                    'CatPack/Cat-5/Cat-5-Meow.png',
                    'CatPack/Cat-5/Cat-5-Run.png',
                    'CatPack/Cat-5/Cat-5-Sitting.png',
                    'CatPack/Cat-5/Cat-5-Sleeping1.png',
                    'CatPack/Cat-5/Cat-5-Sleeping2.png',
                    'CatPack/Cat-5/Cat-5-Stretching.png',
                    'CatPack/Cat-5/Cat-5-Walk.png'],
                    ['CatPack/Cat-6/Cat-6-Idle.png',
                    'CatPack/Cat-6/Cat-6-Itch.png',
                    'CatPack/Cat-6/Cat-6-Laying.png',
                    'CatPack/Cat-6/Cat-6-Licking.png',
                    'CatPack/Cat-6/Cat-6-Meow.png',
                    'CatPack/Cat-6/Cat-6-Run.png',
                    'CatPack/Cat-6/Cat-6-Sitting.png',
                    'CatPack/Cat-6/Cat-6-Sleeping1.png',
                    'CatPack/Cat-6/Cat-6-Sleeping2.png',
                    'CatPack/Cat-6/Cat-6-Stretching.png',
                    'CatPack/Cat-6/Cat-6-Walk.png']
                    ]

OBJECT_PATH = [
    'CatPack/objects/chat_bubble.png'
    ]

ACTIONS = {
    "idle" : 0,
    "itch" : 1,
    "laying" : 2,
    "licking" : 3,
    "meowing" : 4,
    "running" : 5,
    "sitting" : 6,
    "sleeping1" : 7,
    "sleeping2" : 8,
    "stretching" : 9,
    "walking" : 10
    }

OBJECTS = {
    "chat_bubble" : 0,
    }


NUM_FRAMES = [10,2,8,5,4,8,1,1,1,13,8]  # Number of frames in the spritesheet

target_location = [0,0]
position = [100,100]
run = True
fps = 10

action  = "idle"
left    = False
running = False
locked  = False
chat_box = False
writting = False
help_window = False
sleep1 = True
move_speed = 10
scroll_y = 0

cat_type = 0

chat_text = [""]
current_line = 0

current_frame = 0
current_animation = 0

fuchsia = (255, 0, 128)  # Transparency color
dark_red = (139, 0, 0)
#-----------------------------------------------------------------------
# Handling windows
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)

win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

#-----------------------------------------------------------------------
# Animations
animations = []

# Load the spritesheet
for x in range(len(SPRITESHEET_PATH)):
    cats = []
    for i in range(len(SPRITESHEET_PATH[x])):
        spritesheet = pygame.image.load(resource_path(SPRITESHEET_PATH[x][i])).convert_alpha()
        frame_width, frame_height = spritesheet.get_size()
        frames = get_frames(spritesheet, NUM_FRAMES[i], frame_width/NUM_FRAMES[i], frame_height, 4)
        cats.append(frames)
    animations.append(cats)

# Objects
objects = []
for i in range(len(OBJECT_PATH)):
    spritesheet = pygame.image.load(resource_path(OBJECT_PATH[i])).convert_alpha()
    frame_width, frame_height = spritesheet.get_size()
    frames = get_frames(spritesheet, 1, frame_width/1, frame_height, 0.75)
    objects.append(frames)

#print(animations)
#print(objects)
#-----------------------------------------------------------------------
# Main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if help_window:
                if event.button == 4:  # Mouse wheel up
                    scroll_y = max(scroll_y - 20, 0)
                elif event.button == 5:  # Mouse wheel down
                    scroll_y = min(scroll_y + 20, 1300 - HELP_WINDOW_HEIGHT + BORDER_WIDTH)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                sys.exit()

            if chat_box and writting:
                # allow writting
                if event.key == pygame.K_RSHIFT:
                    writting = False
                if event.key == pygame.K_BACKSPACE:
                    chat_text[current_line] = chat_text[current_line][:-1]  
                elif event.key == pygame.K_RETURN:
                    current_line += 1
                    chat_text.append("")
                else:
                    #print(event.unicode)
                    chat_text[current_line] += event.unicode
                
            else:
                if event.key == pygame.K_y:
                    writting = True
                    
                if event.key == pygame.K_h:
                    help_window = not help_window
                if event.key == pygame.K_l:
                    locked = not locked
                    current_animation = ACTIONS["sitting"]
                if event.key == pygame.K_z:
                    locked = not locked
                    if sleep1:
                        current_animation = ACTIONS["sleeping1"]
                    else:
                        current_animation = ACTIONS["sleeping2"]
                    sleep1 = not sleep1
                    
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    running = True
                    move_speed = 30
                    
                if event.key == pygame.K_a:
                    action = "left"
                    left = True
                if event.key == pygame.K_s:
                    action = "down"
                if event.key == pygame.K_w:
                    action = "up"
                if event.key == pygame.K_d:
                    action = "right"
                    left = False

                if event.key == pygame.K_m:
                    action = "meowing"
                if event.key == pygame.K_f:
                    action = "stretching"
                if event.key == pygame.K_c:
                    action = "licking"
                if event.key == pygame.K_e:
                    action = "laying"
                if event.key == pygame.K_r:
                    action = "itch"

                if event.key == pygame.K_q:
                    chat_box = not chat_box
                if event.key == pygame.K_p:
                    Calculator().mainloop()
                if event.key == pygame.K_v:
                    cat_type = (cat_type + 1) % 6
                if event.key == pygame.K_t:
                    translator.main()
                if event.key == pygame.K_g:
                    randomly.main()
                    

        if event.type == pygame.KEYUP:
            action = 'idle'
            running = False
            move_speed = 10

    screen.fill(fuchsia)

    if help_window:
        draw_help_window(screen, scroll_y)

    if chat_box and writting:
         pygame.draw.rect(screen, (0,255,0), (10, 10, 10, 10))
         
    if(locked == False):
        if action == "left" :
            position[0] -= move_speed
            current_animation = ACTIONS["walking"];
            
        if action == "right":
            position[0] += move_speed
            current_animation = ACTIONS["walking"];
            
        if action == "up"   : position[1] -= move_speed
        if action == "down" : position[1] += move_speed
        if action == 'idle' : current_animation = 0;
        if action == "stretching" : current_animation = ACTIONS["stretching"]
        if action == "licking" : current_animation = ACTIONS["licking"]
        if action == "laying" : current_animation = ACTIONS["laying"]
        if action == "itch" : current_animation = ACTIONS["itch"]
        if running : current_animation = ACTIONS["running"];
            
        current_frame = (current_frame + 1) % NUM_FRAMES[current_animation]
    else:
        if action == "meowing":
            current_animation = ACTIONS["sitting"]
            screen.blit(animations[cat_type][current_animation][current_frame], position)
            render_text(screen, "Meow", (position[0] + 135, position[1] + 50))
            pygame.display.update()
            pygame.time.delay(1000)
        current_frame = 0

    if chat_box:
        screen.blit(objects[OBJECTS["chat_bubble"]][0], (position[0] + 40, position[1] - 30))
        for i in range(0,current_line + 1):
            render_text(screen, chat_text[i], (position[0] + 50, position[1] - 20 + (i * 15)), (255,255,255))
    
    if left and locked == False:
        screen.blit(pygame.transform.flip(animations[cat_type][current_animation][current_frame], True, False), position)
    else:
        screen.blit(animations[cat_type][current_animation][current_frame], position)
        
    pygame.display.update()
    
    clock.tick(fps)
