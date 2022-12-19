

"""
Present data calculated from Peter Svenssons EDtoolbox without source adjustment (SA).
All sources has complex amplitude (1+0j).

1. Directivity Polar Plot
2. Normalized Frequency responses together with measurements (to se the offset areas)

"""

import os
import setup.filepaths as filepaths
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
def dB(x):
    return 20*np.log10(np.abs(x))


#load measurement data
mayer4XP = loadmat("/Users/jesperholsten/Desktop/ELSYS/5. År/Høst 2022/RFE4580 Prosjektoppgave/MatlabScripts/Mayer4XPmeasurements.mat")

#print(mayer4XP.keys())

fvec = mayer4XP['fvec'][0,:]
p_meas = mayer4XP['alltfs'][0:int(len(fvec)), :]


#load simulation data (before source adjustment)
result_before_sa_fp = {}

for filename in os.listdir(filepaths.sim_before_sa_9s):
    if filename.endswith(".mat"):
        result_before_sa_fp[filename] = loadmat(os.path.join(filepaths.sim_before_sa_9s,filename))


tf = result_before_sa_fp['mayer4XP_before_SA_tf.mat']
tf_inteq = result_before_sa_fp['mayer4XP_before_SA_tfinteq.mat']


tf_direct = tf['tfdirect']
tf_geom = tf['tfgeom']
tf_diff = tf['tfdiff']
tf_inteq_diff = tf_inteq['tfinteqdiff']

#print(tf_inteq_diff)
n_sources = len(tf_direct[0,0,:])
n_receivers = len(tf_direct[0,:,0])
tftot_sim = tf_direct + tf_geom + tf_diff + tf_inteq_diff
f_sim = tuple(tf['EDsettings'][4][0][0])[0][2][0]


"""
The measured data has shape (4096, 121) which means a much higher frequency resolution 
than the simulated data. We need to find the indices 
of the frequency vector of the measured data that matches the frequencies used in the simulation.
"""

relevant_findices = np.searchsorted(fvec, f_sim)
n_actual_receivers = 121

#allocate new transfer function matrix to match simulation
p_meas_temp = np.zeros(shape=(len(relevant_findices), n_actual_receivers), dtype = complex)

#copy values from the right idx into the new p_meas
for i, idx in enumerate(relevant_findices):
    p_meas_temp[i, :] = p_meas[idx, :]


"""Now p_meas_temp has the right shape (len(f_sim,121) = (freqs,recievers), but 
there is still one problem... In the simulation we reduce the number of receivers
to save time on the calculation. We also discarded the 90 degree receiver angle du to numerical issues.
We therefore have to pick out the relevant receivers as well, i.e. which side of the directivity
polar plot should we use to calculate the complex amplitudes? Should not matter in theory so we chose the first half
from 0 to 180 degress excluding the 90 degree angle."""

p_meas = np.concatenate((p_meas_temp[:, 0:30],
                              p_meas_temp[:, 31:90],
                              p_meas_temp[:,91:]), axis=1)



#print("p_meas.shape: ", p_meas.shape)

"""Need to 'extrapolate' tftot_sim so all receivers are covered except 90 and 270."""
#tftot_sim_second_half = np.flip(tftot_sim, axis=(1,2))

#tftot_sim = np.concatenate((tftot_sim, tftot_sim_second_half[:,1:,:]), axis=1)


#print("tf_tot_sim.shape: ", tftot_sim.shape)

#plt.semilogx(f_sim, dB(tftot_sim[:,0,3]), label = "pos")
#plt.semilogx(f_sim, dB(tftot_sim[:,118,7]), "--", label = "neg")
#plt.legend()
#plt.show()



#plot directivity for sim to verify
alltfs_sim = np.zeros(shape=[len(f_sim),119],dtype=complex)

#sum up all sound pressures from the sources
for i in range(len(f_sim)):
    for j in range(119):
        alltfs_sim[i,j] = np.sum(tftot_sim[i,j,:])


freqs = [2269, 2550, 3519, 5100]
f_idx = np.searchsorted(f_sim, freqs)

p = np.transpose(alltfs_sim[f_idx, :])
p_ref = np.transpose(alltfs_sim[f_idx, 0])


theta = np.concatenate((np.linspace(0,87,30, dtype=int),
                        np.linspace(93,267,59, dtype=int),
                        np.linspace(273, 360, 30, dtype=int)))
#plot initial/true directivity
plt.figure(figsize=(7,7))
plt.polar(theta / 180 * np.pi, dB(p/p_ref), linewidth = 1.7)
ax = plt.gca()
#plt.title("Normalized directivity, Mayer 4XP")
ax.set_theta_zero_location('N')
plt.legend(['{} Hz'.format(f) for f in freqs], loc = 'lower right')
plt.ylim(-30,10)
#plt.savefig(fname = os.path.join(filepaths.drop_box_media_directivities, "simNOSC_bad_freqs_25s"), dpi = 300, bbox_inches = 'tight')
plt.show()



#allocate complex amplitude vector
q = np.zeros(shape=(n_sources, len(f_sim)), dtype = complex)

for i in range(len(f_sim)):
    #solve moore-penroose pseudoinverse matrix:
    soln = np.linalg.pinv(tftot_sim[i,:,:])
    #multiply matrix with p to get the amplitudes
    q[:,i] = np.matmul(soln, p_meas[i,:])


#print(q.shape)


#save matfile
from scipy.io import savemat

matdict = {'source_amplitudes' : q}
directory = "/Users/jesperholsten/Desktop/ELSYS/5. År/Høst 2022/RFE4580 Prosjektoppgave/Målinger og labarbeider/Mayer4XPsimulation_data/"
filename = f'source_amplitudes_fp_{n_sources}.mat'
filepath = directory+filename

#savemat(filepath, mdict=matdict)

#plot q
#need one single frequency, receiver positions in x and y and corresponding amplitudes

vibration_mode_freq = 300
source_positions = tf['EDsettings'][1][0][0][0][0]
freq_idx = np.searchsorted(f_sim, vibration_mode_freq)
fig = plt.figure()
ax = plt.axes(projection = '3d')
#ax.scatter3D(source_positions[:,0], source_positions[:,1], np.abs(q[:,freq_idx]*1e-11))

ax.plot_trisurf(source_positions[:,0],
                source_positions[:,1],
                np.abs(q[:,freq_idx]),
                linewidth=0.1,
                antialiased=True,
                cmap=plt.cm.YlGnBu_r
                )
ax.set_box_aspect((1,1,0.2))
ax.set_xlabel("X")
#plt.legend(str(f_sim[freq_idx]))
plt.xticks(color="w")
plt.yticks(color="w")
plt.title(f"frequency: {f_sim[freq_idx]}")

ax.set_ylabel("Y")
ax.set_zlabel("|q|")
plt.show()
#
#
# #dette ser rart ut.... hvorfor er amplitudene symmetriske?? De burde ikke være det
#
#
# plt.semilogx(f_sim, np.abs(q[0,:]))
# plt.semilogx(f_sim, np.abs(q[1,:]))
# plt.semilogx(f_sim, np.abs(q[9,:]))
# plt.semilogx(f_sim, np.abs(q[25,:]))
# plt.show()



###
#calculate new simulation data with source amplitudes



