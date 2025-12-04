import pygame
import sys
import os
import configparser

# --- 辅助函数：获取资源路径 ---
def resource_path(relative_path):
    """ 获取资源的绝对路径，适用于开发环境和PyInstaller打包环境 """
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件，则基路径是可执行文件所在的目录
        base_path = os.path.dirname(sys.executable)
    else:
        # 如果是直接运行的脚本，则基路径是脚本所在的目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

# --- 1. 配置和初始化 ---
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
CAPTION = "自定义计分板 (布局调整)"

# 颜色常量
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (150, 150, 150)
COLOR_YELLOW = (255, 255, 0)

# 文件名
MATCH_INFO_FILE = 'match.txt'
BACKGROUND_IMAGE_FILE = 'bg.jpg'
FONT_PATH_USER = 'fonts.ttf'
CONFIG_FILE = 'config.ini'

# --- 2. 状态管理 ---
STATE_SCOREBOARD = 0
STATE_SETTINGS = 1
current_state = STATE_SCOREBOARD

# 当前正在编辑的颜色元素和RGB分量
editable_elements = [
    ("比赛名称", "match_name"),
    ("主队名称", "team_name"),
    ("客队名称", "team_name"),
    ("主队分数", "home_score"),
    ("客队分数", "away_score")
]
editable_components = ['R', 'G', 'B']
setting_element_index = 0
setting_component_index = 0

# --- 3. 配置加载和保存 ---
def load_config():
    """从config.ini加载颜色配置"""
    config = configparser.ConfigParser()
    config.read(resource_path(CONFIG_FILE), encoding='utf-8')

    colors = {}
    try:
        section = config['Colors']
        for key, name in editable_elements:
            if name == "team_name" and key == "客队名称": continue

            r = section.getint(f'{name}_r', 255)
            g = section.getint(f'{name}_g', 255)
            b = section.getint(f'{name}_b', 255)
            colors[name] = (r, g, b)

        colors['away_score'] = colors.get('away_score', (255, 255, 255))
        colors['home_score'] = colors.get('home_score', (255, 255, 255))

    except (configparser.NoSectionError, KeyError, ValueError):
        # 默认颜色
        colors['match_name'] = (255, 255, 255)
        colors['team_name'] = (255, 255, 0)
        colors['home_score'] = (255, 255, 255)
        colors['away_score'] = (255, 255, 255)

    return colors

