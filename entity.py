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
