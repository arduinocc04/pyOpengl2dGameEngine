import physicalEngine
import numpy as np

class Actor:
    def __init__(self, coordinate):

        self.collider = False
        self.colliderSetting = 'n'

        self.coordinate = np.array([float(coordinate[0]), float(coordinate[1])])
    
    def update(self):
        pass
    def died(self):
        pass
    def collided(self):
        pass


class Ground:
    def __init__(self, componentList, coordinate, angle=0):
        self.componentList = []
        self.angle = angle
        self.coordinate = np.array(coordinate)

class BackGround:
    def __init__(self):
        pass
