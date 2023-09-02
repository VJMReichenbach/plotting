#!/usr/bin/python3
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import time

def read_data(file):
    x = []
    y1 = []
    y2 = []

    with open(file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                continue
            if i == 4050:
                print(lines[i])
            x.append(i)
            y1.append(float(lines[i].split()[5]))
            y2.append(float(lines[i].split()[6]))
    return x, y1, y2

def extract_interesting_interval(start_index, end_index, x, y1, y2):
    x = x[start_index:end_index]
    y1 = y1[start_index:end_index]
    y2 = y2[start_index:end_index]
    return x, y1, y2

def main(file):
    x, y1, y2 = read_data(file)

    interesting_intervals = {
        # "Test Mixnoise": [extract_interesting_interval(0, 450, x, y1, y2)],
        # "Egal": [extract_interesting_interval(2200, 2400, x, y1, y2)],
        # "TODO: Mehr hieraus": [extract_interesting_interval(4050, 4300, x, y1, y2)],
        "Sinus Messung 1 (Amplitude = 1)": [extract_interesting_interval(10700, 11300, x, y1, y2)],
        "Sinus Messung 2 (Amplitude = 2)": [extract_interesting_interval(12000, 12800, x, y1, y2)],
        # "Normalverteilung Messung": [extract_interesting_interval(13400, 14100, x, y1, y2)],
        # "Mix Messung": [extract_interesting_interval(14900, 15700, x, y1, y2)],
    }

    intervalls = {}
    if args.all:
        intervalls.update({"All": [extract_interesting_interval(0, len(x), x, y1, y2)]})
    else:
        intervalls.update(interesting_intervals)
    print(intervalls.keys())


    for key, value in intervalls.items():
        if args.dump:
            with open("dump.csv", "w") as f:
                f.write("time,noise,regelung\n")
        
                print(value[0][0])
                for t in range(len(value[0][0])):
                    f.write(str(t) + "," + str(value[0][1][t]) + "," + str(value[0][2][t]) + "\n")
                f.close()



        plt.plot(value[0][0], value[0][1], label="Magnet I0SH03 (Sörung)", color="#cc0000")
        plt.plot(value[0][0], value[0][2], label="Magnet I0SH04 (Regelung)", color="g")
        plt.xlabel('Zeit t in Intervallen')
        plt.ylabel('Strom der Dipole I in A')
        # plt.title(f'{key}')
        plt.title("Dipolstrom")
        plt.legend()
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot dipole current')
    parser.add_argument('file', type=Path, help='Input file')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity level')
    parser.add_argument('-a', '--all', action='store_true', help='Show plot the entire file')
    parser.add_argument('--dump', action='store_true', help='Dump specific data')
    args = parser.parse_args()
    main(file=args.file)
