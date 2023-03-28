#!/usr/bin/python3
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import time

def read_data(file: Path) -> list | list | list:
    x = []
    y1 = []
    y2 = []

    with open(file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                continue
            x.append(i)
            y1.append(float(lines[i].split()[5]))
            y2.append(float(lines[i].split()[6]))
    return x, y1, y2

def extract_interesting_interval(start_index: int, end_index:int, x: list, y1: list, y2: list) -> list | list | list:
    x = x[start_index:end_index]
    y1 = y1[start_index:end_index]
    y2 = y2[start_index:end_index]
    return x, y1, y2

def main(file: Path):
    x, y1, y2 = read_data(file)

    interesting_intervals = {
        "Pl1": [extract_interesting_interval(0, 450, x, y1, y2)],
        "Pl2": [extract_interesting_interval(2200, 2400, x, y1, y2)],
        "Pl3": [extract_interesting_interval(4050, 4300, x, y1, y2)],
        "Pl4": [extract_interesting_interval(10700, 11300, x, y1, y2)],
        "Pl5": [extract_interesting_interval(12000, 12800, x, y1, y2)],
        "Pl6": [extract_interesting_interval(13000, 14100, x, y1, y2)],
        "Pl7": [extract_interesting_interval(14900, 15700, x, y1, y2)],
    }

    intervalls = {}
    if args.all:
        intervalls.update({"All": [extract_interesting_interval(0, len(x), x, y1, y2)]})
    else:
        intervalls.update(interesting_intervals)
    print(intervalls.keys())
    
    for key, value in intervalls.items():
        plt.plot(value[0][0], value[0][1], label="I0SH03")
        plt.plot(value[0][0], value[0][2], label="I0SH04")
        plt.xlabel('Time (intervalls)')
        plt.ylabel('Dipole current (A)')
        plt.title(f'{key}')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot dipole current')
    parser.add_argument('file', type=Path, help='Input file')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity level')
    parser.add_argument('-a', '--all', action='store_true', help='Show plot the entire file')
    args = parser.parse_args()
    main(file=args.file)
