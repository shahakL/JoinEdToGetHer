class Player:
    def __init__(self):
        self._x = 44
        self._y = 44
        self._speed = 0.3
 
    def move_right(self):
        self._x = self._x + self._speed
 
    def move_left(self):
        self._x = self._x - self._speed
 
    def move_up(self):
        self._y = self._y - self._speed
 
    def move_down(self):
        self._y = self._y + self._speed

    @property
    def position(self):
        return [self._x, self._y]