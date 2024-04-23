import pygame
import random
import math

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
WATER_BLUE = (0, 191, 255)

# 定义屏幕大小和格子大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20

#定义墙的大小
GRIDgi_SIZE = 20

# 定义坦克类
class Tank:
    def __init__(self, color, x, y):
        self.color = color
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.bullets = []
        self.shoot_interval = 30
        self.shoot_current = 0

    def move(self):
        new_rect = self.rect.copy()
        if self.direction == 'up':
            new_rect.y -= GRID_SIZE
        elif self.direction == 'down':
            new_rect.y += GRID_SIZE
        elif self.direction == 'left':
            new_rect.x -= GRID_SIZE
        elif self.direction == 'right':
            new_rect.x += GRID_SIZE

        # 检查新位置是否在边界内
        if 0 <= new_rect.x < SCREEN_WIDTH - GRID_SIZE and 0 <= new_rect.y < SCREEN_HEIGHT - GRID_SIZE:
            self.rect = new_rect

    def shoot(self):
        if self.shoot_current >= self.shoot_interval or len(self.bullets) == 0:
            bullet_rect = pygame.Rect(self.rect.centerx - 5, self.rect.centery - 5, 10, 10)
            bullet = Bullet(self.direction, bullet_rect)
            self.bullets.append(bullet)
            self.shoot_current = 0
        
    def destroy(self, bullets):
        if len(bullets) > 0:
            for bullet in bullets:
                distance = math.sqrt((bullet.rect.centerx - self.rect.centerx) ** 2 + (bullet.rect.centery - self.rect.centery) ** 2)
                if distance < 6:
                    return True

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.b_outside():
                self.bullets.remove(bullet)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        self.draw_bullets(surface)

    def draw_bullets(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)

class Bullet:
    def __init__(self, direction, rect):
        self.direction = direction
        self.rect = rect

    def move(self):
        if self.direction == 'up':
            self.rect.y -= 10
        elif self.direction == 'down':
            self.rect.y += 10
        elif self.direction == 'left':
            self.rect.x -= 10
        elif self.direction == 'right':
            self.rect.x += 10

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

    # 子弹出界，要删除子弹
    def b_outside(self):
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            return True
        return False
    
#地图
class Map:
    def __init__(self, x, y, wall_type):
        self.x = x
        self.y = y
        self.wall_type = wall_type
        self.health = 100  # 墙的初始健康值

    def damage(self, damage_amount):
        self.health -= damage_amount
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        # 在这里实现墙被摧毁后的逻辑
        pass

        

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# 创建敌方坦克
enemy_tanks = []
num_enemy_tanks = random.randint(1, 1)
for _ in range(num_enemy_tanks):
    x = random.randint(0, SCREEN_WIDTH - GRID_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - GRID_SIZE)
    enemy_tanks.append(Tank(RED, x, y))

# 创建玩家坦克
player_tank = Tank(GREEN, 100, 100)

running = True
game_over = False

while running:
    screen.fill(BLACK)
    enemy_bullets = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                player_tank.shoot()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_tank.direction = 'up'
        elif keys[pygame.K_s]:
            player_tank.direction = 'down'
        elif keys[pygame.K_a]:
            player_tank.direction = 'left'
        elif keys[pygame.K_d]:
            player_tank.direction = 'right'

        player_tank.move()
        player_tank.update_bullets()

        for tank in enemy_tanks:
            for bullet in tank.bullets:
                enemy_bullets.append(bullet)
            tank.direction = random.choice(['up', 'down', 'left', 'right'])
            tank.move()
            tank.update_bullets()

            tank.shoot_current += 1
            if random.random() < 0.1:  # 这里的0.1可以调整为适合你游戏节奏的值
                tank.shoot()
            
    #——————————————敌方坦克毁伤计算————————————————#
    tanks_to_remove = []  # 用于存储需要删除的敌方坦克索引

    for i, tank in enumerate(enemy_tanks):
        if tank.destroy(player_tank.bullets):
            tanks_to_remove.append(i)

    # 删除需要删除的敌方坦克
    for index in reversed(tanks_to_remove):
        enemy_tanks.pop(index)
    
    for tank in enemy_tanks:
        tank.draw(screen)

    if len(enemy_tanks) == 0:
        pygame.quit()
        break

    #——————————————我方坦克毁伤计算————————————————#
    player_tank.shoot_current += 1
    bmy_Died = player_tank.destroy(enemy_bullets)
    if bmy_Died == True:
        pygame.quit()
        break
    player_tank.draw(screen)


    pygame.display.flip()
    clock.tick(5)

pygame.quit()
