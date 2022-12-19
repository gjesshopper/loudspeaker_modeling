import os.path

from setup import constants
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


class Monopole():
    """
    Simulates a monopole sound source in free-field.
    """

    def __init__(self, pos:list[float] = None, q:complex = 1.0+0j):
        """

        Parameters
        ----------
        pos : list[float]
            Position of the monopole, x,y,z in metres
        q : complex, default = 1.0 + 0j
            Source strength/Complex amplitude of the monopole. Contains phase and strength info.
        """
        self.pos = [0,0,0] if pos is None else pos
        self.q = q

    def __str__(self):
        """
        Print method for monopole object. Prints position and complex amplitude.

        Returns
        -------
        str
            string to be printed
        """
        return f"Monopole in pos ({self.pos[0]},{self.pos[1]},{self.pos[2]}) with q = {self.q}."

    def get_pressure(self, receiver_pos : list[float], single_freq:float):
        """
        Calculates the complex pressure from the monopole in the receiver position given

        Parameters
        ----------
        receiver_pos : list[float]
            point of the receiver
        single_freq : float
            single frequency in Hz

        Returns
        -------
        p : complex
            complex pressure in the receiver position
        """

        xs,ys,zs = [pos for pos in self.pos]

        xr,yr,zr = [pos for pos in receiver_pos]

        r = np.sqrt((xr-xs)**2+(yr-ys)**2+(zr-zs)**2)

        w = 2*np.pi*single_freq
        k = w / constants.C
        p = self.q*np.exp(-1j*k*r)/r
        return p

    def plot(self,
             r_max :float = 1,
             res:int = 50,
             inspection_height:float = None,
             single_freq :float = 1000,
             savefig : bool = False):
        """
        Plots a snap shot of the sound field of a monopole in 2D in the x-y-plane.
        The height of the "sheet" is determined by the inspection_height variable.

        Parameters
        ----------
        r_max : float, default = 1
            The distance from the source to one edge of the plot
        res : int, default = 50
            The resolution, number of pixels per row in the pixmap
        inspection_height : float, default = self.pos[2] i.e. in the center of the monopole
            The pressure evaluated in height inspection_height.
        single_freq : float, default = 1000
            Single frequency of the snapshot

        Returns
        -------
        None
        """

        inspection_height = self.pos[2] if inspection_height is None else inspection_height

        x_pos, y_pos, z_pos = [pos for pos in self.pos]

        xr = np.linspace(x_pos - r_max, x_pos + r_max, res)
        yr = np.linspace(y_pos - r_max, y_pos + r_max, res)



        p = np.zeros(shape=[len(xr),len(yr)], dtype=complex)

        for i, x in enumerate(xr):
            for j, y in enumerate(yr):
                p[i, j] = self.get_pressure(receiver_pos=[x, y, inspection_height], single_freq=single_freq)


        plt.imshow(np.real(p), cmap='hot', interpolation="nearest",
                   extent=[x_pos - r_max, x_pos + r_max, y_pos - r_max, y_pos + r_max])

        #plt.title("Snap shot of the sound pressure from a monopole source")
        #plt.xlabel("x [m]")
        #plt.ylabel("y [m]")
        plt.xticks(color="w")
        plt.yticks(color="w")
        plt.tick_params(bottom=False)
        plt.tick_params(left=False)

        if savefig == True:
            import setup.filepaths as filepath
            filename = "monopole_sound_field_ff.png"
            full_path = os.path.join(filepath.drop_box_media_results, filename)
            if os.path.exists(full_path):
                ans = input(f'File "{filename}" already exists. Overwrite? (y/n)')
                if ans == ("y" or "Y"):
                    plt.savefig(fname=full_path, dpi = 200)
                else:
                    pass
        plt.show()



if __name__ == "__main__":
    monopole = Monopole(pos = [0,0,0])
    receiver = [0,0,-1]
    f = 1000
    monopole.plot(r_max=1,single_freq=f,res=300, inspection_height=0.02)
