#!usr/bin/env python
# -*- coding: latin-1 -*-

#  
#  computing parameters for CSP performance


import numpy as np
import pandas as pd
import pylab as py
import operator
import matplotlib.pyplot as plt



# ---------------------------------
# -----------read data---------------
# ----------------------------------


# i_nod = 2
# i_dh = 3
# i_aot500 = 4
# i_aot870 = 5
# i_pec = 8
# i_pm25 = 9

#input_file = "../data/input/data_AOT_VISI_PM_all2.dat"
input_file = "data_AOT_VISI_PM_all.dat"
print input_file
#column_names = ['date', 'time']
data = pd.read_csv(input_file, header=None, sep=r"\s+")
data.columns = ['date', '1', '2','time','aot500','aot870','6','7',
                'pec','pm25','10','11','12','13','14']

#-------------------------------------------------------------------------
##-----------------data operations---------------------------------------------
#-------------------------------------------------------------------------
#  extract single yearly data from original data


def select(data, date, x_axis):

    subtable = data[(data.date >= date*100) & (data.date < date*100+100) & (data.aot500 >0) & (data.pec > 0)]
    #print subtable
    mydata_mean = [subtable[subtable.time==dh].mean(axis = 0).pec for dh in x_axis]
    mydata_std = [subtable[subtable.time==dh].std(axis = 0).pec for dh in x_axis]

   

    return mydata_mean, mydata_std

#-------------------------------------------------------------------------
#-----------------------draw plots--------------------------------------------------
#-------------------------------------------------------------------------

x_axis = np.arange(7.25,16.75,.25)
#x_axis = np.arange(0.00,24.00,0.25)

plt.figure(1)


month = 03
for year,c in zip(range(2010,2011),['b','r','g','y','m']):
#color = ['b','r','g','y','m']

    date = year*100+month
    y_mean, y_std = select(data, date, x_axis)
   
    plt.plot(x_axis,y_mean, c=c, marker='*',label = "%s" %date)
    #plt.plot(x_axis,map(operator.sub, y_mean,y_std), c=c, marker='_',label = 'mean-std')
    #plt.plot(x_axis,map(operator.add, y_mean,y_std), c=c, marker='+',label = 'mean+std')

plt.xlim([0,24])
plt.ylim([0,800])
plt.ylabel("AOT")
plt.xlabel("time (24 hrs)")
plt.title("Diurnal Cycle of AOT "+ "%s" %date)
plt.legend(loc='upper right', prop={'size':10})

plt.show()


