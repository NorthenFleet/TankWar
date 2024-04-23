import configparser


class CONFIG:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

        # General Settings
        self.TICK_RATE = self.config.getint('GENERAL', 'TICK_RATE')
        self.SCREEN_WIDTH = self.config.getint('GENERAL', 'SCREEN_WIDTH')
        self.SCREEN_HEIGHT = self.config.getint('GENERAL', 'SCREEN_HEIGHT')

        # Map Settings
        self.MAP_WIDTH = self.config.getint('MAP', 'MAP_WIDTH')
        self.MAP_HEIGHT = self.config.getint('MAP', 'MAP_HEIGHT')
        self.GRID_SIZE = self.config.getint('MAP', 'GRID_SIZE')
        self.TileType_NONE = self.config.getint('MAP', 'TileType_NONE')
        self.TileType_FIELD = self.config.getint('MAP', 'TileType_FIELD')
        self.TileType_RIVER = self.config.getint('MAP', 'TileType_RIVER')
        self.TileType_BRICK_WALL = self.config.getint(
            'MAP', 'TileType_BRICK_WALL')
        self.TileType_STONE_WALL = self.config.getint(
            'MAP', 'TileType_STONE_WALL')
        self.TileType_SAND = self.config.getint('MAP', 'TileType_SAND')

        self.GAME_STATE_MAIN = self.config.getint(
            'GENERAL', 'GAME_STATE_MAIN')
        self.GAME_STATE_PLAYING = self.config.getint(
            'GENERAL', 'GAME_STATE_PLAYING')
        self.GAME_STATE_EDITING = self.config.getint(
            'GENERAL', 'GAME_STATE_EDITING')
        self.GAME_STATE_END = self.config.getint(
            'GENERAL', 'GAME_STATE_END')

        # Tank Settings
        self.TANK_SPEED = self.config.getint('TANK', 'MOVE_SPEED')
        self.TANK_LEVEL1 = self.config.getint('TANK', 'TANK_LEVEL1')
        self.TANK_LEVEL2 = self.config.getint('TANK', 'TANK_LEVEL2')
        self.TANK_LEVEL3 = self.config.getint('TANK', 'TANK_LEVEL3')

        # Bullet Settings
        self.BULLET_SPEED_MIN = self.config.getint(
            'BULLET', 'BULLET_SPEED_MIN')
        self.BULLET_SPEED_MID = self.config.getint(
            'BULLET', 'BULLET_SPEED_MID')
        self.BULLET_SPEED_MAX = self.config.getint(
            'BULLET', 'BULLET_SPEED_MAX')

        # Colors
        self.WHITE = tuple(
            map(int, self.config.get('COLORS', 'WHITE').split(',')))
        self.BLACK = tuple(
            map(int, self.config.get('COLORS', 'BLACK').split(',')))
        self.GREEN = tuple(
            map(int, self.config.get('COLORS', 'GREEN').split(',')))
        self.RED = tuple(
            map(int, self.config.get('COLORS', 'RED').split(',')))
        self.BLUE = tuple(
            map(int, self.config.get('COLORS', 'BLUE').split(',')))
        self.GRAY = tuple(
            map(int, self.config.get('COLORS', 'GRAY').split(',')))

    @staticmethod
    def parse_color(value):
        return tuple(map(int, value.split(',')))


def load_config(config_file):
    # 创建一个配置解析器对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read(config_file)

    # 从配置文件中提取配置项
    config_dict = {
        'screen_width': config.getint('GENERAL', 'SCREEN_WIDTH'),
        'screen_height': config.getint('GENERAL', 'SCREEN_HEIGHT'),
        'grid_size': config.getint('GENERAL', 'GRID_SIZE'),
        'tick_rate': config.getint('GENERAL', 'TICK_RATE'),
        'colors': {
            'WHITE': tuple(map(int, config.get('COLORS', 'WHITE').split(', '))),
            'BLACK': tuple(map(int, config.get('COLORS', 'BLACK').split(', '))),
            'GREEN': tuple(map(int, config.get('COLORS', 'GREEN').split(', '))),
            'RED': tuple(map(int, config.get('COLORS', 'RED').split(', '))),
            'BLUE': tuple(map(int, config.get('COLORS', 'BLUE').split(', '))),
            'GRAY': tuple(map(int, config.get('COLORS', 'GRAY').split(', '))),
            # ...其他颜色...
        }
        # ...其他配置项...
    }
    return config_dict


