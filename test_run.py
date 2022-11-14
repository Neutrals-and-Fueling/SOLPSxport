#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:50:01 2022

@author: mslaishram
"""
import os
import shutil

path_to_SOLPSxport="/sciclone/data10/mslaishram/solps-iter/SOLPSxport"
os.chdir(path_to_SOLPSxport)
from SOLPSxport_dr_case1 import *

path_main="/sciclone/data10/mslaishram/solps-iter/runs/d3d/1_g175886.02267/Attempt_4"
os.chdir(path_main)

path_to_EXp_data="/sciclone/data10/mslaishram/solps-iter/runs/d3d/gfiles_pfiles_datas"
gfile_loc = os.path.join(path_to_EXp_data,'g175886.02267')
pklfile_loc=os.path.join(path_to_EXp_data,'175886_2250_f8099.pkl')


xp=main(gfile_loc = gfile_loc, new_filename='b2.transport.inputfile_new', 
     profiles_fileloc=pklfile_loc, shotnum=None, ptimeid=None, prunid=None,
     nefit='tanh', tefit='tanh', ncfit='spl', chii_eq_chie = False,
     Dn_min=0.001, vrc_mag=0.0, ti_decay_len=0.015, Dn_max=20,
     ke_use_grad = False, ki_use_grad = True,
     chie_min = 0.01, chii_min = 0.01, chie_max = 200, chii_max = 200,
     reduce_Ti_fileloc='/fusion/projects/results/solps-iter-results/wilcoxr/T_D_C_ratio.txt',
     carbon=False, use_existing_last10=False, plot_xport_coeffs=True,
     plotall=False, verbose=False, figblock=False)






#SOLPSxport_dr.py -g gfile_loc -p pklfile_loc



