import numpy as np
import roshambo

class RuleViolation(Exception):
    """ An exception to be raised when a rule of the game has been broken.
    Prints a message explaining a violation, and returns the index[es] of throws that violate the rules.
    """
    def __init__(self, message, violating_index=None):

        # Call the base class constructor with the parameters it needs
        super(RuleViolation, self).__init__(message)

        # Index of the throws that violated the rules
        self.violating_index = violating_index


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
        outcomes = self.evaluate_round(throws)

        # Tell the robots
        print [throws[0], throws[1], outcomes[0]]
        robot_1_history = np.array([throws[0], throws[1], outcomes[0]])
        robot_2_history = np.array([throws[1], throws[0], outcomes[1]])

        self.robots[1].learn_throw(robot_1_history)
        self.robots[2].learn_throw(robot_2_history)

        return

    @staticmethod
    def evaluate_round(throws):
        """ Evaluate a standard game of 2-player roshambo.
        Legal throws:
        0 = rock, 1 = paper, 2 = scissors

        Possible outcomes:
        1 = win, 0 = draw, -1 = loss

        :param throws: A length-2 list of legal throws
        :return: A length-2 list of outcomes
        """

        # Validate this is a 2-player game
        num_throws = len(throws)
        if num_throws != 2:
            raise RuleViolation("This is a 2-player game, but {nt:d} throws were submitted for evaluation"
                                .format(nt=num_throws))

        # Validate each throw
        for throw, robot_index in enumerate(throws):
            robot_number = robot_index + 1

            if throw not in [0, 1, 2]:
                raise RuleViolation("The legal throws are 0 for rock, 1 for paper, or 2 for scissors, but "
                                    "Robot {rn:d} submitted a throw of {t!s}"
                                    .format(rn=robot_number, t=throw), robot_index)

        # Determine outcomes
        throw_1 = throws[0]
        throw_2 = throws[1]

        # Simplest case, a draw
        if throw_1 == throw_2:
            outcomes = [0, 0]

        # Verbose rules
        # No draw, robot 1 throws rock
        elif throw_1 == 0:
            # If player 2 throws paper, player 2 wins
            if throw_2 == 1:
                outcomes = [-1, 1]
            # P2 threw scissors and lost
            elif throw_2 == 2:
                outcomes = [1, -1]

        # No draw, robot 1 throws paper:
        elif throw_1 == 1:
            # If player 2 throws scissors, player 2 wins
            if throw_2 == 2:
                outcomes = [-1, 1]
            # P2 threw rock and lost
            elif throw_2 == 2:
                outcomes = [1, -1]

        # No draw, robot 1 throws scissors
        elif throw_1 == 2:
            # If player 2 throws rock, player 2 wins
            if throw_2 == 0:
                outcomes = [-1, 1]
            # P2 threw paper and lost
            elif throw_2 == 1:
                outcomes = [1, -1]

        # The rules can be dramatically simplified, each throw loses to all numbers 1 higher than it mod 3
        # and beats numbers 2 higher mod 3
        if throw_1 == throw_2:
            outcomes = [0, 0]

        # if throw_2 is 1 higher than throw_1 mod 3, player 2 wins
        elif throw_2 == (1 + throw_1) % 3:
            outcomes = [-1, 1]

        elif throw_2 == (2+throw_1) % 3:
            outcomes = [1, -1]

        else:
            raise RuleViolation("This should never happen")

        return outcomes

# Test case, conducts a few rounds between a paper and rock bot
if __name__ == "__main__":

    def always_paper(history):
        return 1

    def always_rock (history):
        return 0

    # Build actors
    paper_robot = roshambo.RoshamboRobot("iRobot", always_paper)
    rock_robot = roshambo.RoshamboRobot("uRobot", always_rock)
    ref = roshambo.Referee(paper_robot, rock_robot)

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
