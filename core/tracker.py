"""
时长追踪器 - 每秒钟更新开机时长和活跃时长
"""
import json
import os
from datetime import datetime, date, timedelta
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from core.idle_detector import IdleDetector
from core.app_monitor import AppMonitor
from data.storage import Storage
from config.settings import IDLE_THRESHOLD_SECONDS, DEFAULT_SIT_INTERVAL, DATA_DIR


class TimeTracker(QObject):
    today_uptime_changed = pyqtSignal(str)
    today_active_changed = pyqtSignal(str)
    week_total_changed = pyqtSignal(str)
    month_total_changed = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    app_ranking_changed = pyqtSignal(list)
    history_changed = pyqtSignal()
    remind_triggered = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._storage = Storage()
        self._session_start = datetime.now()
        self._today_date = date.today()

        prev = self._storage.load_today()
        self._today_uptime = prev.get("uptime_seconds", 0)
        self._today_active = prev.get("active_seconds", 0)

        self._was_idle = False
        self._app_monitor = AppMonitor()
        self._remind_counter = 0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)

        self._save_timer = QTimer(self)
        self._save_timer.timeout.connect(self._save)
        self._save_timer.start(60000)

        self._emit_all()

    def _tick(self):
        now = datetime.now()
        today = now.date()

        if today != self._today_date:
            self._today_uptime = 0
            self._today_active = 0
            self._today_date = today

        self._today_uptime += 1

        idle_sec = IdleDetector.get_idle_seconds()
        if idle_sec < 300:
            self._today_active += 1
            self._remind_counter += 1
            self._check_reminder()
        else:
            self._remind_counter = 0

        self._app_monitor.tick()

        currently_idle = idle_sec >= IDLE_THRESHOLD_SECONDS
        if currently_idle != self._was_idle:
            self._was_idle = currently_idle
            self.status_changed.emit("已离开" if currently_idle else "活跃中")

        self._emit_all()
        self.app_ranking_changed.emit(self._app_monitor.get_sorted())

    def _emit_all(self):
        self.today_uptime_changed.emit(self._format(self._today_uptime))
        self.today_active_changed.emit(self._format(self._today_active))

        week = self._storage.sum_range(self._monday(), self._today_date)
        self.week_total_changed.emit(self._format(week["uptime_seconds"]))

        month = self._storage.sum_range(self._today_date.replace(day=1), self._today_date)
        self.month_total_changed.emit(self._format(month["uptime_seconds"]))

    def _save(self):
        self._storage.save_today(
            self._today_uptime,
            self._today_active,
            dict(self._app_monitor.get_sorted())
        )
        self.history_changed.emit()

    def save_now(self):
        self._save()

    def _load_reminder_settings(self):
        path = os.path.join(DATA_DIR, "settings.json")
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _check_reminder(self):
        s = self._load_reminder_settings()
        if not s.get("remind_enabled", False):
            return
        interval_min = s.get("remind_interval", DEFAULT_SIT_INTERVAL)
        if self._remind_counter >= interval_min * 60:
            self._remind_counter = 0
            self.remind_triggered.emit()

    @staticmethod
    def _format(total_seconds: int) -> str:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours} 小时 {minutes} 分钟"

    @staticmethod
    def _monday() -> date:
        today = date.today()
        return today - timedelta(days=today.weekday())
