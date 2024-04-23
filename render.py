from config import CON
import pygame
from entity import Tank
from gameLogic import GameLogic


class Render:
    def __init__(self, screen, game_surface, bottom_surface):
        self.screen = screen
        self.game_surface = game_surface
        self.bottom_surface = bottom_surface
        self.map_tiles_images = self.load_tiles()
        self.player_tank_image = self.load_image("player_tank")  # 加载坦克图片
        self.enemt_tank_image = self.load_image("enemy_tank")  # 加载坦克图片

    def display(self, game_over, state, map):
        self.screen.fill(CON.BLACK)
        self.screen.blit(self.game_surface, (0, 0))
        self.screen.blit(self.bottom_surface, (0, CON.MAP_HEIGHT))
        self.game_surface.fill(CON.BLACK)
        self.bottom_surface.fill(CON.GRAY)
        # 显示地图
        self.render_map(map)
        # 显示坦克
        for tank in state.enemy_tanks:
            self.tank_draw(tank, self.enemt_tank_image)
        self.tank_draw(state.player_tanks, self.player_tank_image)

        # 显示计分板
        self.draw_bottom_surface(self.bottom_surface, state)

        pygame.display.flip()

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

    def render_map(self, map):
        """遍历地图数据并在game_surface上绘制地图。"""
        for y, row in enumerate(map.tiles):
            for x, tile_type in enumerate(row):
                tile_image = self.map_tiles_images.get(tile_type)
                if tile_image:
                    self.game_surface.blit(
                        tile_image, (x * CON.GRID_SIZE, y * CON.GRID_SIZE))

    def load_image(self, name):
        # 根据坦克类型和级别构建图片文件名
        # image_name = f'tank_{self.tank_type}_level{self.level}.png'
        image_name = f'{name}.png'
        # 加载图片
        image = pygame.image.load(f'images/{image_name}').convert_alpha()
        image = pygame.transform.scale(image, (CON.GRID_SIZE, CON.GRID_SIZE))
        return image

    def draw_bottom_surface(self, surface, state):
        # # 在这里绘制辅助信息，如状态指示器、分数板等

        font = pygame.font.SysFont(None, 24)
        text_surfaces = [
            font.render(f"Count of Enemy Tank: {len(state.enemy_tanks)}",
                        True, (255, 255, 255)),
            font.render(f"Count of Player Tank: {1}",  # state.player_tanks_counts
                        True, (255, 255, 255)),
        ]
        for i, text_surface in enumerate(text_surfaces):
            surface.blit(
                text_surface, (10, 10 + i * 30))

    def tank_draw(self, tank, image):
        # pygame.draw.rect(surface, self.color, self.rect)
        # # 获取旋转角度
        if tank.direction == 'up':
            angle = 180
        elif tank.direction == 'down':
            angle = 0
        elif tank.direction == 'left':
            angle = 270
        elif tank.direction == 'right':
            angle = 90

        # 旋转图片
        rotated_image = pygame.transform.rotate(image, angle)
        # 更新rect以确保图片居中
        new_rect = rotated_image.get_rect(center=tank.rect.center)
        # 使用旋转后的图片和新的rect绘制坦克
        # self.game_surface.fill(CON.BLACK)
        self.game_surface.blit(rotated_image, new_rect.topleft)
        for bullet in tank.bullets:
            pygame.draw.rect(self.game_surface, CON.WHITE, bullet.rect)
