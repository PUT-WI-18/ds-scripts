from enum import Enum
from typing import *

class Lottery:
    """
    Class represents lottery. Better variant should be placed always on left side, so default values for utility of variants are correct
    """
    
    def __init__(self, left_variant: int, probability_of_left_variant: int, right_variant:int, left_variant_utility: float = 1, right_variant_utility: float = 0):
        self.left_variant: int = left_variant
        self.right_variant: int = right_variant
        self.probablilty_of_left_variant: float = probability_of_left_variant
        self.left_variant_utility: float = left_variant_utility
        self.right_variant_utility: float = right_variant_utility
        
    def utility(self) -> float:
        """
        Calculates utility of lottery
        Returns:
            float: utility
        """
        return self.left_variant_utility * self.probablilty_of_left_variant + self.right_variant_utility * (1 - self.probablilty_of_left_variant)
        
    def short__str__(self) -> str:
        """
        Shortened version of __str__ magic function, presents only lottery, without utilities of variants
        Returns:
            str: [description]
        """
        return "L({}, {}, {})".format(\
                self.left_variant,
                self.probablilty_of_left_variant,
                self.right_variant
            )
            
    def __str__(self) -> str:
        return "L({}, {}, {})\nUl = {}, Ur = {}".format(\
            self.left_variant,
            self.probablilty_of_left_variant,
            self.right_variant,
            self.left_variant_utility,
            self.right_variant_utility
        )

class ValueSpan:
    """
    Defines span of values, for example 1 to 10
    """
    def __init__(self, left_boundary, right_boundary):
        self.left: float = left_boundary
        self.right: float = right_boundary
        
    def middle_value(self) -> float:
        """
        value being average if span
        Returns:
            float: average
        """
        return (self.left + self.right) / 2

class Choice(Enum):
    LOTTERY = ">"
    CERTAIN_VALUE = "<"
    INDIFFERENT = "~"
    
    def __str__(self) -> str:
        return self.value

