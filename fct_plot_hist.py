#!usr/bin/env python

import numpy as np
import os.path
import pylab as py
import matplotlib.pyplot as plt

def plotHIST( data, output_file_fig, plot_title, x_title, ind_hist, range_min, range_max, nb_steps, project ):
    print output_file_fig
    
    py.figure( edgecolor='r', linewidth=8 )
    tabLegende=[]
    myptab=[]
    
    py.title( plot_title, fontsize=16, fontweight = "bold" )
    py.xlabel( x_title, fontsize=16, fontweight = "bold" )
    py.ylabel( "Number of values", fontsize=16, fontweight = "bold" )
    #    py.ylim( y_min, y_max )    
    py.xlim( range_min, range_max )
    py.yticks( fontsize=12, rotation="vertical" )
    py.xticks( fontsize=12, fontweight = "bold" )
    py.grid( linestyle='-',which='both')
    py.axvline( x=range_min, linewidth=6, color='k'  )
    py.axvline( x=range_max, linewidth=6, color='k'  )
    py.axhline( y=0, linewidth=8, color='k'  )

    color_curve = "grey"
    color_curve = "blue"
#    color_curve = "green"
    color_curve = "red"
#    color_curve = "black"
#    color_curve = "brown"

    #  computation of mean

    min_valid = 0.01     #   aer
#    nb_steps = 41
    if range_max > 10:     #    pm
        min_valid = 0.1
#        nb_steps = range_max+1
    if range_max > 200:     #    anc Grimm
        min_valid = 0.1
#        nb_steps = range_max/10+1
    if range_max > 10000:     #    anc SMPS
        min_valid = 20.
        #        nb_steps = range_max/1000+1

#    ind_not99 = np.where( ( data[ :, ind_hist ] > min_valid ) & ( data[ :, ind_hist ] < range_max ) ) [0]   #   to get rid of -99. and 0 values
    ind_not99 = np.where( ( data[ :, ind_hist ] > range_min ) & ( data[ :, ind_hist ] < range_max ) & ( data[ :, ind_hist ] <> -99. ) ) [0]   #   to get rid of -99. and 0 values
    nb_values = np.shape( data[ ind_not99, ind_hist ] ) [0]

    print " ratio nb of physical values: ", nb_values, np.shape( data[ :, ind_hist ] ) [0]

    if nb_values <> 0:
        plt.hist( data[ ind_not99, ind_hist ], bins=np.linspace( range_min, range_max, num=nb_steps ), normed=False, color=color_curve, edgecolor='none' )

        print "min, max: ", np.min( data[ ind_not99, ind_hist ] ), np.max( data[ ind_not99, ind_hist ] )
        mean_value = -99.
        std_value = -99.
        mean_value = np.mean( data[ ind_not99, ind_hist ] )
        std_value = np.std( data[ ind_not99, ind_hist ] )
        print mean_value, std_value

        # to plot vertical lines 
        bins = np.linspace( range_min, range_max, num=nb_steps )
        top = np.max( np.histogram( data[ ind_not99, ind_hist ], bins=np.linspace( range_min, range_max, num=nb_steps ), normed=False ) [0] )

        y_mean = ( 0., 0.8*top )
        x_mean = ( mean_value, mean_value )
        x_mean_plus = ( mean_value+std_value, mean_value+std_value )
        x_mean_minus = ( mean_value-std_value, mean_value-std_value )
        
        mean_txt = " %5.0f +- %5.0f" % ( mean_value, std_value )
        if mean_value < 100:   #   pm05
            mean_txt = " %4.1f +- %4.1f" % ( mean_value, std_value )
        if mean_value < 5:   #   aer
            mean_txt = " %5.3f +- %5.3f" % ( mean_value, std_value )
        print "mean +- std dev: ", mean_txt
        print
        plt.text( mean_value, 0.82*top, mean_txt, fontsize=16, color='k', backgroundcolor='white' )

        py.plot( x_mean, y_mean, color='k', linewidth=2 )
        py.plot( x_mean_plus, y_mean, color='k', linestyle='--', linewidth=2 )
        py.plot( x_mean_minus, y_mean, color='k', linestyle='--', linewidth=2 )

        plt.text( bins[ 2 ], 0.9*top, project, fontsize=10, color = 'gray', fontstyle = 'italic', fontweight = 'bold' )

# alpha is for text transparency
        
        py.savefig( output_file_fig, bbox_inches = "tight" )
        py.close()
