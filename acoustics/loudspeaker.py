import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
from setup import filepaths


class Loudspeaker():
    """
    The Baffle class represents a box with volume V = x*y*z.
    The box is centered around the z-axis with the top side aligned with z = 0.
    """
    def __init__(self, name : str = "Mayer 4XP",
                 baffle_width:float = 0.1025,
                 baffle_length:float = 0.1025,
                 baffle_heigth:float = 0.1454,
                 driver_radius:float = 0.04,
                 n_layers: int = 3
                 ):
        """

        Parameters
        ----------
        baffle_width: int/float
            width in metres
        baffle_length: int/float
            length in metres
        baffle_heigth: int/float
            heigth in metres
        """

        #baffle dimentions
        self.name = name
        self.x = baffle_width
        self.y = baffle_length
        self.z = baffle_heigth

        #driver parameters
        self.driver_radius = driver_radius
        self.n_layers = n_layers

    def get_baffle_corners(self):
        """

        Returns
        -------
        corners: 8x3 ndarray
            x,y and z coordinates of the corners in the shoebox

        """
        corners = np.zeros([8,3])

        corners[0,:] = [-self.x / 2, -self.y / 2,0]
        corners[1,:] = [self.x / 2, -self.y / 2,0]
        corners[2, :] = [self.x / 2, self.y / 2, 0]
        corners[3, :] = [-self.x / 2, self.y / 2, 0]
        corners[4, :] = [-self.x / 2, -self.y / 2, -self.z]
        corners[5, :] = [self.x / 2, -self.y / 2, -self.z]
        corners[6, :] = [self.x / 2, self.y / 2, -self.z]
        corners[7, :] = [-self.x / 2, self.y / 2, -self.z]
        return corners

    def get_baffle_plane_corners(self):
        plane_corners = np.array([[1, 2, 3, 4],
                         [1, 5, 6, 2],
                         [2, 6, 7, 3],
                         [4, 3, 7, 8],
                         [1, 4, 8, 5],
                         [8, 7, 6, 5]])
        return plane_corners

    def get_monopole_posistions(self, plot:bool = False):
        def pol2cart(r, theta):
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = 0.001
            return (x, y, z)

        spacing = self.driver_radius/(2*self.n_layers+1)
        radius_steps = np.linspace(2,self.n_layers*2, self.n_layers, dtype=int)

        n_sources = 1
        n_first_layer = 8

        if self.n_layers > 0:
            #calculate how many sources around the centered one
            for i in range(self.n_layers):
                n_sources+=n_first_layer*(i+1)


        monopole_positions = np.zeros([n_sources,3])

        monopole_positions[0,:] = [0.0, 0.0, 0.001] # first monopole has pos in origo

        first_idx = 1

        for i in range(self.n_layers):
            n_current_layer = n_first_layer*(i+1)

            theta = np.linspace(0,2*np.pi-(2*np.pi/n_current_layer), n_current_layer)
            radius = radius_steps[i]*spacing

            for j in range(n_current_layer):
                monopole_positions[first_idx+j,:] = pol2cart(radius,theta[j])

            first_idx += n_current_layer
        if plot == True:
            plt.plot(monopole_positions[:,0], monopole_positions[:,1], 'o')
            plt.axis('equal')
            plt.grid(True)
            plt.show()

        return monopole_positions

    def plot(self, savefig = False, fname = filepaths.drop_box_media, dpi = 300, bbox_inches='tight'):
        """
        plots the baffle with the monopoles on top
        Returns
        -------

        """
        #fig = plt.figure(figsize=(10, 7))
        plt.figure(figsize=(8,6))
        ax = plt.axes(projection="3d")

        # Creating plot

        monopole_positions = self.get_monopole_posistions()
        x = monopole_positions[:,0]
        y = monopole_positions[:,1]
        z = monopole_positions[:,2]

        ax.scatter3D(x, y, z, color="black")
        #plt.title("Simulated Loudspeaker")

        # show plot



        # draw cube
        points = self.get_baffle_corners()


        x = [-self.x/2,self.x/2]
        y = [-self.y/2,self.y/2]
        x, y = np.meshgrid(x,y)
        z = np.zeros(shape=[2,2], dtype=float)
        ax.plot_surface(x,y,z, alpha = 0.3, color = 'blue')


        x = [-self.x / 2, self.x / 2]
        y = [-self.y / 2, self.y / 2]
        x, y = np.meshgrid(x, y)
        z = np.zeros(shape=[2, 2], dtype=float)
        z[:,:] = -self.z
        ax.plot_surface(x, y, z, alpha=0.3, color = 'blue')

        x = [-self.x / 2, self.x / 2]
        z = [-self.z, 0]
        x, z = np.meshgrid(x, z)
        y = np.zeros(shape=[2, 2], dtype=float)
        y[:,:] = -self.y/2
        ax.plot_surface(x, y, z, alpha=0.3, color = 'blue')

        x = [-self.x / 2, self.x / 2]
        z = [-self.z, 0]
        x, z = np.meshgrid(x, z)
        y = np.zeros(shape=[2, 2], dtype=float)
        y[:, :] = self.y / 2
        ax.plot_surface(x, y, z, alpha=0.3, color = 'blue')

        y = [-self.y / 2, self.y / 2]
        z = [-self.z, 0]
        y, z = np.meshgrid(y, z)
        x = np.zeros(shape=[2, 2], dtype=float)
        x[:, :] = -self.x / 2
        ax.plot_surface(x, y, z, alpha=0.3, color='blue')

        y = [-self.y / 2, self.y / 2]
        z = [-self.z, 0]
        y, z = np.meshgrid(y, z)
        x = np.zeros(shape=[2, 2], dtype=float)
        x[:, :] = self.x / 2
        ax.plot_surface(x, y, z, alpha=0.3, color='blue')




        ax.scatter3D(points[:, 0], points[:, 1], points[:, 2])
        ax.set_xlabel('x[m]')
        ax.set_ylabel('y[m]')
        ax.set_zlabel('z[m]')

        #set equal axes
        ax.set_box_aspect([self.x, self.y, self.z])
        if savefig == True:
            plt.savefig(fname = fname, dpi = dpi, bbox_inches = bbox_inches)
        plt.show()

if __name__ == "__main__":

    loudspeaker = Loudspeaker(n_layers=2)
    positions = loudspeaker.get_monopole_posistions()



