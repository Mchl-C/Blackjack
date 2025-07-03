import pygame

# Initialize Pygame
pygame.init()

HELP_WINDOW_WIDTH, HELP_WINDOW_HEIGHT = 260, 300
CONTENT_HEIGHT = 1300  # Height of the content surface

BACKGROUND_COLOR = (30, 30, 30)  # Dark background
HELP_BACKGROUND_COLOR = (180, 180, 180)  # Lighter grey for help window
HELP_BORDER_COLOR = (220, 220, 220)  # Even lighter grey border color
TEXT_COLOR = (255,255,255)  # Black text

FONT_SIZE = 16
BORDER_RADIUS = 10
BORDER_WIDTH = 4

#-------------------------------------------------------------------------#
# Messages

# Help windows
help_text = [
    "< Help Window >",
    "- Press H to toggle this window",
    "- Press ESC to exit",
    "- Press aswd to move",
    "- Press Shift to run",
    "- Press l to lock(sit)",
    "- Press z to lock(sleep)",
    "- Press f for stretching",
    "- Press c for licking",
    "- Press e for laying",
    "- Press r for itching",
    "- Press m to meow(only work if locked)",
    "- Press q to open chat box",
    "- Press y to write in chat box",
    "  (must open chat box first)",
    "- Press Right Shift to exit writting mode",
    "- Press p to open calculator",
    "- Press v to change skin",
    "- Press t to open translator",
    "- Press g to open randomize picker"
    ]
    

# Initialize font
pygame.font.init()
font = pygame.font.SysFont('Arial', FONT_SIZE)

# Function to render text
def render_text(surface, text, position, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# Function to draw the help window
def draw_help_window(surface, scroll_y):
    help_rect = pygame.Rect(surface.get_width() - HELP_WINDOW_WIDTH - 20,  # Top-right position with some padding
                            50,
                            HELP_WINDOW_WIDTH, HELP_WINDOW_HEIGHT)
    
    # Draw the border
    pygame.draw.rect(surface, HELP_BORDER_COLOR, help_rect, BORDER_WIDTH, BORDER_RADIUS)
    
    # Draw the help window background
    inner_rect = help_rect.inflate(-BORDER_WIDTH*2, -BORDER_WIDTH*2)
    pygame.draw.rect(surface, HELP_BACKGROUND_COLOR, inner_rect, border_radius=BORDER_RADIUS)
    
    # Draw the visible part of the content surface
    surface.blit(content_surface, (inner_rect.x, inner_rect.y), (0, scroll_y, inner_rect.width, inner_rect.height))


#-------------------------------------------------------------------------#
global content_surface
content_surface = pygame.Surface((HELP_WINDOW_WIDTH - BORDER_WIDTH * 2, CONTENT_HEIGHT))

scroll_y = 0
# Populate the content surface with text
text_padding = 20
for i in range(len(help_text)):
    render_text(content_surface, help_text[i], (text_padding, text_padding + i * 40))


# Function to create and manage the main window with a scrollable help window
def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Main Window with Scrollable Help Window")

    # Create a larger content surface for the help window
    scroll_y = 0
    show_help = True

    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_h:
                    show_help = not show_help
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    scroll_y = max(scroll_y - 20, 0)
                elif event.button == 5:  # Mouse wheel down
                    scroll_y = min(scroll_y + 20, CONTENT_HEIGHT - HELP_WINDOW_HEIGHT + BORDER_WIDTH * 2)

        # Fill the background
        screen.fill(BACKGROUND_COLOR)

        # Draw main content
        render_text(screen, "Main Window Content", (20, 20))

        # Draw the help window if toggled
        if show_help:
            draw_help_window(screen, scroll_y)

        # Update the display
        pygame.display.update()
        clock.tick(60)  # Cap the frame rate

    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
