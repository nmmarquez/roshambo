import numpy as np
import roshambo

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
    rule_set: Object of class RuleSet
        The rules the game is to be played by
    robot_one: object of class RoshamboRobot
        First actors robot
    robot_two: object of class RoshamboRobot
        Second actors robot
    """

    def __init__(self, rule_set, robot_one, robot_two):
        self.rules = rule_set
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

    def conduct_round(self):
        """
        Runs a single round of a match. A round consists of:

        1. Asking each robot for their throw
        2. Evaluating the results of the throw
        3. Informing each robot of the results

        :return: None
        """

        # Get each robot's throw
        throws = []
        # Note, don't try to iterate over self.robots.keys here because dicts are unsorted
        for robot in [1, 2]:
            throws.append(self.robots[robot].make_throw())

        # Evaluate the results of the throw
        outcomes = self.rules.evaluate_round(throws)

        # Tell the robots
        print [throws[0], throws[1], outcomes[0]]
        robot_1_history = np.array([throws[0], throws[1], outcomes[0]])
        robot_2_history = np.array([throws[1], throws[0], outcomes[1]])

        self.robots[1].learn_throw(robot_1_history)
        self.robots[2].learn_throw(robot_2_history)

        return

# Test case, conducts a few rounds between a paper and rock bot
if __name__ == "__main__":

    def always_paper(history):
        return 1

    def always_rock (history):
        return 0

    # Build actors
    paper_robot = roshambo.RoshamboRobot("iRobot", always_paper)
    rock_robot = roshambo.RoshamboRobot("uRobot", always_rock)
    ref = roshambo.Referee(roshambo.rule_sets.StandardRuleSet,
                           paper_robot, rock_robot)

    # Conduct a few rounds
    ref.conduct_round()
    ref.conduct_round()
    ref.conduct_round()

    # Display results
    print("Rock robot's results, he never wins :(")
    print(rock_robot.history)
    print("\n")

    print("Paper robot's results, he always wins :(")
    print(paper_robot.history)
