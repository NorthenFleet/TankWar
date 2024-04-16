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
