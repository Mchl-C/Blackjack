# Import required modules
import pygame, sys, random, time, pprint, math
from font_system import NumberInput
from pygame.locals import *
import sys
import os

#-------------------------------------------------------------------------#
# Find assets loc
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Set Up
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()

width, height = 640, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blackjack - Spend all ur money here ~")
icon = pygame.image.load(resource_path("cards\logo.png"))
pygame.display.set_icon(icon)

#-------------------------------------------------------------------------#
# Variables
run = True
winner = 0
prep = True

skill_1 = False
skill_2 = False
skill_3 = False
skill_4 = False

skill_1_count = 0
skill_2_count = 0
skill_3_count = 0
skill_4_count = 0

initial_chips = 25
card_opened = 0
enemy_card = 0
player_score = 0
enemy_score = 0
current_chips = initial_chips
bet_amt = 1
max_limit = 21

player_slots = 6
enemy_slots = 6

price = [5, 10, 20, 50]
#-------------------------------------------------------------------------#
# Assets



# pngs
table  = pygame.image.load(resource_path("cards\\table.png")).convert_alpha()
image  = pygame.image.load(resource_path("cards\card.png")).convert_alpha()
image2 = pygame.image.load(resource_path("cards\chips.png")).convert_alpha()

draw_button = pygame.image.load(resource_path("cards\draw.png")).convert_alpha()
fold_button = pygame.image.load(resource_path("cards\\fold.png")).convert_alpha()
bet_button  = pygame.image.load(resource_path("cards\\bet.png")).convert_alpha()

board   = pygame.image.load(resource_path("cards\\board.png")).convert_alpha()
set_bet = pygame.image.load(resource_path("cards\set_bet.png")).convert_alpha()

info = pygame.image.load(resource_path("cards\info.png")).convert_alpha()
shop = pygame.image.load(resource_path("cards\shop.png")).convert_alpha()

special_slots  = pygame.image.load(resource_path("cards\special_slots.png")).convert_alpha()
special_card_1 = pygame.image.load(resource_path("cards\special_card_1.png")).convert_alpha()
special_card_2 = pygame.image.load(resource_path("cards\special_card_2.png")).convert_alpha()
special_card_3 = pygame.image.load(resource_path("cards\special_card_3.png")).convert_alpha()
special_card_4 = pygame.image.load(resource_path("cards\special_card_4.png")).convert_alpha()

# Surfaces
cards = []
chips = [image2.subsurface(pygame.Rect(48 * j, 0, 48, 48)) for j in range(4)]
card_back = image.subsurface(pygame.Rect(0, 64 * 4, 48, 64))
chips_holder = pygame.Surface((100, 160))

# Buttons
button_draw = pygame.Rect(width - 200, height - 100, *draw_button.get_size())
button_fold = pygame.Rect(200, height - 100, *fold_button.get_size())
button_bet = pygame.Rect(width - 200, height - 100, *bet_button.get_size())

# Fonts
# Font types
font_1 = pygame.font.SysFont('timesnewroman', 48)
font_2 = pygame.font.SysFont('courier', 20)

# Texts
win_text = font_1.render("You Win!", True, (255, 255, 255))
lose_text = font_1.render("You Lose!", True, (255, 255, 255))
draw_text = font_1.render("Draw!", True, (255, 255, 255))
title = font_1.render("Blackjack", True, (255,255,255))
game_over = font_1.render("GAME OVER", True, (255,255,255))
chip_text = font_2.render("CHIPS", True, (255,255,255))

# Set ups
for i in range(4):
    row = [image.subsurface(pygame.Rect(48 * j, 64 * i, 48, 64)) for j in range(13)]
    cards.append(row)

bot_hands = [card_back for i in range(enemy_slots)]
player_hands = [card_back for i in range(player_slots)]
chips_holder.blit(board,(0,0))

used = [[False for i in range(13)] for _ in range(4)]

#-------------------------------------------------------------------------#
# Functions

