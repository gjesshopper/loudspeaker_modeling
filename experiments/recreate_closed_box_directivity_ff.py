from scipy.io import loadmat   #to read .mat files
import matplotlib.pyplot as plt
import numpy as np
from acoustics.loudspeaker import Loudspeaker
from acoustics.monopole import Monopole
from acoustics.monopoles import Monopoles
def dB(x):
    return 20*np.log10(np.abs(x))

"""
Script that recreates the measured directivity for a closed box loudspeaker in free field and without edge diffraction.
"""

#load measurements as a python dictionary from a .mat file
p_tot_all_directions = loadmat('/Users/jesperholsten/Desktop/ELSYS/4. År/Høst 2021/Electroacoustics/2021_group5/Vented_box_on_axis_B&K_4133_1035mm_directivity_directivity_freqdata.mat')

print(p_tot_all_directions.keys())

#put different data in more specific variables
radius = 1.035 #m
data = p_tot_all_directions['freqdata'] #pressure vector afo. frequency for all angles


theta = p_tot_all_directions['angles'][0, :] #1D vector with all angles
f_directivity = p_tot_all_directions['f'][0, :] #frequency vector


#plot directivity
freqs = [50, 1000, 4000]
f_idx = np.searchsorted(f_directivity, freqs)

p = data[:, 1, f_idx]
p_ref = data[0, 1, f_idx]

#plot initial/true directivity
plt.polar(theta / 180 * np.pi, dB(p/p_ref))
ax = plt.gca()
ax.set_theta_zero_location('N')
plt.legend(['{} Hz'.format(f) for f in freqs], bbox_to_anchor = (1,1))
plt.ylim(-30,10)
plt.show()

#----------------------------SIMULATION---------------------------------

#create loudspeaker:
loudspeaker = Loudspeaker(n_layers=2)
loudspeaker.plot()

eq_source_positions = loudspeaker.get_monopole_posistions()

monopoles = []

for position in eq_source_positions:
    monopoles.append(Monopole(pos=position))

#recreate receiver positions
x = radius*np.cos(theta/180*np.pi)
y = np.zeros(len(x))
z = radius*np.sin(theta/180*np.pi)

receiver_positions = []
for i in range(len(x)):
    receiver_positions.append([x[i],y[i],z[i]])

#plot receiver positions
plt.scatter(x,z)
plt.axis('equal')
plt.xlabel('x')
plt.ylabel('z')
plt.grid(True)
plt.show()


#allocate transfer function matrix
tf = np.zeros(shape=(len(freqs),len(receiver_positions), len(monopoles)), dtype = complex)

#calculate each transferfunction and put in matrix
for ii,freq in enumerate(freqs):
    for i, position in enumerate(receiver_positions):
        for j, monopole in enumerate(monopoles):
            tf[ii,i,j] = monopole.get_pressure(receiver_pos=position,single_freq=freq)


#allocate complex amplitude vector
q = np.zeros(shape=(len(freqs), len(monopoles)), dtype = complex)

for i in range(len(freqs)):
    #solve moore-penroose pseudoinverse matrix:
    soln = np.linalg.pinv(tf[i,:,:])

    #multiply matrix with p to get the amplitudes
    q[i,:] = np.matmul(soln, p[:,i])



mpoles = Monopoles(monopoles)

p_tot_all_directions = np.zeros(shape=(len(receiver_positions), len(freqs)), dtype = complex)



for i, position in enumerate(receiver_positions):
    for j, freq in enumerate(freqs):
        for ii,monopole in enumerate(mpoles.monopoles):
            monopole.q = q[j, ii]
        p_tot_all_directions[i, j] = mpoles.get_pressure(receiver_pos=position, single_freq=freq)




#plot directivity
plt.polar(theta / 180 * np.pi, dB(np.abs(p_tot_all_directions /p_ref)))
ax = plt.gca()
ax.set_theta_zero_location('N')
plt.legend(['{} Hz'.format(f) for f in freqs], bbox_to_anchor = (1,1))

plt.show()

#last but not least we plot the vibration pattern of the diaphragm.
fig = plt.figure()
ax = plt.axes(projection = '3d')

# Create the mesh in polar coordinates and compute corresponding Z.

xs = eq_source_positions[:,0]
ys = eq_source_positions[:,1]
#Z = np.zeros(shape = (len(X),len(Y)), dtype = complex)

#for i in range(len(X)):
#    Z[i,:] = q[0,:]

ax.scatter3D(xs,ys,np.abs(q[0,:]))
plt.show()

