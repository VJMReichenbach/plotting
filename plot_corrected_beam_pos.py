import argparse
from pathlib import Path
import matplotlib.pyplot as plt

def read_data(file: Path):
    time, current_pos, corrected_pos, current_shift, current_current, new_current = [], [], [], [], [], []
    with open(file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i in range(0, 9):
                continue
            time.append(float(lines[i].split(',')[0]))
            current_pos.append(float(lines[i].split(',')[1]))
            corrected_pos.append(float(lines[i].split(',')[2]))
            current_shift.append(float(lines[i].split(',')[3]))
            current_current.append(float(lines[i].split(',')[4]))
            new_current.append(float(lines[i].split(',')[5]))
    return time, current_pos, corrected_pos, current_shift, current_current, new_current

def main(file: Path):
    time, current_pos, corrected_pos, current_shift, current_current, new_current = read_data(file)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
    ax1.plot(time, current_pos, label='Current pos')
    ax1.plot(time, corrected_pos, label='Corrected pos')
    ax1.set_ylabel('Position (px)')
    ax1.legend()
    ax2.plot(time, current_shift)
    ax2.set_ylabel('Shift (px)')
    ax3.plot(time, current_current)
    ax3.set_ylabel('Current (A)')
    ax4.plot(time, new_current)
    ax4.set_ylabel('New current (A)')
    ax4.set_xlabel('Time (ms)')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot beam pos with and without controller')
    parser.add_argument('file', type=Path, help='Path to file')
    args = parser.parse_args()

    main(args.file)