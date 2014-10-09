#!usr/bin/env python

import numpy as np
import os.path
import pylab as py
import matplotlib.pyplot as plt

def plotTS_sevC( data, output_file_fig, nb_curves, plot_title, x_title, y_title, i_x, x_min, x_max, x_ticks, ind_y, y_min, y_max, y_ticks, labels, lab_pos, owner ):
    print output_file_fig

    plot_yes = 0

    py.figure( 1, figsize = ( 16, 8 ) )
    tabLegende=[]
    myptab=[]

    color_curve = [ 'k', 'g', 'r', 'm', 'b', 'k', 'r', 'b' ]
    color_curve = [ 'k', 'g', 'r', 'm', 'b', 'grey', 'r', 'b' ]
    curve_lw = [ 6, 2, 2, 2, 2, 4, 2, 2 ]
    curve_lw = [ 4, 4, 4, 4, 4, 4, 2, 2 ]
    curve_ls = [ '-', '-', '-', '-', '-', ':', '--', '--' ]
    curve_ls = [ '-', '--', '--', '--', '--', '-', '--', '--' ]
    mymarkers = [ 'none', 'none', 'none', 'none', 'none', 'o', 'none', 'none' ]
    mymarkers = [ 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none' ]

    color_curve = [ 'k', 'g', 'r', 'b', 'm', 'grey', 'r', 'b' ]
    curve_ls = [ '--', '--', '--', '--', '--', '--', '--' ]
    curve_lw = [ 2, 2, 2, 2, 2, 2, 2, 2 ]
    mymarkers = [ 's', 'x', '^','o', '+', 'o', 'none' ]

    py.title( plot_title, fontsize=16, fontweight = "bold" )
    py.xlabel( x_title, fontsize=16, fontweight = "bold" )
    py.ylabel( y_title, fontsize=16, fontweight = "bold" )
    
    py.grid( linestyle='-',which='both')
    py.axhline( y=y_min, linewidth=6, color='k'  )
    py.axhline( y=y_max, linewidth=6, color='k'  )
    py.axvline( x=x_min, linewidth=6, color='k'  )
    py.axvline( x=x_max, linewidth=6, color='k'  )
    
    py.xlim( x_min, x_max )
    py.xticks( x_ticks )
    py.ylim( y_min, y_max )
    py.yticks( y_ticks )
    
    plt.text( x_min*1.05, y_max*0.6, owner, fontsize=10, color = '0.4', fontstyle = 'italic', fontweight = 'bold' )

    # --------------------------------------------

    if nb_curves >> 1:
        for i_curve in range( 0, nb_curves ):
            ind_not99 = np.where( data[ :, ind_y[ i_curve ] ] > y_min ) [0]
            nb_pos = np.shape( ind_not99 ) [0]  # nb of positive values
            print i_curve, nb_pos
            if nb_pos > 0:
                plot_yes = 1
                py.plot( data[ ind_not99, i_x ], data[ ind_not99, ind_y[ i_curve ] ], color_curve[ i_curve ], linewidth=curve_lw[ i_curve ], linestyle = curve_ls[ i_curve ], marker = mymarkers[ i_curve ], markersize=8, markeredgewidth=1, markerfacecolor='grey', markeredgecolor=color_curve[ i_curve ], label=labels[ i_curve ] )
#                plt.bar( data[ ind_not99, i_x ], data[ ind_not99, ind_y[ i_curve ] ], color=color_curve[ i_curve ], width=0.25, linewidth=0, label=labels[ i_curve ] )

    if nb_curves == 1:
        ind_not99 = np.where( data[ :, ind_y[ 0 ] ] > y_min ) [0]
        nb_pos = np.shape( ind_not99 ) [0]  # nb of positive values
        print nb_pos
        if nb_pos > 0:
            plot_yes = 1
            py.plot( data[ ind_not99, i_x ], data[ ind_not99, ind_y[ 0 ] ], 'r', linewidth=2, linestyle = '--', marker = 'o', markersize=8, markeredgewidth=1, markerfacecolor='grey', markeredgecolor='k', label=labels[ 0 ] )


    if nb_curves > 1:
#        py.legend( loc = lab_pos, labelspacing = 0.1, numpoints=2, handlelength=2, prop={'size':10} )
        py.legend( loc = lab_pos, labelspacing = 0.1, numpoints=2, handlelength=2, prop={'size':12} )

    if plot_yes == 1:
        py.savefig( output_file_fig, bbox_inches = "tight" )
        
    py.close( 1 )
