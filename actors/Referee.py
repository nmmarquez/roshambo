import numpy as np


class Referee(object):

    """
    Roshambo Referee that takes in two RoshamboRobots and executes a series of
    of games that total in length anywhere between one and ten thousand
    individual games. The referee will update both robots histories after a
    game and will ask each robot for throws at the start of a game. If either
    robot makes a throw other than 0, 1, or 2 they will be immediately
    disqualified and the game will be over.

    Parameters
    ----------
    robot_one: object of class RoshamboRobot
        First actors robot
    robot_two: object of class RoshamboRobot
        Second actors robot
    """

    def __init__(self, robot_one, robot_two):
        self.robots = {1: robot_one, 2: robot_two}

    def check_throw_function(self, robot_id):
        """
        Check if a robot has a proper call function that returns
        :param robot_id: int
            Either 1 or 2 to indicate which robot to test
        :return: boolean
            True or False indicating whether a robot has a proper throw
            function.
        """
        return hasattr(self.robots[robot_id], '__call__')

    def check_robots_throw_function(self):
        """
        Check both robots to see if they have a throw function. If one is
        missing a throw function declares the other the winner by
        disqualification. If both are missing the function, a tie is returned.

        :return:
        """
        return self.robots

    @staticmethod
    def check_throw_outcome(throw):
        """
        Checks to see if what was returned by a robot is a valid response.
        :param throw: any
            The return of a robot throw
        :return: boolean
            True if the return is a float, long, or int of 0, 1, or 2.
        """
        return isinstance(throw, (int, long, float)) and throw in [0., 1., 2.]
