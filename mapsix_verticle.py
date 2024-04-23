import pygame
import math
import json

# Function to draw a hexagon given its center and size


def draw_hex(surface, center, size, color):
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        points.append((center[0] + size * math.cos(angle_rad),
                       center[1] + size * math.sin(angle_rad)))
    pygame.draw.polygon(surface, color, points)


# Load the hex map data from the JSON file
with open('maps/basic.json', 'r') as f:
    hex_map_data = json.load(f)['map_data']

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Render the hex map
    hex_size = 20  # Size of the hexagon
    for hex_row in hex_map_data:
        for hex_data in hex_row:
            # Calculate the position of this hex
            # Assuming your grid width is 10 for simplicity
            x = hex_data['pos'] % 10
            y = hex_data['pos'] // 10
            center_x = x * hex_size * 1.5
            offset_y = hex_size * math.sqrt(3) * (y + 0.5 * (x % 2))
            center_y = offset_y

            # Determine the color based on elevation and condition
            if hex_data['cond'] == 0:
                color = (0, 150, 0)  # Green for fields
            else:
                color = (150, 75, 0)  # Brown for mountains

            draw_hex(screen, (center_x, center_y), hex_size, color)

    pygame.display.flip()

pygame.quit()
