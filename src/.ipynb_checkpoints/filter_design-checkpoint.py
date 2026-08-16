import numpy as np

def get_g_values(filter_type, order, ripple=None):
    if filter_type == "butterworth":
        g_values = []
        for k in range(1, order + 1):
            gk = 2*np.sin((2*k - 1)*np.pi/(2*order))
            g_values.append(gk)
        return g_values
        
    elif filter_type == "chebyshev":
        if order == 5 and ripple == 3.0:
            g_values = [
                3.4817,
                0.7618,
                4.5381,
                0.7618,
                3.4817
            ]
            return g_values

        elif order == 3 and ripple == 0.5:
            g_values = [
                1.5963,
                1.0967,
                1.5963
            ]
            return g_values

        else:
            raise ValueError("Chebyshev g-values are not available for this order and ripple.")

    elif filter_type == "linear_phase":
        if order == 4:
            g_values = [
                1.0598,
                0.5116,
                0.3181,
                0.1104
            ]
            return g_values

        else:
            raise ValueError("Linear phase g-values are not available for this order.")

    else:
        raise ValueError("Unknown filter type.")