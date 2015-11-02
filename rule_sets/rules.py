class RuleViolation(Exception):
    """ An exception to be raised when a rule of the game has been broken.
    Prints a message explaining a violation, and returns the index[es] of throws that violate the rules.
    """
    def __init__(self, message, violating_index=None):

        # Call the base class constructor with the parameters it needs
        super(RuleViolation, self).__init__(message)

        # Index of the throws that violated the rules
        self.violating_index = violating_index


class RuleSet(object):
    """ A class governing the rules of the game. The rule object will take in a list of throws and return a list of
    outcomes
    """

    def __init__(self, evaluation_function):
        self.evaluate_round = evaluation_function


def evaluate_standard_rules(throws):
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


# The basic rule set
StandardRuleSet = RuleSet(evaluate_standard_rules)
