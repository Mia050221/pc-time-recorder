"""
空闲检测 - 通过 Windows API 获取用户最后操作时间
"""
import ctypes
from ctypes import wintypes


class _LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("dwTime", wintypes.DWORD),
    ]


class IdleDetector:
    """检测用户空闲时长（鼠标/键盘无操作的时间）"""

    _user32 = ctypes.windll.user32
    _kernel32 = ctypes.windll.kernel32
    _kernel32.GetTickCount64.restype = ctypes.c_ulonglong

    @staticmethod
    def get_idle_seconds() -> float:
        """返回用户空闲秒数，即距离最后一次鼠标或键盘操作过去了多少秒"""
        info = _LASTINPUTINFO()
        info.cbSize = ctypes.sizeof(info)
        IdleDetector._user32.GetLastInputInfo(ctypes.byref(info))
        tick_count = IdleDetector._kernel32.GetTickCount64()
        elapsed_ms = tick_count - info.dwTime
        return elapsed_ms / 1000.0
