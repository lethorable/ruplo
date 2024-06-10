import argparse
import os,sys
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter
import pandas as pd




parser = argparse.ArgumentParser(description="Extract quality parameters")
parser.add_argument("input_file", help="Input file")
parser.add_argument("-o",dest="output file",help="Enter png to output, if omitted output is to screen",default="screen")








def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[n:] - cumsum[:-n]) / float(n)


def main(args):
    pargs = parser.parse_args(args[1:])
    fnam = pargs.input_file
    ga = np.array([])
    gp = np.array([])

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

#            v1 = l[261:276].strip()
#            if v1 !='':
#                f1.append(float(v1))


#            v1 = l[280:295].strip()
#            if v1 !='':
#                f1.append(float(v1))

#            v1 = l[296:310].strip()
#            if v1 !='':
#                f1.append(float(v1))

#            v1 = l[310:322].strip()
#            if v1 !='':
#                f1.append(float(v1))

            if l[0]=='G' and headerdone:
                b=l.split()
                v1 = l[261:276].strip()
                if v1 !='':
                    f2.append(float(v1))




            if l[0]=='>': # > 2024 05 16 00 03 00.0000000  0 55
                ti=ti+1
                headerdone = True
            #print (f1)
                a=l.split(' ')
                currtime = a[1]+'-'+a[2]+'-'+a[3]+'-'+a[4]+'-'+a[5]+'-'+a[6]
            #print (currtime)
                if np.mean(f1)<40:
                    print(currtime)
                ga= np.append(ga, [np.mean(f1)])
                gp= np.append(gp, [np.mean(f2)])
                f1=[]
                f2=[]


    f.close()

    n=25
    filtered_ga = pd.Series(ga).rolling(window=n).mean().iloc[n-1:].values
    filtered_gp = pd.Series(gp).rolling(window=n).mean().iloc[n-1:].values





    plt.title(fnam, fontsize = 8, style = 'italic')
    plt.xlabel("time (x30 sec)")
    plt.ylabel("Sig str")

    plt.ylim((34,46))
    plt.axhline(y=40.5, color='tab:orange', linestyle='--', alpha=0.5)

    plt.plot(filtered_ga, label='Ga')
    plt.plot(filtered_gp, color=(0.1, 0.1, 0.1, 0.15), label='Gp')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
