import logging
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12



class Receivers():
    "Places N microphones (receiver positions) in a certain grid. "

    def __init__(self):
        pass



    def get_sphere_receiver_positions(self,
                                      nthetadivisions : int = 30,
                                      radius : float = 10.0,
                                      center_position : list[float] = [0,0,0],
                                      plot : bool  = False):
        """
        Calculates the receiver positions distributed over
        a sphere surrounding a given center position.

        Parameters
        ----------
        nthetadivisions : int, default = 45
            number of divisions between theta[0, π] (latitudinal angle).
        radius : float, default = 10.0
            radius of the sphere in m
        center_position : list[float], default = [0,0,0]
            The center position of the sphere in m
        plot : bool, default = False
            Plots the receiver points in 3D

        Returns
        -------
        points : ndarray
            Numpy array with shape (n_microphones,3) containing the x,y,z-position of each microphone.
        """

        layers = nthetadivisions+1 #(included north and south pole)

        theta = np.linspace(0,np.pi, layers)

        points = []
        x_center, y_center, z_center = center_position[0], center_position[1], center_position[2]

        n_mics_current_layer = 1

        for i, theta in enumerate(theta):
            if theta == 0:
                n_mics_current_layer = 1
                points.append([x_center,y_center,z_center+radius])
                continue
            elif theta == np.pi:
                n_mics_current_layer = 1
                points.append([x_center, y_center, z_center - radius])
                continue

            elif (0 < theta <= np.pi/2):
                n_mics_current_layer = i*6

            elif (np.pi >= theta > np.pi/2):
                n_mics_current_layer = 6*(layers-(i+1))

            phi = np.linspace(0, 2 * np.pi - (2 * np.pi / n_mics_current_layer), n_mics_current_layer)

            for phi in phi:
                x = radius*np.sin(theta)*np.cos(phi) + x_center
                y = radius*np.sin(theta)*np.sin(phi) + y_center
                z = radius*np.cos(theta) + z_center
                points.append([x,y,z])


        points = np.array(points)
        if plot == True:
            ax = plt.axes(projection="3d")

            #points = self.get_sphere_microphone_positions()
            # Creating plot
            x = points[:, 0]
            y = points[:, 1]
            z = points[:, 2]

            ax.scatter3D(x, y, z, 'o', color="black")
            plt.title("simple 3D scatter plot")
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

            # set equal axes
            ax.set_box_aspect([1, 1, 1])

            plt.show()

        return points



    def get_circle_receiver_positions(self,
                                      radius : float = 1,
                                      center_position : list[float] = None,
                                      layout_plane : list[int] = None,
                                      n_receivers : int = 16,
                                      plot : bool = False,
                                      remove_problematic_angles : bool = True):

        # set default values to center position and layout plane
        center_position = [0, 0, 0] if center_position is None else center_position
        layout_plane = [0, 0, 1] if layout_plane is None else layout_plane

        theta = np.linspace(0,360,n_receivers)

        if remove_problematic_angles == True:
            #remove 90 and 270 deg angles
            theta = theta[theta != 90]
            theta = theta[theta != 270]
            n_receivers = len(theta)

        # recreate receiver positions
        if layout_plane == [0,0,1]:
            x = radius * np.cos(theta / 180 * np.pi) + center_position[0]
            y = radius * np.sin(theta / 180 * np.pi) + center_position[1]
            z = np.zeros(len(x)) + center_position[2]
        elif layout_plane == [0,1,0]:
            x = radius * np.sin(theta / 180 * np.pi) + center_position[0]
            y = np.zeros(len(x)) + center_position[1]
            z = radius * np.cos(theta / 180 * np.pi) + center_position[2]
        elif layout_plane == [1,0,0]:
            x = np.zeros(len(x)) + center_position[0]
            y = radius * np.cos(theta / 180 * np.pi) + center_position[1]
            z = radius * np.sin(theta / 180 * np.pi) + center_position[2]
        else:
            logging.error("Invalid variable layout_plane. Using default [0,0,1]...")
            x = radius * np.cos(theta / 180 * np.pi) + center_position[0]
            y = radius * np.sin(theta / 180 * np.pi) + center_position[1]
            z = np.zeros(len(x)) + center_position[2]


        receiver_positions = []
        for i in range(len(x)):
            receiver_positions.append([x[i], y[i], z[i]])

        if plot == True:
            # plot receiver positions
            if layout_plane == [0,0,1]:
                plt.scatter(x,y)
                plt.xlabel('x[m]')
                plt.ylabel('y[m]')
            elif layout_plane == [0,1,0]:
                plt.scatter(x,z)
                plt.xlabel('x[m]')
                plt.ylabel('z[m]')
            elif layout_plane == [1,0,0]:
                plt.scatter(y,z)
                plt.xlabel('y[m]')
                plt.ylabel('z[m]')
            plt.axis('equal')
            plt.title(f"n = {n_receivers}")
            plt.grid(True)
            plt.show()




        return receiver_positions




if __name__ == "__main__":
    mics = Receivers()
    mics.get_circle_receiver_positions(layout_plane=[0,1,0], center_position=[1,1,1],plot=True, n_receivers=9)