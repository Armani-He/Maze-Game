class Helper:
    def __init__(self, name, cost, skill, rounds, allow_mode:list, skill_execution_time:str):
        """
        Initialize a Helper object with specified attributes.

        Args:
            name (str): The name of the helper.
            cost (int): The cost of activating the helper.
            skill (function): The function representing the skill executed by the helper.
            rounds (int): The number of rounds the helper remains active.
            allow_mode (list): A list of modes in which the helper can be activated.
            skill_execution_time (str): The timing for helper to execute the skill.
        """
        self.activate = False
        self.available = True
        self.name = name
        self.cost = cost
        self.skill = skill
        self.rounds = rounds
        self.allow_mode = allow_mode
        self.skill_execution_time = skill_execution_time
        
    def use_skill(self, *args, **kwargs):
        """
        Execute the skill of the helper.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.skill(*args, **kwargs)
    
    def reduce_remaining_rounds(self):
        """Reduce the remaining rounds of the helper by 1."""
        self.rounds -= 1