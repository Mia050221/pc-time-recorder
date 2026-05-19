"""
应用监控 - 检测当前前台窗口，统计各应用使用时长
"""
import win32gui
import win32process
import psutil


class AppMonitor:
    """前台窗口监控，每秒调用一次 tick()"""

    def __init__(self):
        self._usage = {}  # {app_name: total_seconds}
        self._current_app = None

    def tick(self):
        """检测当前前台应用并累计 1 秒"""
        app_name = self._get_foreground_app()
        if app_name:
            self._usage[app_name] = self._usage.get(app_name, 0) + 1
            self._current_app = app_name

    def get_sorted(self):
        """返回按使用时长降序排列的列表 [(app_name, seconds), ...]"""
        return sorted(self._usage.items(), key=lambda x: x[1], reverse=True)

    def total_seconds(self):
        return sum(self._usage.values())

    def app_count(self):
        return len(self._usage)

    def top_app_name(self):
        sorted_list = self.get_sorted()
        return sorted_list[0][0] if sorted_list else None

    # ==================== 内部 ====================
    def _get_foreground_app(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if not pid:
                return None
            proc = psutil.Process(pid)
            exe = proc.name()
            # 去 .exe 后缀
            if exe.lower().endswith(".exe"):
                exe = exe[:-4]
            return exe
        except Exception:
            return None
