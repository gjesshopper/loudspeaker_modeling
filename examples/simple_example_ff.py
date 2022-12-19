"""
Simple example on how to calculate the complex amplitudes of 5 monopoles when using synthesized data from
a single monopole placed in the origin.
"""

from acoustics.monopoles import Monopoles
from acoustics.monopole import Monopole
import numpy as np
import matplotlib.pyplot as plt


#create 8 receiver positions around the origin:

n_receivers = 100
theta = np.linspace(0,2*np.pi,n_receivers)
radius = 1
x = radius*np.cos(theta)
y = radius*np.sin(theta)
z = np.zeros(len(x))

receiver_positions = []
for i in range(len(x)):
    receiver_positions.append([x[i],y[i],z[i]])


plot = True #set to True if plot

if plot == True:
    plt.scatter(x,y)
    plt.grid(True)
    plt.axis('equal')
    plt.show()


#create a synthesized data set from monopole in origin:
synthesized_monopole = Monopole(pos=[0,0.2,0])

freq = 1000 #Hz

synthesized_data = np.zeros(shape = len(receiver_positions), dtype = complex)

for i, position in enumerate(receiver_positions):
    synthesized_data[i] = synthesized_monopole.get_pressure(receiver_pos=position,single_freq=freq)


#create 5 monopoles
monopole1 = Monopole(pos=[-0.2,0,0])
monopole2 = Monopole(pos=[-0.1,0,0])
monopole3 = Monopole(pos=[0,0,0])
monopole4 = Monopole(pos=[0.1,0,0])
monopole5 = Monopole(pos=[0.2,0,0])

monopoles = [monopole1,monopole2,monopole3,monopole4,monopole5]

transfer_function_matrix = np.zeros(shape=[len(receiver_positions), len(monopoles)], dtype = complex)


for i, position in enumerate(receiver_positions):
    for j, monopole in enumerate(monopoles):
        exec(f"transfer_function_matrix[i,j] = monopole{j+1}.get_pressure(receiver_pos=position,single_freq=freq)")

#solve moore-penroose pseudoinverse matrix:
soln = np.linalg.pinv(transfer_function_matrix)

q = np.matmul(soln, synthesized_data)

#plot result:
plt.plot(np.abs(q))
plt.grid(True)
plt.show()

#set complex amplitudes
for i, monopole in enumerate(monopoles):
    exec(f"monopole{i+1}.q = q[i]")

monopoles = Monopoles(monopoles = monopoles)
monopoles.plot_sound_field(single_freq=freq, res = 200, r_max=2)


directivity = np.zeros(shape=len(receiver_positions), dtype = complex)
#plot directivity
for i, position in enumerate(receiver_positions):
    directivity[i] = monopoles.get_pressure(receiver_pos=position, single_freq=freq)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, np.real(directivity))
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
ax.grid(True)
ax.set_title("Directivity", va='bottom')
plt.show()


if __name__ == "__main__":
    pass


