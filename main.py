"""
PC时光记录器 - 程序入口
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from config.settings import APP_ID
from core.tracker import TimeTracker
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_ID)
    app.setQuitOnLastWindowClosed(False)

    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    # 启动时长追踪
    tracker = TimeTracker()

    # 创建主窗口，传入追踪器
    window = MainWindow(tracker)
    window.show()

    # 系统托盘
    tray = TrayIcon(window)
    tray.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
