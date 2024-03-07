import pygame
import os
import random

import pygame.mask

# Initialize Pygame
pygame.init()

# Set the window size
WINDOW_SIZE = (1300, 1300)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pygame Example")

# Load the player character image
player_image = pygame.image.load(r"C:\Users\Admin\Pictures\txt\949d4355bc8d5d366a00dc0cdf2b495c_transparent.png")
player_image = pygame.transform.scale(player_image, (player_image.get_width() // 2.9, player_image.get_height() // 2.9))
player_mask = pygame.mask.from_surface(player_image)

# Load the first NPC character image
npc1_image = pygame.image.load(r"C:\Users\Admin\Pictures\txt\Transparent\top-car-view-png-34868_transparent.png")
npc1_image = pygame.transform.scale(npc1_image, (npc1_image.get_width() // 2, npc1_image.get_height() // 2))
npc1_mask = pygame.mask.from_surface(npc1_image)

# Load the second NPC character image
npc2_image = pygame.image.load(r"C:\Users\Admin\Pictures\txt\Transparent\top-car-view-png-34871_transparent.png")
npc2_image = pygame.transform.scale(npc2_image, (npc2_image.get_width() // 2, npc2_image.get_height() // 2))
npc2_mask = pygame.mask.from_surface(npc2_image)

# Get the character's width and height
player_width, player_height = player_image.get_size()
npc1_width, npc1_height = npc1_image.get_size()
npc2_width, npc2_height = npc2_image.get_size()

# Set the player's initial position
player_x = WINDOW_SIZE[0] // 2 - player_width // 2
player_y = WINDOW_SIZE[1] // 2 - player_height // 2

# Set the player's initial rotation
player_rotation = 0

# Set the NPCs' initial positions and speeds
npc1_x = WINDOW_SIZE[0] // 2 - npc1_width // 2
npc1_y = -npc1_height
npc1_speed = 2

npc2_x = WINDOW_SIZE[0] // 2 - npc2_width // 2
npc2_y = -npc2_height
npc2_speed = 2

# Set the player's speed
player_speed = 5

# Set the joystick threshold
JOYSTICK_THRESHOLD = 0.2

# Set up the PlayStation controller
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define the lane positions
left_lane_x = WINDOW_SIZE[0] // 4 - npc1_width // 2
middle_lane_x = WINDOW_SIZE[0] // 2 - npc1_width // 2
right_lane_x = 3 * WINDOW_SIZE[0] // 4 - npc1_width // 2

# Define the line colors
line_color = (255, 255, 255)  # White color

# Define the possible wrap positions for the NPCs
wrap_positions = [left_lane_x, middle_lane_x, right_lane_x]

# Set the rate at which the NPCs slow down when the left trigger is pressed
slow_down_rate = 0.05

# Set the rate at which the NPCs speed up when the right trigger is pressed
speed_up_rate = 0.007

# Set the maximum speed for the NPCs
max_speed = 9



# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle controller input
    # Get the axis values (left stick)
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Get the trigger values
    left_trigger = joystick.get_axis(4)
    right_trigger = joystick.get_axis(5)

    # Apply the joystick threshold
    if abs(x_axis) < JOYSTICK_THRESHOLD:
        x_axis = 0
    if abs(y_axis) < JOYSTICK_THRESHOLD:
        y_axis = 0

    # Move the player character based on the axis values
    player_x += x_axis * player_speed
    player_y += y_axis * player_speed

    # Keep the player character within the window bounds
    player_x = max(0, min(player_x, WINDOW_SIZE[0] - player_width))
    player_y = max(0, min(player_y, WINDOW_SIZE[1] - player_height))



    # Adjust the player's rotation based on the x-axis value
    if x_axis < 0:
        player_rotation = 15  # Rotate to the left
    elif x_axis > 0:
        player_rotation = -15  # Rotate to the right
    else:
        player_rotation = 0  # Return to the original rotation

    # Adjust the NPCs' speeds based on the trigger input
    if right_trigger > 0:
        npc1_speed = min(npc1_speed + speed_up_rate, max_speed)
        npc2_speed = min(npc2_speed + speed_up_rate, max_speed)
    elif left_trigger > 0:
        npc1_speed = max(npc1_speed - slow_down_rate, 0.5)
        npc2_speed = max(npc2_speed - slow_down_rate, 0.5)
    else:
        npc1_speed = max(min(npc1_speed, 2), 0.5)
        npc2_speed = max(min(npc2_speed, 2), 0.5)

    # Move the NPC characters
    npc1_y += npc1_speed
    if npc1_y > WINDOW_SIZE[1]:
        npc1_x = random.choice(wrap_positions)
        npc1_y = -npc1_height

    npc2_y += npc2_speed
    if npc2_y > WINDOW_SIZE[1]:
        npc2_x = random.choice(wrap_positions)
        npc2_y = -npc2_height

    # Check for collision between player and NPCs
    offset_x1 = npc1_x - player_x
    offset_y1 = npc1_y - player_y
    collision1 = player_mask.overlap(npc1_mask, (offset_x1, offset_y1))

    offset_x2 = npc2_x - player_x
    offset_y2 = npc2_y - player_y
    collision2 = player_mask.overlap(npc2_mask, (offset_x2, offset_y2))

    if collision1 or collision2:
        # Respawn the player
        player_x = WINDOW_SIZE[0] // 2 - player_width // 2
        player_y = WINDOW_SIZE[1] // 2 - player_height // 2

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the lane lines
    pygame.draw.line(screen, line_color, (left_lane_x, 0), (left_lane_x, WINDOW_SIZE[1]), 5)
    pygame.draw.line(screen, line_color, (middle_lane_x, 0), (middle_lane_x, WINDOW_SIZE[1]), 5)
    pygame.draw.line(screen, line_color, (right_lane_x, 0), (right_lane_x, WINDOW_SIZE[1]), 5)

    # Rotate the player character
    rotated_player_image = pygame.transform.rotate(player_image, player_rotation)

    # Calculate the new position of the player character after rotation
    player_rect = rotated_player_image.get_rect(center=(player_x + player_width // 2, player_y + player_height // 2))

    # Draw the rotated player character
    screen.blit(rotated_player_image, player_rect)

    # Draw the NPC characters
    screen.blit(npc1_image, (npc1_x, npc1_y))
    screen.blit(npc2_image, (npc2_x, npc2_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()