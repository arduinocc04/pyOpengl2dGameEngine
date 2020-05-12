import physicalEngine
import numpy as np

class Actor:
    def __init__(self, coordinate):
        #this are components. you can what that you want
        self.collider = False
        self.colliderSetting = 'n'#n->None, g->ground, c->character. usage: 'n' or 'gc' or 'cg' or 'g' 'c'

        self.renderer = False
        self.soundSystem = False
        self.healthSystem = False
        self.mover = False
        self.trigger = False
        self.triggerSetting = 'n'#n->None, p->playerOnly, c->characterOnly. usage: 'n' or 'pc' or 'cp' or 'p' or 'c'

        self.coordinate = np.array([float(coordinate[0]), float(coordinate[1])])
    
    def update(self):
        pass
    def died(self):
        pass
    def collided(self):
        pass
    def triggerCollided(self, collidedObj):
        pass


class Ground:
    def __init__(self, componentList, coordinate, angle=0):
        self.componentList = []
        self.angle = angle
        self.coordinate = np.array(coordinate)
        self.friction = 1

class BackGround:
    def __init__(self):
        pass
