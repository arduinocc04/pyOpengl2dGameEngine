import PhysicalEngine
import numpy as np

class Actor:
    def __init__(self, coordinate):
        #this are components. you can what that you want
        self.type = False
        self.collider = False
        self.colliderSetting = 'n'#n->None, g->ground, c->character. usage: 'n' or 'gc' or 'cg' or 'g' 'c'

        self.renderer = False
        self.soundSystem = False
        self.healthSystem = False
        self.mover = False
        self.trigger = False
        self.triggerSetting = 'n'#n->None, p->playerOnly, c->characterOnly. usage: 'n' or 'pc' or 'cp' or 'p' or 'c'

        self.coordinate = np.array([float(coordinate[0]), float(coordinate[1])])
        self.angle = 0
    
    def update(self):
        pass
    def died(self):
        pass
    def collided(self, collidedObj):
        pass
    def triggerCollided(self, collidedObj):
        pass


class Ground:
    def __init__(self, coordinate):
        self.collider = False
        self.coordinate = np.array(coordinate)
        self.angle = 0
        self.type = True
class BackGround:
    def __init__(self):
        pass