CON = CONFIG('config.ini')
import random
import pygame
import math
from config import CON


class Tank:
    def __init__(self, name, color, x, y):
        self.name = name
        self.color = color
        self.rect = pygame.Rect(x, y, CON.GRID_SIZE, CON.GRID_SIZE)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.bullets = []
        self.shoot_interval = 30
        self.shoot_current = 0
        self.current_level = CON.TANK_LEVEL1
        self.image = self.load_image()  # 加载坦克图片
        self.rect = self.image.get_rect(topleft=(x, y))  # 更新rect以匹配图片大小

    def load_image(self):
        # 根据坦克类型和级别构建图片文件名
        # image_name = f'tank_{self.tank_type}_level{self.level}.png'
        image_name = f'{self.name}.png'
        # 加载图片
        image = pygame.image.load(f'images/{image_name}').convert_alpha()
        image = pygame.transform.scale(image, (CON.GRID_SIZE, CON.GRID_SIZE))
        return image

    def get_rotation_angle(self):
        if self.direction == 'up':
            return 180  # 无需旋转
        elif self.direction == 'right':
            return 90  # 顺时针旋转90度
        elif self.direction == 'down':
            return 0  # 旋转180度
        elif self.direction == 'left':
            return 270  # 顺时针旋转270度
        return 0  # 默认不旋转

    def move(self, all_tanks, map_data):
        new_rect = self.rect.copy()
        if self.direction == 'up':
            new_rect.y -= CON.TANK_SPEED
        elif self.direction == 'down':
            new_rect.y += CON.TANK_SPEED
        elif self.direction == 'left':
            new_rect.x -= CON.TANK_SPEED
        elif self.direction == 'right':
            new_rect.x += CON.TANK_SPEED

        # 碰撞检测 - 其他坦克
        for tank in all_tanks:
            if tank != self and new_rect.colliderect(tank.rect):
                return

        # 碰撞检测 - 地图要素
        tile_x, tile_y = new_rect.centerx // CON.GRID_SIZE, new_rect.centery // CON.GRID_SIZE
        if map_data[tile_y][tile_x] in [CON.TileType_BRICK_WALL, CON.TileType_STONE_WALL, CON.TileType_RIVER]:
            return  # 如果新位置是障碍物，取消移动

        # 检查新位置是否在边界内
        if 0 <= new_rect.x < CON.MAP_WIDTH - CON.GRID_SIZE and 0 <= new_rect.y < CON.MAP_HEIGHT - CON.GRID_SIZE:
            self.rect = new_rect

    def shoot(self):
        if self.shoot_current >= self.shoot_interval or len(self.bullets) == 0:
            bullet_rect = pygame.Rect(
                self.rect.centerx - 5, self.rect.centery - 5, 10, 10)
            bullet = Bullet(self.direction, bullet_rect, self.current_level)
            self.bullets.append(bullet)
            self.shoot_current = 0

    def destroy(self, bullets):
        if len(bullets) > 0:
            for bullet in bullets:
                distance = math.sqrt((bullet.rect.centerx - self.rect.centerx)
                                     ** 2 + (bullet.rect.centery - self.rect.centery) ** 2)
                if distance < 20:
                    return True

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.b_outside():
                self.bullets.remove(bullet)

    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, self.rect)
        # 获取旋转角度
        angle = self.get_rotation_angle()
        # 旋转图片
        rotated_image = pygame.transform.rotate(self.image, angle)
        # 更新rect以确保图片居中
        new_rect = rotated_image.get_rect(center=self.rect.center)
        # 使用旋转后的图片和新的rect绘制坦克
        surface.blit(rotated_image, new_rect.topleft)
        self.draw_bullets(surface)

    def draw_bullets(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)

    def move_random(self, all_tanks, tiles):
        # 随机改变坦克的方向或者继续前进
        if random.randint(0, 3) == 0:  # 有大约25%的概率改变方向
            self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.move(all_tanks, tiles)

    def attempt_shoot(self):
        self.shoot_current += 1
        if self.shoot_current >= self.shoot_interval:
            if random.random() < 0.1:  # 有10%的概率进行射击
                self.shoot()


