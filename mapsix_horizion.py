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


def load_hex_images(hex_size):
    # 假设你有两种类型的六角形图像，一种用于条件0，一种用于条件1
    # 图像应已预先缩放到合适的尺寸
    alphat = 1.75
    belt = 1.5
    return {
        0: pygame.transform.scale(pygame.image.load('images/sex_geo/city.png').convert_alpha(), (alphat*hex_size, belt*hex_size)),
        1: pygame.transform.scale(pygame.image.load('images/sex_geo/conlin.png').convert_alpha(), (alphat*hex_size, belt*hex_size)),
        2: pygame.transform.scale(pygame.image.load('images/sex_geo/sand.png').convert_alpha(), (alphat*hex_size, belt*hex_size)),
        3: pygame.transform.scale(pygame.image.load('images/sex_geo/sand1.png').convert_alpha(), (alphat*hex_size, belt*hex_size)),
        4: pygame.transform.scale(pygame.image.load('images/sex_geo/sand2.png').convert_alpha(), (alphat*hex_size, belt*hex_size))
    }


def draw_map(screen, map_data, hex_images, hex_size):
    for hex_row in map_data:
        for hex_data in hex_row:
            x = hex_data['pos'] % 100
            y = hex_data['pos'] % len(map_data[1])
            center = get_hex_center(x, y, hex_size)
            hex_image = hex_images[hex_data['cond']]
            # Here we need to adjust the position to blit the image correctly
            hex_rect = hex_image.get_rect(center=center)
            screen.blit(hex_image, hex_rect.topleft)


pygame.init()
screen = pygame.display.set_mode((1800, 1000))

with open('maps/basic.json', 'r') as f:
    map_data = json.load(f)['map_data']

hex_size = 20
hex_images = load_hex_images(hex_size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    draw_map(screen, map_data, hex_images, hex_size)

    pygame.display.flip()

pygame.quit()
