"""
Simple example on how to use the Monopole class
"""

# import the Monopole class from the acoustics package
from acoustics.monopole import Monopole

#create a monopole with default position in (0,0,0)
monopole = Monopole()

#place it somewhere else with a complex amplitude != 1+0j
monopole = Monopole(pos=[1,2,-4], q = (1.2+0.5j))

#print the monopole to verify position and complex amplitude
print(monopole)

#create a receiver position
receiver = [1,1,3]

#calculate the pressure in the receiver for one single frequency
f = 800
p = monopole.get_pressure(receiver_pos=receiver,single_freq=f)

#print the complex pressure value...
print(p)

#or plot the sound field
monopole.plot(single_freq=f)