class Bullet:
    def __init__(self, direction, rect, tank_level):
        self.direction = direction
        self.rect = rect
        self.tank_level = tank_level
        self.speed = self.set_speed_by_level(tank_level)  # 根据坦克级别设置速度

    def set_speed_by_level(self, level):
        # 假设有三个级别的速度设置：1, 2, 3
        # 你可以根据实际需求调整这些值
        if level == CON.TANK_LEVEL1:
            return CON.BULLET_SPEED_MIN  # 级别1的速度
        elif level == CON.TANK_LEVEL2:
            return CON.BULLET_SPEED_MID  # 级别2的速度
        elif level == CON.TANK_LEVEL3:
            return CON.BULLET_SPEED_MAX  # 级别3的速度
        else:
            return CON.BULLET_SPEED_MIN  # 默认速度

    def move(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, CON.WHITE, self.rect)

    # 子弹出界，要删除子弹
    def b_outside(self):
        if self.rect.x < 0 or self.rect.x > CON.MAP_WIDTH or self.rect.y < 0 or self.rect.y > CON.MAP_HEIGHT:
            return True
        return False
import pygame
import os
from gameLogic import GameLogic
from map import Map, Button, MapEdit
from config import CON


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (CON.SCREEN_WIDTH, CON.SCREEN_HEIGHT))
        pygame.display.set_caption("Tank Battle")
        # 创建两个显示区域
        self.game_surface = pygame.Surface(
            (CON.MAP_WIDTH, CON.MAP_HEIGHT))
        self.bottom_surface = pygame.Surface(
            (CON.MAP_WIDTH, CON.SCREEN_HEIGHT - CON.MAP_HEIGHT))
        self.game_surface.fill((CON.BLACK))  # 设置顶部显示区域的颜色为红色
        self.bottom_surface.fill((CON.GRAY))  # 设置底部显示区域的颜色为蓝色

        self.clock = pygame.time.Clock()
        self.buttons_start = pygame.sprite.Group()
        self.buttons_game = pygame.sprite.Group()
        self.current_screen = CON.GAME_STATE_MAIN
        self.setup_buttons()
        self.map_names = None
        self.selected_map = "maps/level1.txt"
        self.map_edit = MapEdit(
            self.screen, self.game_surface,  self.bottom_surface)
        self.game_logic = GameLogic(
            self.screen, self.game_surface, self.bottom_surface)

        self.selected_map_index = None
        self.last_selected_map_index = -1
        self.font = pygame.font.SysFont(None, 24)
        self.list_area = pygame.Rect(300, 500, 500, 800)

    def get_map_names(self):
        """获取maps文件夹下所有的地图文件名"""
        map_dir = os.path.join(os.getcwd(), 'maps')
        return [f for f in os.listdir(map_dir) if os.path.isfile(os.path.join(map_dir, f))]

    def draw_list(self):
        start_y = self.list_area.top
        for index, map_name in enumerate(self.map_names):
            y = start_y + index * 30
            color = pygame.Color(
                'dodgerblue') if index == self.selected_map_index else pygame.Color('white')
            text_surf = self.font.render(map_name, True, color)
            self.screen.blit(text_surf, (self.list_area.left, y))

    def handle_list_click(self, pos):
        if self.list_area.collidepoint(pos):
            relative_y = pos[1] - self.list_area.top
            clicked_index = relative_y // 30
            if 0 <= clicked_index < len(self.map_names):
                # 只有在选中的地图发生变化时才更新
                if self.selected_map_index != clicked_index:
                    self.selected_map_index = clicked_index
                    selected_map = self.map_names[clicked_index]
                    self.load_selected_map(selected_map)

    def draw_dropdown(self):
        font = pygame.font.Font(None, 24)
        y = 20
        for map_name in self.map_names:
            text_surf = font.render(map_name, True, CON.WHITE)
            self.screen.blit(text_surf, (20, y))
            y += 30

    def setup_buttons(self):
        start_button = Button("START GAME", "START GAME", CON.GREEN,
                              CON.BLUE, 300, 200, 200, 50)
        edit_button = Button("EDIT MAP", "EDIT MAP",
                             CON.RED, CON.BLUE, 300, 300, 200, 50)
        back_button = Button("BACK", "BACK", CON.BLUE,
                             CON.BLUE, 300, 500, 200, 50)
        self.buttons_start.add(start_button, edit_button)
        self.buttons_game.add(back_button)

    def load_selected_map(self, map_name):
        if self.selected_map_index != self.last_selected_map_index:
            self.last_selected_map_index = self.selected_map_index
            map_path = os.path.join('maps', map_name)
            self.selected_map = map_path
            print(f"Map {map_name} loaded")

    def run(self):
        running = True
        while running:
            self.map_names = self.get_map_names()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_screen == CON.GAME_STATE_MAIN:
                        self.handle_list_click(event.pos)
                self.handle_mouse_click(event)

                self.draw_list()
            if self.selected_map_index is not None:
                selected_map = self.map_names[self.selected_map_index]
                selected_text = self.font.render(
                    f"Selected map: {selected_map}", True, pygame.Color('green'))
                self.screen.blit(selected_text, (50, 10))
                self.load_selected_map(selected_map)  # Load the selected map

            self.screen.fill(CON.BLACK)
            if self.current_screen == CON.GAME_STATE_MAIN:
                self.draw_list()
                self.draw_screen()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self.current_screen == CON.GAME_STATE_MAIN:
                self.handle_main_screen_click(pos)
            elif self.current_screen == CON.GAME_STATE_PLAYING:
                self.handle_game_screen_click(pos)

    def handle_main_screen_click(self, pos):
        clicked_buttons = [
            btn for btn in self.buttons_start if btn.rect.collidepoint(pos)]
        for btn in clicked_buttons:
            if btn.text == "START GAME":
                self.game_logic.load_map(self.selected_map)
                self.current_screen = self.game_logic.run()
            elif btn.text == "EDIT MAP":
                self.map_edit.load_map(self.selected_map)
                self.current_screen = self.map_edit.edit()

    def handle_game_screen_click(self, pos):
        clicked_buttons = [
            btn for btn in self.buttons_game if btn.rect.collidepoint(pos)]
        for btn in clicked_buttons:
            if btn.text == "返回":
                self.current_screen = CON.GAME_STATE_MAIN

    def draw_screen(self):
        if self.current_screen == CON.GAME_STATE_MAIN:
            self.buttons_start.draw(self.screen)
        elif self.current_screen == CON.GAME_STATE_PLAYING:
            self.buttons_game.draw(self.screen)
