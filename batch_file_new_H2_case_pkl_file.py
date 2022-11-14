
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

from SOLPSxport_dr import *

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#path to datas and working folders

path="/sciclone/data10/mslaishram/solps-iter/runs/d3d/H2_g183508.05317_H_case_pklfile"
path_old1="/sciclone/data10/mslaishram/solps-iter/runs/d3d/H2_g183508.05317_H_case_pklfile/Attempt_0"

path_to_EXp_data="/sciclone/data10/mslaishram/solps-iter/runs/d3d/gfiles_pfiles_datas"
gfile_loc = os.path.join(path_to_EXp_data,'g183508.05317')
pklfile_loc=os.path.join(path_to_EXp_data,'183508_5300_e8099.pkl')

#setenv B2PLOT_DEV ps                                        setenv B2PLOT_DEV ps
#echo $B2PLOT_DEV
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
def batch_file_for_job_submission(j):
    path_init= os.path.join(path, 'Attempt_' + str(j))
    os.chdir(path_init)
    # workdir=os.getcwd()

    f = open('batchfile_for_stopping_cond', 'w')
    
    f.writelines(['#!/bin/tcsh','\n#PBS -l nodes=1:hima:ppn=1',\
                  '\n#PBS -l walltime=4:0:00',f'\n#PBS -N Attempt_{j}',\
                      '\n#PBS -j oe','\n'])
     
    f.writelines(['\necho "Attempt_{} job Submitted!" | mail -s "job Submitted!" mslaishram@wm.edu'.format(j)])    
    #f.writelines(['\necho "Attempt_+ str(j) job submitted!" | mail -s "job submitted!" mslaishram@wm.edu' ])
    f.writelines(['\nenv'])
    f.writelines(['\ncd {}/Attempt_{} \n'.format(path,j)])    
    #f.writelines([f'\ncd path_init'])
    f.writelines(['\nb2run b2mn > run.log'])
    
    #f.writelines(['\necho "Attempt_+str(j) job completed!" | mail -s "job finished!" mslaishram@wm.edu' ])
    #f.writelines(['\necho "Attempt_{j} job completed!" | mail -s "job finished!" mslaishram@wm.edu' ])
    f.writelines(['\necho "Attempt_{} job completed!" | mail -s "job finished!" mslaishram@wm.edu'.format(j)])
    #f.writelines(['\ncp b2.transport.inputfile test_file_{} \n'.format(j)]) 
    f.writelines(['\ncp b2.transport.inputfile test_file_i.txt \n'])   

    f.close()
    # print("the batch_iteration is running for j = " , j)

    os.system('qsub batchfile_for_stopping_cond') 
#-sync y 
#    os.system('qsub -sync y batchfile_for_stopping_cond') 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def Run_SOLPSXport_and_generate_transport_inputfile_new():
    xp=main(gfile_loc = gfile_loc, new_filename='b2.transport.inputfile_new', 
         profiles_fileloc=pklfile_loc, shotnum=None, ptimeid=None, prunid=None,
         nefit='tanh', tefit='tanh', ncfit='spl', chii_eq_chie = False,
         Dn_min=0.001, vrc_mag=0.0, ti_decay_len=0.015, Dn_max=20,
         ke_use_grad = False, ki_use_grad = True,
         chie_min = 0.01, chii_min = 0.01, chie_max = 200, chii_max = 200,
         reduce_Ti_fileloc=None,
         #reduce_Ti_fileloc='/fusion/projects/results/solps-iter-results/wilcoxr/T_D_C_ratio.txt',
         carbon=False, use_existing_last10=False, plot_xport_coeffs=False,
         plotall=False, verbose=False, figblock=False)
    return(xp)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
     
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    


#                                         	MAIN PROGRAM STARTS HERE


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
## Go tho the initial folder run SOLPSXPORT 
# import os

os.chdir(path_old1)
Run_SOLPSXport_and_generate_transport_inputfile_new()
print("the SOLPS_Xport has ran in Attempt_0 ")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## Go back one-step and copy to new folder Attempt_i
os.chdir(path)
f2 = open('other_run_info.txt', 'w+')
f3 = open('iter_run_info.txt', 'w+') 
Nn=15
for i in range (1,Nn): 
 
    # print("i-iteration starts here for i= ", i)
    f2.write("i-iteration starts here for i=  " + str(i) + '\n')

    path_init = os.path.join(path, 'Attempt_' + str(i))
    try:
        os.makedirs(path_init)
    except FileExistsError:
        print('folders already exists')
    path_old=os.path.join(path, 'Attempt_'+ str(i-1))
    files = os.listdir(path_old)

    for ff in files:
        all_files = os.path.join(path_old, ff)
        if os.path.isfile(all_files):
            shutil.copy(all_files, path_init)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
# Updates files in Attempt_i for re-run simulation 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       
    os.chdir(path_init)
    os.system('cp b2fstate b2fstati')
    os.system('cp b2.transport.inputfile_new  b2.transport.inputfile')
    os.system('mv b2.transport.inputfile_new  b2.transport.inputfile_old')
    os.system('cp iter_b2mn100_1_4.dat b2mn.dat')
    
