import pygame
import math


def draw_hexagon(surface, x, y, size):
    """在给定的位置绘制一个六边形"""
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        points.append((x + size * math.cos(angle_rad),
                       y + size * math.sin(angle_rad)))
    pygame.draw.polygon(surface, (255, 255, 255), points)


def render_hex_map(surface, map_width, map_height, hex_size):
    """渲染六边形地图"""
    hex_height = math.sqrt(3) * hex_size
    hex_width = 2 * hex_size
    vert_dist = hex_height
    horiz_dist = hex_width * 3/4

    for row in range(map_height):
        for col in range(map_width):
            x = col * horiz_dist
            y = row * vert_dist
            if col % 2 == 1:
                y += vert_dist / 2
            draw_hexagon(surface, x, y, hex_size)


pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    render_hex_map(screen, 10, 10, 30)  # 示例：10x10的地图，每个六边形边长为30像素
    pygame.display.flip()

pygame.quit()
