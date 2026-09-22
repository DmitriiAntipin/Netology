from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

U_ZERO = 0.5
U_ONE = 4.5
DURATION = 1e-3
H = 1e-6
FREQUENCIES = (5_000, 10_000)
TIME_CONSTANTS = (10e-6, 20e-6)
NOISE_AMPLITUDES = (0.1, 0.3)
THRESHOLDS = ((1.5, 3.5), (2.0, 4.0))
n_steps = int(round(DURATION / H))
time = np.arange(n_steps) * H
ms = time * 1e3
rng = np.random.default_rng(42)
OUTPUT_DIR = Path("")
OUTPUT_DIR.mkdir(exist_ok=True)

def square_wave(frequency):
    half_period_steps = round(1 / (2 * frequency * H))
    logical_levels = (np.arange(n_steps) // half_period_steps) % 2
    return np.where(logical_levels == 0, U_ZERO, U_ONE)

def euler_line_response(source, tau):
    response = np.empty_like(source)
    response[0] = U_ZERO
    for n in range(n_steps - 1):
        response[n + 1] = response[n] + H * (source[n] - response[n]) / tau
    return response

def logic_output(input_voltage, u_min, u_max):
    output = np.empty_like(input_voltage)
    previous_level = 0
    for n, voltage in enumerate(input_voltage):
        if previous_level == 0 and voltage > u_max:
            previous_level = 1
        elif previous_level == 1 and voltage < u_min:
            previous_level = 0
        output[n] = U_ONE if previous_level == 1 else U_ZERO
    return output

def count_pulses(signal):
    high = signal > (U_ZERO + U_ONE) / 2
    return int(high[0]) + int(np.count_nonzero(~high[:-1] & high[1:]))

for frequency in FREQUENCIES:
    source = square_wave(frequency)
    for tau in TIME_CONSTANTS:
        smooth = euler_line_response(source, tau)
        fig, axes = plt.subplots(2, 2, figsize=(16, 10), sharex=True, sharey=True)
        axes = axes.flatten()
        plot_index = 0
        for amplitude in NOISE_AMPLITUDES:
            noisy = smooth + rng.uniform(-amplitude, amplitude, size=n_steps)
            for u_min, u_max in THRESHOLDS:
                output = logic_output(noisy, u_min, u_max)
                ax = axes[plot_index]
                ax.step(ms, source, where="post", label="Генератор", linewidth=1.5)
                ax.plot(ms, smooth, label="После RC", linewidth=1.5)
                ax.plot(ms, noisy, label=f"С помехой ±{amplitude:g} В", linewidth=1.0)
                ax.step(ms, output, where="post", label="Выход", linewidth=1.5)
                ax.set_title(f"A = {amplitude:g} В, зона {u_min:g}–{u_max:g} В, импульсов = {count_pulses(output)}")
                ax.set_xlabel("Время, мс")
                ax.set_ylabel("Напряжение, В")
                ax.set_xlim(0, DURATION * 1e3)
                ax.set_ylim(0, 5)
                ax.grid(True, alpha=0.3)
                ax.legend(fontsize=8)
                plot_index += 1
        fig.suptitle(f"Цифровой сигнал: f = {frequency / 1000:g} кГц, T = {tau * 1e6:g} мкс", fontsize=16)
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        fig.savefig(OUTPUT_DIR / f"f{frequency // 1000}k_T{tau * 1e6:.0f}us.png", dpi=125, bbox_inches="tight")
        plt.close(fig)

# Вывод:
# 1. Исходный цифровой сигнал представляет собой меандр с частотой 5 кГц и 10 кГц.
# 2. После прохождения через RC-цепь фронты сигнала сглаживаются.
# 3. При увеличении постоянной времени T сглаживание выражено сильнее.
# 4. Добавление случайной помехи вызывает искажения входного сигнала.
# 5. Логический каскад с гистерезисом восстанавливает прямоугольную форму сигнала.
# 6. Ширина запрещённой зоны и амплитуда помех влияют на моменты переключения.
# 7. В исследованных режимах количество импульсов на выходе сохраняется.