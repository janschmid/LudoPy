import fnmatch
import os
import re
from shutil import copyfile
"""This file is plotting the results."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties

def go(sourceDir="TestResults", targetDir="", pattern="Test_pl2_df_0.0_lr0.*.*", twoPlayerResults=False):
    """Plot results"""
    pltDpi = 900
    dataframes = []
    xAxisMax = 2000
    name = []
    axes = plt.gca()
    axes.set_ylim([0, 1])
    patternFileName = pattern.replace(".csv", "").replace(".", "_").replace("*", "x")
    for filename in os.listdir(sourceDir):
        if re.match(fnmatch.translate(pattern), filename):
            if sourceDir != targetDir:
                copyfile(os.path.join(sourceDir, filename), os.path.join(targetDir, filename))
            testResult = np.genfromtxt(os.path.join(sourceDir, filename), delimiter=",")
            # df = pd.DataFrame({'win': testResult[1], 'qTable':testResult[2]})
            if twoPlayerResults:
                df = pd.DataFrame({"win": testResult[1], "qTable": testResult[2], "winPl2": testResult[3]})
            else:
                df = pd.DataFrame({"win": testResult[1], "qTable": testResult[2]})
            dataframes.append(df)
            name.append(filename)
    if len(dataframes) == 0:
        print("Error, could not find file with pattern: " + pattern)
        return

    # for i in range(1, len(dataframes)):
    ax = None
    plt.figure()
    legend = []
    fontP = FontProperties()
    # if(len(dataframes)>10):
    # fontP.set_size('xx-small')

    for i in range(0, len(dataframes)):
        df = dataframes[i]
        df = df.expanding().mean()
        ax = df[("win")].plot(ax=ax)
        # legend.append("Discount factor: {0:.2f}, WR: {1:.3%}".format(float(name[i].split('df_')[1].split('_lr')[0]), df['win'].mean()))
        legend.append("Winning average Q-Player".format(int(name[i].split("pl")[1].split("_")[0]) - 1))
        if twoPlayerResults:
            ax = df[("winPl2")].plot(ax=ax)
            legend.append("Winning average Nathan Durocher's player")
        print("WinningRate: {0:.3%},   pattern: {1}".format(df["win"].mean(), name[i]))
    ax.legend(["New approach", "Old approach"], prop=fontP)
    ax.axis([0, xAxisMax, 0, 1])
    # title = "Average winning rate against random player(s)"
    title = "Average winning rate against Nathan Durocher's player"
    plt.title(title)
    plt.savefig(os.path.join(targetDir, title.replace(":", "") + patternFileName + ".png"), dpi=pltDpi)
    plt.close()

    ax = None
    plt.figure()
    legend = []
    title = "Q-table change"
    for i in range(0, len(dataframes)):
        df = dataframes[i]
        df = df.rolling(window=5).mean()
        ax = df[("qTable")].plot(ax=ax)
        legend.append("Learning rate: {0}".format(float(name[i].split("lr")[1].split("_")[0])))
        # legend.append(name[i]+"  Mean: {:.3%}".format(df['qTable'].mean()))
    ax.legend(legend, prop=fontP)
    ax.axis([0, 500, 0, 1])
    plt.title(title)
    plt.savefig(os.path.join(targetDir, title.replace(":", "_") + patternFileName + ".png"), dpi=pltDpi)
    plt.close()


if __name__ == "__main__":
  
    go(pattern="*pl*.csv", sourceDir="TestResults", targetDir="TestResults", twoPlayerResults=False)
 
