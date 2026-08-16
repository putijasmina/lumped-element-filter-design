import matplotlib.pyplot as plt

def plot_amplitude(frequency, amplitude, title):
    plt.figure(figsize=(9, 6))
    plt.plot(frequency/1e9, amplitude)
    plt.xlabel("Frequency (GHz)")
    plt.ylabel("Amplitude (dB)")
    plt.title(title)
    plt.grid()
    plt.show()

def plot_insertion_loss(frequency, insertion_loss, title):
    plt.figure(figsize=(9, 6))
    plt.plot(frequency/1e9, insertion_loss)
    plt.xlabel("Frequency (GHz)")
    plt.ylabel("Insertion Loss (dB)")
    plt.title(title)
    plt.grid()
    plt.show()

def plot_group_delay(frequency, group_delay, title):
    plt.figure(figsize=(9, 6))
    plt.plot(frequency/1e9, group_delay)
    plt.xlabel("Frequency (GHz)")
    plt.ylabel("Group Delay (ns)")
    plt.title(title)
    plt.grid()
    plt.show()