# Visual
def blit_cards(player_slots, enemy_slots):
    # Bot
    for j in range(enemy_slots):
        screen.blit(bot_hands[j], (width // 2 - (3 - j) * 64, height * 1/4))

    # Player
    for j in range(player_slots):
        screen.blit(player_hands[j], (width // 2 - (3 - j) * 64, height / 2))

    score_1 = font_1.render(str(enemy_score), True, (255, 255, 255))
    score_2 = font_1.render(str(player_score), True, (255, 255, 255))

    # Bot
    screen.blit(score_1, (width // 2 - (3 - enemy_slots) * 64, height * 1/4))
    # Player
    screen.blit(score_2, (width // 2 - (3 - player_slots) * 64, height * 1/2))

def blit_chip():
    global current_chips
    chip_amount = font_1.render(str(current_chips), True, (255, 255, 255))

    screen.blit(chips_holder, (30, height - 180))
    screen.blit(chips[3], (30, height - 90))
    screen.blit(chips[2], (20, height - 70))
    screen.blit(chips[3], (40, height - 70))
    screen.blit(chip_text, (50, height - 165))

    screen.blit(chip_amount, (85 - (15 * math.ceil(math.log10(current_chips + 1))), height - 130))

#-------------------------------------------------------------------------#
# Features
# INFO 
def info_slide():
    info_s = True
    while info_s:
        screen.blit(table,(0,0))

        instruction_font = pygame.font.Font(None, 28)
        instructions = [
            "The goal is to get a hand value closer to 21 than the dealer",
            "without going over. Number cards (2-10) are worth their face",
            "value, face cards (J, Q, K) count as 10, and Aces can be 1 or 11",
            'You can "draw" (take another card) or "fold" (keep your hand).',
            'Before starting, you can set "bet" with your chips. You lose when',
            'you ran out of chips'
        ]

        title_surf = font_1.render("How to play?", True, (240,240,240))
        screen.blit(title_surf, (190, 30))
        
        for i, text in enumerate(instructions):
            instr_surface = instruction_font.render(text, True, (220, 210, 210))
            screen.blit(instr_surface, (20, 130 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_q):
                    info_s = False

        instr_surf = font_2.render("Press q to close info slide", True, (240,240,240))
        screen.blit(instr_surf, (20, height - 40))
        pygame.display.update()
    
def info_button(mouse_pos):
    rect_info = pygame.Rect((width - 50, 32),info.get_size())
    if rect_info.collidepoint(mouse_pos):
        info_slide()

# shop
def shop_slide():
    global skill_1_count, skill_2_count, skill_3_count, skill_4_count, current_chips
    global price
    shop_s = True

    # Cards - Their descriptions 
    special_cards = [special_card_1, special_card_2, special_card_3, special_card_4]
    descriptions = ["You won't lose any chip even if you lose the game this turn",
                    "Double the amount of the chips reward if you win this turn",
                    "Randomly give you chips amount[0-40], 5% chance to get 100 chips",
                    "Increase the highest limit number by 10"]
    
    cards_surfaces = [pygame.Rect((50, 80*i),(48, 64)) for i in range(1,len(special_cards)+1)]
    

    instruction_font = pygame.font.Font(None, 18)
    
    while shop_s:
        screen.blit(table,(0,0))

        title_surf = font_1.render("Shop", True, (240,240,240))
        screen.blit(title_surf, (270, 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_q):
                    shop_s = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if(cards_surfaces[0].collidepoint(mouse_pos) and current_chips >= price[0]):
                    skill_1_count += 1
                    current_chips -= price[0]
                    price[0] *= 2
                    
                elif(cards_surfaces[1].collidepoint(mouse_pos) and current_chips >= price[1]):
                    skill_2_count += 1
                    current_chips -= price[1]
                    price[1] *= 2

                elif(cards_surfaces[2].collidepoint(mouse_pos) and current_chips >= price[2]):
                    skill_3_count += 1
                    current_chips -= price[2]

                elif(cards_surfaces[3].collidepoint(mouse_pos) and current_chips >= price[3]):
                    skill_4_count += 1
                    current_chips -= price[3]
                    price[3] *= 2

        for i in range(1,len(special_cards)+1):
            screen.blit(special_cards[i - 1], (50, 80*i))
            
        for i, text in enumerate(descriptions):
            instr_surface = instruction_font.render(text, True, (220, 210, 210))
            price_tag = instruction_font.render(f"Item price : {price[i]} chips", True, (240, 240, 240))

            screen.blit(instr_surface, (110, 80*(i+1) + 10))
            screen.blit(price_tag, (110, 80*(i+1) + 30))

        money = instruction_font.render(f"Current chips: {current_chips}", True, (180,180,180))
        screen.blit(money, (width // 2 - 60, height - 120))
                
        instr_surf = font_2.render("Press q to close shop slide", True, (240,240,240))
        screen.blit(instr_surf, (20, height - 40))
        pygame.display.update()
    
def shop_button(mouse_pos):
    rect_shop = pygame.Rect((20, 20),shop.get_size())
    if rect_shop.collidepoint(mouse_pos):
        shop_slide()

# Buttons
def buttons():
    # Buttons
    if(card_opened == 0):
        screen.blit(bet_button, (width - 200, height - 100))
    else:
        screen.blit(draw_button, (width - 200, height - 100))
        screen.blit(fold_button, (200, height - 100))

# Special slots
def specialSlot():
    screen.blit(special_slots, (150, height - 140))
    special_cards = [special_card_2, special_card_3, special_card_4, special_card_1]
    for i in range(len(special_cards)):
        screen.blit(special_cards[i - 1], (158 + 64*i, height - 132))

    amount = [str(skill_1_count), str(skill_2_count), str(skill_3_count), str(skill_4_count)]
    for i, text in enumerate(amount):
        instr_surface = font_2.render(text, True, (220, 210, 210))
        screen.blit(instr_surface, (172 + 64 * i, height - 64))
        
def use_skill(mouse_pos):
    global skill_1_count, skill_2_count, skill_3_count, skill_4_count
    global current_chips
    
    special_surf = [pygame.Rect(158 + 64 * i, height - 132, 48, 64) for i in range(4)]

    if special_surf[0].collidepoint(mouse_pos) and skill_1_count > 0:
        print("Skill 1")
        print("Protect")
        skill_1_count -= 1
        activate_ss_1()
        
    elif special_surf[1].collidepoint(mouse_pos) and skill_2_count > 0:
        print("skill 2")
        print("double")
        skill_2_count -= 1
        activate_ss_2()
        
    elif special_surf[2].collidepoint(mouse_pos) and skill_3_count > 0:
        print("skill 3")
        print("Wager")
        skill_3_count -= 1
        activate_ss_3()
        current_chips += random_chips(0,40)[0]

    elif special_surf[3].collidepoint(mouse_pos) and skill_4_count > 0:
        print("skill 4")
        print("Upgrade")
        skill_4_count -= 1
        activate_ss_4()

#-------------------------------------------------------------------------#
# Skills

# Protect
def activate_ss_1():
    global skill_1
    skill_1 = True

# Double
def activate_ss_2():
    global skill_2
    skill_2 = True

# Wager
def activate_ss_3():
    global skill_3
    skill_3 = True

def random_chips(a,b):
    return random.choices([random.randint(a,b), 100], weights = [95, 5])

# Upgrade
def activate_ss_4():
    global skill_4, max_limit
    skill_4 = True
    max_limit += 10
    
    
#-------------------------------------------------------------------------#
# Functional
def generate_draw(side):
    global player_score, enemy_score
    r, c = random.randint(0,3), random.randint(0,12)
    while(used[r][c]):
        r, c = random.randint(0,3), random.randint(0,12)
    used[r][c] = True

    if(side == "bot"):
        enemy_score += 11 if (c == 0 and enemy_score + 11 <= max_limit) else 1 if (c == 0 and enemy_score + 11 > max_limit)  else c + 1 if c < 10 else 10
    if(side == "player"):
        player_score += 11 if (c == 0 and player_score + 11 <= max_limit) else 1 if (c == 0 and player_score + 11 > max_limit) else c + 1 if c < 10 else 10

    return r,c

def bot_draw_card():
    global enemy_card
    r, c = generate_draw("bot")
    bot_hands[enemy_card] = cards[r][c]
    enemy_card += 1
    
def player_draw_card():
    global card_opened
    if(card_opened < player_slots):
        r, c = generate_draw("player")
        player_hands[card_opened] = cards[r][c]
        card_opened += 1

def reset_hands():
    global card_opened, enemy_card, player_score, enemy_score 
    global bot_hands, player_hands, used, bet_amt
    global skill_1, skill_2, skill_3, skill_4

    bet_amt = 1
    card_opened = 0
    enemy_card = 0
    player_score = 0
    enemy_score = 0

    skill_1 = False
    skill_2 = False
    skill_3 = False
    skill_4 = False

    bot_hands = [card_back for i in range(enemy_slots)]
    player_hands = [card_back for i in range(player_slots)]
    used = [[False for i in range(13)] for _ in range(4)]

def bot_strategy():
    if(player_score <= max_limit):
        while(enemy_score < player_score and enemy_card < enemy_slots):
            screen.blit(table,(0,0))
            bot_draw_card()
            blit_cards(player_slots, enemy_slots)
            pygame.display.update()
            time.sleep(1)
    else:
        bot_draw_card()
        blit_cards(player_slots, enemy_slots)
        pygame.display.update()
        time.sleep(1)    

def draw_card():
    try:
        player_draw_card()
        print("Player-score :", player_score)
        print("Enemy-score  :", enemy_score)
    except:
        pass
    
def fold():
    global current_chips, prep
    
    print("Fold")
    bot_strategy()
    print("Player vs Enemy :", player_score, enemy_score)
    screen.blit(table,(0,0))

    # win
    if(player_score <= max_limit and (player_score > enemy_score or enemy_score > max_limit)):
        text_rect = win_text.get_rect(center=(width/2, height/2))
        screen.blit(win_text, text_rect)

        if(skill_2):
            current_chips += 2*bet_amt
        else:
            current_chips += bet_amt

    # draw
    elif(player_score == enemy_score):
        text_rect = draw_text.get_rect(center=(width/2, height/2))
        screen.blit(draw_text, text_rect)

    # lose
    elif(player_score > max_limit or enemy_score > player_score):
        text_rect = lose_text.get_rect(center=(width/2, height/2))
        screen.blit(lose_text, text_rect)

        if(skill_1):
            pass
        else:
            current_chips -= bet_amt

    prep = True
    
    pygame.display.update()
    time.sleep(2)
    reset_hands()

def bet():
    global bet_amt, current_chips, prep
    
    setting_bet = True

    set_bet_pos = set_bet.get_rect(center=(width/2, height/2))
    number_input = NumberInput(
        x=(set_bet_pos[0] + 60),  
        y=(set_bet_pos[1] + 60),
        width=60,
        height=70
    )
    while setting_bet:
        screen.blit(table, (0,0))
        screen.blit(set_bet, set_bet_pos)

        down_button = pygame.Rect((set_bet_pos[0] + 145, set_bet_pos[1] + 115), (22,22))
        up_button = pygame.Rect((set_bet_pos[0] + 175, set_bet_pos[1] + 115), (22,22))
        submit_button = pygame.Rect((set_bet_pos[0] + 145, set_bet_pos[1] + 54), (52,42))

        
    
        for event in pygame.event.get():
            amt = number_input.get_amt()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if up_button.collidepoint(mouse_pos) and amt < current_chips:
                    number_input.change_number(1)
                elif down_button.collidepoint(mouse_pos) and amt - 1 >= 0:
                    number_input.change_number(-1)
                elif submit_button.collidepoint(mouse_pos):
                    bet_amt = number_input.get_amt()
                    setting_bet = False
                    prep = False
                    
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_UP) and amt < current_chips:
                    number_input.change_number(1)
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_DOWN) and amt - 1 >= 0:
                    number_input.change_number(-1)
                elif event.key == pygame.K_RETURN:
                    bet_amt = number_input.get_amt()
                    setting_bet = False
                    prep = False
            res = number_input.handle_event(event)
            if(res):
                if(bet_amt > current_chips):
                    bet_amt = current_chips
                else:
                    bet_amt = res
            
        #chip_bet = font_1.render(str(bet_amt), True, (255, 255, 255))
        #screen.blit(chip_bet, (set_bet_pos[0] + 100 - (15 * math.ceil(math.log10(bet_amt + 1))), set_bet_pos[1] + 70))

        submit = font_1.render("V", True, (255, 255, 255))
        screen.blit(submit, (set_bet_pos[0] + 155, set_bet_pos[1] + 48))

        down = font_2.render("<", True, (255, 255, 255))
        up = font_2.render(">", True, (255, 255, 255))
        
        screen.blit(down, (set_bet_pos[0] + 150, set_bet_pos[1] + 115))
        screen.blit(up, (set_bet_pos[0] + 180, set_bet_pos[1] + 115))

        number_input.update()
        number_input.draw(screen)
        #pygame.draw.rect(screen, (255,255,255), up_button)
        #pygame.draw.rect(screen, (255,255,255), down_button)
        #pygame.draw.rect(screen, (255,255,255), submit_button)
        
        pygame.display.update()

def check_lose():
    global current_chips
    global skill_1_count, skill_2_count, skill_3_count, skill_4_count
    
    if current_chips <= 0:
        screen.blit(table, (0, 0))
        
        # Game Over text with subtle shadow
        shadow_rect = game_over.get_rect(center=(width/2+2, height/2-48))
        screen.blit(game_over, shadow_rect, special_flags=pygame.BLEND_MULT)
        text_rect = game_over.get_rect(center=(width/2, height/2-50))
        screen.blit(game_over, text_rect)
        
        # Retry prompt with elegant font
        retry_font = pygame.font.SysFont('Arial', 42)  # Use a nicer font if available
        retry_text = retry_font.render("Play Again?", True, (240, 240, 240))
        text_shadow = retry_font.render("Play Again?", True, (80, 80, 80))
        
        # Draw text shadow
        shadow_rect = retry_text.get_rect(center=(width/2+2, height/2+22))
        screen.blit(text_shadow, shadow_rect)
        
        # Draw main text
        text_rect = retry_text.get_rect(center=(width/2, height/2+20))
        screen.blit(retry_text, text_rect)
        
        # Button parameters
        button_width, button_height = 120, 50
        button_radius = 10
        button_y = height/2 + 80
        
        # Yes button (gradient effect)
        yes_button = pygame.Rect(width/2 - 140, button_y, button_width, button_height)
        pygame.draw.rect(screen, (50, 180, 50), yes_button, border_radius=button_radius)
        pygame.draw.rect(screen, (100, 220, 100), yes_button.inflate(-4, -4), border_radius=button_radius-2)
        
        # No button (gradient effect)
        no_button = pygame.Rect(width/2 + 20, button_y, button_width, button_height)
        pygame.draw.rect(screen, (180, 50, 50), no_button, border_radius=button_radius)
        pygame.draw.rect(screen, (220, 100, 100), no_button.inflate(-4, -4), border_radius=button_radius-2)
        
        # Button text
        button_font = pygame.font.SysFont('Arial', 32)
        yes_text = button_font.render("YES", True, (255, 255, 255))
        no_text = button_font.render("NO", True, (255, 255, 255))
        
        # Center text in buttons
        screen.blit(yes_text, (yes_button.centerx - yes_text.get_width()//2, 
                              yes_button.centery - yes_text.get_height()//2))
        screen.blit(no_text, (no_button.centerx - no_text.get_width()//2, 
                             no_button.centery - no_text.get_height()//2))
        
        # Button hover effects
        mouse_pos = pygame.mouse.get_pos()
        for button in [yes_button, no_button]:
            if button.collidepoint(mouse_pos):
                highlight = pygame.Surface((button.width, button.height), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 30))
                screen.blit(highlight, button)
        
        pygame.display.update()

        reset_hands()
        skill_1_count = 0
        skill_2_count = 0
        skill_3_count = 0
        skill_4_count = 0

        
        # Input handling (same as before)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(event.pos):
                        current_chips = initial_chips
                        waiting = False
                    elif no_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        current_chips = initial_chips
                        waiting = False
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()
                        
    
#-------------------------------------------------------------------------#
# Main
while run:
    screen.fill((255,255,255))
    screen.blit(table,(0,0))

    text_rec = title.get_rect(center=(width/2, 50))
    screen.blit(title,text_rec)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and card_opened == 0:
                bet()
                draw_card()
            elif event.key == pygame.K_p:
                draw_card()
                
            if event.key == pygame.K_f and not prep:
                fold()

            if event.key == pygame.K_i:
                info_button((width - 40, 45))

            if event.key == pygame.K_s:
                shop_button((25, 25))
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if button_draw.collidepoint(mouse_pos) and card_opened == 0:
                bet()
                draw_card()
            elif button_draw.collidepoint(mouse_pos):
                draw_card()

            if button_fold.collidepoint(mouse_pos) and not prep:
                fold()
                
            info_button(mouse_pos)
            shop_button(mouse_pos)
            if prep:
                use_skill(mouse_pos)

    # render graphics
    blit_cards(player_slots, enemy_slots)
    buttons()
    blit_chip()
    check_lose()

    if prep:
        specialSlot()
    
    screen.blit(info, (width - 50, 32))
    screen.blit(shop, (20, 20))
    
    chip_bet = font_2.render(f"Current bet : {bet_amt}", True, (255, 255, 255))
    screen.blit(chip_bet, (width // 2 - 85, height // 2 - 50))
    
    pygame.display.update()
    clock.tick(60)
    
