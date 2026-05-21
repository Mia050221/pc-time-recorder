from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint


class _ReminderDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("休息提醒")
        self.setFixedSize(420, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        GREEN = "#4CAF50"
        GREEN_DARK = "#388E3C"
        BG = "#FFFFFF"
        WHITE = "#333333"
        GRAY = "#888888"

        self.setStyleSheet(f"background-color: {BG};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title_bar = QFrame()
        title_bar.setFixedHeight(42)
        title_bar.setStyleSheet(f"background-color: {GREEN};")
        title_bar.installEventFilter(self)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 12, 0)
        title_layout.setAlignment(Qt.AlignVCenter)
        title_layout.addStretch()

        close_btn = QLabel("✕")
        close_btn.setFixedSize(36, 36)
        close_btn.setAlignment(Qt.AlignCenter)
        close_btn.setStyleSheet("color: white; font-size: 18px; background: transparent;")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.mousePressEvent = lambda e: self.reject()
        title_layout.addWidget(close_btn)

        layout.addWidget(title_bar)

        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #E0E0E0;")
        layout.addWidget(line)

        body = QVBoxLayout()
        body.setAlignment(Qt.AlignCenter)

        body.addSpacing(28)

        icon = QLabel("◷")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet(f"color: {GRAY}; font-size: 52px; background: transparent;")
        body.addWidget(icon)

        body.addSpacing(14)

        title = QLabel("该休息一下啦")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {WHITE}; font-size: 18px; font-weight: bold; background: transparent;")
        body.addWidget(title)

        body.addSpacing(10)

        subtitle = QLabel("站起来活动活动，保护颈椎和眼睛哦~")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {GRAY}; font-size: 13px; background: transparent;")
        body.addWidget(subtitle)

        body.addSpacing(30)

        btn = QPushButton("知道了")
        btn.setFixedSize(140, 44)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {GREEN};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-family: "Microsoft YaHei";
            }}
            QPushButton:hover {{
                background-color: {GREEN_DARK};
            }}
        """)
        btn.clicked.connect(self.accept)

        btn_wrap = QHBoxLayout()
        btn_wrap.setAlignment(Qt.AlignCenter)
        btn_wrap.addWidget(btn)
        body.addLayout(btn_wrap)
        body.addStretch()

        layout.addLayout(body)
        self._drag_pos = None

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress and event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            return True
        if event.type() == event.MouseMove and self._drag_pos is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            return True
        if event.type() == event.MouseButtonRelease:
            self._drag_pos = None
            return True
        return super().eventFilter(obj, event)


def show_reminder():
    dlg = _ReminderDialog()
    dlg.exec_()
