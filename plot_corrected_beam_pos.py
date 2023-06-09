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

def delta_I_to_delta_x(delta_I: float):
    # Output of calibration:
    # x(I) = -45.796722 * I + 410.90
    # y(I) = -0.210579 * I + 342.08
    # I(x) = -0.021836 * x + -8.97
    # I(y) = -4.748816 * y + -1624.48
    return -45.796722 * delta_I

def main(file: Path):
    time, current_pos, corrected_pos, current_shift, current_current, new_current = read_data(file)

    not_controlled_pos = []

    # The first position is the initial position and is not controlled
    first_pos = current_pos[0]

    not_controlled_pos.append(first_pos)

    for i in range(len(current_shift)):
        # Skip the first one because it's the initial position
        if i == 0:
            continue
        x_shift = delta_I_to_delta_x(current_shift[i]) #-1
        not_controlled_pos.append(not_controlled_pos[i-1] - x_shift)
        # not_controlled_pos.append(not_controlled_pos[i-1])

    # Einzelner plot vllt besser? Strom von I0SH03 Schwierig zu bekommen    

    # # plot the not controlled position and the corrected position
    # fig, (ax1, ax2) = plt.subplots(2, 1)

    # # plot 1: Niveau, not controlled pos, controlled pos
    # # ax1 plot niveau at 150
    # ax1.axhline(y=150, color='r', label='Niveau')
    # ax1.plot(time, not_controlled_pos, label='Not controlled')
    # ax1.plot(time, corrected_pos, label='Controlled')
    # ax1.set_ylabel('x (px)')
    # ax1.legend()


    # #TODO: Stadessen unterer plot: current vom regelnden und störenden steerer
    # # plot 2: current shift, current current, new current
    # ax2.plot(time, current_current, label='Current I0SH04')
    # # TODO: Woher I0SH03?
    # ax2.set_ylabel('Current (A)')
    # ax2.set_xlabel('Time (s)')
    # ax2.legend()

    plt.axhline(y=150, color='r', label='Niveau')
    plt.plot(time, not_controlled_pos, label='Not Controlled')
    plt.plot(time, corrected_pos, label='Controlled')
    plt.ylabel('x (px)')
    plt.xlabel('Time (s)')
    plt.legend()

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot beam pos with and without controller')
    parser.add_argument('file', type=Path, help='Path to file')
    args = parser.parse_args()

    main(args.file)