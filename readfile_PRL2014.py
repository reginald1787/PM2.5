#!usr/bin/env python
# -*- coding: latin-1 -*-

#  
#  computing parameters for CSP performance

import os
import glob
import filecmp
import shutil
import sys
import numpy as np
from getopt import getopt
#sys.path.append( "./Utils" )
#sys.path.append( "/home/telias/Prg/Libr/Python" )
import pylab as py
import datetime
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.pyplot as plt

import fct_plot_hist
import fct_plot_hist_regimes
import fct_plot_timeSeries_sevC_absc

from os.path import expanduser
home = expanduser("~"); print (home)


# ---------------------------------
# input data

#year = 2011
#month = 03
#year = int( sys.argv[ 1 ] )

# dir_yyyymm = "%04d/%02d/" % ( year, month )
# name_yyyymm = "_%04d%02d" % ( year, month )
# title_yyyymm = ". %04d%02d" % ( year, month )
#dir_yyyymm ="%04d" % year
# name_yyyymm ="_%04d" % year
# title_yyyymm ="%04d" % year

reso="_15min"
owner = "HYGEOS"
#output_dir_fig = "../data/output/"
output_dir_fig = ""

i_nod = 2
i_dh = 3
i_aot500 = 4
i_aot870 = 5
i_pm25 = 9

#input_file = "../data/input/data_AOT_VISI_PM.dat"
input_file = "data_AOT_VISI_PM.dat"
print input_file
data = np.loadtxt( input_file ) 
#print np.shape( data )

##-----------------truncate data---------------------------------------------
#  extract single yearly data from original data


def findyear (year):
	n = np.shape(data)[0]
	start = -1
	end = -1
	i = 0
	while i < n:
		if str(year) in str(data[i,0]):
			start = i
			#print i, data[i,0]
			j = i+1
			while j < n and str(year) in str(data[j,0]):
				j+=1
			end = j	
			#print j, data[j,0]
			break
		i+=1
	return data[start:end,:]


#data = findyear(data,year)
#print np.shape(data)

##-----------------------------------------------------------------------------------------
##--------------------frequent analysis---------------------

# def frequent_analysis(data):

# 	date = data[ :, 0 ]
# 	time = data[ :, 1 ]
# 	nod = data[ :, i_nod ]   #  number of the day
# 	dh = data[ :, i_dh ]    #   decimal hour
# 	aot500 = data[ :, i_aot500 ]     #   
# 	aot870 = data[ :, i_aot870 ]    #   aot at 870 nm
# 	ae = data[ :, 6 ]     #   Angstrom exponent
# 	visi = data[ :, 7 ]     #   visibility (m)
# 	pec = data[ :, 8 ]    #  particle extinction coefficient (Mm-1)
# 	pm25 = data[ :, i_pm25 ]   # microg/m3


# 	ind_allDay = np.where( ( data[ :, i_dh ] > 0. ) ) [0]; nb_allDay = np.shape( ind_allDay ) [0]
# 	ind_morn = np.where( ( data[ :, i_dh ] <= 12. ) ) [0]; nb_morn = np.shape( ind_morn ) [0]
# 	ind_aft = np.where( ( data[ :, i_dh ] > 12. ) ) [0]; nb_aft = np.shape( ind_aft ) [0]

# 	#print aot500,pm25

# 	aot500_mean = np.mean(aot500[aot500>0])
# 	aot500_std = np.std(aot500[aot500>0])
# 	pm25_mean = np.mean(pm25[pm25>0])
# 	pm25_std = np.std(pm25[pm25>0])

# 	return [aot500_mean,aot500_std,pm25_mean,pm25_std]

# tmp = []
# for month in ["01","02","03","04","05","06","07","08","09","10","11","12"]:
# 	year = "2013"+month
# 	newdata = findyear(data,year)
# 	#print frequent_analysis(newdata) 
# 	tmp.append(frequent_analysis(newdata))

# tmp = np.array(tmp,dtype = np.float32)
# print tmp

# plt.figure(1)
# plt.plot(range(1,13),tmp[:,0], c='r', marker='*')
# plt.plot(range(1,13),tmp[:,0] - tmp[:,1], c='g', marker='>')
# plt.plot(range(1,13),tmp[:,0] + tmp[:,1], c='b', marker='<')

# ##plt.figure(2)
# #plt.scatter(range(1,13),tmp[:,2],'r',tmp[:,2] - tmp[:,3], tmp[:,2] + tmp[:,3],'b')

# plt.show()

##----------------------------------------Daily Cycle------------
##
##----------------------------------------------------------------


