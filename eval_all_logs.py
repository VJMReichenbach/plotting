# 	Packages

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

#	Functions

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

def deltaI_zu_deltaX(deltaI):
	return 28.78992376 * deltaI # + 151.9469296655137

def mean(liste):
    return sum(liste)/len(liste)

############################################################
#
#	main

measurements = ["data/log_mix.txt","data/log_normal.txt","data/log_sin_1A.txt","data/log_sin_2A.txt"]

for measurement in range(len(measurements)):

    time, pos, _, _, cur, _ = read_data(measurements[measurement])
    niveau = 150

    # 	calculate position shifts

    last_pos = pos[0]
    last_cur = cur[0]

    shifts_pos = []
    shifts_cur = []
    shifts_pos_uncontr = []

    pos_uncontr = [last_pos]

    for i in range(0,len(time)):

        if i == 0:
        	continue

        shift_pos = pos[i]-last_pos
        shift_cur = cur[i]-last_cur
        shift_pos_uncontr = deltaI_zu_deltaX(shift_cur)

        shifts_pos.append(shift_pos)
        shifts_cur.append(shift_cur)
        shifts_pos_uncontr.append(shift_pos_uncontr)
        pos_uncontr.append(pos_uncontr[i-1] + shift_pos_uncontr)
        
        last_pos = pos[i]
        last_cur = cur[i]

    #	Calibration pixel -> mm
    a = 20/216
    b = -150*20/216

    pos = [a*x+b for x in pos] 
    pos_uncontr = [a*x+b for x in pos_uncontr] 

    # Stds

    std_pos = np.std(pos)
    std_pos_uncontr = np.std(pos_uncontr)

    x = np.linspace(min(time),max(time), 20)

    # 	Plots

    sigma_interval_min = (mean(pos)-2*std_pos)
    sigma_interval_max = (mean(pos)+2*std_pos)
    print(f"Measurment: {measurement}")
    print(f"$2\, \sigma$ Abweichung min: {sigma_interval_min}")
    print(f"$2\, \sigma$ Abweichung max: {sigma_interval_max}")
    print()

    fig, axs = plt.subplots(1, 1, sharex=True,dpi=300)
    #plt.title(measurements[measurement].replace("log_","").replace(".txt",""))
    axs.set_xlabel("Zeit t in s")
    axs.set_ylabel("Horizontale Strahlposition in mm")
    plt.plot(time,pos,label="Geregelter Strahlverlauf")
    plt.plot(time,pos_uncontr,label="Ungeregelter Strahlverlauf")
    axs.hlines(0,min(time),max(time),color="black",label="Sollwert")
    axs.fill_between(x, sigma_interval_min, sigma_interval_max, color='blue', alpha=.1,label="$2\, \sigma$ Abweichung")
    #axs.fill_between(x, (mean(pos_uncontr)-1*std_pos_uncontr), (mean(pos_uncontr)+1*std_pos_uncontr), color='gray', alpha=.1,label="$1\, \sigma$ interval")
    plt.legend()
    plt.savefig(measurements[measurement].replace("log_","").replace(".txt","") + ".png",dpi=300)
    plt.show()









