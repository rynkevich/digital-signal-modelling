from math import sin, pi


def harmonic_signal(n, amplitude, frequency, phase):
    return lambda i: amplitude * sin(2 * pi * frequency * i / n + phase)


def polyharmonic_signal(big_n, params_of_signals):
    signals = harmonic_signals(big_n, params_of_signals)
    return aggregate_to_polyharmonic_signal(signals)


def harmonic_signals(big_n, params_of_signals):
    signals = []
    for params in params_of_signals:
        amplitude, frequency, phase = params
        signals.append(harmonic_signal(big_n, amplitude, frequency, phase))
    return signals


def aggregate_to_polyharmonic_signal(signals):
    return lambda i: sum(s(i) for s in signals)


def linearly_changing_polyharmonic_signal(big_n, params, fading=True):
    step_value = lambda i: big_n - (i % big_n) if fading else i % big_n
    reference_amplitude, reference_frequency, reference_phase = params

    amplitude = lambda i: reference_amplitude * (reference_amplitude * 0.2 / big_n) * step_value(i)
    frequency = lambda i: reference_frequency * (reference_frequency * 0.2 / big_n) * step_value(i)
    phase = lambda i: reference_phase * (reference_phase * 0.2 / big_n) * step_value(i)

    return lambda i: harmonic_signal(big_n, amplitude(i), frequency(i), phase(i))(step_value(i))
