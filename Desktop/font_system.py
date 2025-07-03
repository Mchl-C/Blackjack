import pygame
import sys

class NumberInput:
    def __init__(self, x, y, width=300, height=60):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = (230, 230, 230)
        self.color_active = (200, 230, 255)
        self.color = self.color_inactive
        self.text = ""
        self.active = False
        self.font = pygame.font.Font(None, 18)
        self.max_length = 7
        self.cursor_visible = False
        self.cursor_timer = 0
        self.border_radius = 8
        self.label = "Enter a number:"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
            if self.active:
                print("Active")
                pygame.key.start_text_input()
                pygame.key.set_text_input_rect(self.rect)
            else:
                pygame.key.stop_text_input()

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                try:
                    number = float(self.text) if '.' in self.text else int(self.text)
                    print(f"Submitted number: {number}")
                    return number
                except ValueError:
                    print("Please enter a valid number")
            
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.cursor_visible = True
                self.cursor_timer = 0
            
            elif event.unicode.isdigit() or (event.unicode == '.' and '.' not in self.text):
                if len(self.text) < self.max_length:
                    self.text += event.unicode
                    self.cursor_visible = True
                    self.cursor_timer = 0

    def update(self):
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer > 30:  # Blink every 30 frames (0.5s at 60 FPS)
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

    def draw(self, surface):
        # Draw main input box
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2, border_radius=self.border_radius)
        
        # Replace the text rendering section with this:
        text = self.text
        text_surfaces = []
        max_width = self.rect.width - 10
        line_height = self.font.get_linesize()
        
        while text:
            for i in range(len(text), 0, -1):
                test_text = text[:i]
                test_width = self.font.size(test_text)[0]
                if test_width <= max_width or i == 1:
                    text_surfaces.append(self.font.render(test_text, True, (40, 40, 40)))
                    text = text[i:]
                    break
        
        # Draw text lines and track cursor position
        cursor_x, cursor_text_y = 0, 0  # Initialize
        for i, text_surface in enumerate(text_surfaces):
            text_y = self.rect.y + 10 + (i * line_height)
            if text_y + line_height > self.rect.y + self.rect.height - 10:
                break
            surface.blit(text_surface, (self.rect.x + 5, text_y))
            # Store position for cursor
            cursor_x = self.rect.x + 5 + text_surface.get_width() + 2
            cursor_text_y = text_y
        
        # Draw cursor (only if we have text)
        if self.active and self.cursor_visible and text_surfaces:
            cursor_height = line_height - 8
            pygame.draw.line(surface, (40, 40, 40),
                           (cursor_x, cursor_text_y + 4),
                           (cursor_x, cursor_text_y + cursor_height + 4), 2)

    def change_number(self, num):
        try:
            number = int(self.text)
        except:
            number = 0
        number += num
        self.text = str(number)

    def get_amt(self):
        return int(self.text) if self.text != "" else 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Number Input")
    clock = pygame.time.Clock()
    
    number_input = NumberInput(
        x=800//2 - 150,  
        y=500//2 - 30,
        width=300,
        height=60
    )
    
    # Background color
    bg_color = (245, 245, 250)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            number_input.handle_event(event)
        
        number_input.update()
        
        # Draw
        screen.fill(bg_color)
        number_input.draw(screen)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 28)
        instructions = [
            "- Click the box to activate",
            "- Enter numbers (0-9) and one decimal point",
            "- Press Enter to submit"
        ]
        
        for i, text in enumerate(instructions):
            instr_surface = instruction_font.render(text, True, (120, 120, 120))
            screen.blit(instr_surface, (50, 400 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
