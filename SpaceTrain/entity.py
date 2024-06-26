from abc import abstractmethod
from drawable import Drawable

class Entity(Drawable):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def getDimensions(self):
        pass

    def collides(self, entity):
        x1, y1, w1, h1 = entity.getDimensions()
        x2, y2, w2, h2 = self.getDimensions()
        return (x2 < (x1 + w1) and (x2 + w2) > x1) and (y2 < (y1 + h1) and (y2 + h2) > y1)
