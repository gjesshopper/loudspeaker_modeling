import logging
import numpy as np
from acoustics.monopole import Monopole
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12





class Monopoles():
    """
    This class represents a set of monopoles in free-field
    """
    def __init__(self, monopoles : list[Monopole]):
        """

        Parameters
        ----------
        monopoles : list[Monopole]
            A list of Monopole objects.
        """
        self.monopoles = monopoles

    def __str__(self):
        """
        Print method for Monopoles object.
        Returns
        -------
        str
        """

        str = "Set of monopoles:\n---------------------------------------------------\n"
        for i, monopole in enumerate(self.monopoles):
            str += f"Monopole {i+1} in pos ({monopole.pos[0]},{monopole.pos[1]},{monopole.pos[2]}) with q = {monopole.q}\n"
        return str


    def get_pressure(self, receiver_pos:list[float], single_freq:float):
        """
        Adds up the pressure from all the monopoles in a receiver position and returns it.

        Parameters
        ----------
        receiver_pos : list[float]
            Single position [x,y,z] (m) of the receiver, i.e. where to calculate the sound pressure.
        single_freq :float
            Single frequency in Hz

        Returns
        -------
        p : ndarray
            Complex pressure in Pa
        """
        pressure = 0+0j

        self.monopoles[0].get_pressure(receiver_pos,single_freq)

        for i, monopoles in enumerate(self.monopoles):
            pressure += self.monopoles[i].get_pressure(receiver_pos,single_freq)
        return pressure


    def plot_sound_field(self, inspection_plane :list[int] = None, inspection_height : float = 0, single_freq:float = 1000, r_max:float = 1, res:int = 50):
        """
        Plots the added pressure from multiple monopoles.

        Parameters
        ----------
        inspection_plane : list[int]
            The plane of inspection.
            Valid:
            xy-plane: [0,0,1]
            xz-plane: [0,1,0]
            yz-plane: [1,0,0]

        inspection_height : float, default = 0
            The inspection "height" in the respective inspection plane (m).
        single_freq : float, default = 1000
            Single frequency in Hz.
        r_max : float, default = 1
            The distance in m from an enclosing box around all of the monopoles sources to the edge of the plot.
        res : int, default = 50
            Resolution, number of pixels per row.

        Returns
        -------
        None
        """

        #set default value of inspection plane if not given
        inspection_plane = [0,0,1] if inspection_plane is None else inspection_plane

        #make sure inspection plane is correct format
        zeros = 0
        ones = 0
        for pos in inspection_plane:
            if pos == 0:
                zeros += 1
            elif pos == 1:
                ones += 1

        if zeros != 2 and ones != 1:
            logging.error(msg = "Inspection plane must contain two 0's and one 1... \nUsing default inspection plane [0,0,1]")
            inspection_plane = [0,0,1]

        # find box around all sources in inspection plane
        x_val, y_val, z_val = [], [], []
        for monopole in self.monopoles:
            x, y, z = [pos for pos in monopole.pos]
            if inspection_plane == [1,0,0]:
                y_val.append(y)
                z_val.append(z)

            elif inspection_plane == [0,1,0]:
                x_val.append(x)
                z_val.append(z)

            elif inspection_plane == [0,0,1]:
                x_val.append(x)
                y_val.append(y)

        if not z_val:
            x_min, x_max = min(x_val), max(x_val)
            y_min, y_max = min(y_val), max(y_val)

            # create vectors
            x = np.linspace(x_min - r_max, x_max + r_max, res)
            y = np.linspace(y_min - r_max, y_max + r_max, res)

            p = np.zeros(shape=[len(x),len(y)],dtype=complex)

            for i in range(len(x)):
                for j in range(len(y)):
                    p[j,i] = self.get_pressure(receiver_pos=[x[i],y[j],inspection_height] , single_freq=single_freq)

            p = p[::-1,:]

            plt.imshow(np.real(p), cmap='hot', interpolation="nearest",extent=[x_min - r_max, x_max + r_max, y_min - r_max, y_max + r_max])



            plt.title("Sound pressure field from multiple monopole sources")
            plt.xlabel("x distance in meters")
            plt.ylabel("y distance in meters")
            plt.show()

        elif not y_val:
            x_min, x_max = min(x_val), max(x_val)
            z_min, z_max = min(z_val), max(z_val)

            # create vectors
            x = np.linspace(x_min - r_max, x_max + r_max, res)
            z = np.linspace(z_min - r_max, z_max + r_max, res)

            p = np.zeros(shape=[len(x), len(z)], dtype=complex)

            for i in range(len(x)):
                for j in range(len(z)):
                    p[j, i] = self.get_pressure(receiver_pos=[x[i],inspection_height,z[j]],
                                                single_freq=single_freq)

            p = p[::-1, :]

            plt.imshow(np.real(p), cmap='hot', interpolation="nearest",
                       extent=[x_min - r_max, x_max + r_max, z_min - r_max, z_max + r_max])

            plt.title("Sound pressure field from multiple monopole sources")
            plt.xlabel("x distance in meters")
            plt.ylabel("z distance in meters")
            plt.show()

        elif not x_val:
            y_min, y_max = min(y_val), max(y_val)
            z_min, z_max = min(z_val), max(z_val)

            # create vectors
            y = np.linspace(y_min - r_max, y_max + r_max, res)
            z = np.linspace(z_min - r_max, z_max + r_max, res)

            p = np.zeros(shape=[len(y), len(z)], dtype=complex)

            for i in range(len(y)):
                for j in range(len(z)):
                    p[j, i] = self.get_pressure(receiver_pos=[inspection_height,y[i],z[j]],
                                                single_freq=single_freq)

            p = p[::-1, :]

            plt.imshow(np.real(p), cmap='hot', interpolation="nearest",
                       extent=[y_min - r_max, y_max + r_max, z_min - r_max, z_max + r_max])

            plt.title("Sound pressure field from multiple monopole sources")
            plt.xlabel("y distance in meters")
            plt.ylabel("z distance in meters")
            plt.show()










if __name__ == "__main__":
    m1 = Monopole(pos = [1,1,2])
    m2 = Monopole(pos=[-1,2,-2])
    m3 = Monopole(pos=[-2,-1,1])


    monopoles = Monopoles(monopoles=[m1,m2,m3])

    receiver = [1,1,1]
    f = 1000
    monopoles.plot_sound_field(inspection_plane=[0, 1, 0], res = 200, inspection_height=0)