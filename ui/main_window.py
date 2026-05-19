"""
PC时光记录器 - 主窗口UI
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget, QFrame, QPushButton, QCheckBox, QSpinBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QSizePolicy, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from config.settings import (
    APP_NAME, APP_VERSION,
    COLOR_PRIMARY, COLOR_PRIMARY_LIGHT, COLOR_PRIMARY_DARK,
    COLOR_BG, COLOR_CARD, COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_BORDER,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    DEFAULT_SIT_INTERVAL
)

FONT = '"Microsoft YaHei"'


def _fmt_seconds(total_seconds: int) -> str:
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    return f"{h} 小时 {m} 分钟"


def _top_app_name(app_usage: dict) -> str:
    if not app_usage:
        return "—"
    return max(app_usage, key=app_usage.get)


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, tracker):
        super().__init__()
        self._tracker = tracker
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLOR_BG};
                font-family: {FONT};
            }}
            QToolTip {{
                background-color: #2A2A2A;
                color: {COLOR_TEXT};
                border: 1px solid {COLOR_BORDER};
                padding: 4px;
                font-family: {FONT};
            }}
        """)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(self._tab_style())
        self.tabs.addTab(self._build_overview_tab(), "  📊 时长统计  ")
        self.tabs.addTab(self._build_app_ranking_tab(), "  📱 应用排行  ")
        self.tabs.addTab(self._build_history_tab(), "  📅 历史记录  ")
        self.tabs.addTab(self._build_settings_tab(), "  ⚙️ 设置  ")
        root.addWidget(self.tabs, 1)
        root.addWidget(self._build_footer())

        self._tracker.remind_triggered.connect(self._show_reminder)

    # ==================== 顶部标题栏 ====================
    def _build_header(self) -> QFrame:
        frame = QFrame()
        frame.setFixedHeight(56)
        frame.setStyleSheet(
            f"background-color: {COLOR_PRIMARY}; border: none;"
        )
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setAlignment(Qt.AlignVCenter)

        logo = QLabel("◷")
        logo.setFixedWidth(40)
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet(
            f"color: white; font-size: 24px; background: transparent; font-family: {FONT};"
        )
        layout.addWidget(logo)

        title = QLabel(APP_NAME)
        title.setStyleSheet(
            f"color: white; font-size: 18px; font-weight: bold; background: transparent; font-family: {FONT};"
        )
        layout.addWidget(title)

        layout.addStretch()

        status_dot = QLabel("●")
        status_dot.setStyleSheet(
            "color: #A5D6A7; font-size: 10px; background: transparent;"
        )
        layout.addWidget(status_dot)

        layout.addSpacing(4)

        status_text = QLabel("运行中")
        status_text.setStyleSheet(
            "color: #A5D6A7; font-size: 13px; background: transparent; font-family: {FONT};"
        )
        layout.addWidget(status_text)

        layout.addSpacing(20)

        ver = QLabel(f"v{APP_VERSION}")
        ver.setStyleSheet(
            f"color: rgba(255,255,255,0.7); font-size: 13px; background: transparent; font-family: {FONT};"
        )
        layout.addWidget(ver)

        return frame

    # ==================== 底部状态栏 ====================
    def _build_footer(self) -> QFrame:
        frame = QFrame()
        frame.setFixedHeight(46)
        frame.setStyleSheet(
            f"background-color: {COLOR_CARD}; "
            f"border-top: 1px solid {COLOR_BORDER};"
        )
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setAlignment(Qt.AlignVCenter)

        status = QLabel("🟢  正在记录中…")
        status.setStyleSheet(
            f"color: {COLOR_PRIMARY}; font-size: 13px; font-family: {FONT};"
        )
        layout.addWidget(status)

        layout.addStretch()

        btn_settings = QPushButton("  设置  ")
        btn_settings.setCursor(Qt.PointingHandCursor)
        btn_settings.setMinimumWidth(72)
        btn_settings.setStyleSheet(self._footer_btn_style())
        btn_settings.clicked.connect(lambda: self.tabs.setCurrentIndex(3))
        layout.addWidget(btn_settings)

        layout.addSpacing(8)

        btn_quit = QPushButton("  退出程序  ")
        btn_quit.setCursor(Qt.PointingHandCursor)
        btn_quit.setMinimumWidth(96)
        btn_quit.setStyleSheet(self._footer_btn_style())
        btn_quit.clicked.connect(self._quit_app)
        layout.addWidget(btn_quit)

        return frame

    def _footer_btn_style(self) -> str:
        return f"""
            QPushButton {{
                background: transparent;
                color: {COLOR_TEXT_SECONDARY};
                border: none;
                padding: 8px 16px;
                font-size: 13px;
                font-family: {FONT};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_PRIMARY_LIGHT};
                color: {COLOR_TEXT};
            }}
        """

    # ==================== 时长统计页 ====================
    def _build_overview_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(20)

        layout.addWidget(self._section_label("今日使用概览"))

        cards = QHBoxLayout()
        cards.setSpacing(16)

        card1, self._label_uptime = self._stat_card("🖥  今日开机", "0 小时 0 分钟", "自今日首次开机起算")
        card2, self._label_active = self._stat_card("⌨️  今日活跃", "0 小时 0 分钟", "排除锁屏/待机时间")
        card3, self._label_week = self._stat_card("📆  本周总计", "0 小时 0 分钟", "周一 00:00 至今")
        card4, self._label_month = self._stat_card("📅  本月总计", "0 小时 0 分钟", "本月 1 日 00:00 至今")

        cards.addWidget(card1)
        cards.addWidget(card2)
        cards.addWidget(card3)
        cards.addWidget(card4)
        layout.addLayout(cards)

        layout.addWidget(self._divider())
        layout.addWidget(self._section_label("当前状态"))

        status_panel = QFrame()
        status_panel.setStyleSheet(
            f"background-color: {COLOR_CARD}; border: 1px solid {COLOR_BORDER}; "
            f"border-radius: 8px;"
        )
        status_panel_layout = QHBoxLayout(status_panel)
        status_panel_layout.setContentsMargins(24, 18, 24, 18)
        status_panel_layout.setSpacing(16)

        status_icon = QLabel("●")
        status_icon.setFixedWidth(48)
        status_icon.setAlignment(Qt.AlignCenter)
        status_icon.setStyleSheet(
            f"color: {COLOR_PRIMARY}; font-size: 36px; background: transparent;"
        )
        status_panel_layout.addWidget(status_icon)

        self._status_title = QLabel("活跃中")
        self._status_title.setStyleSheet(
            f"color: {COLOR_TEXT}; font-size: 16px; font-weight: bold; font-family: {FONT};"
        )
        status_panel_layout.addWidget(self._status_title)

        status_panel_layout.addStretch()

        status_desc = QLabel("鼠标或键盘有操作时视为活跃状态")
        status_desc.setWordWrap(True)
        status_desc.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 13px; font-family: {FONT};"
        )
        status_panel_layout.addWidget(status_desc)

        layout.addWidget(status_panel)
        layout.addStretch()

        # 绑定追踪器信号 → 实时更新卡片
        self._tracker.today_uptime_changed.connect(lambda v: self._label_uptime.setText(v))
        self._tracker.today_active_changed.connect(lambda v: self._label_active.setText(v))
        self._tracker.week_total_changed.connect(lambda v: self._label_week.setText(v))
        self._tracker.month_total_changed.connect(lambda v: self._label_month.setText(v))
        self._tracker.status_changed.connect(lambda v: self._status_title.setText(v))

        return page

    def _stat_card(self, title: str, value: str, hint: str) -> QFrame:
        card = QFrame()
        card.setMinimumHeight(135)
        card.setStyleSheet(
            f"background-color: {COLOR_CARD}; "
            f"border: 1px solid {COLOR_BORDER}; "
            f"border-radius: 10px;"
        )
        inner = QVBoxLayout(card)
        inner.setContentsMargins(14, 14, 14, 14)
        inner.setSpacing(6)

        label_title = QLabel(title)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setWordWrap(True)
        label_title.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 13px; font-family: {FONT};"
        )
        inner.addWidget(label_title)

        label_value = QLabel(value)
        label_value.setAlignment(Qt.AlignCenter)
        label_value.setWordWrap(True)
        label_value.setStyleSheet(
            f"color: {COLOR_PRIMARY}; font-size: 18px; font-weight: bold; font-family: {FONT};"
        )
        inner.addWidget(label_value)

        label_hint = QLabel(hint)
        label_hint.setAlignment(Qt.AlignCenter)
        label_hint.setWordWrap(True)
        label_hint.setStyleSheet(
            f"color: #666666; font-size: 12px; font-family: {FONT};"
        )
        inner.addWidget(label_hint)

        return card, label_value

    # ==================== 应用排行页 ====================
    def _build_app_ranking_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(16)

        layout.addWidget(self._section_label("应用使用时长排行"))

        summary_bar = QFrame()
        summary_bar.setStyleSheet(
            "background-color: #263E26; "
            "border-radius: 8px;"
        )
        summary_layout = QHBoxLayout(summary_bar)
        summary_layout.setContentsMargins(18, 12, 18, 12)
        summary_layout.setSpacing(8)

        summary_icon = QLabel("📱")
        summary_icon.setFixedWidth(28)
        summary_icon.setAlignment(Qt.AlignCenter)
        summary_icon.setStyleSheet("font-size: 18px; background: transparent;")
        summary_layout.addWidget(summary_icon)

        self._ranking_summary = QLabel("共监控 <b>0</b> 个应用，今日最常用应用：<b>暂无数据</b>")
        self._ranking_summary.setWordWrap(True)
        self._ranking_summary.setStyleSheet(
            "color: #A5D6A7; font-size: 13px; font-family: {FONT};"
        )
        summary_layout.addWidget(self._ranking_summary, 1)
        layout.addWidget(summary_bar)

        self._ranking_table = QTableWidget()
        self._ranking_table.setColumnCount(4)
        self._ranking_table.setHorizontalHeaderLabels(["排名", "应用名称", "使用时长", "占比"])
        self._ranking_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ranking_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ranking_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._ranking_table.setShowGrid(False)
        self._ranking_table.verticalHeader().setVisible(False)
        self._ranking_table.setAlternatingRowColors(True)

        h = self._ranking_table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Fixed)
        h.resizeSection(0, 80)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.Fixed)
        h.resizeSection(2, 180)
        h.setSectionResizeMode(3, QHeaderView.Fixed)
        h.resizeSection(3, 110)

        self._ranking_table.setStyleSheet(self._table_style())
        self._show_ranking_placeholder()

        layout.addWidget(self._ranking_table, 1)

        # 绑定应用排行数据信号
        self._tracker.app_ranking_changed.connect(self._update_ranking)

        return page

    # ==================== 历史记录页 ====================
    def _build_history_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(16)

        layout.addWidget(self._section_label("历史使用记录"))

        filter_bar = QFrame()
        filter_bar.setStyleSheet(
            f"background-color: {COLOR_CARD}; border: 1px solid {COLOR_BORDER}; "
            f"border-radius: 8px;"
        )
        filter_layout = QHBoxLayout(filter_bar)
        filter_layout.setContentsMargins(18, 12, 18, 12)
        filter_layout.setAlignment(Qt.AlignVCenter)
        filter_layout.setSpacing(10)

        filter_label = QLabel("筛选日期：")
        filter_label.setStyleSheet(
            f"color: {COLOR_TEXT}; font-size: 14px; font-family: {FONT};"
        )
        filter_layout.addWidget(filter_label)

        self._filter_btns = {}
        for key, text in [("today", "今天"), ("week", "本周"), ("month", "本月")]:
            btn = QPushButton(text)
            btn.setMinimumWidth(64)
            btn.setStyleSheet(self._filter_btn_style(active=(key == "today")))
            btn.clicked.connect(lambda checked, k=key: self._apply_history_filter(k))
            self._filter_btns[key] = btn
            filter_layout.addWidget(btn)

        filter_layout.addStretch()

        btn_export = QPushButton("  导出 CSV  ")
        btn_export.setCursor(Qt.PointingHandCursor)
        btn_export.setMinimumWidth(100)
        btn_export.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border: none;
                padding: 10px 24px;
                font-size: 14px;
                font-family: {FONT};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_PRIMARY_DARK};
            }}
        """)
        btn_export.clicked.connect(self._export_csv)
        filter_layout.addWidget(btn_export)

        layout.addWidget(filter_bar)

        self._history_table = QTableWidget()
        self._history_table.setColumnCount(4)
        self._history_table.setHorizontalHeaderLabels(["日期", "开机时长", "活跃时长", "主要应用"])
        self._history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._history_table.setShowGrid(False)
        self._history_table.verticalHeader().setVisible(False)
        self._history_table.setAlternatingRowColors(True)

        h = self._history_table.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Fixed)
        h.resizeSection(0, 170)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        h.setSectionResizeMode(3, QHeaderView.Stretch)
        self._history_table.setStyleSheet(self._table_style())

        layout.addWidget(self._history_table, 1)

        self._history_filter = "today"
        self._tracker.history_changed.connect(self._load_history)
        self._load_history()

        return page

    def _apply_history_filter(self, mode):
        self._history_filter = mode
        for key, btn in self._filter_btns.items():
            btn.setStyleSheet(self._filter_btn_style(active=(key == mode)))
        self._load_history()

    def _load_history(self):
        from data.storage import Storage
        from datetime import date, timedelta

        storage = Storage()
        all_days = storage.list_all_days()

        today = date.today()
        if self._history_filter == "today":
            days = [d for d in all_days if d.get("date") == today.isoformat()]
        elif self._history_filter == "week":
            monday = today - timedelta(days=today.weekday())
            days = [d for d in all_days if d.get("date", "") >= monday.isoformat()]
        else:
            month_start = today.replace(day=1).isoformat()
            days = [d for d in all_days if d.get("date", "") >= month_start]

        self._history_table.setRowCount(max(len(days), 1))
        for i, d in enumerate(days):
            items = [
                d.get("date", ""),
                _fmt_seconds(d.get("uptime_seconds", 0)),
                _fmt_seconds(d.get("active_seconds", 0)),
                _top_app_name(d.get("app_usage", {}))
            ]
            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self._history_table.setItem(i, col, item)
            self._history_table.setRowHeight(i, 44)

        if len(days) == 0:
            for col, text in enumerate(["暂无记录", "—", "—", "—"]):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor("#666666"))
                self._history_table.setItem(0, col, item)
            self._history_table.setRowHeight(0, 44)

    def _export_csv(self):
        from datetime import date, timedelta
        from PyQt5.QtWidgets import QFileDialog

        path, _ = QFileDialog.getSaveFileName(
            self, "导出 CSV", f"使用记录_{date.today().isoformat()}.csv", "CSV 文件 (*.csv)"
        )
        if not path:
            return

        from data.storage import Storage
        storage = Storage()
        all_days = storage.list_all_days()

        with open(path, "w", encoding="utf-8-sig") as f:
            f.write("日期,开机时长(秒),活跃时长(秒),主要应用\r\n")
            for d in all_days:
                f.write(f"{d.get('date','')},{d.get('uptime_seconds',0)},{d.get('active_seconds',0)},{_top_app_name(d.get('app_usage',{}))}\r\n")

    # ==================== 设置页 ====================
    def _build_settings_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(16)

        self._settings_data = self._load_settings()

        layout.addWidget(self._section_label("久坐提醒"))

        remind_card = QFrame()
        remind_card.setStyleSheet(
            f"background-color: {COLOR_CARD}; border: 1px solid {COLOR_BORDER}; "
            f"border-radius: 10px;"
        )
        remind_layout = QVBoxLayout(remind_card)
        remind_layout.setContentsMargins(24, 18, 24, 18)
        remind_layout.setSpacing(16)

        toggle_row = QHBoxLayout()
        toggle_label = QLabel("启用久坐提醒")
        toggle_label.setStyleSheet(
            f"color: {COLOR_TEXT}; font-size: 15px; font-family: {FONT};"
        )
        toggle_row.addWidget(toggle_label)
        toggle_row.addStretch()
        self._remind_toggle = QCheckBox()
        self._remind_toggle.setChecked(self._settings_data.get("remind_enabled", False))
        self._remind_toggle.setText("")
        self._remind_toggle.setFixedSize(50, 28)
        self._remind_toggle.setStyleSheet(self._toggle_style())
        self._remind_toggle.stateChanged.connect(self._save_settings)
        toggle_row.addWidget(self._remind_toggle)
        remind_layout.addLayout(toggle_row)

        interval_row = QHBoxLayout()
        interval_label = QLabel("提醒间隔")
        interval_label.setStyleSheet(
            f"color: {COLOR_TEXT}; font-size: 15px; font-family: {FONT};"
        )
        interval_row.addWidget(interval_label)
        interval_row.addStretch()

        self._interval_spin = QSpinBox()
        self._interval_spin.setMinimum(5)
        self._interval_spin.setMaximum(180)
        self._interval_spin.setValue(self._settings_data.get("remind_interval", DEFAULT_SIT_INTERVAL))
        self._interval_spin.setSuffix(" 分钟")
        self._interval_spin.setMinimumWidth(150)
        self._interval_spin.setStyleSheet(self._spinbox_style())
        self._interval_spin.valueChanged.connect(self._save_settings)
        interval_row.addWidget(self._interval_spin)
        remind_layout.addLayout(interval_row)

        layout.addWidget(remind_card)

        layout.addWidget(self._section_label("系统设置"))

        sys_card = QFrame()
        sys_card.setStyleSheet(
            f"background-color: {COLOR_CARD}; border: 1px solid {COLOR_BORDER}; "
            f"border-radius: 10px;"
        )
        sys_layout = QVBoxLayout(sys_card)
        sys_layout.setContentsMargins(24, 18, 24, 18)
        sys_layout.setSpacing(16)

        startup_row = QHBoxLayout()
        startup_label = QLabel("开机自动启动")
        startup_label.setStyleSheet(
            f"color: {COLOR_TEXT}; font-size: 15px; font-family: {FONT};"
        )
        startup_row.addWidget(startup_label)
        startup_row.addStretch()
        self._startup_toggle = QCheckBox()
        self._startup_toggle.setChecked(self._settings_data.get("auto_start", False))
        self._startup_toggle.setText("")
        self._startup_toggle.setFixedSize(50, 28)
        self._startup_toggle.setStyleSheet(self._toggle_style())
        self._startup_toggle.stateChanged.connect(self._toggle_auto_start)
        startup_row.addWidget(self._startup_toggle)
        sys_layout.addLayout(startup_row)

        layout.addWidget(sys_card)

        # ---- 关于 ----
        layout.addWidget(self._section_label("关于"))

        about_card = QFrame()
        about_card.setStyleSheet(
            f"background-color: {COLOR_CARD}; border: 1px solid {COLOR_BORDER}; "
            f"border-radius: 10px;"
        )
        about_layout = QVBoxLayout(about_card)
        about_layout.setContentsMargins(24, 18, 24, 18)
        about_layout.setSpacing(8)

        about_name = QLabel(f"PC时光记录器 v{APP_VERSION}")
        about_name.setStyleSheet(
            f"color: {COLOR_TEXT}; font-size: 15px; font-weight: bold; font-family: {FONT};"
        )
        about_layout.addWidget(about_name)

        about_desc = QLabel("一款简洁的 Windows 电脑使用时长监控工具")
        about_desc.setWordWrap(True)
        about_desc.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 14px; font-family: {FONT};"
        )
        about_layout.addWidget(about_desc)

        layout.addWidget(about_card)
        layout.addStretch()
        return page

    # ==================== 应用排行更新 ====================
    def _update_ranking(self, sorted_apps):
        """接收追踪器数据，刷新排行表格和汇总条"""
        count = len(sorted_apps)
        total = sum(sec for _, sec in sorted_apps)

        # 更新汇总条
        top_name = sorted_apps[0][0] if sorted_apps else "暂无数据"
        top_formatted = _fmt_seconds(sorted_apps[0][1]) if sorted_apps else ""
        self._ranking_summary.setText(
            f"共监控 <b>{count}</b> 个应用，今日最常用应用：<b>{top_name}</b>"
        )

        # 更新表格
        self._ranking_table.setRowCount(max(count, 5))
        for i, (name, sec) in enumerate(sorted_apps):
            rank = QTableWidgetItem(str(i + 1))
            rank.setTextAlignment(Qt.AlignCenter)
            self._ranking_table.setItem(i, 0, rank)

            app_item = QTableWidgetItem(name)
            app_item.setTextAlignment(Qt.AlignCenter)
            self._ranking_table.setItem(i, 1, app_item)

            time_item = QTableWidgetItem(_fmt_seconds(sec))
            time_item.setTextAlignment(Qt.AlignCenter)
            self._ranking_table.setItem(i, 2, time_item)

            pct = f"{sec / total * 100:.1f}%" if total > 0 else "—"
            pct_item = QTableWidgetItem(pct)
            pct_item.setTextAlignment(Qt.AlignCenter)
            self._ranking_table.setItem(i, 3, pct_item)

            self._ranking_table.setRowHeight(i, 46)

        # 剩余行清空
        for i in range(count, self._ranking_table.rowCount()):
            for col in range(4):
                item = QTableWidgetItem("")
                self._ranking_table.setItem(i, col, item)

        if count == 0:
            self._show_ranking_placeholder()

    def _show_ranking_placeholder(self):
        self._ranking_table.setRowCount(5)
        for i in range(5):
            self._ranking_table.setRowHeight(i, 46)
            for col in range(4):
                text = "暂无数据" if col > 1 else ("—" if col == 0 else "等待记录…")
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor("#666666"))
                self._ranking_table.setItem(i, col, item)

    def _show_reminder(self):
        from ui.reminder_dialog import show_reminder
        show_reminder()

    # ==================== 设置功能 ====================
    def _settings_path(self):
        from config.settings import DATA_DIR
        import os
        return os.path.join(DATA_DIR, "settings.json")

    def _load_settings(self):
        import json, os
        path = self._settings_path()
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_settings(self):
        import json
        data = {
            "remind_enabled": self._remind_toggle.isChecked(),
            "remind_interval": self._interval_spin.value(),
            "auto_start": self._startup_toggle.isChecked(),
        }
        with open(self._settings_path(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _toggle_auto_start(self):
        import os, sys
        import winreg
        enabled = self._startup_toggle.isChecked()

        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = sys.executable
            args = f'"{os.path.abspath("main.py")}"'
            exe_path = f'"{exe_path}" {args}'

        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"

        if enabled:
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as k:
                from config.settings import APP_NAME
                winreg.SetValueEx(k, APP_NAME, 0, winreg.REG_SZ, exe_path)
        else:
            try:
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as k:
                    from config.settings import APP_NAME
                    winreg.DeleteValue(k, APP_NAME)
            except FileNotFoundError:
                pass

        self._save_settings()

    # ==================== UI 工具方法 ====================
    def _section_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(
            f"color: {COLOR_TEXT}; font-size: 16px; font-weight: bold; "
            f"font-family: {FONT};"
        )
        return label

    def _divider(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background-color: {COLOR_BORDER}; max-height: 1px;")
        return line

    def _filter_btn_style(self, active: bool = False) -> str:
        if active:
            return f"""
                QPushButton {{
                    background-color: {COLOR_PRIMARY};
                    color: white;
                    border: none;
                    padding: 9px 20px;
                    font-size: 14px;
                    font-family: {FONT};
                    border-radius: 4px;
                }}
            """
        return f"""
            QPushButton {{
                background: transparent;
                color: {COLOR_TEXT_SECONDARY};
                border: 1px solid {COLOR_BORDER};
                padding: 9px 20px;
                font-size: 14px;
                font-family: {FONT};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_PRIMARY_LIGHT};
                color: {COLOR_TEXT};
            }}
        """

    # ==================== 样式表 ====================
    def _tab_style(self) -> str:
        return f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLOR_BG};
            }}
            QTabBar::tab {{
                background: {COLOR_CARD};
                border: none;
                border-bottom: 3px solid transparent;
                padding: 14px 24px;
                margin-right: 0px;
                color: {COLOR_TEXT_SECONDARY};
                font-size: 15px;
                font-family: {FONT};
            }}
            QTabBar::tab:selected {{
                color: {COLOR_PRIMARY};
                border-bottom: 3px solid {COLOR_PRIMARY};
                background: {COLOR_BG};
            }}
            QTabBar::tab:hover:!selected {{
                background: {COLOR_BG};
                color: {COLOR_TEXT};
            }}
        """

    def _table_style(self) -> str:
        return f"""
            QTableWidget {{
                background-color: {COLOR_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                gridline-color: transparent;
                font-family: {FONT};
            }}
            QTableWidget::item {{
                padding: 10px 14px;
                border-bottom: 1px solid {COLOR_PRIMARY_LIGHT};
                color: {COLOR_TEXT};
                font-size: 14px;
                font-family: {FONT};
            }}
            QHeaderView::section {{
                background-color: {COLOR_CARD};
                color: {COLOR_TEXT};
                font-weight: bold;
                font-size: 14px;
                font-family: {FONT};
                padding: 12px 14px;
                border: none;
                border-bottom: 2px solid {COLOR_PRIMARY_LIGHT};
            }}
            QTableWidget::item:alternate {{
                background-color: #2A2A2A;
            }}
        """

    def _toggle_style(self) -> str:
        return f"""
            QCheckBox::indicator {{
                width: 46px;
                height: 26px;
                border-radius: 13px;
                border: 2px solid {COLOR_BORDER};
                background-color: {COLOR_BORDER};
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLOR_PRIMARY};
                border-color: {COLOR_PRIMARY};
            }}
        """

    def _spinbox_style(self) -> str:
        return f"""
            QSpinBox {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 15px;
                font-family: {FONT};
                color: {COLOR_TEXT};
                background: #2A2A2A;
                min-width: 150px;
            }}
            QSpinBox:focus {{
                border-color: {COLOR_PRIMARY};
            }}
        """

    # ==================== 窗口控制 ====================
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def _quit_app(self):
        from PyQt5.QtWidgets import QApplication
        self._tracker.save_now()
        self.closeEvent = lambda e: None
        self.close()
        QApplication.quit()
