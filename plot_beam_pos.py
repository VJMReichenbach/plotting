import argparse
from pathlib import Path
import matplotlib.pyplot as plt

def read_data(file: Path):
    t = []
    x = []
    y = []

    with open(file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                continue
            t.append(float(lines[i].split(',')[0]))
            x.append(float(lines[i].split(',')[1]))
            y.append(float(lines[i].split(',')[2]))
    
    return t, x, y

def main(file: Path):
    # The file contains the time, x and y position of the beam
    t, x, y = read_data(file)

    # Plot the x and y position of the beam as two subplots as a scatter plot
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.scatter(t, x, s=0.1)
    ax1.set_ylabel('x (px)')
    ax2.scatter(t, y, s=0.1)
    ax2.set_ylabel('y (px)')
    ax2.set_xlabel('Time (ms)')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot dipole current')
    parser.add_argument('file', type=Path, help='Path to file')
    args = parser.parse_args()

    main(args.file)