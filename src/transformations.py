import numpy as np

def lowpass_transform(g_values, Z0, fc):
    wc = 2*np.pi*fc
    components = []
    for k in range(1, len(g_values) + 1):
        g = g_values[k-1]
        if k % 2 == 1:
            C = g/(20*wc)
            components.append({"number": k, "type": "shunt capacitor", "C": C})

        else:
            L = 20 * g / wc
            components.append({"number": k, "type": "series inductor", "L": L})

    return components

def highpass_transform(g_values, Z0, fc):
    wc = 2*np.pi*fc
    components = []
    for k in range(1, len(g_values) + 1):
        g = g_values[k-1]
        if k % 2 == 1:
            L = Z0/(wc*g)
            components.append({"number": k, "type": "shunt inductor", "L": L})
        
        else:
            C = 1/(Z0*wc*g)
            components.append({"number": k, "type": "series capacitor", "C": C})

    return components

def bandpass_transform(g_values, Z0, f0, fractional_bandwidth):
    w0 = 2*np.pi*f0
    delta = fractional_bandwidth
    components = []
    for k in range(1, len(g_values) + 1):
        g = g_values[k-1]
        if k % 2 == 1:
            C = g/(Z0*w0*delta)
            L = Z0*delta/(w0*g)
            components.append({"number": k, "type": "shunt parallel LC", "L": L, "C": C})

        else:
            L = Z0*g/(w0*delta)
            C = delta/(Z0*g*w0)
            components.append({"number": k, "type": "series LC", "L": L, "C": C})

    return components

def bandstop_transform(g_values, Z0, f0, fractional_bandwidth):
    w0 = 2*np.pi*f0
    delta = fractional_bandwidth
    components = []
    for k in range(1, len(g_values) + 1):
        g = g_values[k-1]
        if k % 2 == 1:
            L = Z0/(g*delta*w0)
            C = g*delta/(Z0*w0)
            components.append({"number": k, "type": "shunt series LC", "L": L, "C": C})

        else:
            L = Z0*g*delta/w0
            C = 1/(Z0*g*delta*w0)
            components.append({"number": k, "type": "series parallel LC", "L": L, "C": C})

    return components