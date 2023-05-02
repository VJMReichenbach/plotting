import argparse
from pathlib import Path
import matplotlib.pyplot as plt

def read_file(file: Path):
    time = []
    current_pos = []
    corrected_pos = []
    current_shift = []
    current_current = []
    new_current = []

    with open(file, 'r') as f:
        lines = f.readlines()

        # skip first 9 lines
        for l in lines[9:]:
            line = l.split(",")
            time.append(float(line[0]))
            current_pos.append(float(line[1]))
            corrected_pos.append(float(line[2]))
            current_shift.append(float(line[3]))
            current_current.append(float(line[4]))
            new_current.append(float(line[5]))

    return time, current_pos, corrected_pos, current_shift, current_current, new_current

def main(file: Path, niveau: int):
    time, current_pos, corrected_pos, current_shift, current_current, new_current = read_file(file)
    # make 2 subplots: one for the positions and one for the currents
    fig, (ax1, ax2) = plt.subplots(2, 1)

    # plot positions
    ax1.plot(time, current_pos, label="Current position")
    ax1.plot(time, corrected_pos, label="Corrected position")
    # plot niveau
    ax1.plot(time, [niveau for _ in range(len(time))], label="Niveau")
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Position (px)')
    ax1.set_title('Positions')
    ax1.legend()

    # plot currents
    ax2.plot(time, current_current, label="Current current")
    ax2.plot(time, new_current, label="New current")
    ax2.plot(time, current_shift, label="Current shift")
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Current (A)')
    ax2.set_title('Currents')
    ax2.legend()

    # show plot
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot dipole current')
    parser.add_argument('file', type=Path, help='Input file')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity level')
    parser.add_argument('-n', '--niveau', type=int, default=150, help='Niveau')
    args = parser.parse_args()
    main(file=args.file, niveau=args.niveau)