import pygame
import random
import sys
from entity import Tank, Bullet
from config import CON
from map import Map

# 定义坦克类


class GameLogic:
    def __init__(self, screen, game_surface, bottom_surface):
        self.screen = screen
        self.game_surface = game_surface
        self.bottom_surface = bottom_surface
        self.map = Map()
        self.map_tiles_images = self.load_tiles()
        self.clock = pygame.time.Clock()
        self.enemy_tanks = self.create_enemy_tanks()
        self.player_tank = Tank("player_tank", CON.GREEN, 100, 100)
        self.all_tanks = [self.player_tank] + self.enemy_tanks
        self.game_over = False
        self.time_count = 0
        self.player_tanks_count = 1

    def load_tiles(self):
        tiles_images = {
            CON.TileType_NONE: pygame.image.load('images/geo/None.png').convert_alpha(),
            CON.TileType_FIELD: pygame.image.load('images/geo/Field.png').convert_alpha(),
            CON.TileType_RIVER: pygame.image.load('images/geo/River.png').convert_alpha(),
            CON.TileType_SAND: pygame.image.load('images/geo/Sand.png').convert_alpha(),
            CON.TileType_BRICK_WALL: pygame.image.load('images/geo/Brick.png').convert_alpha(),
            CON.TileType_STONE_WALL: pygame.image.load(
                'images/geo/Stone.png').convert_alpha()
        }
        for tile_type, image in tiles_images.items():
            tiles_images[tile_type] = pygame.transform.scale(
                image, (CON.GRID_SIZE, CON.GRID_SIZE))
        return tiles_images

    def load_map(self, map):
        self.map.load_map(map)

    def create_enemy_tanks(self):
        enemy_tanks = []

        num_enemy_tanks = random.randint(1, 10)
        for _ in range(num_enemy_tanks):
            x = random.randint(0, CON.MAP_WIDTH - CON.GRID_SIZE)
            y = random.randint(0, CON.MAP_HEIGHT - CON.GRID_SIZE)
            enemy_tanks.append(Tank("enemy_tank", CON.RED, x, y))
        return enemy_tanks

    def run(self):
        running = True
        while running:
            self.screen.fill(CON.BLACK)
            self.game_surface.fill(CON.BLACK)
            self.bottom_surface.fill(CON.GRAY)
            self.render_map()
            enemy_bullets = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.player_tank.shoot()
                    elif event.key == pygame.K_ESCAPE:
                        return CON.GAME_STATE_MAIN

            if not self.game_over:
                self.handle_player_input()
                self.award()
                state = self.update_game_state()
                if state == CON.GAME_STATE_MAIN:
                    return CON.GAME_STATE_MAIN
                self.render_game_objects()

            self.draw_bottom_surface(self.bottom_surface)

            self.screen.blit(self.game_surface, (0, 0))
            self.screen.blit(self.bottom_surface, (0, CON.MAP_HEIGHT))

            pygame.display.flip()
            self.clock.tick(6)

    def draw_bottom_surface(self, surface):
        # # 在这里绘制辅助信息，如状态指示器、分数板等

        font = pygame.font.SysFont(None, 24)
        text_surfaces = [
            font.render(f"Count of Enemy Tank: {len(self.enemy_tanks)}",
                        True, (255, 255, 255)),
            font.render(f"Count of Player Tank: {self.player_tanks_count}",
                        True, (255, 255, 255)),
        ]
        for i, text_surface in enumerate(text_surfaces):
            surface.blit(
                text_surface, (10, 10 + i * 30))

    def get_tile_color(self, tile_type):
        """根据地图单元类型获取颜色。"""
        tile_colors = {
            0: CON.GRASS_COLOR,
            1: CON.WATER_COLOR,
            2: CON.WALL_COLOR,
            # 其他地图元素类型...
        }
        return tile_colors.get(tile_type, CON.DEFAULT_COLOR)  # 默认颜色

    def render_map(self):
        """遍历地图数据并在game_surface上绘制地图。"""
        for y, row in enumerate(self.map.tiles):
            for x, tile_type in enumerate(row):
                tile_image = self.map_tiles_images.get(tile_type)
                if tile_image:
                    self.game_surface.blit(
                        tile_image, (x * CON.GRID_SIZE, y * CON.GRID_SIZE))

    def award(self):
        self.time_count += 1
        if self.time_count > 15:
            # 产生奖励
            self.time_count = 0

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_tank.direction = 'up'
        elif keys[pygame.K_s]:
            self.player_tank.direction = 'down'
        elif keys[pygame.K_a]:
            self.player_tank.direction = 'left'
        elif keys[pygame.K_d]:
            self.player_tank.direction = 'right'

    def update_game_state(self):
        self.player_tank.move(self.all_tanks, self.map.tiles)
        self.player_tank.update_bullets()
        enemy_bullets = []

        for tank in self.enemy_tanks:
            tank.move_random(self.all_tanks, self.map.tiles)
            tank.update_bullets()
            tank.attempt_shoot()

            for bullet in tank.bullets:
                enemy_bullets.append(bullet)
        self.destroy_tanks()

        tanks_to_remove = []  # 用于存储需要删除的敌方坦克索引
        for i, tank in enumerate(self.enemy_tanks):
            if tank.destroy(self.player_tank.bullets):
                tanks_to_remove.append(i)
        # 删除需要删除的敌方坦克
        for index in reversed(tanks_to_remove):
            self.enemy_tanks.pop(index)

        if len(self.enemy_tanks) == 0:
            return CON.GAME_STATE_MAIN

        bmy_Died = self.player_tank.destroy(enemy_bullets)
        if bmy_Died == True:
            return CON.GAME_STATE_MAIN

    def render_game_objects(self):
        for tank in self.enemy_tanks:
            tank.draw(self.game_surface)
        self.player_tank.draw(self.game_surface)

    def destroy_tanks(self):
        bullets_to_remove = []  # 用于存储需要删除的子弹
        for i, tank in reversed(list(enumerate(self.enemy_tanks))):
            for bullet in self.player_tank.bullets:
                if tank.destroy([bullet]):
                    self.enemy_tanks.pop(i)
                    bullets_to_remove.append(bullet)
                    break  # 假设每颗子弹只能击毁一个坦克，击毁后跳出循环

        # 删除击中坦克的子弹
        for bullet in bullets_to_remove:
            if bullet in self.player_tank.bullets:
                self.player_tank.bullets.remove(bullet)

        if self.player_tank.destroy([bullet for tank in self.enemy_tanks for bullet in tank.bullets]):
            self.game_over = True
            print("Game Over!")

    def quit_game():
        pygame.quit()
        sys.exit()
from game import Game


if __name__ == "__main__":
    game = Game()
    game.run()
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
