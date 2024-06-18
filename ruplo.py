import argparse
import os,sys
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter
import pandas as pd

#NB! Udpakning fra gz sker med 7zip
#NB! Konvertering til rnx sker med kommandoen rinex-decompress. Installeres med pip install hatanaka

parser = argparse.ArgumentParser(description="Plot quality parameters from Rinex (C1S)")
parser.add_argument("input_file", help="Input file")
#parser.add_argument("-o",dest="output file",help="Enter png to output, if omitted output is to screen",default="screen")


def main(args):
    pargs = parser.parse_args(args[1:])
    fnam = pargs.input_file
    gal = np.array([])
    gps = np.array([])

    ti=0
    f1=[]
    f2=[]


    headerdone=False

    with open(fnam,"r") as f:
        for l in f:
            if l[0]=='E' and headerdone:
                #print (l)
                a=l.split()
                #print(a)
                v1 = l[245:260].strip()
                if v1 !='':
                    f1.append(float(v1))


            if l[0]=='G' and headerdone:
                b=l.split()
                v1 = l[261:276].strip()
                if v1 !='':
                    f2.append(float(v1))




            if l[0]=='>': # > 2024 05 16 00 03 00.0000000  0 55
                ti=ti+1
                headerdone = True
                a=l.split(' ')
                currtime = a[1]+'-'+a[2]+'-'+a[3]+'-'+a[4]+'-'+a[5]+'-'+a[6]
#                if np.mean(f1)<40:
#                    print(currtime)
                gal= np.append(gal, [np.mean(f1)])
                gps= np.append(gps, [np.mean(f2)])
                f1=[]
                f2=[]

    f.close()

    n=25
    filtered_gal = pd.Series(gal).rolling(window=n).mean().iloc[n-1:].values
    filtered_gps = pd.Series(gps).rolling(window=n).mean().iloc[n-1:].values





    plt.title(fnam, fontsize = 8, style = 'italic')
    plt.xlabel("time (x30 sec)")
    plt.ylabel("Signal strength")

    plt.ylim((34,46))
    plt.axhline(y=40.5, color='tab:orange', linestyle='--', alpha=0.5)

    plt.plot(filtered_gal, label='Galileo')
    plt.plot(filtered_gps, color=(0.1, 0.1, 0.1, 0.15), label='GPS')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
