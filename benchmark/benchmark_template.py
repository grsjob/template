"""Мини-фреймворк для замера бенчмарков «до/после».

На хакатоне баллы часто идут за измеримый выигрыш (время, %, полнота).
Этот модуль даёт единый способ замерить и оформить результат для защиты.

Использование:
    from benchmark_template import Benchmark, timer

    bench = Benchmark("Смарт-регрессия")

    with timer() as t:
        result = run_agent_solution(...)
    bench.record("agent", duration_s=t.seconds, extra={"tests_selected": len(result)})

    with timer() as t:
        baseline = run_full_regression(...)
    bench.record("baseline", duration_s=t.seconds, extra={"tests_selected": baseline_count})

    bench.add_metric("time_saved_%", bench.improvement("baseline", "agent"))
    bench.report()          # печать в консоль
    bench.save("result.json")
"""
from __future__ import annotations

import json
import time
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Run:
    name: str
    duration_s: float
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Benchmark:
    case: str
    runs: list[Run] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def record(self, name: str, duration_s: float, extra: dict[str, Any] | None = None) -> None:
        """Зафиксировать один прогон (например, 'baseline' или 'agent')."""
        self.runs.append(Run(name=name, duration_s=round(duration_s, 3), extra=extra or {}))

    def _run(self, name: str) -> Run:
        for r in self.runs:
            if r.name == name:
                return r
        raise KeyError(f"Прогон '{name}' не найден. Есть: {[r.name for r in self.runs]}")

    def improvement(self, baseline: str, candidate: str) -> float:
        """Выигрыш по времени в процентах: насколько candidate быстрее baseline."""
        b = self._run(baseline).duration_s
        c = self._run(candidate).duration_s
        if b == 0:
            return 0.0
        return round((b - c) / b * 100, 1)

    def add_metric(self, name: str, value: Any) -> None:
        """Добавить произвольную метрику кейса (%, полнота, точность и т.п.)."""
        self.metrics[name] = value

    def report(self) -> None:
        print(f"\n=== Бенчмарк: {self.case} ===")
        for r in self.runs:
            extra = f"  {r.extra}" if r.extra else ""
            print(f"  [{r.name:>10}] {r.duration_s:>8.3f} s{extra}")
        if self.metrics:
            print("  --- метрики ---")
            for k, v in self.metrics.items():
                print(f"  {k}: {v}")
        print("=" * (len(self.case) + 16))

    def save(self, path: str) -> None:
        payload = {
            "case": self.case,
            "runs": [asdict(r) for r in self.runs],
            "metrics": self.metrics,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)


class _Timer:
    seconds: float = 0.0


@contextmanager
def timer():
    """Контекст-менеджер для замера времени блока кода."""
    t = _Timer()
    start = time.perf_counter()
    try:
        yield t
    finally:
        t.seconds = time.perf_counter() - start


# --------------------------------------------------------------------------- #
# Демонстрация (запусти файл напрямую: python benchmark/benchmark_template.py)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    bench = Benchmark("Пример: подготовка БТ")

    with timer() as t:
        time.sleep(0.3)  # имитация ручной работы
    bench.record("baseline", t.seconds, extra={"полнота_%": 70})

    with timer() as t:
        time.sleep(0.05)  # имитация работы агента
    bench.record("agent", t.seconds, extra={"полнота_%": 95})

    bench.add_metric("экономия_времени_%", bench.improvement("baseline", "agent"))
    bench.add_metric("прирост_полноты_пп", 95 - 70)
    bench.report()