#Re-run the simulation in Attempt_i through a batch file
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    batch_file_for_job_submission(i)
    
    path_test=os.path.join(path_init, "test_file_i.txt")
    isFile = os.path.isfile(path_test)
    import time
    k=1
    mn=1
    sec=mn*60
    while isFile== False :
        #f2.write("the code is in sleeping mode for " + str(isFile)+ ' '+ str(k)+ ' '+ str(mn) + " minutes "+ '\n')
                 # f3.write(str(i)+ ' ' + str(resT_te)+ ' ' +str(resT_ne)+ '\n')

        k+=1
        time.sleep(sec)
        isFile = os.path.isfile(path_test)
    else:
        # print("the code is running forward with ", isFile, k, 'times', mn,"minutes")
        f2.write("the code is running forward with " + str(isFile)+ ' '+ str(k)+ ' '+ str(mn) + " minutes "+ '\n')

    os.system('mv test_file_i.txt test_file_i_old.txt')    
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    # Go to Attempt_i Run_SOLPSXport_and_generate_transport_inputfile_new(i)
    os.chdir(path_init)
    xp_new_i=Run_SOLPSXport_and_generate_transport_inputfile_new()
    xp=xp_new_i
    print("SOLPS_Xport has given b2.transport.inputfile_new in Attempt_j ", i)    
    f2.write("SOLPS_Xport has given b2.transport.inputfile_new in Attempt_j "+ str(i)+ '\n')    

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

    # loaded_datas(i)
# Export SOLPS_datas and Exp_datas from xp_datas in Attempt_i
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
    # Load SOLPS profiles and transport coefficients   
    neSOLPS = xp.data['solpsData']['last10']['ne']  
    niSOLPS = xp.data['solpsData']['last10']['ne']  

    teSOLPS = xp.data['solpsData']['last10']['te']*1.0e-3
    tiSOLPS = xp.data['solpsData']['last10']['ti']*1.0e-3
    xxSOLPS=xp.data['solpsData']['last10']['rx']
    psinSOLPS = xp.data['solpsData']['psiSOLPS']
  
    # Load experimental profiles from pkl-file
    psi_data_fit = xp.data['pedData']['fitPsiProf']
    nefit = 1.0e20*xp.data['pedData']['fitVals']['nedatpsi']['y']
    x_nefit = xp.data['pedData']['fitVals']['nedatpsi']['x']
    
    tefit = 1000*xp.data['pedData']['fitVals']['tedatpsi']['y']
    x_tefit = xp.data['pedData']['fitVals']['tedatpsi']['x']

    tifit = 1000*xp.data['pedData']['fitVals']['tidatpsi']['y']
    x_tifit = xp.data['pedData']['fitVals']['tidatpsi']['x']
    
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  

 # Calculation of residue
    from scipy.interpolate import interp1d
    ff_ne=interp1d(psinSOLPS,neSOLPS,kind='cubic')

    ff_te=interp1d(psinSOLPS,teSOLPS,kind='cubic')
    ff_ti=interp1d(psinSOLPS,tiSOLPS,kind='cubic')
