import yaml
import numpy as np
import argparse

from src.filter_design import get_g_values
from src.transformations import lowpass_transform, highpass_transform, bandpass_transform, bandstop_transform
from src.abcd import calculate_S21, calculate_response
from src.plot_response import plot_amplitude, plot_insertion_loss, plot_group_delay

# read user input
parser = argparse.ArgumentParser(description="Lumped-Element Filter Design")
parser.add_argument("--filter_name", required=True, choices=["lpf", "hpf", "bpf", "bsf"])
parser.add_argument("--filter_type", required=True, choices=["butterworth", "chebyshev", "linear_phase"])
args = parser.parse_args()

#read yaml config
config_file = "configs/" + args.filter_name + ".yaml"
with open(config_file, "r") as file:
    config = yaml.safe_load(file)

# get filter parameters
order = int(config["filter"]["order"])
Z0 = float(config["system"]["impedance"])
f_min = float(config["frequency"]["minimum"])
f_max = float(config["frequency"]["maximum"])
points = int(config["frequency"]["points"])
frequency = np.linspace(f_min, f_max, points)

if "requirements" in config:
    ripple = config["requirements"].get("ripple")
else:
    ripple = None

# get normalized g-values
g_values = get_g_values(args.filter_type, order, ripple)

# design filter
if args.filter_name == "lpf":
    fc = float(config["frequency"]["cutoff"])
    components = lowpass_transform(g_values, Z0, fc)
elif args.filter_name == "hpf":
    fc = float(config["frequency"]["cutoff"])
    components = highpass_transform(g_values, Z0, fc)
elif args.filter_name == "bpf":
    f0 = float(config["frequency"]["center"])
    FBW = float(config["frequency"]["fractional_bandwidth"])
    components = bandpass_transform(g_values, Z0, f0, FBW)
elif args.filter_name == "bsf":
    f0 = float(config["frequency"]["center"])
    FBW = float(config["frequency"]["fractional_bandwidth"])
    components = bandstop_transform(g_values, Z0, f0, FBW)

# display component values
print()
print("FILTER DESIGN")
print("-----------------------------")
print("Filter name:", args.filter_name.upper())
print("Filter type:", args.filter_type)
print("Order:", order)
print("Impedance:", Z0, "ohm")
print()

for component in components:
    print("Section", component["number"], "-", component["type"])
    if "L" in component:
        print("L =", round(component["L"]*1e9, 4), "nH")
    if "C" in component:
        print("C =", round(component["C"]*1e12, 4), "pF")
    print()

# calculate S21 and responses
S21 = calculate_S21(components, frequency, Z0)
amplitude, insertion_loss, phase, group_delay = calculate_response(S21, frequency)

# check specified frequency
if "check" in config["frequency"]:
    check_frequency = float(config["frequency"]["check"])
    index = np.argmin(np.abs(frequency - check_frequency))
    print("Insertion loss at", check_frequency / 1e9, "GHz =", round(insertion_loss[index], 4), "dB")

# plots
title = args.filter_type + " " + args.filter_name.upper()
plot_amplitude(frequency, amplitude, title)
plot_insertion_loss(frequency, insertion_loss, title)
plot_group_delay(frequency, group_delay, title)