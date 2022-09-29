
import numpy as np
import matplotlib.pyplot as plt



class Microphones():
    "Places N microphones (receiver positions) in a certain grid. "

    def __init__(self):
        pass



    def get_sphere_microphone_positions(self,
                                        nthetadivisions:int = 30,
                                        radius:float = 10.0,
                                        center_position:list[float] = [0,0,0]):
        """

        Parameters
        ----------
        nthetadivisions : int, default = 45
            number of divisions between theta[0, π] (latitudinal angle).
        radius : float, default = 10.0
            radius of the sphere in m
        center_position : list[float], default = [0,0,0]
            The center position of the sphere in m

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



        return points

    def plot(self):
        ax = plt.axes(projection="3d")

        points = self.get_sphere_microphone_positions()
        # Creating plot
        x = points[:,0]
        y = points[:,1]
        z = points[:,2]

        ax.scatter3D(x, y, z, 'o', color="black")
        plt.title("simple 3D scatter plot")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # set equal axes
        ax.set_box_aspect([1,1,1])

        plt.show()





if __name__ == "__main__":
    mics = Microphones()
    mics.plot()