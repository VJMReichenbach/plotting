import argparse
from pathlib import Path
from os.path import isdir, isfile
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import datetime
import cv2
from tqdm import tqdm

def gaussian(x, a, x0, sigma):
    """The gaussian function used for fitting"""
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


def getXValues(img: np.ndarray, threshold: int):
    """Returns the light intensity for each row in image img"""
    xValues = []
    for x in range(img.shape[1]):
        currentVal = 0
        for y in range(img.shape[0]):
            if img[y, x] > threshold:
                currentVal += img[y, x]
        xValues.append(currentVal)
    return xValues


def getYValues(img: np.ndarray, threshold: int):
    """Returns the light intensity for each column in image img"""
    yValues = []
    for y in range(img.shape[0]):
        currentVal = 0
        for x in range(img.shape[1]):
            if img[y, x] > threshold:
                currentVal += img[y, x]
        yValues.append(currentVal)
    return yValues

def fitGaussian(xValues: list):
    """Fits a gaussian to the data and returns the fit curve"""
    x = np.arange(0, len(xValues), 1)
    # increased the maxfev value since the fit failed otherwise
    # TODO: parameter for gaus fit 
    popt, pcov = curve_fit(gaussian, x, xValues, p0=[1, 0, 1], maxfev=100000)
    # PArameter:
    # a = aplitude --> max value of array
    # x0 = center --> position of max value
    # sigma = width --> manuelly set
    xGauss = gaussian(x, *popt)
    return xGauss

def main(folder: Path, background: Path, verbose: int, all: bool, threshold: int, output: Path):
    time = []
    xValues = []
    yValues = []
    background = cv2.imread(str(background), cv2.IMREAD_GRAYSCALE)

    # crop margin
    left = 250 
    right = 180 
    top = 140 
    bottom = 220 

    i = 0
    with tqdm(total=len(list(folder.iterdir()))) as pbar:
        for file in folder.iterdir():
            # get time from filename
            # filename format: 2023-02-23_15:55:52.50.jpg
            t = file.name.split(".jpg")[0]
            # convert to milliseconds via datetime
            t = datetime.datetime.strptime(t, "%Y-%m-%d_%H:%M:%S.%f").timestamp() * 1000
            time.append(t)

            # load image
            img = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)
            # subtract background
            img = cv2.subtract(img, background)
            # crop margin
            v, h = img.shape
            img = img[top:v-bottom, left:h-right]
            # median blur
            img = cv2.medianBlur(img, 3)

            # get x and y values
            x = getXValues(img, threshold)
            y = getYValues(img, threshold)

            # fit gaussians
            xGauss = fitGaussian(x)
            yGauss = fitGaussian(y)

            # get mean of gaussians
            xMean = np.mean(xGauss)
            yMean = np.mean(yGauss)

            # append to list
            xValues.append(xMean)
            yValues.append(yMean)

            # update progress bar
            pbar.update(1)

            if verbose > 1:
                print(f"{file.name}({t}): x={xMean}, y={yMean}")

        if all:
            # plot all values
            plt.plot(time, xValues, label="x")
            plt.plot(time, yValues, label="y")

        # write values to csv file
        with open(output, "w") as f:
            f.write("time,x,y\n")
            for i in range(len(time)):
                f.write(f"{time[i]},{xValues[i]},{yValues[i]}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts the beam position from a collection of photos and plots it. Input has to be a folder, containing the photos. They have to be named like this: "2023-02-23_15:55:52.50.jpg"')
    parser.add_argument('folder', type=Path, help='Input folder')
    parser.add_argument('background', type=Path, help='Background image')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity level')
    parser.add_argument('-a', '--all', action='store_true', help='Show plot the entire file')
    parser.add_argument('-t', '--threshold', type=int, default=20, help='Threshold for the light intensity')
    parser.add_argument('-o', '--output', type=Path, default="output.csv", help='Output file')
    args = parser.parse_args()

    if not isdir(args.folder):
        print(f"The given folder \"{args.folder}\" is not a directory.")
        exit(1)
    
    if not isfile(args.background):
        print(f"The given background image \"{args.background}\" is not a file.")
        exit(1)

    if isfile(args.output):
        print(f"The given output file \"{args.output}\" is already a file.")
        exit(1)

    main(folder=args.folder, background=args.background, verbose=args.verbose, all=args.all, threshold=args.threshold, output=args.output)