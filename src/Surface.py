import numpy as np

class Surface:

    def have_collided(self, veh1, veh2):
        """
        Returns true if the two vehicles are collided, and false otherwise
        :param veh1:
        :param veh2:
        :return:
        """

        # Separating axis theorem reference: https://hackmd.io/s/ryFmIZrsl

        pts1 = veh1.get_bounding_points()
        pts2 = veh2.get_bounding_points()

        edges = []

        # Vectors 1 and 2 are the normals to edges of vehicle 1
        edges.append(np.subtract(pts1[1], pts1[0]))
        edges.append(np.subtract(pts1[2], pts1[1]))
        # Vectors 3 and 4 are the normals to edges of vehicle 2
        edges.append(np.subtract(pts2[1], pts2[0]))
        edges.append(np.subtract(pts2[2], pts2[1]))

        for edge in edges:
            if self.separating(pts1, pts2, edge):
                return False

        return True


    def separating(self, pts1, pts2, vector):
        """
        Returns true if the projection of pts1 onto vector does not overlap with the projection of pts2
        :param pts1:
        :param pts2:
        :param vector:
        :return:
        """
        min1, max1 = float('+inf'), float('-inf')
        min2, max2 = float('+inf'), float('-inf')

        for point in pts1:
            projection = np.dot(vector, point)

            min1 = min(min1, projection)
            max1 = max(max1, projection)

        for point in pts2:
            projection = np.dot(vector, point)

            min2 = min(min2, projection)
            max2 = max(max2, projection)

        # This makes more sense if you think about De Morgan's law
        if max1 >= min2 and max2 >= min1:
            return False
        else:
            return True