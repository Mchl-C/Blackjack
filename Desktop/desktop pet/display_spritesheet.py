import pygame
import sys

# Initialize Pygame
pygame.init()

def get_frames(spritesheet, num_frames, frame_width, frame_height, scale):
    frames = []
    for i in range(num_frames):
        frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        scaled_frame = pygame.transform.scale(frame, 
                                            (frame_width * scale, 
                                             frame_height * scale))
        frames.append(scaled_frame)
    return frames

animations = []

'''
# Main loop
done = False
current_frame = 0
current_animation = 0
animation_change = 30
current_time = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # Clear the screen
    screen.fill((0, 0, 0))

    # Update the frame index
    current_frame = (current_frame + 1) % NUM_FRAMES[current_animation]

    # Draw the current frame
    screen.blit(animations[current_animation][current_frame], (0,0))

    if(current_time >= animation_change):
        current_animation = (current_animation + 1) % len(animations)
        current_time = 0
    
    current_time += 1
                                            
    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()

'''
