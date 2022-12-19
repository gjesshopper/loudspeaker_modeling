import logging
from scipy.io import loadmat, savemat   #to read .mat files
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
import setup.filepaths as filepaths
import os

import numpy as np
def dB(x):
    return 20*np.log10(np.abs(x))


"""
This script recreates the measured directivity for a closed box loudspeaker of
type Meyer 4XP. Measurements is done by professor Ulf Peter Svensson at the Norwegian University
of Science and Technology. The edge diffracted pressure is obtained from Svenssons EDtoolbox:
https://github.com/upsvensson/Edge-diffraction-Matlab-toolbox.

"""


#plot the measured directivity
meyer4XP = loadmat("/Users/jesperholsten/Desktop/ELSYS/5. År/Høst 2022/RFE4580 Prosjektoppgave/MatlabScripts/Mayer4XPmeasurements.mat")

print(meyer4XP.keys())

fvec = meyer4XP['fvec'][0,:]
alltfs = meyer4XP['alltfs'][0:int(len(fvec)),:]


plt.semilogx(fvec, dB(alltfs), linewidth = 0.7)
#plt.title("All frequency responses, Meyer 4XP")
plt.xlabel("Frequency in Hz")
plt.ylabel("FR magnitude in dB")
plt.grid(True)
plt.axis([80, 20000, -10, 50])
plt.savefig(os.path.join(filepaths.drop_box_media_results, "all_frequency_responses_Meyer_4XP_meas.png"), dpi = 300, bbox_inches='tight')
plt.show()


#take mean of alltfs:
tfs_mean = np.mean(alltfs, axis=1)
print(tfs_mean.shape)

plt.semilogx(fvec, dB(tfs_mean), linewidth = 2, label = 'Mean, all angles')
plt.semilogx(fvec, dB(alltfs[:,0]), linewidth = 2, label = 'On-axis response')
plt.xlabel("Frequency in Hz")
plt.ylabel("FR magnitude in dB")
plt.grid(True)
plt.legend(loc = 'lower left')
plt.axis([80, 20000, -10, 50])
plt.savefig(os.path.join(filepaths.drop_box_media_results, "average_on_axis_FR_meas.png"), dpi = 300, bbox_inches='tight')
plt.show()

#now in a polar plot:
freqs = [2269, 2550, 3519, 5100]
f_idx = np.searchsorted(fvec, freqs)

p = np.transpose(alltfs[f_idx, :])
p_ref = np.transpose(alltfs[f_idx, 0])

#print(p.shape, p_ref.shape)

theta = np.linspace(0,360,121)
#plot initial/true directivity
plt.figure(figsize=(7,7))
plt.polar(theta / 180 * np.pi, dB(p/p_ref), linewidth = 1.7)
ax = plt.gca()
#plt.title("Normalized directivity, Meyer 4XP")
ax.set_theta_zero_location('N')
plt.legend(['{} Hz'.format(f) for f in freqs], loc = 'lower right')
plt.ylim(-30,10)
#plt.savefig(fname = os.path.join(filepaths.drop_box_media_directivities, "meas_bad_freqs"), dpi = 300, bbox_inches = 'tight')
plt.show()



#energy-based mean of all frequency responses:
intensity = np.abs(alltfs)**2
intensity_avg = intensity.mean(axis=1)

plt.semilogx(fvec,10*np.log10(intensity_avg))
plt.title('Energy-based average')
plt.xlim(80,20000)
plt.ylim(15,50)
plt.grid(True)

plt.show()


#Simulated vs measured normalized frequency responses
actual_angles = [0,30,60,90,120,150,180,210,240,270,300,330]
angle_index = np.linspace(0,110,12, dtype = int)
displacement = np.linspace(0,165, 12)


for i in range(len(actual_angles)):
    exec(f"intensity_{actual_angles[i]} = intensity[:,{angle_index[i]}]")
    exec(f"DF_2D_{actual_angles[i]} = intensity_{actual_angles[i]}/intensity_avg")
    exec(f"DI_2D_{actual_angles[i]} = 10*np.log10(DF_2D_{actual_angles[i]})")
    exec(f"plt.semilogx(fvec, DI_2D_{actual_angles[i]} + displacement[{i}], label = '{actual_angles[i]} deg., measured, {'{:+}'.format(int(displacement[i]))} dB')")
plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
plt.title("Normalized frequency responses")
plt.tight_layout()
plt.grid(True)
plt.xlim(80, 20000)
plt.show()


#include simulations
result_before_sa_fp = {}

for filename in os.listdir(filepaths.sim_before_sa_49s):
    if filename.endswith(".mat"):
        result_before_sa_fp[filename] = loadmat(os.path.join(filepaths.sim_before_sa_49s,filename))

tf = result_before_sa_fp['mayer4XP_before_SA_tf.mat']
tf_inteq = result_before_sa_fp['mayer4XP_before_SA_tfinteq.mat']

tf_direct = tf['tfdirect']
tf_geom = tf['tfgeom']
tf_diff = tf['tfdiff']
tf_inteq_diff = tf_inteq['tfinteqdiff']
f_sim = tuple(tf['EDsettings'][4][0][0])[0][2][0]

#print(len(f_sim))

n_sources = 49
n_receivers = 119
tftot = tf_direct + tf_geom + tf_diff + tf_inteq_diff


alltfs_sim = np.zeros(shape=[len(f_sim),n_receivers],dtype=complex)

#sum up all sound pressures from the sources
for i in range(len(f_sim)):
    for j in range(n_receivers):
        alltfs_sim[i,j] = np.sum(tftot[i,j,:])

#print(alltfs_sim.shape)
#energy-based mean of all simulateed frequency responses:
intensity_sim = np.abs(alltfs_sim)**2
intensity_avg_sim = intensity_sim.mean(axis=1)

intensity_sim_0 = intensity_sim[:,0]
intensity_sim_30 = intensity_sim[:,10]
intensity_sim_60 = intensity_sim[:,20]
intensity_sim_90 = intensity_sim[:,30] #actually 93 because 90 is excluded
intensity_sim_120 = intensity_sim[:,39]
intensity_sim_150 = intensity_sim[:,49]
intensity_sim_180 = intensity_sim[:,59]
intensity_sim_210 = intensity_sim[:,49]
intensity_sim_240 = intensity_sim[:,39]
intensity_sim_270 = intensity_sim[:,30] #actually 267 because 270 is mirror of 90
intensity_sim_300 = intensity_sim[:,20]
intensity_sim_330 = intensity_sim[:,10]
intensity_sim_360 = intensity_sim[:,0]


plt.semilogx(f_sim, 10*np.log10(intensity_avg_sim))
plt.grid(True)
plt.title("Energy-based average simulation")
plt.xlabel("Frequency [Hz]")
plt.show()

#Simulated vs measured normalized frequency responses
actual_angles = [0,30,60,90,120,150,180,210,240,270,300,330]
angle_index = np.linspace(0,110,12, dtype = int)
displacement = np.linspace(0,165, 12)

plt.figure(figsize=(16,8))
for i in range(len(actual_angles)):
    exec(f"plt.semilogx(fvec, DI_2D_{actual_angles[i]} + displacement[{i}], label = '{actual_angles[i]} deg, meas, {'{:+}'.format(int(displacement[i]))} dB')")
    exec(f"DF_2D_sim_{actual_angles[i]} = intensity_sim_{actual_angles[i]}/intensity_avg_sim")
    exec(f"DI_2D_sim_{actual_angles[i]} = 10*np.log10(DF_2D_sim_{actual_angles[i]})")
    exec(f"plt.semilogx(f_sim, DI_2D_sim_{actual_angles[i]} + displacement[{i}], label = '{actual_angles[i]} deg, sim, {'{:+}'.format(int(displacement[i]))} dB', linestyle = 'dotted')")

plt.legend(loc="best", prop={'size': 12})
#plt.title("Normalized frequency responses before source adjustment")
plt.grid(True)
plt.xlim(80, 20000)
plt.xlabel("Frequency in Hz")
plt.ylabel("Normalized FR in dB (re. 1)")

#plt.savefig(fname = os.path.join(filepaths.drop_box_media_results, f'FRnorm_sim_meas_{n_sources}s_noSC'), dpi = 300, bbox_inches='tight')
plt.show()