def save_config(colors):
    """将颜色配置保存到config.ini"""
    config = configparser.ConfigParser()
    config['Colors'] = {}
    for name, color_tuple in colors.items():
        if name in ['away_score', 'home_score', 'match_name', 'team_name']:
            config['Colors'][f'{name}_r'] = str(color_tuple[0])
            config['Colors'][f'{name}_g'] = str(color_tuple[1])
            config['Colors'][f'{name}_b'] = str(color_tuple[2])

    with open(resource_path(CONFIG_FILE), 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    print("颜色配置已保存.")

# 初始化颜色
CUSTOM_COLORS = load_config()

# --- 4. 比赛信息读取函数 (保持不变) ---
def load_match_info(filename):
    """从match.txt文件中读取比赛信息"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

            if len(lines) >= 3:
                match_name = lines[0]
                home_team_name = lines[1]
                away_team_name = lines[2]
                return match_name, home_team_name, away_team_name
            else:
                return "2025年春季联赛", "主队", "客队"
    except Exception:
        return "2025年春季联赛", "主队", "客队"

# --- 5. 初始化 Pygame ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

match_name, home_team_name, away_team_name = load_match_info(resource_path(MATCH_INFO_FILE))

try:
    font_path = resource_path(FONT_PATH_USER)
    # *** 比赛名称字体大小翻倍: 90 ***
    font_team_name = pygame.font.Font(font_path, 80)
    font_match_name = pygame.font.Font(font_path, 90)
    font_score_large = pygame.font.Font(font_path, 400)
    font_settings = pygame.font.Font(font_path, 30)
except Exception:
    font_team_name = pygame.font.SysFont(None, 80)
    font_match_name = pygame.font.SysFont(None, 90)
    font_score_large = pygame.font.SysFont(None, 400)
    font_settings = pygame.font.SysFont(None, 30)


try:
    background_image = pygame.image.load(resource_path(BACKGROUND_IMAGE_FILE))
    background_image = background_image.convert()
except Exception:
    background_image = None

# --- 6. 游戏状态变量 (保持不变) ---
home_score_main = 1
away_score_main = 0
is_fullscreen = False

# --- 7. 绘图函数 ---
def draw_scoreboard(screen, width, height):
    """绘制主计分板界面"""

    if background_image:
        bg_scaled = pygame.transform.scale(background_image, (width, height))
        screen.blit(bg_scaled, (0, 0))
    else:
        screen.fill(COLOR_BLACK)

    center_x = width // 2

    # *** 调整垂直坐标：给比赛名称留出更多空间 ***
    top_y = height * 0.03       # 比赛名称位置稍微下移
    team_name_y = height * 0.25 # 队名位置下移
    score_y = height * 0.55     # 分数位置下移

    # 比赛名称 (使用 90 号字体)
    text_match = font_match_name.render(match_name, True, CUSTOM_COLORS.get('match_name', COLOR_WHITE))
    screen.blit(text_match, (center_x - text_match.get_width() // 2, top_y))

    # 主队名称
    text_home_name = font_team_name.render(home_team_name, True, CUSTOM_COLORS.get('team_name', COLOR_YELLOW))
    home_name_x = width * 0.25 - text_home_name.get_width() // 2
    screen.blit(text_home_name, (home_name_x, team_name_y))

    # 客队名称
    text_away_name = font_team_name.render(away_team_name, True, CUSTOM_COLORS.get('team_name', COLOR_YELLOW))
    away_name_x = width * 0.75 - text_away_name.get_width() // 2
    screen.blit(text_away_name, (away_name_x, team_name_y))

    # 主队分数
    text_home_score = font_score_large.render(str(home_score_main), True, CUSTOM_COLORS.get('home_score', COLOR_WHITE))
    home_score_x = width * 0.25 - text_home_score.get_width() // 2
    home_score_y = score_y - text_home_score.get_height() // 2
    screen.blit(text_home_score, (home_score_x, home_score_y))

    # 客队分数
    text_away_score = font_score_large.render(str(away_score_main), True, CUSTOM_COLORS.get('away_score', COLOR_WHITE))
    away_score_x = width * 0.75 - text_away_score.get_width() // 2
    away_score_y = score_y - text_away_score.get_height() // 2
    screen.blit(text_away_score, (away_score_x, away_score_y))

    # 提示
    text_hint = font_settings.render("↑", True, COLOR_GRAY)
    screen.blit(text_hint, (10, height - text_hint.get_height() - 10))

def draw_settings(screen, width, height):
    """绘制颜色设置界面 (保持不变)"""
    screen.fill(COLOR_BLACK)

    # 标题使用新的大字体
    title = font_match_name.render("颜色设置界面", True, COLOR_WHITE)
    screen.blit(title, (width // 2 - title.get_width() // 2, 30))

    y_start = 150
    line_height = 80

    display_elements = [e for i, e in enumerate(editable_elements) if not (e[1] == "team_name" and i > 1)]

    for i, (name, key) in enumerate(display_elements):

        is_selected = (i == setting_element_index)
        color = CUSTOM_COLORS[key]

        text_name = font_settings.render(f"{name}:", True, COLOR_WHITE if not is_selected else COLOR_YELLOW)
        screen.blit(text_name, (50, y_start + i * line_height))

        preview_rect = pygame.Rect(width // 2 - 200, y_start + i * line_height, 50, 30)
        pygame.draw.rect(screen, color, preview_rect)
        pygame.draw.rect(screen, COLOR_WHITE, preview_rect, 2)

        if is_selected:
            current_color = list(CUSTOM_COLORS[key])
            for j in range(3):
                component_text = editable_components[j]
                component_val = current_color[j]

                is_comp_selected = (j == setting_component_index)

                comp_color = COLOR_WHITE if not is_comp_selected else (255, 100, 100)

                text_comp = font_settings.render(f"{component_text}: {component_val:03d}", True, comp_color)
                screen.blit(text_comp, (width // 2 + 50 + j * 150, y_start + i * line_height))

    hint_text = "↑/↓ 切换元素 | ←/→ 切换 R/G/B | +/- 调整值 | Enter 返回并保存"
    text_hint = font_settings.render(hint_text, True, COLOR_GRAY)
    screen.blit(text_hint, (width // 2 - text_hint.get_width() // 2, height - 50))


# --- 8. 主循环 (控制逻辑保持不变) ---
running = True
while running:

    current_width, current_height = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            # --- 通用控制 ---
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_f:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)


            if current_state == STATE_SCOREBOARD:
                # --- 计分板状态下的控制 ---
                if event.key == pygame.K_UP:
                    current_state = STATE_SETTINGS

                elif event.key == pygame.K_1:
                    home_score_main += 1
                elif event.key == pygame.K_3:
                    home_score_main += 3
                elif event.key == pygame.K_2:
                    home_score_main = max(0, home_score_main - 1)
                elif event.key == pygame.K_4:
                    home_score_main = max(0, home_score_main - 3)

                elif event.key == pygame.K_q:
                    away_score_main += 1
                elif event.key == pygame.K_e:
                    away_score_main += 3
                elif event.key == pygame.K_w:
                    away_score_main = max(0, away_score_main - 1)
                elif event.key == pygame.K_r:
                    away_score_main = max(0, away_score_main - 3)

            elif current_state == STATE_SETTINGS:
                # --- 设置状态下的控制 ---

                if event.key == pygame.K_RETURN:
                    save_config(CUSTOM_COLORS)
                    current_state = STATE_SCOREBOARD

                elif event.key == pygame.K_UP:
                    setting_element_index = (setting_element_index - 1) % len(editable_elements)
                    if setting_element_index == 2:
                        setting_element_index = 1
                elif event.key == pygame.K_DOWN:
                    setting_element_index = (setting_element_index + 1) % len(editable_elements)
                    if setting_element_index == 2:
                        setting_element_index = 3

                elif event.key == pygame.K_LEFT:
                    setting_component_index = (setting_component_index - 1) % len(editable_components)
                elif event.key == pygame.K_RIGHT:
                    setting_component_index = (setting_component_index + 1) % len(editable_components)

                _, current_element_key = editable_elements[setting_element_index]

                is_plus = (event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS)
                is_minus = (event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS)

                if is_plus or is_minus:
                    change = 10 if is_plus else -10

                    current_color_list = list(CUSTOM_COLORS[current_element_key])
                    current_val = current_color_list[setting_component_index]

                    new_val = max(0, min(255, current_val + change))
                    current_color_list[setting_component_index] = new_val

                    CUSTOM_COLORS[current_element_key] = tuple(current_color_list)

                    if current_element_key == 'team_name':
                        CUSTOM_COLORS['team_name'] = tuple(current_color_list)


    # 绘制
    if current_state == STATE_SCOREBOARD:
        draw_scoreboard(screen, current_width, current_height)
    elif current_state == STATE_SETTINGS:
        draw_settings(screen, current_width, current_height)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
