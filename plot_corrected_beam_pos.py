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

def main(file: Path, cut: bool, begin: int , end: int):
    # TODO: Wenn Current auf 2.0 A -> nicht den Shift draufrechnen
    time, current_pos, corrected_pos, current_shift, current_current, new_current = read_data(file)

    not_controlled_pos = []

    # The first position is the initial position and is not controlled
    first_pos = current_pos[0]

    not_controlled_pos.append(first_pos)

    for i in range(len(current_shift)):
        # Skip the first one because it's the initial position
        if i == 0:
            continue
        # If the current is +- 2.0 A, the shift is not added
        if abs(current_current[i]) == 2.0:
            x_shift = 0
        else:
            x_shift = delta_I_to_delta_x(current_shift[i]) #-1
        not_controlled_pos.append(not_controlled_pos[i-1] - x_shift)

    # print length after calculation and cut if necessary
    if cut:
        print(f'Length of the controlled position: {len(corrected_pos[begin:end])}')
        print(f'Length of the not controlled position: {len(not_controlled_pos[begin:end])}')
        corrected_pos = corrected_pos[begin:end]
        not_controlled_pos = not_controlled_pos[begin:end]
        time = time[begin:end]
    print(f'Maximum of the controlled position: {max(corrected_pos)}')
    print(f'Maximum of the not controlled position: {max(not_controlled_pos)}')
    print(f'Minimum of the controlled position: {min(corrected_pos)}')
    print(f'Minimum of the not controlled position: {min(not_controlled_pos)}')
    print(f'Average of the controlled position: {sum(corrected_pos)/len(corrected_pos)}')
    print(f'Average of the not controlled position: {sum(not_controlled_pos)/len(not_controlled_pos)}')



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
    parser.add_argument('--cut', action='store_true', help='Cut the data with the specified beginning and end')
    parser.add_argument('--begin', type=int, help='Beginning of the window to cut the data')
    parser.add_argument('--end', type=int, help='End of the window to cut the data')
    args = parser.parse_args()

    main(args.file, args.cut, args.begin, args.end)