class Assess:
    """
    Generic class for all assess methods
    """
    def __init__(self, lottery: Lottery, certain_value: float, value_span: ValueSpan):
        # method name
        self.name: str = "Generic Assess"
        # lottery in interation
        self.lottery: Lottery = lottery
        # certain value for iteration
        self.certain_value: float = certain_value
        # last choice made by user
        self.last_choice: Choice = None
        # mark if criterion is gain or cost type
        self.is_gain: bool = (lottery.left_variant > lottery.right_variant)
        # span of criterion values for iteration
        self.value_span: ValueSpan = value_span
    
    def choose_certain_value(self):
        """
        Represents decision of decident to choose certain value and not lottery
        """
        raise NotImplementedError
    
    def choose_lottery(self):
        """
        Represents decision to take lottery instead of certain value
        """
        raise NotImplementedError
    
    def choose_indifferent(self):
        """
        For decident both lottery and certain value represents same utility
        """
        raise NotImplementedError
    
    def get_method_name(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return "{} {} {}".format(\
            self.lottery.short__str__(),
            self.last_choice,
            str(self.certain_value)
        )
        
    def __repr__(self) -> str:
        return self.__str__()
      
class ConfidenceEquivalentWithConstantProbablility(Assess):
    def __init__(self, lottery: Lottery, certain_value: float):
        super().__init__(lottery, certain_value, ValueSpan(lottery.left_variant, lottery.right_variant))
        self.certain_value = self.value_span.middle_value()
        self.name = "Confidence Equivalent with Constant Probability"
        
    def choose_certain_value(self) -> Assess:
        if self.is_gain:
            self.value_span = ValueSpan(self.certain_value, self.value_span.right)
            self.certain_value = self.value_span.middle_value()
        else:
            self.value_span = ValueSpan(self.value_span.left, self.certain_value)
            self.certain_value = self.value_span.middle_value()
        self.last_choice = Choice.CERTAIN_VALUE
        return self
    
    def choose_lottery(self) -> Assess:
        if self.is_gain:
            self.value_span = ValueSpan(self.value_span.left, self.certain_value)
            self.certain_value = self.value_span.middle_value()
        else:
            self.value_span = ValueSpan(self.certain_value, self.value_span.right)
            self.certain_value = self.value_span.middle_value()
        self.last_choice = Choice.LOTTERY
        return self
    
    def choose_indifferent(self) -> List[Assess]:
        self.last_choice = Choice.INDIFFERENT
        return [
            ConfidenceEquivalentWithConstantProbablility(
                Lottery(self.lottery.left_variant, self.lottery.probablilty_of_left_variant, self.certain_value, self.lottery.left_variant_utility, self.lottery.utility()),
                (self.lottery.left_variant + self.certain_value) / 2
            ),
            ConfidenceEquivalentWithConstantProbablility(
                Lottery(self.certain_value, self.lottery.probablilty_of_left_variant, self.lottery.right_variant, self.lottery.utility(), self.lottery.right_variant_utility),
                (self.lottery.right_variant + self.certain_value) / 2
            )
        ]

class ConfidenceEquivalentWithChangingProbability(Assess):
    def __init__(self, lottery: Lottery, certain_value: float, variants_span: ValueSpan, probability_span: ValueSpan):
        super().__init__(lottery, certain_value, variants_span)
        self.probability_span: ValueSpan = probability_span
        self.binary_search_value_span: ValueSpan = variants_span
        
    def choose_certain_value(self) -> Assess:
        self.last_choice = Choice.CERTAIN_VALUE
        if self.is_gain:
            self.binary_search_value_span = ValueSpan(self.certain_value, self.binary_search_value_span.right)
            self.certain_value = self.binary_search_value_span.middle_value()
        else:
            self.binary_search_value_span = ValueSpan(self.binary_search_value_span.left, self.certain_value)
            self.certain_value = self.binary_search_value_span.middle_value()
        return self
    
    def choose_lottery(self) -> Assess:
        self.last_choice = Choice.LOTTERY
        if self.is_gain:
            self.binary_search_value_span = ValueSpan(self.binary_search_value_span.right, self.binary_search_value_span.middle_value())
            self.certain_value = self.binary_search_value_span.middle_value()
        else:
            self.binary_search_value_span = ValueSpan(self.certain_value, self.binary_search_value_span.right)
            self.certain_value = self.binary_search_value_span.middle_value()
        return self
            
    def choose_indifferent(self):
        self.last_choice = Choice.INDIFFERENT
        return [
            ConfidenceEquivalentWithChangingProbability(
                Lottery(self.lottery.left_variant, (self.probability_span.left + self.probability_span.middle_value()) / 2, self.lottery.right_variant),
                (self.value_span.left + self.certain_value) / 2,
                ValueSpan(self.value_span.left, self.certain_value),
                ValueSpan(self.probability_span.left, self.probability_span.middle_value())
            ),
            ConfidenceEquivalentWithChangingProbability(
                Lottery(self.lottery.left_variant, (self.probability_span.middle_value() + self.probability_span.right) / 2, self.lottery.right_variant), (self.certain_value + self.value_span.right) / 2,
                ValueSpan(self.certain_value, self.value_span.right),
                ValueSpan(self.probability_span.middle_value(), self.probability_span.right)
            )
        ]

class ProbabilityComparation(Assess):
    def __init__(self, lottery: Lottery, certain_value: float, variants_span: ValueSpan, probability_span: ValueSpan):
        super().__init__(lottery, certain_value, variants_span)
        self.probability_span: ValueSpan = probability_span
        self.binary_search_probability_span: ValueSpan = probability_span
        
    def choose_certain_value(self) -> Assess:
        self.last_choice = Choice.CERTAIN_VALUE
        if self.is_gain:
            self.binary_search_probability_span = ValueSpan(self.binary_search_probability_span.left, self.binary_search_probability_span.middle_value())
            self.lottery = Lottery(self.lottery.left_variant, self.binary_search_probability_span.middle_value(), self.lottery.right_variant)
        else:
            self.binary_search_probability_span = ValueSpan(self.binary_search_probability_span.middle_value(), self.binary_search_probability_span.right)
            self.lottery = Lottery(self.lottery.left_variant, self.binary_search_probability_span.middle_value(), self.lottery.right_variant)
        return self
        
    def choose_lottery(self) -> Assess:
        self.last_choice = Choice.LOTTERY
        if self.is_gain:
            self.binary_search_probability_span = ValueSpan(self.binary_search_probability_span.middle_value(), self.binary_search_probability_span.right)
            self.lottery = Lottery(self.lottery.left_variant, self.binary_search_probability_span.middle_value(), self.lottery.right_variant)
        else:
            self.binary_search_probability_span = ValueSpan(self.binary_search_probability_span.left, self.binary_search_probability_span.middle_value())
            self.lottery = Lottery(self.lottery.left_variant, self.binary_search_probability_span.middle_value(), self.lottery.right_variant)
        return self
            
    def choose_indifferent(self) -> Assess:
        self.last_choice = Choice.INDIFFERENT
        return [
            ProbabilityComparation(
                Lottery(self.lottery.left_variant, (self.probability_span.left + self.binary_search_probability_span.middle_value()) / 2, self.lottery.right_variant),
                (self.value_span.left + self.value_span.middle_value()) / 2,
                ValueSpan(self.value_span.left, self.value_span.middle_value()),
                ValueSpan(self.probability_span.left, self.binary_search_probability_span.middle_value())
            ),
            ProbabilityComparation(
                Lottery(self.lottery.left_variant, (self.probability_span.right + self.binary_search_probability_span.middle_value()) / 2, self.lottery.right_variant),
                (self.value_span.middle_value() + self.value_span.right) / 2,
                ValueSpan(self.value_span.middle_value(), self.value_span.right),
                ValueSpan(self.binary_search_probability_span.middle_value(), self.probability_span.right)
            )
        ]

class CLI:
    """
    CLI for API usage
    """
    def __init__(self):
        lottery, certain_value = self._get_first_comparation()
        self.comparations: List[Assess] = [self._get_method(lottery, certain_value)]
        self._compare()
        
    def _compare(self):
        """
        User main loop of execution
        """
        # typing two empty lines ends program
        empty_lines: int = 0
        # user can work on more than 1 span, and all of spans are stored in array, this is just indexer for array
        active_comparation_idx: int = 0
        self._show_controlls()
        print(self.comparations[active_comparation_idx])
        while True:
            inputs: str = input()
            if len(inputs.strip()) == 0:
                empty_lines += 1
                if empty_lines >= 2:
                    break
            else:
                empty_lines = 0
            if inputs == "h":
                self._show_controlls()
            elif inputs == "c":
                print()
                print("Certain value")
                print(self.comparations[active_comparation_idx].choose_certain_value())
            elif inputs == "l":
                print()
                print("Lottery")
                print(self.comparations[active_comparation_idx].choose_lottery())
            elif inputs == "i":
                print()
                print("Indifferent")
                # new spans should be injected into list in place of previous span which should be deleted
                # exact place of dropped span took righter new span
                new_comparations: List[Assess] = self.comparations[active_comparation_idx].choose_indifferent()
                self.comparations.pop(active_comparation_idx)
                self.comparations.insert(active_comparation_idx, new_comparations[1])
                self.comparations.insert(active_comparation_idx - 1, new_comparations[0])
                print(self.comparations[active_comparation_idx])
            elif inputs == "a":
                print()
                print("Show all")
                line_num: int = 1
                for comparation in self.comparations:
                    print(str(line_num) + ": " + str(comparation))
                    line_num += 1
            elif int(inputs) > 0:
                print()
                print("Change to {}".format(int(inputs)))
                active_comparation_idx = int(inputs) - 1
                print(self.comparations[active_comparation_idx])
    
    def _get_method(self, lottery: Lottery, certain_value: float) -> Assess:
        """
        Displays menu to choose from which method use
        Args:
            lottery (Lottery): lottery object, take form previous queries
            certain_value (float): certain value obtained from user

        Returns:
            Assess: Full initialised method
        """
        print("\nChoose method: ")
        print("1 -> Confidence Equivalent with Constant Probability")
        print("2 -> Confidence Equivalent with Changing Probability")
        print("3 -> Probability comparation")
        
        is_input_correct: bool = False
        
        while not is_input_correct:
            is_input_correct = True
            inputs: int = int(input())
            if inputs < 0 or inputs > 4:
                is_input_correct = False
                print("Option {} is incorrect".format(inputs))
        
        if inputs == 1:
            return ConfidenceEquivalentWithConstantProbablility(lottery, certain_value)
        
        if inputs == 2:
            return ConfidenceEquivalentWithChangingProbability(
                lottery,
                certain_value,
                ValueSpan(lottery.left_variant, lottery.right_variant),
                ValueSpan(1, 0)
            )
            
        if inputs == 3:
            return ProbabilityComparation(
                lottery,
                certain_value,
                ValueSpan(lottery.left_variant, lottery.right_variant),
                ValueSpan(1, 0)
            )
            
    def _get_first_comparation(self) -> Tuple[Lottery, float]:
        """
        Grasp initial data from user in form of
        L(<left_variant>, <probability_of_left_variant>, <right_variant>) <some equivalent>
        left variant has by definition utility of 1 and right 0
        Returns:
            Tuple[Lottery, float]: initialised lottery and certain value
        """
        is_input_correct: str = False
        certain_value: float = 0
        lottery: Lottery = None
        print("Type first initial values")
        print("Example: L(10, 0.3, 0) 28")
        print("Note: there is no preference sign inbetween\n")

        while not is_input_correct:
            inputs: str = input()
            is_input_correct = True
            if any(forbidden_sign in inputs for forbidden_sign in [">", "<", "~", "="]):
                is_input_correct = False
                print("\nInput contains comparation, remove it")
            elif inputs.find("L") == -1:
                is_input_correct = False
                print("Missing L sign")
            elif inputs.find("(") == -1 or inputs.find(")") == -1:
                is_input_correct = False
                print("Missing open or close bracket... or both")
        
            inputs = inputs.replace(" ", "")
            
            # lottery
            lottery_string: str = inputs[inputs.find("(") + 1 : inputs.find(")")]
            lottery_string_tokens = lottery_string.split(",")
            
            if len(lottery_string_tokens) != 3:
                print("Lottery is incorrect formed, insufficient number of colons - should be 3, found " + min(0,str(len(lottery_string_tokens) - 1)))
                is_input_correct = False
            
            lottery = Lottery(\
                float(lottery_string_tokens[0]),
                float(lottery_string_tokens[1]),
                float(lottery_string_tokens[2]),
                1, 0
            )
            
            print("\nCreated lottery:")
            print(lottery)
            
            certain_value = float(inputs[inputs.find(")") + 1 :])
            print("\nCertain value: ")
            print(certain_value)
        
        return lottery, certain_value
        
    
    def _show_controlls(self) -> str:
        """
        Simple help
        Returns:
            str: ???
        """
        print("\nPrint this help:\t h")
        print("Choose certain value:\t c")
        print("Choose lottery:\t\t l")
        print("Choose indifferent:\t i")
        print("Show all comparations:\t a")
        print("Typing digits 1-9 will move to another parrarel comparation\n")
        

if __name__ == "__main__":
    CLI()