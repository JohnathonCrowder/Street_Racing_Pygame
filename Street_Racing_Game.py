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

# Shrink the player character image by 50%
#player_image = pygame.transform.scale(player_image, (player_image.get_width() // 2.9, player_image.get_height() // 2.9))

# Load the NPC character image
npc_image = pygame.image.load(r"C:\Users\Admin\Pictures\txt\Transparent\top-car-view-png-34868_transparent.png")

# Shrink the NPC character image by 50%
npc_image = pygame.transform.scale(npc_image, (npc_image.get_width() // 2, npc_image.get_height() // 2))
npc_mask = pygame.mask.from_surface(npc_image)


# Get the character's width and height
player_width, player_height = player_image.get_size()
npc_width, npc_height = npc_image.get_size()

# Set the player's initial position
player_x = WINDOW_SIZE[0] // 2 - player_width // 2
player_y = WINDOW_SIZE[1] // 2 - player_height // 2

# Set the player's initial rotation
player_rotation = 0

# Set the NPC's initial position and speed
npc_x = WINDOW_SIZE[0] // 2 - npc_width // 2
npc_y = -npc_height  # Start above the screen
npc_speed = 2

# Set the player's speed
player_speed = 5

# Set the joystick threshold
JOYSTICK_THRESHOLD = 0.2

# Set up the PlayStation controller
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define the lane positions
left_lane_x = WINDOW_SIZE[0] // 4 - npc_width // 2
middle_lane_x = WINDOW_SIZE[0] // 2 - npc_width // 2
right_lane_x = 3 * WINDOW_SIZE[0] // 4 - npc_width // 2

# Define the line colors
line_color = (255, 255, 255)  # White color

# Define the possible wrap positions for the NPC
wrap_positions = [left_lane_x, middle_lane_x, right_lane_x]

# Set the rate at which the NPC slows down when the left trigger is pressed
slow_down_rate = 0.05

# Set the rate at which the NPC speeds up when the right trigger is pressed
speed_up_rate = 0.007

# Set the maximum speed for the NPC
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

    # Adjust the NPC's speed based on the trigger input
    if right_trigger > 0:
        npc_speed = min(npc_speed + speed_up_rate, max_speed)  # Gradually speed up the NPC
    elif left_trigger > 0:
        npc_speed = max(npc_speed - slow_down_rate, 0.5)  # Gradually slow down the NPC
    else:
        npc_speed = max(min(npc_speed, 2), 0.5)  # Maintain the speed within the range of 0.5 to 2

    # Move the NPC character
    npc_y += npc_speed
    if npc_y > WINDOW_SIZE[1]:
        npc_x = random.choice(wrap_positions)  # Choose a random wrap position
        npc_y = -npc_height  # Wrap the NPC back to the top

    # Check for collision between player and NPC
    offset_x = npc_x - player_x
    offset_y = npc_y - player_y
    collision = player_mask.overlap(npc_mask, (offset_x, offset_y))
    if collision:
        # Respawn the player
        player_x = WINDOW_SIZE[0] // 2 - player_width // 2
        player_y = WINDOW_SIZE[1] // 2 - player_height // 2

    # Clear the screen
    screen.fill((0, 0, 0))

    # Rotate the player character
    rotated_player_image = pygame.transform.rotate(player_image, player_rotation)

    # Calculate the new position of the player character after rotation
    player_rect = rotated_player_image.get_rect(center=(player_x + player_width // 2, player_y + player_height // 2))

    # Draw the rotated player character
    screen.blit(rotated_player_image, player_rect)

    # Draw the NPC character
    screen.blit(npc_image, (npc_x, npc_y))

    # Draw the lane lines
    pygame.draw.line(screen, line_color, (left_lane_x, 0), (left_lane_x, WINDOW_SIZE[1]), 5)
    pygame.draw.line(screen, line_color, (middle_lane_x, 0), (middle_lane_x, WINDOW_SIZE[1]), 5)
    pygame.draw.line(screen, line_color, (right_lane_x, 0), (right_lane_x, WINDOW_SIZE[1]), 5)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()