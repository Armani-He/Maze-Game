from variables import *
class Dice:
    def __init__(self, lower_bound, upper_bound):
        """
        Initialize a Dice object with lower and upper bounds.

        Args:
            lower_bound (int): The lower bound of the dice.
            upper_bound (int): The upper bound of the dice.
        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
    
    def roll_dice(self):
        """
        Roll the dice and return the result.

        Returns:
            int: A random number between the lower and upper bounds.
        """
        global my_seed
        my_seed += 1
        return random.choice(range(self.lower_bound, self.upper_bound+1))