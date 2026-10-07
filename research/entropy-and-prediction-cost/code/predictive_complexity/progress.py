from __future__ import annotations
import time

def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return 'unknown'
    seconds = max(0.0, seconds)
    if seconds < 60.0:
        return f'{seconds:.0f}s'
    minutes, sec = divmod(int(round(seconds)), 60)
    if minutes < 60:
        return f'{minutes}m{sec:02d}s'
    hours, minutes = divmod(minutes, 60)
    return f'{hours}h{minutes:02d}m'

class ProgressTimer:

    def __init__(self, total: int) -> None:
        if total <= 0:
            raise ValueError('total must be positive')
        self.total = total
        self.started = time.perf_counter()

    @property
    def elapsed_s(self) -> float:
        return time.perf_counter() - self.started

    def eta_s(self, current: int) -> float | None:
        if current <= 0:
            return None
        rate = self.elapsed_s / current
        return rate * max(self.total - current, 0)

    def status(self, current: int) -> str:
        elapsed = self.elapsed_s
        eta = self.eta_s(current)
        if current <= 0:
            rate = 0.0
        else:
            rate = current / max(elapsed, 1e-12)
        return f'elapsed={format_duration(elapsed)} eta={format_duration(eta)} rate={rate:.3f}/s'
