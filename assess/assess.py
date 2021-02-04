from enum import Enum
from typing import *

class Lottery:
    def __init__(self, left_variant: int, probability_of_left_variant: int, right_variant:int, left_variant_utility: float, right_variant_utility: float):
        self.left_variant: int = left_variant
        self.right_variant: int = right_variant
        self.probablilty_of_left_variant: float = probability_of_left_variant
        self.left_variant_utility: float = left_variant_utility
        self.right_variant_utility: float = right_variant_utility
        
    def utility(self) -> float:
        return self.left_variant_utility * self.probablilty_of_left_variant + self.right_variant_utility * (1 - self.probablilty_of_left_variant)
        
    def short__str__(self) -> str:
        return "L({}, {}, {})".format(\
                self.left_variant,
                self.probablilty_of_left_variant,
                self.right_variant
            )
            
    def __str__(self) -> str:
        return "L({}, {}, {})\nUl = {}, Ur = {}".format(\
            self.right_variant,
            self.probablilty_of_left_variant,
            self.right_variant,
            self.left_variant_utility,
            self.right_variant_utility
        )

class Choice(Enum):
    LOTTERY = ">"
    CERTAIN_VALUE = "<"
    INDIFFERENT = "~"

class Assess:
    def __init__(self, lottery: Lottery, certain_value: float):
        self.lottery: Lottery = lottery
        self.certain_value: float = certain_value
        self.last_choice: Choice = None
    
    def certain_value(self) -> Assess:
        raise NotImplementedError
    
    def lottery(self) -> Assess:
        raise NotImplementedError
    
    def indifferent(self) -> List[Assess]:
        raise NotImplementedError
    
    def __str__(self) -> str:
        return "{} {} {}".format(\
            self.lottery.short__str__(),
            self.last_choice,
            str(self.certain_value)
        )
      
# class ConfidenceEquivalentWithConstantProbablility

if __name__ == "__main__":
    print(Lottery(100, 0.3, 20, 0.2, 0.5).utility())