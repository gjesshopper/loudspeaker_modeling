import logging
from scipy.io import loadmat, savemat   #to read .mat files
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
import numpy as np
def dB(x):
    return 20*np.log10(np.abs(x))

"""
First we start by defining our source and receiver positions as well ass other parameters
that we will later feed into Peter Svenssons script "EDmain_convexESIE.m", where we will
get the diffracted pressure from the scattering polyhedron since we are no longer in free field.
"""

from acoustics.loudspeaker import Loudspeaker
from acoustics.receivers import Receivers

#mayer 4XP specs:
length = 0.1025
width = 0.1025
height = 0.1454
driver_radius = 0.04

#create loudspeaker
loudspeaker = Loudspeaker(driver_radius=driver_radius,
                          baffle_length=length,
                          baffle_width=width,
                          baffle_heigth=height,
                          n_layers=3)

from setup import filepaths
import os
loudspeaker.plot()

#save figures
for i in range(3):
    Loudspeaker(driver_radius=driver_radius,
                              baffle_length=length,
                              baffle_width=width,
                              baffle_heigth=height,
                              n_layers=i+1).plot(savefig=False,
                                               fname = os.path.join(filepaths.drop_box_media, f'loudspeaker_sim{i+1}.png'),
                                               dpi = 300,
                                               bbox_inches='tight')

#create receivers
receivers = Receivers()

source_positions = loudspeaker.get_monopole_posistions()

#make sure receiver function arguments match measurement setup
receiver_positions = receivers.get_circle_receiver_positions(radius=2.35,
                                                             center_position=[0,0,0],
                                                             layout_plane=[0,1,0],
                                                             n_receivers=121,
                                                             plot = True)



#to make sure we have an overdetermined system we add this if statement:
if len(source_positions) > len(receiver_positions):
    logging.warning("Problem is not overdetermined... ")
else:
    logging.info("Problem is overdetermined.")

#finally we export the data we need to a .mat file
import os
directory = "/Users/jesperholsten/Desktop/ELSYS/5. År/Høst 2022/RFE4580 Prosjektoppgave/Målinger og labarbeider/Mayer4XPsimulation_data/"
filename = 'mayer4XP_ED_setup.mat'
filepath = directory+filename

import setup.constants as constant

datadict = {"corners" : loudspeaker.get_baffle_corners(),
            "plane_corners" : loudspeaker.get_baffle_plane_corners(),
            "source_positions" : source_positions,
            "receiver_positions" : receiver_positions,
            "c_air" : constant.C,
            "rho_air" : constant.RHO_0,
            "diff_order" : 8,
            "ngauss" : 48}

savemat(filepath, mdict=datadict)

"""
Now we move over to matlab to calculate the edge diffraction sound pressure from the 
scattering polyhedron. 
"""













