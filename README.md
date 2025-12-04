# 自定义计分板 / Custom Scoreboard

这是一个使用 Pygame 构建的简单、可自定义的体育比赛计分板。它可以通过文本文件轻松配置，并允许实时调整颜色。

This is a simple and customizable sports scoreboard built with Pygame. It's designed for easy configuration via text files and real-time color adjustments.

![Screenshot](https://raw.githubusercontent.com/linlinsunny/scoreboard/refs/heads/main/screenshot.png)
*(请将上面的链接替换为您的屏幕截图)*

---

## English

### Features
- **Dynamic Match Info**: Load match name and team names from `match.txt`.
- **Live Score Updates**: Easily add or subtract points for home and away teams.
- **Real-time Customization**: An in-app settings panel to change the color of all text elements.
- **Persistent Settings**: Color preferences are saved to and loaded from `config.ini`.
- **Custom Assets**: Supports custom fonts and background images.
- **Fullscreen Mode**: Toggle between windowed and fullscreen display.

### Requirements
- Python 3
- Pygame

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### How to Use

1.  **Configure the Match**:
    *   Edit `match.txt`. The first line is the match title, the second is the home team name, and the third is the away team name.
2.  **Customize Assets (Optional)**:
    *   Replace `bg.jpg` with your own background image.
    *   Replace `fonts.ttf` with your preferred font file.
3.  **Run the Application**:
    ```bash
    python scoreboard.py
    ```

### Keyboard Shortcuts

**In Scoreboard View:**
- `1`: Home Score +1
- `3`: Home Score +3
- `2`: Home Score -1
- `4`: Home Score -3
- `q`: Away Score +1
- `e`: Away Score +3
- `w`: Away Score -1
- `r`: Away Score -3
- `↑` (Up Arrow): Open the Color Settings panel.
- `f`: Toggle fullscreen mode.
- `ESC`: Quit the application.

**In Settings View:**
- `↑` / `↓`: Navigate between UI elements (e.g., Match Name, Team Name).
- `←` / `→`: Select the R, G, or B color component.
- `+` / `-`: Increase or decrease the value of the selected color component.
- `Enter`: Save changes and return to the scoreboard.

---

## 中文说明

### 功能特性
- **动态比赛信息**: 从 `match.txt` 文件加载比赛名称和队伍名称。
- **实时分数更新**: 方便地为主队和客队加减分数。
- **实时定制**: 内置设置面板，可以修改所有文本元素的颜色。
- **持久化配置**: 颜色偏好会被保存到 `config.ini` 文件中，并在下次启动时自动加载。
- **自定义资源**: 支持自定义字体和背景图片。
- **全屏模式**: 在窗口和全屏模式之间切换。

### 运行环境
- Python 3
- Pygame

### 安装步骤
1. 克隆仓库:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. 安装所需依赖:
   ```bash
   pip install -r requirements.txt
   ```

### 如何使用

1.  **配置比赛信息**:
    *   编辑 `match.txt` 文件。第一行是比赛标题，第二行是主队名称，第三行是客队名称。
2.  **自定义资源 (可选)**:
    *   用你自己的背景图片替换 `bg.jpg`。
    *   用你喜欢的字体文件替换 `fonts.ttf`。
3.  **运行程序**:
    ```bash
    python scoreboard.py
    ```

### 快捷键说明

**计分板界面:**
- `1`: 主队分数 +1
- `3`: 主队分数 +3
- `2`: 主队分数 -1
- `4`: 主队分数 -3
- `q`: 客队分数 +1
- `e`: 客队分数 +3
- `w`: 客队分数 -1
- `r`: 客队分数 -3
- `↑` (上箭头): 打开颜色设置面板。
- `f`: 切换全屏模式。
- `ESC`: 退出程序。

**设置界面:**
- `↑` / `↓`: 在不同界面元素（如比赛名称、队伍名称）之间切换。
- `←` / `→`: 选择 R、G、B 颜色分量。
- `+` / `-`: 增加或减少当前颜色分量的值。
- `Enter`: 保存修改并返回计分板。
