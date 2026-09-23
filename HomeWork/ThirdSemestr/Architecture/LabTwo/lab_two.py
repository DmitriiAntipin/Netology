from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("")
OUT.mkdir(exist_ok=True)
t = np.arange(640)
X1, X2, X3, X4, a1, a2 = [(t // p) % 2 for p in (10, 20, 40, 80, 160, 320)]
X = [X1, X2, X3, X4]

def finish(fig, filename):
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=140, bbox_inches='tight')
    plt.close(fig)

print('X1 X2 X3 X4 a1 a2 | F')
for b1 in range(2):
    for b2 in range(2):
        for bits in np.ndindex(2, 2, 2, 2):
            print(*bits, b1, b2, '|', bits[2*b1+b2])
print('\na1 a2 | D0 D1 D2 D3')
for b1 in range(2):
    for b2 in range(2):
        print(b1, b2, '|', *(int(2*b1+b2 == i) for i in range(4)))

fig, ax = plt.subplots(figsize=(12, 7))
ax.set(xlim=(0, 12), ylim=(0, 8))
ax.axis('off')
for i, (p, q) in enumerate([('НЕ(a1)', 'НЕ(a2)'), ('НЕ(a1)', 'a2'), ('a1', 'НЕ(a2)'), ('a1', 'a2')]):
    y = 7 - 1.7*i
    for offset, label in ((0.27, p), (-0.27, q)):
        ax.text(1.2, y+offset, label, ha='center', va='center', bbox=dict(boxstyle='round,pad=.24', fc='white'))
        ax.annotate('', xy=(3.55, y+offset/2), xytext=(2.05, y+offset), arrowprops=dict(arrowstyle='->'))
    for x, label in ((4, f'И\nD{i}'), (6.8, 'И')):
        ax.text(x, y, label, ha='center', va='center', bbox=dict(boxstyle='round,pad=.4', fc='white'))
    ax.annotate('', xy=(6.4, y), xytext=(4.45, y), arrowprops=dict(arrowstyle='->'))
    ax.text(6.8, y+0.54, f'X{i+1}', ha='center')
    ax.annotate('', xy=(6.8, y+0.25), xytext=(6.8, y+0.41), arrowprops=dict(arrowstyle='->'))
    ax.plot([7.2, 8.3, 9.35], [y, y, 4.3+(1.5-i)*.18], 'k-', lw=1)
ax.text(10, 4.3, 'ИЛИ\n(4 входа)', ha='center', va='center', bbox=dict(boxstyle='round,pad=.5', fc='white'))
ax.annotate('F', xy=(11.6, 4.3), xytext=(10.7, 4.3), va='center', arrowprops=dict(arrowstyle='->'))
ax.set_title('Мультиплексор 4:1: дешифратор и схема выбора')
finish(fig, '01_scheme.png')

F = np.choose(2*a1 + a2, X)

def delay(s):
    return np.r_[s[0], s[:-1]]

not_a1_0, not_a2_0, not_a1_1, not_a2_2 = [delay(1-s) for s in (a1, a2, a1, a2)]
D = [delay(not_a1_0 & not_a2_0), delay(not_a1_1 & a2), delay(a1 & not_a2_2), delay(a1 & a2)]
F_delay = delay(np.bitwise_or.reduce([delay(x & d) for x, d in zip(X, D)]))

fig, ax = plt.subplots(7, 1, figsize=(13, 9), sharex=True)
for a, signal, name in zip(ax, [*X, a1, a2, F], ['X1', 'X2', 'X3', 'X4', 'a1', 'a2', 'F']):
    a.step(t, 5*signal, where='post')
    a.set(ylim=(-.5, 5.5), yticks=[0, 5], ylabel=name)
    a.grid(axis='x', alpha=.3)
ax[-1].set_xlabel('Время, мкс')
fig.suptitle('Входы и выход F без задержки (0 или 5 В)')
finish(fig, '02_signals.png')

active = np.sum(D, axis=0)
fig, ax = plt.subplots(3, 1, figsize=(13, 7), sharex=True)
for a, s, label in zip(ax[:2], [F, F_delay], ['F без задержки', 'F с задержкой']):
    a.step(t, 5*s, where='post')
    a.set(ylim=(-.5, 5.5), yticks=[0, 5], ylabel=label)
    a.grid(axis='x', alpha=.3)
ax[2].step(t, active, where='post', color='tab:red')
ax[2].set(ylabel='Активных D', yticks=[0, 1, 2], xlabel='Время, мкс')
ax[2].grid(axis='x', alpha=.3)
finish(fig, '03_delays.png')
print('\nМоменты гонок дешифратора (мкс):', t[active != 1].tolist())
print('Вывод: из-за задержек возможны гонки внутри дешифратора; их наличие не обязательно означает ложный импульс на F.')