#    for k in range(len(psinSOLPS)):
#        if psinSOLPS[k]==0:
#            n0=k

    for k in range(len(x_nefit)):
        if (x_nefit[k] > psinSOLPS[0]) and (x_nefit[k] < psinSOLPS[1]):
            ne_in=k 
        elif (x_nefit[k] > psinSOLPS[0]) and (x_nefit[k] < psinSOLPS[2]):
            ne_in=k 
    for k in range(len(x_nefit)):
        if (x_nefit[k] > psinSOLPS[-2]) and (x_nefit[k] < psinSOLPS[-1]):
            ne_out=k
        elif (x_nefit[k] > psinSOLPS[-3]) and (x_nefit[k] < psinSOLPS[-1]):
            ne_out=k 
            
    for k in range(len(x_tefit)):
        if (x_tefit[k] > psinSOLPS[0]) and (x_tefit[k] < psinSOLPS[1]):
            te_in=k 
        elif (x_tefit[k] > psinSOLPS[0]) and (x_tefit[k] < psinSOLPS[2]):
            te_in=k 
    for k in range(len(x_tefit)):
        if (x_tefit[k] > psinSOLPS[-2]) and (x_tefit[k] < psinSOLPS[-1]):
            te_out=k
        elif (x_tefit[k] > psinSOLPS[-3]) and (x_tefit[k] < psinSOLPS[-1]):
            te_out=k  

    for k in range(len(x_tifit)):
        if (x_tifit[k] > psinSOLPS[0]) and (x_tifit[k] < psinSOLPS[1]):
            ti_in=k 
        elif (x_tifit[k] > psinSOLPS[0]) and (x_tifit[k] < psinSOLPS[2]):
            ti_in=k 
    for k in range(len(x_tifit)):
        if (x_tifit[k] > psinSOLPS[-2]) and (x_tifit[k] < psinSOLPS[-1]):
            ti_out=k
        elif (x_tifit[k] > psinSOLPS[-3]) and (x_tifit[k] < psinSOLPS[-1]):
            ti_out=k             
       
        
    x_nefit_range= x_nefit[ne_in:ne_out]
    nefit_range= nefit[ne_in:ne_out]
    
    
    x_tefit_range= x_tefit[te_in:te_out]
    tefit_range= tefit[te_in:te_out]

    x_tifit_range= x_tifit[ti_in:ti_out]
    tifit_range= tifit[ti_in:ti_out]

    solps_ne_range=ff_ne(x_nefit_range)
    
    solps_te_range=ff_te(x_tefit_range)
    solps_ti_range=ff_ti(x_tifit_range)
    
    res1_ne=nefit_range-solps_ne_range
    resT_ne=np.sqrt(np.sum(res1_ne**2)/len(res1_ne))

    res1_te=tefit_range-solps_te_range
    resT_te=np.sqrt(np.sum(res1_te**2)/len(res1_te))

    res1_ti=tifit_range-solps_ti_range
    resT_ti=np.sqrt(np.sum(res1_ti**2)/len(res1_ti))    
    
    #plt.figure(8)
    #plt.plot(x_nefit, nefit,'o', t, p30_ne(t), '-') 
    #plt.plot(t, t_ne,'-.')
    #plt.show()
    
   # stopping condition of the loop
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  

    # '''    
    # # Stopping conditions
    if i >1:        
        if resT_ti < resT_ti_old and resT_ne < resT_ne_old :
            f2.write("iteration is going forward with resT_ti and resT_ne"+ '\n')
            print("iteration is going forward with resT_ti and resT_ne")

            # print("iteration is going on with resT_te", resT_te)
            # print("iteration is going on with resT_ne", resT_ne)
            f3.write(str(i)+ ' ' + str(resT_te)+' ' + str(resT_ti)+ ' ' +str(resT_ne)+ '\n')
            resT_ne_old=resT_ne
            resT_te_old=resT_te
            resT_ti_old=resT_ti            
            
        elif resT_ti >= resT_ti_old and resT_ne < resT_ne_old : 
            # print("current new resT_te is ", resT_te)
            # print("current new resT_ne is ", resT_ne)
            f3.write(str(i)+ ' ' + str(resT_te)+' ' + str(resT_ti)+ ' ' +str(resT_ne)+ '\n')
            print("Covergence in ti has started in Attempt- ", i)
            f2.write("Covergence in ti has started in Attempt- " + str(i)+ '\n')

            resT_ne_old=resT_ne
            resT_te_old=resT_te
            resT_ti_old=resT_ti            

        elif resT_ti < resT_ti_old and resT_ne >= resT_ne_old :
            # print("current new resT_te is ", resT_te)
            # print("current new resT_ne is ", resT_ne)
            f3.write(str(i)+ ' ' + str(resT_te)+' ' + str(resT_ti)+ ' ' +str(resT_ne)+ '\n')
            print("Covergence in ne has started in Attempt- ", i)
            f2.write("Covergence in ne has started in Attempt- " + str(i)+ '\n')

            resT_ne_old=resT_ne
            resT_te_old=resT_te
            resT_ti_old=resT_ti
            
        elif resT_ti >= resT_ti_old and resT_ne >= resT_ne_old :
            # print("2nd current new resT_te is ", resT_te)
            # print("2nd current new resT_ne is ", resT_ne)
            f3.write(str(i)+ ' ' + str(resT_te)+' ' + str(resT_ti)+ ' ' +str(resT_ne)+ '\n')

            # print("Covergence has achieved in both te and ne in Attempt- ", i)
            f2.write("Covergence has achieved in both ti and ne in Attempt- "+ str(i)+ '\n')

            resT_ne_old=resT_ne
            resT_te_old=resT_te
            resT_ti_old=resT_ti
            #break

        elif i==Nn-1:
            print("more iterations requires for convergence ")
            f2.write("more iterations requires for convergence ")
            #break
        # elif resT_te >= 10e-3*resT_te_old or resT_ne >= 10e-3*resT_ne_old :
            # print("Iteration has force stopped")
          
    else:
         resT_ne_old=resT_ne
         resT_te_old=resT_te
         resT_ti_old=resT_ti
         f2.write("iteration is going on with resT_te_old and resT_ne_old"+ '\n')
         # print("iteration is going on with resT_te_old", resT_te_old)
         # print("iteration is going on with resT_ne_old", resT_ne_old)
         f3.write(str(i)+ ' ' + str(resT_te)+' ' + str(resT_ti)+ ' ' +str(resT_ne)+ '\n')

         continue

    print("The iteration has concluded in the Attempt- ", i)
    f2.write("The iteration has concluded in the Attempt- "+ str(i)+ '\n')
f2.close()
f3.close()

#         continue
#print("The iteration has concluded in the Attempt- ", i)
#f2.write("The iteration has concluded in the Attempt- "+ str(i)+ '\n')

#f2.close()
#f3.close()

    # '''
   
    

