"""
PC时光记录器 - 全局配置
"""
import os
import sys

# ---- 应用信息 ----
APP_NAME = "PC时光记录器"
APP_VERSION = "1.0.0"
APP_ID = "PCTimeTracker"

# ---- 数据存储路径 ----
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(os.environ.get('LOCALAPPDATA', BASE_DIR), APP_ID)
os.makedirs(DATA_DIR, exist_ok=True)

# ---- 配色方案（深色简约） ----
COLOR_PRIMARY = "#4CAF50"
COLOR_PRIMARY_LIGHT = "#2E7D32"
COLOR_PRIMARY_DARK = "#1B5E20"
COLOR_BG = "#1E1E1E"
COLOR_CARD = "#252525"
COLOR_TEXT = "#E0E0E0"
COLOR_TEXT_SECONDARY = "#999999"
COLOR_BORDER = "#333333"

# ---- 时长统计 ----
IDLE_THRESHOLD_SECONDS = 2    # 无操作视为空闲

# ---- 久坐提醒 ----
DEFAULT_SIT_INTERVAL = 45       # 默认提醒间隔（分钟）
DEFAULT_REST_DURATION = 2       # 默认休息时长（分钟）

# ---- 窗口尺寸 ----
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 660
