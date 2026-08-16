# Lumped-Element Filter Design

A Python program for designing and analyzing lumped-element RF filters.

The program supports:

* Low-pass filter (LPF)
* High-pass filter (HPF)
* Band-pass filter (BPF)
* Band-stop filter (BSF)

The filter specifications are stored in YAML configuration files.

## Features

The program calculates:

* Inductor and capacitor values
* (S_{21})
* Amplitude response
* Insertion loss
* Group delay

It also plots:

* Amplitude vs. frequency
* Insertion loss vs. frequency
* Group delay vs. frequency

## Project Structure

```text
filter_project/
│
├── configs/
│   ├── lpf.yaml
│   ├── hpf.yaml
│   ├── bpf.yaml
│   └── bsf.yaml
│
├── src/
│   ├── filter_design.py
│   ├── transformations.py
│   ├── abcd.py
│   └── plot_response.py
│
├── main.py
└── README.md
```

## Requirements

* Python 3
* NumPy
* Matplotlib
* PyYAML

Install the required packages using:

```bash
pip3 install numpy matplotlib pyyaml
```

## How to Run

Low-pass Butterworth filter:

```bash
python3 main.py --filter_name lpf --filter_type butterworth
```

High-pass Chebyshev filter:

```bash
python3 main.py --filter_name hpf --filter_type chebyshev
```

Band-pass linear-phase filter:

```bash
python3 main.py --filter_name bpf --filter_type linear_phase
```

Band-stop Chebyshev filter:

```bash
python3 main.py --filter_name bsf --filter_type chebyshev
```

## Method

The program uses normalized low-pass prototype (g)-values and transforms them into LPF, HPF, BPF, or BSF circuit components.

ABCD matrices are used to model the filter network and calculate (S_{21}). The program then uses (S_{21}) to calculate amplitude, insertion loss, phase, and group delay.
