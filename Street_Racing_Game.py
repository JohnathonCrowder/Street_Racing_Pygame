import pygame
import os
import random
import math
import time

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

# Load the third NPC character image
npc3_image = pygame.image.load(r"C:\Users\Admin\Pictures\txt\Transparent\top-car-view-png-34870_transparent.png")
npc3_image = pygame.transform.scale(npc3_image, (npc3_image.get_width() // 3.5, npc3_image.get_height() // 3.5))
npc3_mask = pygame.mask.from_surface(npc3_image)

# Get the character's width and height
player_width, player_height = player_image.get_size()
npc1_width, npc1_height = npc1_image.get_size()
npc2_width, npc2_height = npc2_image.get_size()
npc3_width, npc3_height = npc3_image.get_size()

# Set the player's initial position
player_x = WINDOW_SIZE[0] // 2 - player_width // 2
player_y = WINDOW_SIZE[1] // 2 - player_height // 2

# Set the player's initial rotation
player_rotation = 0

# Define the lane positions
left_lane_x = WINDOW_SIZE[0] // 4 - npc1_width // 2
middle_lane_x = WINDOW_SIZE[0] // 2 - npc1_width // 2
right_lane_x = 3 * WINDOW_SIZE[0] // 4 - npc1_width // 2
rightmost_lane_x = WINDOW_SIZE[0] - npc1_width // 2

# Set the NPCs' initial positions and speeds
npc1_x = random.randint(left_lane_x + npc1_width // 2, right_lane_x - npc1_width // 2)
npc1_y = -npc1_height
npc1_speed = 2

npc2_x = random.randint(middle_lane_x + npc2_width // 2, rightmost_lane_x - npc2_width // 2)
npc2_y = -npc2_height
npc2_speed = 2

npc3_x = random.randint(left_lane_x + npc3_width // 2, right_lane_x - npc3_width // 2)
npc3_y = -npc3_height
npc3_speed = 2

# Define the wrap positions for the NPCs
wrap_positions = [left_lane_x + npc1_width // 2,
                 middle_lane_x,
                 right_lane_x - npc1_width // 2,
                 WINDOW_SIZE[0] - npc1_width//0.7]

# Set the player's speed
player_speed = 5

# Set the joystick threshold
JOYSTICK_THRESHOLD = 0.2

# Set up the PlayStation controller
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define the line colors
line_color = (255, 255, 255)  # White color

# Define the grass color
grass_color = (154, 205, 50)

# Set the rate at which the NPCs slow down when the left trigger is pressed
slow_down_rate = 0.05

# Set the rate at which the NPCs speed up when the right trigger is pressed
speed_up_rate = 0.002

# Set the initial maximum speed for the NPCs
initial_max_speed = 7
max_speed = initial_max_speed

# Initialize the score
score = 0

# Initialize the lives
lives = 3

# Define the font for the score and lives display
font = pygame.font.Font(None, 36)

# Initialize the waiting for respawn flag
waiting_for_respawn = False



# Load the fourth NPC character image
npc4_image = pygame.image.load(r"C:\Users\Admin\Pictures\txt\Transparent\mpjm_7eoy_210607_transparent.png")
npc4_image = pygame.transform.scale(npc4_image, (npc4_image.get_width() // 16.5, npc4_image.get_height() // 16.5))
npc4_mask = pygame.mask.from_surface(npc4_image)

# Get the fourth NPC's width and height
npc4_width, npc4_height = npc4_image.get_size()

# Set the fourth NPC's initial position and speed
npc4_x = left_lane_x // 2 - npc4_width // 2
npc4_y = -npc4_height
npc4_speed = 4

# Define the wrap position for the fourth NPC
npc4_wrap_positions = [left_lane_x // 2 - npc4_width // 2,
                      WINDOW_SIZE[0] - npc4_width // 2]


def reset_npc_positions():
    global npc1_x, npc1_y, npc2_x, npc2_y, npc3_x, npc3_y, npc4_x, npc4_y

    # Set random y-coordinates for each NPC to stagger their respawning
    npc1_y = -random.randint(npc1_height, WINDOW_SIZE[1])
    npc2_y = -random.randint(npc2_height, WINDOW_SIZE[1])
    npc3_y = -random.randint(npc3_height, WINDOW_SIZE[1])
    npc4_y = -random.randint(npc4_height, WINDOW_SIZE[1])

    # Set random x-coordinates for each NPC
    npc1_x = random.choice(wrap_positions)
    npc2_x = random.choice(wrap_positions)
    npc3_x = random.choice(wrap_positions)
    npc4_x = random.choice(npc4_wrap_positions)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 8 and waiting_for_respawn:  # Start button (button index 7)
                # Respawn the player
                player_x = WINDOW_SIZE[0] // 2 - player_width // 2
                player_y = WINDOW_SIZE[1] // 2 - player_height // 2
                waiting_for_respawn = False

    # Skip player movement and collision checks if waiting for respawn
    if waiting_for_respawn:
        continue

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

    # Check if the score reaches a multiple of 50 and increase the max speed
    if score > 0 and score % 50 == 0:
        max_speed += 1

    # Adjust the NPCs' speeds based on the trigger input
    if right_trigger > 0:
        npc1_speed = min(npc1_speed + speed_up_rate, max_speed)
        npc2_speed = min(npc2_speed + speed_up_rate, max_speed)
        npc3_speed = min(npc3_speed + speed_up_rate, max_speed)
    elif left_trigger > 0:
        npc1_speed = max(npc1_speed - slow_down_rate, 0.5)
        npc2_speed = max(npc2_speed - slow_down_rate, 0.5)
        npc3_speed = max(npc3_speed - slow_down_rate, 0.5)
    else:
        npc1_speed = max(min(npc1_speed, 2), 0.5)
        npc2_speed = max(min(npc2_speed, 2), 0.5)
        npc3_speed = max(min(npc3_speed, 2), 0.5)

    # Move NPC1
    npc1_y += npc1_speed
    if npc1_y > WINDOW_SIZE[1]:
        npc1_x = random.choice(wrap_positions)
        npc1_y = -npc1_height
        score += 1  # Increment the score when NPC1 is wrapped

    # Move NPC2 only if the score is above 3
    if score >= 5:
        # Before moving NPC2, check if it will collide with NPC1
        proposed_npc2_y = npc2_y + npc2_speed
        proposed_npc2_rect = pygame.Rect(npc2_x, proposed_npc2_y, npc2_width, npc2_height)
        if proposed_npc2_rect.colliderect(pygame.Rect(npc1_x, npc1_y, npc1_width, npc1_height)):
            # NPCs would collide, so update NPC2 x position to avoid collision
            avoidance_x = npc1_x + npc1_width + 1 if npc2_x < npc1_x else npc1_x - npc2_width - 1
            npc2_x = avoidance_x

        # Move NPC2 with updated position
        npc2_y += npc2_speed
        if npc2_y > WINDOW_SIZE[1]:
            npc2_x = random.choice(wrap_positions)
            npc2_y = -npc2_height
            score += 1  # Increment the score when NPC2 is wrapped
    else:
        # If the score is below 3, set NPC2 off-screen
        npc2_y = WINDOW_SIZE[1] + npc2_height

    # Move NPC3 only if the score is above 20
    if score >= 20:
        # Before moving NPC3, check if it will collide with NPC1 or NPC2
        proposed_npc3_y = npc3_y + npc3_speed
        proposed_npc3_rect = pygame.Rect(npc3_x, proposed_npc3_y, npc3_width, npc3_height)
        if proposed_npc3_rect.colliderect(pygame.Rect(npc1_x, npc1_y, npc1_width, npc1_height)) or \
                proposed_npc3_rect.colliderect(pygame.Rect(npc2_x, npc2_y, npc2_width, npc2_height)):
            # NPCs would collide, so update NPC3 x position to avoid collision
            avoidance_x = npc1_x + npc1_width + 1 if npc3_x < npc1_x else npc2_x - npc3_width - 1
            npc3_x = avoidance_x

        # Move NPC3 with updated position
        npc3_y += npc3_speed
        if npc3_y > WINDOW_SIZE[1]:
            npc3_x = random.choice(wrap_positions)
            npc3_y = -npc3_height
            score += 1  # Increment the score when NPC3 is wrapped
    else:
        # If the score is below 20, set NPC3 off-screen
        npc3_y = WINDOW_SIZE[1] + npc3_height

    # Check for collision between player and NPCs
    offset_x1 = npc1_x - player_x
    offset_y1 = npc1_y - player_y
    collision1 = player_mask.overlap(npc1_mask, (offset_x1, offset_y1))

    # Move NPC4 only if the score is above 20
    if score > 20:
        # Move NPC4 without collision check
        npc4_y += npc4_speed
        if npc4_y > WINDOW_SIZE[1]:
            npc4_x = random.choice(npc4_wrap_positions)  # Choose a random wrap position from the new list
            npc4_y = -npc4_height
            score += 1  # Increment the score when NPC4 is wrapped
    else:
        # If the score is below 20, set NPC4 off-screen
        npc4_y = WINDOW_SIZE[1] + npc4_height

    # Check for collision between player and NPC4 only if the score is above 20
    if score > 20:
        offset_x4 = npc4_x - player_x
        offset_y4 = npc4_y - player_y
        collision4 = player_mask.overlap(npc4_mask, (offset_x4, offset_y4))
    else:
        collision4 = False

    # Check for collision with NPC2 only if the score is above 3
    if score >= 5:
        offset_x2 = npc2_x - player_x
        offset_y2 = npc2_y - player_y
        collision2 = player_mask.overlap(npc2_mask, (offset_x2, offset_y2))
    else:
        collision2 = False

    # Check for collision with NPC3 only if the score is above 20
    if score >= 20:
        offset_x3 = npc3_x - player_x
        offset_y3 = npc3_y - player_y
        collision3 = player_mask.overlap(npc3_mask, (offset_x3, offset_y3))
    else:
        collision3 = False

    if collision1 or collision2 or collision3 or collision4:
        # Decrease the number of lives
        lives -= 1

        # Set the waiting for respawn flag
        waiting_for_respawn = True

        # Reset the positions of the NPCs
        reset_npc_positions()

        # Reset the score if no lives remain
        if lives == 0:
            score = 0
            lives = 3  # Reset the lives to 3
            max_speed = initial_max_speed  # Reset the maximum speed to the default

    # Clear the screen
    screen.fill((0, 0, 0))

    # Clear left side green
    screen.fill(grass_color, rect=(0, 0, WINDOW_SIZE[0]//5.4, WINDOW_SIZE[1]))

    # Clear middle black
    screen.fill((0, 0, 0), rect=(WINDOW_SIZE[0]//2, 0, WINDOW_SIZE[0]//2, WINDOW_SIZE[1]))

    # Clear right side green
    screen.fill(grass_color, rect=(WINDOW_SIZE[0]//1.1, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]))

    # Draw the lane lines
    pygame.draw.line(screen, line_color, (left_lane_x, 0), (left_lane_x, WINDOW_SIZE[1]), 5)
    pygame.draw.line(screen, line_color, (middle_lane_x, 0), (middle_lane_x, WINDOW_SIZE[1]), 5)
    pygame.draw.line(screen, line_color, (right_lane_x, 0), (right_lane_x, WINDOW_SIZE[1]), 5)
    rightmost_lane_x_adjusted = rightmost_lane_x - 30  # Adjust the rightmost_lane_x value
    pygame.draw.line(screen, line_color, (rightmost_lane_x_adjusted, 0), (rightmost_lane_x_adjusted, WINDOW_SIZE[1]), 5)

    # Rotate the player character
    rotated_player_image = pygame.transform.rotate(player_image, player_rotation)

    # Calculate the new position of the player character after rotation
    player_rect = rotated_player_image.get_rect(center=(player_x + player_width // 2, player_y + player_height // 2))

    # Draw the rotated player character
    screen.blit(rotated_player_image, player_rect)

    # Draw the NPC characters
    screen.blit(npc1_image, (npc1_x, npc1_y))
    screen.blit(npc2_image, (npc2_x, npc2_y))
    screen.blit(npc3_image, (npc3_x, npc3_y))
    # Draw the fourth NPC character
    screen.blit(npc4_image, (npc4_x, npc4_y))

    # Draw the score and lives
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WINDOW_SIZE[0] - 150, 10))

    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (WINDOW_SIZE[0] - 150, 40))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()