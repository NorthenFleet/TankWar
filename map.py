import pygame
import re
import datetime
import os
from config import CON


class Button(pygame.sprite.Sprite):
    def __init__(self, text, tile_type, color, text_color, x, y, width, height, image=None, selected=False):
        super().__init__()
        self.text = text
        self.tile_type = tile_type
        self.color = color
        self.text_color = text_color
        self.image = pygame.Surface((width, height))
        self.image.fill(color)  # 按钮背景颜色
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 36)

        if image:
            self.tile_image = pygame.transform.scale(
                image, (width, height))  # 缩放图像以适应按钮大小
        else:
            self.tile_image = None

        self.render_text()

    def render_text(self):
        if self.tile_image:
            # 如果提供了图像，则在按钮上绘制图像
            self.image.blit(self.tile_image, (0, 0))
        else:
            # 如果没有提供图像，则在按钮上绘制文字
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(
                center=(self.width / 2, self.height / 2))
            self.image.blit(text_surface, text_rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_selected(self, surface):
        """绘制选中状态的边框"""
        pygame.draw.rect(surface, CON.WHITE, self.rect, 2)  # 绘制白色边框


class Map:
    def __init__(self):
        self.width = CON.MAP_WIDTH
        self.height = CON.MAP_HEIGHT
        self.tile_size = CON.GRID_SIZE
        self.grid_x = int(CON.MAP_WIDTH / self.tile_size)
        self.grid_y = int(CON.MAP_HEIGHT / self.tile_size)
        self.tiles = [[CON.TileType_FIELD for _ in range(
            CON.MAP_WIDTH)] for _ in range(CON.MAP_HEIGHT)]

    def load_map(self, file_path):
        with open(file_path, 'r') as file:
            # 读取所有行
            lines = file.readlines()

            # 初始化地图数据列表
            map_data = []

            for line in lines:
                # 使用正则表达式找出所有的数字
                numbers = re.findall(r'-?\d+', line.strip())
                # 将找到的数字字符串转换为整数，并添加到地图数据列表
                map_data.append([int(num) for num in numbers])
        self.tiles = map_data


class MapEdit():
    def __init__(self, screen, map_surface, bottom_surface):
        self.screen = screen
        self.map_surface = map_surface
        self.map = Map()
        self.bottom_surface = bottom_surface
        self.selected_tile_type = CON.TileType_NONE  # 默认选中的地图元素
        self.tile_buttons = []  # 存储地图元素按钮
        self.save_button = None
        self.tile_size = CON.GRID_SIZE

        # 加载地图元素图片并创建按钮
        self.load_tiles()
        self.create_buttons()

    def button(self):
        # 创建按钮组
        buttons_start = pygame.sprite.Group()
        buttons_game = pygame.sprite.Group()

    def save_map(self):
        # 获取当前日期和时间
        now = datetime.datetime.now()
        # 将日期和时间格式化为字符串（例如：'2023-03-29_15-30-25'）
        filename = now.strftime("map_%Y-%m-%d_%H-%M-%S.txt")
        # 拼接文件路径（如果需要保存在特定文件夹，可以在这里指定路径）
        directory = 'maps'
        # 确保目录存在
        if not os.path.exists(directory):
            os.makedirs(directory)
        # 拼接文件路径
        file_path = os.path.join(directory, filename)
        # 保存地图数据到文件
        with open(file_path, 'w') as file:
            for row in self.map.tiles:
                line = ','.join(str(tile) for tile in row)
                file.write(line + "\n")
        print(f"Map saved as {file_path}")

    def load_map(self, map):
        self.map.load_map(map)

    def load_tiles(self):
        self.tiles_images = {
            CON.TileType_NONE: pygame.image.load('images/geo/None.png').convert_alpha(),
            CON.TileType_FIELD: pygame.image.load('images/geo/Field.png').convert_alpha(),
            CON.TileType_RIVER: pygame.image.load('images/geo/River.png').convert_alpha(),
            CON.TileType_SAND: pygame.image.load('images/geo/Sand.png').convert_alpha(),
            CON.TileType_BRICK_WALL: pygame.image.load('images/geo/Brick.png').convert_alpha(),
            CON.TileType_STONE_WALL: pygame.image.load(
                'images/geo/Stone.png').convert_alpha()
        }

    def create_buttons(self):
        # 地 图元素按钮
        button_positions = [(i * 60 + 10, 30)
                            for i in range(len(self.tiles_images))]  # 按钮位置
        for i, (tile_type, image) in enumerate(self.tiles_images.items()):
            button_x, button_y = button_positions[i]
            # 注意去掉展开操作符(*)，直接传递坐标值
            button = Button(" ", tile_type, CON.GRAY, CON.BLACK,
                            button_x, button_y, 50, 50, image=image)
            self.tile_buttons.append(button)
        # 保存按钮
        self.save_button = Button(
            "Save", "Save", CON.GREEN, CON.WHITE, 700, 30, 80, 40)

    def draw_ui(self):
        for button in self.tile_buttons:
            if button.tile_type == self.selected_tile_type:
                button.selected = True  # 标记为选中状态
                button.draw_selected(self.bottom_surface)
            else:
                button.selected = False  # 标记为非选中状态
                button.draw(self.bottom_surface)
        self.save_button.draw(self.bottom_surface)

    def draw_map(self):
        """渲染地图"""
        for y in range(self.map.grid_y):
            for x in range(self.map.grid_x):
                tile_type = self.map.tiles[y][x]
                color = self.get_tile_color(tile_type)
                tile_image = self.get_tile_image(tile_type)
                if tile_image:
                    self.map_surface.blit(
                        tile_image, (x * self.tile_size, y * self.tile_size))
                else:
                    pygame.draw.rect(self.map_surface, color, (x * self.tile_size,
                                                               y * self.tile_size, self.tile_size, self.tile_size))

    def move_tank(self, dx, dy):
        new_x = self.tank_x + dx
        new_y = self.tank_y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.tank_x = new_x
            self.tank_y = new_y

    def get_tile_image(self, tile_type):
        """根据地形元素类型获取对应的图片"""
        return self.tiles_images.get(tile_type, None)

    def get_tile_color(self, tile_type):
        """根据地形元素类型获取对应的颜色"""
        tile_colors = {
            CON.TileType_NONE: (0, 0, 0),
            CON.TileType_FIELD: (124, 252, 0),  # 浅绿色
            CON.TileType_RIVER: (30, 144, 255),  # 深蓝色
            CON.TileType_BRICK_WALL: (139, 69, 19),  # 棕色
            CON.TileType_STONE_WALL: (128, 128, 128),  # 灰色
            CON.TileType_SAND: (238, 232, 170),  # 沙色
        }
        return tile_colors.get(tile_type, (124, 252, 0))

    def edit(self):
        running = True
        while running:
            self.screen.fill(CON.BLACK)
            self.map_surface.fill(CON.BLACK)
            self.bottom_surface.fill(CON.GRAY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 转换鼠标位置到地图格子坐标
                    x, y = pygame.mouse.get_pos()
                    # 检查是否点击了地图元素按钮
                    button_clicked = False
                    for button in self.tile_buttons:
                        if button.rect.collidepoint(x, y - CON.MAP_HEIGHT):
                            # 点击了地图元素按钮，更新选中状态
                            self.selected_tile_type = button.tile_type
                            button_clicked = True
                            break  # 找到点击的按钮后跳出循环

                    if self.save_button.rect.collidepoint(x, y - CON.MAP_HEIGHT):
                        self.save_map()
                        return CON.GAME_STATE_MAIN

                    if not button_clicked and self.map_surface.get_rect(topleft=(0, 0)).collidepoint(x, y):
                        # 没有点击按钮，但点击了地图区域，更新地图格子
                        grid_x = x // self.tile_size
                        grid_y = y // self.tile_size
                        if 0 <= grid_x < self.map.grid_x and 0 <= grid_y < self.map.grid_y:
                            self.map.tiles[grid_y][grid_x] = self.selected_tile_type

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return CON.GAME_STATE_MAIN

            # 在每次迭代末尾更新所有按钮的选中状态
            for button in self.tile_buttons:
                button.selected = (button.tile_type == self.selected_tile_type)

            self.draw_map()
            self.draw_ui()

            self.screen.blit(self.map_surface, (0, 0))
            self.screen.blit(self.bottom_surface, (0, CON.MAP_HEIGHT))
            pygame.display.flip()
