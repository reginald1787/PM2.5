#!/bin/env python

import numpy as np
import os.path
import pylab as py
import matplotlib.pyplot as plt

import fct_plot_hist


def plot( name_yyyymm, reso, output_dir_fig, output_name_1, plot_title_1, plot_title_2, title_yyyymm, x_title, owner, i_hist, range_min, range_max, nb_steps, regimes, ind_regimes, data ):

  nb_curves = np.shape( regimes ) [0]
  print; print x_title; print nb_curves
  
  for i_curve in range( 0, nb_curves ):
    regime = regimes[ i_curve]
    title_regime = regime
    ind_data = ind_regimes[ i_curve ]
    print i_curve, regime

    if regime == "ct1":
      title_regime = "Cloud-free from MSG"
    if regime == "ct2":
      title_regime = "Very low clouds from MSG"
    if regime == "ct3":
      title_regime = "Low clouds from MSG"
    if regime == "ct4":
      title_regime = "Medium clouds from MSG"
    if regime == "ct5":
      title_regime = "High thick clouds from MSG"
    if regime == "ct6":
      title_regime = "Thin cirrus from MSG"
    if regime == "ct7":
      title_regime = "Scattered clouds from MSG"
    if regime == "poll":
      title_regime = "Pollution event"
      
    plot_title_3 = title_regime + title_yyyymm
    output_name_fig = name_yyyymm + "_" + regime + reso + ".png"
    output_file_fig_h = output_dir_fig + output_name_1 + output_name_fig
    plot_title = plot_title_1 + plot_title_2 + plot_title_3
    fct_plot_hist.plotHIST( data[ ind_data ], output_file_fig_h, plot_title, x_title, i_hist, range_min, range_max, nb_steps, owner )


