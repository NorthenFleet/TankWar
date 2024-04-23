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