def DailyCycle(month):

	def getData(year):
		#year = "201003"
		newdata = findyear(year)
		days = np.shape(newdata)[0]/96
		#dh = float(newdata[ :, i_dh ])    #   decimal hour
		aot500 = np.array(newdata[ :, i_aot500 ],dtype = np.float)     #   
		#aot870 = newdata[ :, i_aot870 ]    #   aot at 870 nm
		pm25 = np.array(newdata[ :, i_pm25 ],dtype = np.float)   # microg/m3

		y_axis_pm25 = np.zeros(96)
		y_axis_aot500 = np.zeros(96)

		for i in range(len(pm25)):
			if pm25[i]> -0.1:
				y_axis_pm25[i%96] += pm25[i]
			if aot500[i]> -0.1:
				y_axis_aot500[i%96] += aot500[i]

		# print pm25
		y_axis_pm25 /= days
		y_axis_aot500 /= days

		y_pm = np.zeros(24)
		y_aot = np.zeros(24)
		i = 0
		j=0
		while i<24:
			y_pm[i] = np.mean(y_axis_pm25[j:j+4])
			y_aot[i] = np.mean(y_axis_aot500[j:j+4])
			i+=1
			j+=4

		return y_pm,y_aot

	x_axis = np.arange(0.00,24.00,1.00)
	plt.figure(1)
	for year,c in zip(["%s" %("201"+str(i)+month) for i in range(0,5)],['b','r','g','y','m']):
		y_pm, y_aot = getData(year)
		plt.plot(x_axis,y_pm, c=c, marker='*',label = year)
	
	plt.ylabel("PM2.5")
	plt.xlabel("time (24 hrs)")
	plt.title(month)
	plt.legend(loc='upper right', prop={'size':10})

	plt.figure(2)
	for year,c in zip(["%s" %("201"+str(i)+month) for i in range(0,5)],['b','r','g','y','m']):
		y_pm, y_aot = getData(year)
		plt.plot(x_axis,y_aot, c=c, marker='*', label = year)
	
	plt.ylabel("AOT")
	plt.xlabel("time (24 hrs)")
	plt.title(month)
	plt.legend(loc='upper right', prop={'size':10})

	plt.show()


# figures

# fig time series
# output_name_1 = "fig_aot500and870_ts"
# output_name_fig = name_yyyymm + reso + ".png"
# output_file_fig_ts = output_dir_fig + output_name_1 + output_name_fig
# plot_title = "Time series of AOT" + name_yyyymm
# y_title = "AOT at 500 nm and 870 nm"
# x_title = "number of the day"
# i_x = i_nod
# nb_curves = 2; ind_y = ( i_aot500, i_aot870 )
# y_min = 0; y_max = 1; y_ticks = [ 0, 0.5, 0.75, 1 ]
# x_min = 420; x_max = 460; x_ticks = [ 420, 430, 440, 450, 460 ]
# labels = [ "500 nm", "870 nm" ]; lab_pos = "upper left"
# fct_plot_timeSeries_sevC_absc.plotTS_sevC( data, output_file_fig_ts, nb_curves, plot_title, x_title, y_title, i_x, x_min, x_max, x_ticks, ind_y, y_min, y_max, y_ticks, labels, lab_pos, owner )

# output_name_2 = "fig_pm25_ts"
# output_name_fig = name_yyyymm + reso + ".png"
# output_file_fig_ts = output_dir_fig + output_name_2 + output_name_fig
# plot_title = "Time series of PM25" + name_yyyymm
# y_title = "PM25"
# x_title = "number of the day"
# i_x = i_nod
# nb_curves = 1; ind_y = ( i_pm25, i_pm25 )
# y_min = 0; y_max = 150; y_ticks = [ 0, 50, 100, 150 ]
# x_min = 420; x_max = 460; x_ticks = [ 420, 430, 440, 450, 460 ]
# labels = [ "PM25" ]; lab_pos = "upper left"
# fct_plot_timeSeries_sevC_absc.plotTS_sevC( data, output_file_fig_ts, nb_curves, plot_title, x_title, y_title, i_x, x_min, x_max, x_ticks, ind_y, y_min, y_max, y_ticks, labels, lab_pos, owner )

# # frequency distribution
# range_min = 0; range_max = 1; nb_steps = 51
# i_hist = i_aot500
# output_name_1 = "fig_aot500_hist"
# x_title = "AOT at 500 nm, from AERONET"
# plot_title_1 = "Frequency distribution of AOT.\n"
# plot_title_2 = "" 

# regimes = [ "morning", "afternoon", "allDay" ]
# ind_regimes = [ ind_morn, ind_aft, ind_allDay ]
# fct_plot_hist_regimes.plot( name_yyyymm, reso, output_dir_fig, output_name_1, plot_title_1, plot_title_2, title_yyyymm, x_title, owner, i_hist, range_min, range_max, nb_steps, regimes, ind_regimes, data )

if __name__ == '__main__':
	DailyCycle("03")



	
