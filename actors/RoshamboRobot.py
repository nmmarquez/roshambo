import numpy as np


class RoshamboRobot(object):

    """
    Roshambo Robot that can make throws by reading a 2-d array with 3 columns
    and n-rows. Each row represents one game played previously aginst another
    robot. the columns are zero indexed with the columns representing

    1[index 0 coulmn]) Your throw in game either 0,1,2
    2[index 1 coulmn]) Your oppenents throw in game either 0,1,2
    3[index 2 column]) The winner of a game, 1, -1 or 0 for you, opponent or tie

    0 = rock, 1 = paper, 2 = scissors

    Parameters
    ----------
    name: str
        The name for your robot should be a string
    throw_function : function
        function that takes in a 2d array and is able to make a throw i.e.
        return a 0, 1, 0r 2
    """

    def __init__(self, name, throw_function):
        assert isinstance(name, str), "name must be of type 'str'"
        self.name = name
        self.history = np.zeros((0, 3))
        self.throw_function = throw_function

    def learn_throw(self, new_results):
        # Add an extra dimension to new results to make it 2-d, this lets us append to existing history
        self.history = np.append(self.history, [new_results], axis=0)

    def __repr__(self):
        return "My name is {name}!".format(name=self.name)

    def make_throw(self):
        return self.throw_function(self.history)

if __name__ == "__main__":

    def always_paper(history):
        print history
        return 1

    robot = RoshamboRobot("iRobot", always_paper)

    robot

    robot.make_throw()

    robot.learn_throw([[1, 1, 0]])
    robot.learn_throw([[1, 1, 0]])
    robot.learn_throw([[1, 1, 0]])

    robot.make_throw()
