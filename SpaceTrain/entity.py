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

    def collides(self, x1, y1, w1, h1):
        x2, y2, w2, h2 = self.getDimensions()

        #if ((getDestX() < (x + w)) && ((getDestX() + getDestW()) > x) && (getDestY() < (y + h)) && ((getDestY() + getDestH()) > y))
        if (x2 < (x1 + w1) and (x2 + w2) > x1) and (y2 < (y1 + h1) and (y2 + h2) > y1):
            return True

        return False
