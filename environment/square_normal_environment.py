# square environment. there are the wall at the edge
from environment import super_environment


class SquareNormal(super_environment.Environment):
    def __init__(self, size_x, size_y):
        super().__init__(size_x, size_y)

    @staticmethod
    def environment_type():
        return 'square'

    def get_converted_position(self, position_before, position_after, radius):
        # return the able position.if the position over the edge wall it is impossible.
        x = position_after[0]
        if x < radius:
            x = radius
        elif x + radius > self.screen_size_x:
            x = self.screen_size_x - radius
        y = position_after[1]
        if y < radius:
            y = radius
        elif y > self.screen_size_y - radius:
            y = self.screen_size_y - radius
        return x, y

