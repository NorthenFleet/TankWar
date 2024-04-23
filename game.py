import pygame
import os
from gameLogic import GameLogic
from map import Map, Button, MapEdit
from config import CON
from render import Render


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
        render = Render(self.screen, self.game_surface, self.bottom_surface)
        self.game_logic = GameLogic(render)
        
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
