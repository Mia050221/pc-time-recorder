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

# ---- 配色方案（浅色简约） ----
COLOR_PRIMARY = "#4CAF50"
COLOR_PRIMARY_LIGHT = "#66BB6A"
COLOR_PRIMARY_DARK = "#388E3C"
COLOR_BG = "#F8F9FA"
COLOR_CARD = "#FFFFFF"
COLOR_TEXT = "#212529"
COLOR_TEXT_SECONDARY = "#6C757D"
COLOR_BORDER = "#DEE2E6"

# ---- 时长统计 ----
IDLE_THRESHOLD_SECONDS = 2    # 无操作视为空闲

# ---- 久坐提醒 ----
DEFAULT_SIT_INTERVAL = 45       # 默认提醒间隔（分钟）
DEFAULT_REST_DURATION = 2       # 默认休息时长（分钟）

# ---- 窗口尺寸 ----
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 660
