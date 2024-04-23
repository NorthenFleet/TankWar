import pygame
import math
import json


def draw_hex(surface, center, size, color):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        points.append((center[0] + size * math.cos(angle_rad),
                       center[1] + size * math.sin(angle_rad)))
    pygame.draw.polygon(surface, color, points)


def get_hex_center(x, y, size):
    offset_x = size * math.sqrt(3) * (x + 0.5 * (y % 2))
    offset_y = size * 1.5 * y
    return offset_x, offset_y


def load_map_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)['map_data']


def draw_map(screen, map_data, hex_size):
    for hex_row in map_data:
        for hex_data in hex_row:
            x = hex_data['pos'] % 10  # �����ͼ����Ϊ10
            y = hex_data['pos'] // 10
            center = get_hex_center(x, y, hex_size)
            color = (0, 150, 0) if hex_data['cond'] == 0 else (150, 75, 0)
            draw_hex(screen, center, hex_size, color)


pygame.init()
screen = pygame.display.set_mode((800, 600))


map_data = load_map_data('maps/basic.json')
hex_size = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # ����

    # ���Ƶ�ͼ
    draw_map(screen, map_data, hex_size)

    pygame.display.flip()  # ������ʾ

pygame.quit()
