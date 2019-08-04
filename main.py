import sys
import json
from math import pi

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from signals import polyharmonic_signal, harmonic_signal, linearly_changing_polyharmonic_signal

N = 1024
TASK_E_REFERENCE_PARAMS = (5, 10, 0)


def main():
    data_path = sys.argv[1]
    variant = int(sys.argv[2])
    with open(data_path, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    data = data[variant - 1]

    # widgets must be kept globally
    widgets = [figure_3(), figure_2(data), figure_1(data)]

    plt.show()


def figure_1(data):
    fig, axes = plt.subplots(3, sharex=True)
    fig.canvas.set_window_title('Harmonic Signals Modelling (#1)')
    fig.suptitle('Harmonic Signals')
    axes[1].set_ylabel('x(n)')
    plt.xlabel('n')

    task_a(axes[0], data['a'])
    task_b(axes[1], data['b'])
    task_c(axes[2], data['c'])


def figure_2(data):
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.35)
    fig.canvas.set_window_title('Harmonic Signals Modelling (#2)')
    fig.suptitle('Harmonic Signals')
    ax.set_ylabel('x(n)')
    ax.set_xlabel('n')
    ax.margins(0.01)

    return task_d(ax, data['d'])


def figure_3():
    fig, axes = plt.subplots(2)
    fig.canvas.set_window_title('Harmonic Signals Modelling (#3)')
    fig.suptitle('Harmonic Signals')
    plt.ylabel('x(n)')
    plt.xlabel('n')

    task_e(axes)


def task_a(ax, data):
    params_of_signals = tuple((data['A'], data['f'], phase) for phase in data['phi'])
    get_info = lambda amplitude, frequency, _: '\n'.join([f'A = {amplitude}', f'f = {frequency}'])
    get_legend_label = lambda i, _, __, phase: rf'$\phi_{i} = {beautify_pi(phase)}$'
    plot_harmonic_signals(ax, params_of_signals, get_info, get_legend_label)


def task_b(ax, data):
    params_of_signals = tuple((data['A'], frequency, data['phi']) for frequency in data['f'])
    get_info = lambda amplitude, _, phase: '\n'.join([f'A = {amplitude}', rf'$\phi = {beautify_pi(phase)}$'])
    get_legend_label = lambda i, _, frequency, __: rf'$f_{i} = {frequency}$'
    plot_harmonic_signals(ax, params_of_signals, get_info, get_legend_label)


def task_c(ax, data):
    params_of_signals = tuple((amplitude, data['f'], data['phi']) for amplitude in data['A'])
    get_info = lambda _, frequency, phase: '\n'.join([rf'$\phi = {beautify_pi(phase)}$', f'f = {frequency}'])
    get_legend_label = lambda i, amplitude, _, __: rf'$A_{i} = {amplitude}$'
    plot_harmonic_signals(ax, params_of_signals, get_info, get_legend_label)


def task_d(ax, data):
    def update(_):
        for i, params in enumerate(params_of_signals):
            params[2] = sliders[i].val
        plot.set_ydata(tuple(map(polyharmonic_signal(N, params_of_signals), n)))

    def reset(_):
        for slider in sliders:
            slider.reset()

    params_of_signals = tuple([data['A'][i], data['f'][i], to_number(data['phi'][i])] for i in range(len(data['A'])))
    signal = polyharmonic_signal(N, params_of_signals)

    n = range(N)
    plot, = ax.plot(n, tuple(map(signal, n)))

    sliders = []
    for i, params in enumerate(params_of_signals):
        _, frequency, phase = params
        phi_axes = plt.axes([0.15, 0.1 + i * 0.03, 0.73, 0.02])
        slider = Slider(phi_axes, label=f'$f={frequency}$', valmin=0, valmax=2.5 * pi, valinit=phase, valfmt=r'$\phi=%1.2f$')
        slider.on_changed(update)
        sliders.append(slider)

    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset')
    button.on_clicked(reset)

    return [button] + sliders


def task_e(axes):
    def plot(ax, signal, title):
        ax.plot(n, tuple(map(signal, n)))
        ax.text(10, ax.get_ylim()[0] * 0.8, title, fontsize='10', bbox={'boxstyle': 'round', 'alpha': 0.8})

    fading_signal = linearly_changing_polyharmonic_signal(N, TASK_E_REFERENCE_PARAMS, fading=True)
    growing_signal = linearly_changing_polyharmonic_signal(N, TASK_E_REFERENCE_PARAMS, fading=False)

    n = range(N * 2)

    plot(axes[0], fading_signal, "Fading Signal")
    plot(axes[1], growing_signal, "Growing Signal")


def plot_harmonic_signals(ax, params_of_signals, get_info=None, get_legend_label=None):
    amplitude = frequency = phase = None

    for i, params in enumerate(params_of_signals):
        amplitude, frequency, phase = params
        signal = harmonic_signal(N, amplitude, frequency, to_number(phase))
        n = range(N)
        if get_legend_label is not None:
            ax.plot(n, tuple(map(signal, n)), label=get_legend_label(i, amplitude, frequency, phase))
            ax.legend(loc=7, prop={'size': 9})
        else:
            ax.plot(n, tuple(map(signal, n)))

    ax.margins(0.01)
    if get_legend_label is not None:
        ax.text(10, ax.get_ylim()[0] * 0.8, get_info(amplitude, frequency, phase),
                fontsize='8', bbox={'boxstyle': 'round', 'alpha': 0.5})


def beautify_pi(string):
    return string.replace(r'pi', r'\pi')


def to_number(string):
    return eval(string.replace('pi', str(pi)))


if __name__ == '__main__':
    main()
