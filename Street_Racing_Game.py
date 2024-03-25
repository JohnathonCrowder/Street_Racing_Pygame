import pygame
import os
import random
import math
import time

import pygame.mask

# Initialize Pygame
pygame.init()

# Check if a controller is connected
controller_connected = pygame.joystick.get_count() > 0



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

# Load the coin image
coin_image = pygame.image.load(r"C:\Users\Admin\Pictures\txt\Transparent\Coin.png")
coin_image = pygame.transform.scale(coin_image, (coin_image.get_width() // 9, coin_image.get_height() // 9))
coin_mask = pygame.mask.from_surface(coin_image)

# Get the coin's width and height
coin_width, coin_height = coin_image.get_size()

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

flashing_state = False


road_line_offset = 0


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

high_scores = []


store_menu_open = False

# Define the wrap positions for the NPCs
wrap_positions = [left_lane_x + npc1_width // 2,
                 middle_lane_x,
                 right_lane_x - npc1_width // 2,
                 WINDOW_SIZE[0] - npc1_width//0.7]

# Set the coin's initial position
coin_x = random.choice(wrap_positions)
coin_y = -coin_height

# Set the player's speed
player_speed = 5

# Set the joystick threshold
JOYSTICK_THRESHOLD = 0.2

# Set up the PlayStation controller
pygame.joystick.init()
#joystick = pygame.joystick.Joystick(0)
#joystick.init()

# Initialize the joystick if a controller is connected
if controller_connected:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# Define the line colors
line_color = (255, 255, 255)  # White color

# Define the grass color
grass_color = (154, 205, 50)

# Set the rate at which the NPCs slow down when the left trigger is pressed
slow_down_rate = 0.05

# Set the rate at which the NPCs speed up when the right trigger is pressed
speed_up_rate = 0.007

# Set the initial maximum speed for the NPCs
initial_max_speed = 7
max_speed = initial_max_speed

# Initialize the score
score = 0

total_coins = 0

switch_cost = 20


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

# Create a surface for the labels rectangle
labels_rect_width = 200
labels_rect_height = 100
labels_rect_surface = pygame.Surface((labels_rect_width, labels_rect_height))
labels_rect_surface.set_alpha(225)  # Set the transparency of the rectangle (0-255)

# Set the position of the labels rectangle
labels_rect_x = WINDOW_SIZE[0] - labels_rect_width - 10
labels_rect_y = 10

# Load the semi NPC image
semi_image = pygame.image.load(r"C:\Users\Admin\Pictures\txt\Transparent\large-black-american-truck-with-trailer-type-dump-truck-transporting-bulk-cargo-white-background-3d-illustration_101266-6000 (1).png")
semi_image = pygame.transform.scale(semi_image, (semi_image.get_width() // 0.8, semi_image.get_height() ))
semi_mask = pygame.mask.from_surface(semi_image)

# Get the semi's width and height
semi_width, semi_height = semi_image.get_size()

# Set the semi's initial position and speed
semi_x = random.choice(wrap_positions)
semi_y = -semi_height
semi_speed = 2

# Define the image paths
image_paths = [
    r"C:\Users\Admin\Pictures\txt\Transparent\top-car-view-png-34868_transparent.png",
    r"C:\Users\Admin\Pictures\txt\Transparent\top-car-view-png-34870_transparent.png",
    r"C:\Users\Admin\Pictures\txt\Transparent\top-car-view-png-34872.png"
]

def draw_store_menu(flashing_state=False):
    # Clear the store menu surface
    store_menu_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    store_menu_surface.fill((0, 0, 0, 128))  # Semi-transparent black background

    # Draw the store menu title
    title_text = font.render("Store Menu", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 4))
    store_menu_surface.blit(title_text, title_rect)

    # Set the desired image size
    image_size = (200, 200)  # Adjust the size as needed

    # Calculate the total width of the images and spacing
    total_width = len(image_paths) * image_size[0] + (len(image_paths) - 1) * 50  # 50 is the spacing between images

    # Calculate the starting position for the images
    start_x = (WINDOW_SIZE[0] - total_width) // 2

    # Load and display the images
    for i, image_path in enumerate(image_paths):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, image_size)
        image_rect = image.get_rect(topleft=(start_x + i * (image_size[0] + 50), WINDOW_SIZE[1] // 2))
        store_menu_surface.blit(image, image_rect)

        # Draw a rectangle around the selected image
        if selected_image == i:
            if flashing_state:
                pygame.draw.rect(store_menu_surface, (255, 255, 0), image_rect, 4)  # Bright yellow color when flashing
            else:
                pygame.draw.rect(store_menu_surface, (255, 255, 255), image_rect, 2)  # White color when not flashing

    # Display the high scores
    high_scores_title = font.render("High Scores:", True, (255, 255, 255))
    high_scores_title_rect = high_scores_title.get_rect(topleft=(50, 50))
    store_menu_surface.blit(high_scores_title, high_scores_title_rect)

    for i, score in enumerate(high_scores, start=1):
        high_score_text = font.render(f"{i}. {score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(topleft=(50, 50 + i * 30))
        store_menu_surface.blit(high_score_text, high_score_rect)

    # Display the switch cost
    switch_cost_text = font.render(f"Switch Cost: {switch_cost} coins", True, (255, 255, 255))
    switch_cost_rect = switch_cost_text.get_rect(topleft=(50, WINDOW_SIZE[1] - 50))
    store_menu_surface.blit(switch_cost_text, switch_cost_rect)

    # Blit the store menu surface onto the main screen
    screen.blit(store_menu_surface, (0, 0))

    return store_menu_surface



def draw_background():
    global road_line_offset

    # Clear the screen
    screen.fill((0, 0, 0))

    # Clear left side green
    screen.fill(grass_color, rect=(0, 0, WINDOW_SIZE[0]//5.4, WINDOW_SIZE[1]))

    # Clear middle black
    screen.fill((0, 0, 0), rect=(WINDOW_SIZE[0]//2, 0, WINDOW_SIZE[0]//2, WINDOW_SIZE[1]))

    # Clear right side green
    screen.fill(grass_color, rect=(WINDOW_SIZE[0]//1.1, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]))

    # Draw the solid lane lines
    pygame.draw.line(screen, line_color, (left_lane_x, 0), (left_lane_x, WINDOW_SIZE[1]), 5)
    rightmost_lane_x_adjusted = rightmost_lane_x - 30  # Adjust the rightmost_lane_x value
    pygame.draw.line(screen, line_color, (rightmost_lane_x_adjusted, 0), (rightmost_lane_x_adjusted, WINDOW_SIZE[1]), 5)

    # Set the yellow color for the dotted lines
    yellow_color = (255, 255, 0)

    # Draw the dotted lane lines
    dash_length = 40
    dash_gap = 80
    y = road_line_offset
    while y < WINDOW_SIZE[1]:
        pygame.draw.line(screen, yellow_color, (middle_lane_x, y), (middle_lane_x, y + dash_length), 5)
        pygame.draw.line(screen, yellow_color, (right_lane_x, y), (right_lane_x, y + dash_length), 5)
        y += dash_length + dash_gap

    # Update the road line offset based on NPC1's speed if not waiting for respawn
    if not waiting_for_respawn:
        road_line_offset = (road_line_offset + npc1_speed) % (dash_length + dash_gap)


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


def check_collisions():
    global lives, waiting_for_respawn, score, max_speed, coin_y, total_coins, high_scores

    # Create a list of NPCs and their corresponding collision offsets
    npcs = [
        (npc1_image, npc1_mask, npc1_x, npc1_y),
        (npc2_image, npc2_mask, npc2_x, npc2_y),
        (npc3_image, npc3_mask, npc3_x, npc3_y),
        (npc4_image, npc4_mask, npc4_x, npc4_y),
        (semi_image, semi_mask, semi_x, semi_y)  # Add the semi to the list of NPCs
    ]

    for npc_image, npc_mask, npc_x, npc_y in npcs:
        offset_x = npc_x - player_x
        offset_y = npc_y - player_y
        collision = player_mask.overlap(npc_mask, (offset_x, offset_y))

        if collision:
            # Decrease the number of lives
            lives -= 1

            # Set the waiting for respawn flag
            waiting_for_respawn = True

            # Reset the positions of the NPCs
            reset_npc_positions()

            # Check for high scores and reset the score if no lives remain
            if lives == 0:
                # Check if the current score is a new high score
                if len(high_scores) < 3:
                    high_scores.append(score)
                    high_scores.sort(reverse=True)
                elif score > min(high_scores):
                    high_scores.append(score)
                    high_scores.sort(reverse=True)
                    high_scores = high_scores[:3]

                score = 0
                lives = 3  # Reset the lives to 3
                max_speed = initial_max_speed  # Reset the maximum speed to the default

            break  # Exit the loop if a collision is detected

    # Check for collision with the coin only if the score is above 15
    if score >= 15:
        offset_coin_x = coin_x - player_x
        offset_coin_y = coin_y - player_y
        coin_collision = player_mask.overlap(coin_mask, (offset_coin_x, offset_coin_y))

        if coin_collision:
            # If the player collects the coin, move it off-screen
            coin_y = WINDOW_SIZE[1] + coin_height
            score += 1  # Increment the score when the coin is collected
            total_coins += 1  # Increment the total coins collected






def handle_player_movement(player_x, player_y, player_width, player_height, player_speed, player_rotation):
    if controller_connected:
        # Get the axis values (left stick)
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)

        # Apply the joystick threshold
        if abs(x_axis) < JOYSTICK_THRESHOLD:
            x_axis = 0
        if abs(y_axis) < JOYSTICK_THRESHOLD:
            y_axis = 0

        # Move the player character based on the axis values
        player_x += x_axis * player_speed
        player_y += y_axis * player_speed
    else:
        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
            player_rotation = 15  # Rotate to the left
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
            player_rotation = -15  # Rotate to the right
        else:
            player_rotation = 0  # Return to the original rotation

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed

    # Keep the player character within the window bounds
    player_x = max(0, min(player_x, WINDOW_SIZE[0] - player_width))
    player_y = max(0, min(player_y, WINDOW_SIZE[1] - player_height))

    # Rotate the player character
    rotated_player_image = pygame.transform.rotate(player_image, player_rotation)

    # Calculate the new position of the player character after rotation
    player_rect = rotated_player_image.get_rect(center=(player_x + player_width // 2, player_y + player_height // 2))

    return player_x, player_y, player_rotation, rotated_player_image, player_rect






def handle_npc_movement(score, npc_speeds, npc_positions, npc_heights, npc_widths, wrap_positions, max_speed, speed_up_rate, slow_down_rate):
    if controller_connected:
        left_trigger = joystick.get_axis(4)
        right_trigger = joystick.get_axis(5)
    else:
        keys = pygame.key.get_pressed()
        left_trigger = keys[pygame.K_SPACE]  # Check if spacebar is pressed
        right_trigger = keys[pygame.K_LSHIFT]  # Check if left shift key is pressed

    for i in range(len(npc_speeds)):
        if right_trigger > 0:
            npc_speeds[i] = min(npc_speeds[i] + speed_up_rate, max_speed)
        elif left_trigger > 0:
            npc_speeds[i] = max(npc_speeds[i] - slow_down_rate, 0.5)
        else:
            npc_speeds[i] = max(min(npc_speeds[i], 2), 0.5)

        npc_x, npc_y = npc_positions[i]
        npc_height = npc_heights[i]
        npc_width = npc_widths[i]

        if i == 0:  # Move NPC1 always
            npc_y += npc_speeds[i]
            if npc_y > WINDOW_SIZE[1]:
                npc_x = random.choice(wrap_positions)
                npc_y = -npc_height
                score += 1
        elif i == 1 and score >= 20:  # Move NPC2 only if score is above 20
            npc_y += npc_speeds[i]
            if npc_y > WINDOW_SIZE[1]:
                npc_x = random.choice(wrap_positions)
                npc_y = -npc_height
                score += 1
        elif i == 2 and score >= 35:  # Move NPC3 only if score is above 35
            npc_y += npc_speeds[i]
            if npc_y > WINDOW_SIZE[1]:
                npc_x = random.choice(wrap_positions)
                npc_y = -npc_height
                score += 1
        elif i == 3 and score >= 50:  # Move semi only if score is above 50
            npc_y += npc_speeds[i]
            if npc_y > WINDOW_SIZE[1]:
                npc_x = random.choice(wrap_positions)
                npc_y = -npc_height
                score += 1
        else:
            npc_y = WINDOW_SIZE[1] + npc_height

        npc_positions[i] = (npc_x, npc_y)

    # Check for collisions between NPCs and respawn only one of them
    for i in range(len(npc_positions)):
        for j in range(i + 1, len(npc_positions)):
            npc1_rect = pygame.Rect(npc_positions[i][0], npc_positions[i][1], npc_widths[i], npc_heights[i])
            npc2_rect = pygame.Rect(npc_positions[j][0], npc_positions[j][1], npc_widths[j], npc_heights[j])

            if npc1_rect.colliderect(npc2_rect):
                # Give priority to the semi (index 3)
                if i == 3:
                    npc_positions[j] = (random.choice(wrap_positions), -npc_heights[j])
                elif j == 3:
                    npc_positions[i] = (random.choice(wrap_positions), -npc_heights[i])
                else:
                    # Respawn only one of the colliding NPCs (excluding the semi)
                    if random.choice([True, False]):
                        npc_positions[i] = (random.choice(wrap_positions), -npc_heights[i])
                    else:
                        npc_positions[j] = (random.choice(wrap_positions), -npc_heights[j])

    return score, npc_speeds, npc_positions








def draw_labels(score, lives, total_coins):
    # Clear the labels rectangle surface
    labels_rect_surface.fill((128, 128, 128))  # Fill with gray color

    # Draw the score on the labels rectangle surface
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    labels_rect_surface.blit(score_text, (10, 10))

    # Draw the lives on the labels rectangle surface
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    labels_rect_surface.blit(lives_text, (10, 40))

    # Draw the total coins collected on the labels rectangle surface
    total_coins_text = font.render(f"Coins: {total_coins}", True, (255, 255, 255))
    labels_rect_surface.blit(total_coins_text, (10, 70))

    # Blit the labels rectangle surface onto the main screen
    screen.blit(labels_rect_surface, (labels_rect_x, labels_rect_y))







def check_coin_npc_collision():
    global coin_x, coin_y

    # Create a list of NPCs and their positions
    npcs = [
        (npc1_image, npc1_x, npc1_y),
        (npc2_image, npc2_x, npc2_y),
        (npc3_image, npc3_x, npc3_y),
        (npc4_image, npc4_x, npc4_y)
    ]

    for npc_image, npc_x, npc_y in npcs:
        npc_rect = npc_image.get_rect(topleft=(npc_x, npc_y))
        coin_rect = coin_image.get_rect(topleft=(coin_x, coin_y))

        if npc_rect.colliderect(coin_rect):
            # Respawn the coin at a new position
            coin_x = random.choice(wrap_positions)
            coin_y = -coin_height
            break


# Game loop
selected_image = 0
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and waiting_for_respawn and not store_menu_open:
                # Respawn the player
                player_x = WINDOW_SIZE[0] // 2 - player_width // 2
                player_y = WINDOW_SIZE[1] // 2 - player_height // 2
                waiting_for_respawn = False
            elif event.key == pygame.K_SPACE and waiting_for_respawn:
                # Toggle the store menu
                store_menu_open = not store_menu_open
                if not store_menu_open:
                    # If the store menu is closed, redraw the background and respawn message
                    draw_background()
                    respawn_text = font.render("Press Enter to Respawn", True, (255, 255, 255))
                    respawn_rect = respawn_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
                    screen.blit(respawn_text, respawn_rect)
                    pygame.display.flip()
            elif event.key == pygame.K_RETURN and store_menu_open:
                if total_coins >= switch_cost:
                    # Change the player's character to the selected image
                    player_image = pygame.image.load(image_paths[selected_image])
                    player_image = pygame.transform.scale(player_image, (player_image.get_width() // 5.9, player_image.get_height() // 2.9))
                    player_mask = pygame.mask.from_surface(player_image)
                    player_width, player_height = player_image.get_size()
                    total_coins -= switch_cost  # Subtract the switch cost from the total coins
                    flashing_state = True  # Set flashing_state to True when the Enter key is pressed
                    store_menu_surface = draw_store_menu(flashing_state)  # Redraw the store menu with flashing_state
                    screen.blit(store_menu_surface, (0, 0))  # Blit the store menu surface onto the main screen
                    pygame.display.flip()
                    pygame.time.delay(200)  # Display the flashing state for a short duration (e.g., 200ms)
                    flashing_state = False  # Set flashing_state back to False
                    store_menu_surface = draw_store_menu(flashing_state)  # Redraw the store menu without flashing_state
                    screen.blit(store_menu_surface, (0, 0))  # Blit the store menu surface onto the main screen
                    pygame.display.flip()
                else:
                    # Display a message when the player doesn't have enough coins
                    store_menu_surface = draw_store_menu()  # Get the store_menu_surface from the function
                    not_enough_coins_text = font.render("Not enough coins to switch characters!", True, (255, 0, 0))
                    not_enough_coins_rect = not_enough_coins_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] - 50))
                    store_menu_surface.blit(not_enough_coins_text, not_enough_coins_rect)
                    screen.blit(store_menu_surface, (0, 0))  # Blit the store menu surface onto the main screen
                    pygame.display.flip()
                    pygame.time.delay(2000)  # Display the message for 2 seconds
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and store_menu_open:
                selected_image = (selected_image - 1) % len(image_paths)
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and store_menu_open:
                selected_image = (selected_image + 1) % len(image_paths)
        elif event.type == pygame.JOYBUTTONDOWN and controller_connected:
            if event.button == 8 and waiting_for_respawn and not store_menu_open:  # Start button (button index 7)
                # Respawn the player
                player_x = WINDOW_SIZE[0] // 2 - player_width // 2
                player_y = WINDOW_SIZE[1] // 2 - player_height // 2
                waiting_for_respawn = False
            elif event.button == 9 and waiting_for_respawn:  # Select button (button index 8)
                # Toggle the store menu
                store_menu_open = not store_menu_open
                if not store_menu_open:
                    # If the store menu is closed, redraw the background and respawn message
                    draw_background()
                    respawn_text = font.render("Press Start to Respawn", True, (255, 255, 255))
                    respawn_rect = respawn_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
                    screen.blit(respawn_text, respawn_rect)
                    pygame.display.flip()
            elif event.button == 0 and store_menu_open:  # X button (button index 0)
                if total_coins >= switch_cost:
                    # Change the player's character to the selected image
                    player_image = pygame.image.load(image_paths[selected_image])
                    player_image = pygame.transform.scale(player_image, (player_image.get_width() // 5.9, player_image.get_height() // 2.9))
                    player_mask = pygame.mask.from_surface(player_image)
                    player_width, player_height = player_image.get_size()
                    total_coins -= switch_cost  # Subtract the switch cost from the total coins
                    flashing_state = True  # Set flashing_state to True when the X button is pressed
                    store_menu_surface = draw_store_menu(flashing_state)  # Redraw the store menu with flashing_state
                    screen.blit(store_menu_surface, (0, 0))  # Blit the store menu surface onto the main screen
                    pygame.display.flip()
                    pygame.time.delay(200)  # Display the flashing state for a short duration (e.g., 200ms)
                    flashing_state = False  # Set flashing_state back to False
                    store_menu_surface = draw_store_menu(flashing_state)  # Redraw the store menu without flashing_state
                    screen.blit(store_menu_surface, (0, 0))  # Blit the store menu surface onto the main screen
                    pygame.display.flip()
                else:
                    # Display a message when the player doesn't have enough coins
                    store_menu_surface = draw_store_menu()  # Get the store_menu_surface from the function
                    not_enough_coins_text = font.render("Not enough coins to switch characters!", True, (255, 0, 0))
                    not_enough_coins_rect = not_enough_coins_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] - 50))
                    store_menu_surface.blit(not_enough_coins_text, not_enough_coins_rect)
                    screen.blit(store_menu_surface, (0, 0))  # Blit the store menu surface onto the main screen
                    pygame.display.flip()
                    pygame.time.delay(2000)  # Display the message for 2 seconds
            elif event.button == 10 and store_menu_open:  # Left arrow button (button index 10)
                selected_image = (selected_image - 1) % len(image_paths)
            elif event.button == 11 and store_menu_open:  # Right arrow button (button index 11)
                selected_image = (selected_image + 1) % len(image_paths)

    # Skip player movement and collision checks if waiting for respawn
    if waiting_for_respawn:
        if store_menu_open:
            # Draw the store menu
            draw_store_menu()
            pygame.display.flip()
        else:
            # Draw the background and respawn message
            draw_background()
            respawn_text = font.render("Press Start to Respawn", True, (255, 255, 255))
            respawn_rect = respawn_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            screen.blit(respawn_text, respawn_rect)
            pygame.display.flip()

        continue


    ###### Player Movement #######################################

    # Handle player movement
    player_x, player_y, player_rotation, rotated_player_image, player_rect = handle_player_movement(
        player_x, player_y, player_width, player_height, player_speed, player_rotation)


    ###### NPC Movement ######################

    # Handle NPC movement
    score, npc_speeds, npc_positions = handle_npc_movement(
        score,
        [npc1_speed, npc2_speed, npc3_speed, semi_speed],
        [(npc1_x, npc1_y), (npc2_x, npc2_y), (npc3_x, npc3_y), (semi_x, semi_y)],
        [npc1_height, npc2_height, npc3_height, semi_height],
        [npc1_width, npc2_width, npc3_width, semi_width],
        wrap_positions,
        max_speed,
        speed_up_rate,
        slow_down_rate
    )

    npc1_x, npc1_y = npc_positions[0]
    npc2_x, npc2_y = npc_positions[1]
    npc3_x, npc3_y = npc_positions[2]
    semi_x, semi_y = npc_positions[3]

    npc1_speed, npc2_speed, npc3_speed, semi_speed = npc_speeds


    #Tree Movement
    # Move Tree only if the score is above 20
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


    # Move the coin only if the score is above 15
    if score >= 15:
        coin_y += npc1_speed  # Use npc1_speed for the coin's speed
        if coin_y > WINDOW_SIZE[1]:
            coin_x = random.choice(wrap_positions)
            coin_y = -coin_height

        # Check for collision between the coin and NPCs
        check_coin_npc_collision()
    else:
        # If the score is below 15, set the coin off-screen
        coin_y = WINDOW_SIZE[1] + coin_height




    ######## Drawing Game #######################################################

    # Check for collisions
    check_collisions()

    # Draw the background and lines
    draw_background()

    # Draw the rotated player character
    screen.blit(rotated_player_image, player_rect)

    # Draw the NPC characters
    screen.blit(npc1_image, (npc1_x, npc1_y))
    screen.blit(npc2_image, (npc2_x, npc2_y))
    screen.blit(npc3_image, (npc3_x, npc3_y))
    screen.blit(npc4_image, (npc4_x, npc4_y))
    screen.blit(semi_image, (semi_x, semi_y))

    # Draw the coin only if the score is above 15
    if score >= 15:
        screen.blit(coin_image, (coin_x, coin_y))

    # Draw the Score/Lives/Coins labels and grey rectangle
    draw_labels(score, lives, total_coins)




    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()