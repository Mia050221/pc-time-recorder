"""
数据存储 - JSON 文件持久化，按日期分文件
"""
import json
import os
import glob
from datetime import datetime, date, timedelta
from config.settings import DATA_DIR


class Storage:
    """本地 JSON 文件存储"""

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

    # ---- 路径 ----
    def _file_path(self, day: date) -> str:
        return os.path.join(DATA_DIR, f"{day.isoformat()}.json")

    # ---- 读取 ----
    def load_day(self, day: date) -> dict:
        """读取某天的统计数据，没有则返回空字典"""
        path = self._file_path(day)
        if not os.path.isfile(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---- 保存 ----
    def save_day(self, day: date, data: dict):
        """保存某天的统计数据"""
        data["date"] = day.isoformat()
        with open(self._file_path(day), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---- 今日快照 ----
    def load_today(self) -> dict:
        return self.load_day(date.today())

    def save_today(self, uptime_seconds: int, active_seconds: int, app_usage: dict = None):
        self.save_day(date.today(), {
            "uptime_seconds": uptime_seconds,
            "active_seconds": active_seconds,
            "app_usage": app_usage or {},
            "updated_at": datetime.now().isoformat(),
        })

    # ---- 列出所有历史记录 ----
    def list_all_days(self) -> list:
        """扫描 DATA_DIR，返回所有日期的统计数据列表，按日期倒序"""
        result = []
        for path in glob.glob(os.path.join(DATA_DIR, "*.json")):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                day_str = data.get("date", "")
                if day_str:
                    result.append(data)
            except Exception:
                pass
        result.sort(key=lambda d: d.get("date", ""), reverse=True)
        return result

    # ---- 本周 / 本月汇总 ----
    def sum_range(self, start_day: date, end_day: date) -> dict:
        """汇总一段日期内的数据"""
        total_uptime = 0
        total_active = 0
        day = start_day
        while day <= end_day:
            d = self.load_day(day)
            total_uptime += d.get("uptime_seconds", 0)
            total_active += d.get("active_seconds", 0)
            day = day.fromordinal(day.toordinal() + 1)  # next day
        return {"uptime_seconds": total_uptime, "active_seconds": total_active}
