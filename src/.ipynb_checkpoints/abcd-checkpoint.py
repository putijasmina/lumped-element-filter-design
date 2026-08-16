import numpy as np

def series_matrix(Z):
    return np.array([
        [1, Z],
        [0, 1]
    ], dtype=complex)

def shunt_matrix(Y):
    return np.array([
        [1, 0],
        [Y, 1]
    ], dtype=complex)

def component_matrix(component, w):
    component_type = component["type"]
    if component_type == "series inductor":
        L = component["L"]
        Z = 1j*w*L
        return series_matrix(Z)

    elif component_type == "shunt capacitor":
        C = component["C"]
        Y = 1j*w*C
        return shunt_matrix(Y)

    elif component_type == "series capacitor":
        C = component["C"]
        Z = 1/(1j*w*C)
        return series_matrix(Z)

    elif component_type == "shunt inductor":
        L = component["L"]
        Y = 1/(1j*w*L)
        return shunt_matrix(Y)

    elif component_type == "series LC":
        L = component["L"]
        C = component["C"]
        Z = 1j*w*L+1/(1j*w*C)
        return series_matrix(Z)

    elif component_type == "shunt parallel LC":
        L = component["L"]
        C = component["C"]
        Y = 1/(1j*w*L) + 1j*w*C
        return shunt_matrix(Y)

    elif component_type == "shunt series LC":
        L = component["L"]
        C = component["C"]
        Z = 1j*w*L+1/(1j*w*C)
        if abs(Z) < 1e-15:
            Y = 1e15
        else:
            Y = 1/Z
        return shunt_matrix(Y)

    elif component_type == "series parallel LC":
        L = component["L"]
        C = component["C"]
        Y = 1/(1j*w*L) + 1j*w*C
        if abs(Y) < 1e-15:
            Z = 1e15
        else:
            Z = 1/Y
        return series_matrix(Z)

    else:
        raise ValueError("Unknown component type.")

def calculate_S21(components, frequency, Z0):
    S21 = np.zeros(len(frequency), dtype=complex)
    for i in range(len(frequency)):
        w = 2*np.pi*frequency[i]
        total_matrix = np.eye(2, dtype=complex)
        for component in components:
            matrix = component_matrix(component, w)
            total_matrix = np.dot(total_matrix, matrix)

        A = total_matrix[0, 0]
        B = total_matrix[0, 1]
        C = total_matrix[1, 0]
        D = total_matrix[1, 1]

        denominator = A + B/Z0 + C*Z0 + D
        S21[i] = 2/denominator
    return S21

def calculate_response(S21, frequency):
    magnitude = np.abs(S21)
    magnitude = np.maximum(magnitude, 1e-15)
    amplitude_dB = 20*np.log10(magnitude)
    insertion_loss_dB = -amplitude_dB
    phase = np.angle(S21)
    phase = np.unwrap(phase)
    omega = 2*np.pi*frequency
    group_delay = -np.gradient(phase, omega)
    group_delay_ns = group_delay*1e9
    return amplitude_dB, insertion_loss_dB, phase, group_delay_ns