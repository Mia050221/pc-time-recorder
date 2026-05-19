"""
PC时光记录器 - 系统托盘图标
"""
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QFont
from config.settings import APP_NAME, COLOR_PRIMARY


class TrayIcon(QSystemTrayIcon):
    """系统托盘图标，含右键菜单"""

    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window

        # 生成一个简单的绿色圆形图标（后续可替换为自定义图标）
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(COLOR_PRIMARY))
        painter.setPen(QColor(COLOR_PRIMARY))
        painter.drawEllipse(2, 2, 28, 28)
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(pixmap.rect(), 0x0084, "T")
        painter.end()

        self.setIcon(QIcon(pixmap))
        self.setToolTip(APP_NAME)

        # 右键菜单
        menu = QMenu()
        action_show = QAction("显示主窗口")
        action_show.triggered.connect(self._show_main_window)
        menu.addAction(action_show)

        menu.addSeparator()

        action_quit = QAction("退出")
        action_quit.triggered.connect(self._quit_app)
        menu.addAction(action_quit)

        self.setContextMenu(menu)

        # 双击托盘图标 → 显示主窗口
        self.activated.connect(self._on_activated)

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self._show_main_window()

    def _show_main_window(self):
        self._main_window.show()
        self._main_window.raise_()
        self._main_window.activateWindow()

    def _quit_app(self):
        from PyQt5.QtWidgets import QApplication
        self._main_window.closeEvent = lambda e: None  # 移除拦截，允许真正关闭
        self._main_window.close()
        QApplication.quit()
