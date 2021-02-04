from enum import Enum
from typing import List
from typing import Tuple
from typing import Dict
from typing import Set
from itertools import permutations
import os
import copy

"""Error raised on Preference Profile to Preference Matrix conversion"""
class ConversionError(Exception):
    pass

"""Error raised when user provides insufficient input for given voting system"""
class WrongRepresentationException(Exception):
    pass

class VotingType(Enum):
    PLURALITY = 1
    ANTI_PLURALITY = 2
    APPROVAL = 3
    PLURALITY_RUN_OFF = 4
    STV = 5
    BORDA = 6
    CONDORCETE = 7
    COPELAND = 8
    KAMMENY = 9
    COOMBS = 10
    BALDWIN = 11
    DHONDT = 12
    SAINTE_LEAGUE = 13

class Candidate:
    """
    Class represents single candidate in voting.
    Name field in required, but votes have no strictly defined usage. It can be anything useful for voting like votes on its own but also scores in Borda Voring or other numeric thing losely connected to voting on its own
    """
    def __init__(self, name: str, votes: int = 0):
        self.name: str = name
        self.votes: int = votes
    
    def __str__(self) -> str:
        result: str = "Candidate\n"
        result += "votes: " + str(self.votes) + "\n"
        result += "name: " + str(self.name) + "\n"
        return result

class Ranking:
    """
    Ranking is single ordered list of candidates pointed by voter.
    Class is used in Preference Profile input mode
    """
    def __init__(self, profile: str):
        self.candidates: List[Candidate] = []
        self.votes: int = 0
        self._convert_str_to_object(profile)
        
    def _convert_str_to_object(self, string: str):
        """
        Used to convert input collected from user into Ranking object
        Args:
            string (str): user input
                sample input 
                A > B > C > D : 20
        """

        string = string.replace(" ", "")
        self.votes = int(string.split(":")[1])
        string = string.split(":")[0]
        candidate_names = string.split(">")
        for name in candidate_names:
            self.candidates.append(
                Candidate(name, self.votes)
            )
    
    def is_before(self, a: Candidate, b: Candidate) -> bool:
        """
        Check if candidate a is before candidate b in ranking
        Args:
            a (Candidate)
            b (Candidate)

        Returns:
            bool: true if candidate a is first, otherwise false
        """
        a_pos = 6732487
        b_pos = 6732487
        i = 0
        for candidate in self.candidates:
            if candidate.name == a.name:
                a_pos = i
            if candidate.name == b.name:
                b_pos = i
            i += 1
        return a_pos < b_pos
    
    def last_candidate(self) -> Candidate:
        return self.candidates[len(self.candidates) - 1]
        
    def first_candidate(self) -> Candidate:
        return self.candidates[0]
    
    def remove_candidate(self, candidate_name: str):
        self.candidates = [c for c in self.candidates if c.name != candidate_name]
    
    def __str__(self) -> str:
        response: str = ""
        for candidate in self.candidates:
            response += "{} > ".format(candidate.name)
        response = response[:-3]
        response += " : {}".format(candidate.votes)
        return response
        
class Preference:
    """
    Superclass of any Preference representation like PreferenceProfile or PreferenceMatrix
    """
    def __init__(self):
        pass

class PreferenceMatrix(Preference):
    """
    Represents preference as a matrix. Each field in given as a/b which means candidate in row was before candidate in column a times and b times after him / her.
    Candidates field contains all Candidates mentioned by user.
    Votes are matrix on its own - matrix has no named indexes then
    Sample user input could look like this:
    #> A B C
    #> 0/0 10/20 11/9
    #> 20/10 0/0 3/17
    #> 9/11 17/3 0/0
    Cells on diagonal are 0/0 as of A cannot be before or after itself
    """
    def __init__(self):
        self.candidates: List[Candidate] = []
        self.votes: List[List[Tuple[int]]] = []
    
    def add_candidates(self, string: str):
        """
        Matrix construction proces starts with defining columns headers which are candidates names
        Args:
            string (str): string with list of candidates separated by single space
                sample
                A B C D E
        """
        candidates_names = string.split(" ")
        for name in candidates_names:
            self.candidates.append(
                Candidate(name, 0)
            )

    def add_row(self, string: str):
        """
        Each next typed row is part of votes matrix
        Args:
            string (str): string containing list of pairs divided by space
                sample
                10/21 0/0 12/19 21/10
        """
        cells = string.split(" ")
        row = []
        for cell in cells:
            fields = cell.split("/")
            row.append((int(fields[0]), int(fields[1])))
        self.votes.append(row)
    
    def __str__(self) -> str:
        result = "Preference Matrix: \n"
        for candidate in self.candidates:
            result += candidate.name
            result += "\t"
        result += "\n"
        for row in self.votes:
            for field in row:
                result += str(field[0]) + "/" + str(field[1]) + "\t"
            result += "\n"
        return result

class PreferenceProfile(Preference):
    """
    Represents Preference as list of candidates in order given by users
    Rankings holds mentioned orders in form of list of candidates and number of voters with same proposed order
        Sample rankings are:
            A > B > D : 20
            D > A > C : 10
            A > C > D > B : 5
        Which means that 20 voters prefers candidate A over candidate B over candidate C
    Preference profile track names of all users in all rankings - useful in transformation to preference matrix
    """
    def __init__(self):
        self.rankings: [Ranking] = []
        self.total_votes: int = 0
        self.candidates_names: Set[str] = set()
    
    def add_ranking(self, ranking: str):
        """
        Adds single ranking in form of
            <candidate> > <candidate> > <candidate> ... : <number of voters>
        Args:
            ranking (str): string containing list of candidates in prefered order separated by greater than sign
        """
        ranking = Ranking(ranking)
        self.rankings.append(ranking)
        self.total_votes += ranking.votes
        self._add_candidate_names(ranking)
        
    def _add_candidate_names(self, ranking: Ranking) -> Set[str]:
        """
        Adds non duplicating candidates names into tracking list
        Args:
            ranking (Ranking): ranking from which names should be fetched

        Returns:
            Set[str]: set with appended non-duplicative names
        """
        for candidate in ranking.candidates:
            self.candidates_names.add(candidate.name)
        return self.candidates_names
        
    def remove_candidate(self, candidate_name: str):
        self.candidates_names = set()
        for ranking_idx in range(len(self.rankings)):
            self.rankings[ranking_idx].remove_candidate(candidate_name)
            self._add_candidate_names(self.rankings[ranking_idx])
            
    def to_preference_matrix(self) -> PreferenceMatrix:
        """
        Converts Preference Profile into Preference Matrix. Reverse conversion is not possible
        Returns:
            PreferenceMatrix: equivalent of Preference Profile but in Preference Matrix representation
        """
        # first count in how many rankings candidate A was higher than candidate B
        wins: Dict[str, int] = {}
        # wins key in combined names of candidate A and candidate B
        for ranking in self.rankings:
            better_candidate_idx: int = 0
            ranking_length = len(ranking.candidates)
            while better_candidate_idx < ranking_length:
                for worser_candidate_idx in range(better_candidate_idx + 1, ranking_length):
                    try:
                        wins[ranking.candidates[better_candidate_idx].name + ranking.candidates[worser_candidate_idx].name] += ranking.votes
                    except:
                        wins[ranking.candidates[better_candidate_idx].name + ranking.candidates[worser_candidate_idx].name] = ranking.votes
                # not all rankings contains all candidates, thus not mentioned candidates are added as last and are counted only as candidates which are outranked not outranking others or themselves
                # e.g.
                # candidates = {A, B, C, D, E}
                # single ranking: A > C > B missing D and E which are appended
                # A > C > B (> D > E)
                # to wins dictionary will be added keys: AC, AB, CB, but also AD, AE, CD, CE, BD, BE but not DE - added candidates are not outranking each other as we dont know in which order are they
                missing_candidates = list(self.candidates_names - set(map(lambda e: e.name, ranking.candidates)))
                for missing_candidate_idx in range(len(missing_candidates)):
                    try:
                        wins[ranking.candidates[better_candidate_idx].name + missing_candidates[missing_candidate_idx]] += ranking.votes
                    except:
                        wins[ranking.candidates[better_candidate_idx].name + missing_candidates[missing_candidate_idx]] = ranking.votes
                better_candidate_idx += 1
        # print(wins)
        pm = PreferenceMatrix()
        pm.add_candidates(" ".join(self.candidates_names))
        # converting dictionary into matrix
        for better_candidate_name in self.candidates_names:
            row: str = ""
            for worser_candidate_name in self.candidates_names:
                try:
                    row += str(wins[better_candidate_name + worser_candidate_name]) + "/" + str(self.total_votes - wins[better_candidate_name + worser_candidate_name]) + " "
                except:
                    if better_candidate_name == worser_candidate_name:
                        row += "0/0 "
                    else:
                        row += "0/" + str(self.total_votes) + " "
            row = row[:-1]
            pm.add_row(row)
        return pm
            
    
    def __str__(self) -> str:
        response: str = ""
        response += "PreferenceProfile\n"
        for ranking in self.rankings:
            response += str(ranking) + "\n"
        response += "Candidates names: " + " ".join(self.candidates_names) + "\n"
        response += "Total votes: " + str(self.total_votes) + "\n"
        return response
      
class Token:
    def __init__(self, token_sign: str):
        self.token_string: str = token_sign
        
    def __str__(self) -> str:
        return self.token_string + " "
        
    def __repr__(self):
        return __str__()
        
class Tokens(Enum):
    BETTER = Token(">")
    WORSE = Token("<")
    SAME = Token("~")
    
    def __str__(self):
        return str(self.value)
     
class VotingResult:
    """
    Voting result contains result of single voting. It somewhat follows builder pattern but somehow more chunky. For normalization enumeration containing constant signs / tokens are used. For e.g. better is modeled by Tokens.BETTER and have > sign
        Sample usage
            VotingResult().candidate(<candidate object>).same().candidate(<candidate object>).better(). [...]
    """ 
    def __init__(self):
        self.token_sequence: List[Token] = []  
                
    def tokenize_candidate(self, candidate: Candidate) -> str:
        return Token(candidate.name)
    
    def candidate(self, candidate: Candidate):
        self.token_sequence.append(self.tokenize_candidate(candidate))
        return self
    
    def better(self):
        self.token_sequence.append(Tokens.BETTER)
        return self
    
    def worser(self):
        self.token_sequence.append(Tokens.WORSE)
        return self
        
    def same(self):
        self.token_sequence.append(Tokens.SAME)
        return self
        
    def __str__(self) -> str:
        result: str = ""
        for t in self.token_sequence:
            result += str(t) + " "
        return result
    
class Rule:
    """
    Superclass of any voting system. Contains some common functionalites as preference representation transformation (PreferenceProfile -> PreferenceMatrix). Also has method for checking if conversion was posible otherwise throws an ConversionException
    """
    def __init__(self, votes: Preference):
        self.preference: Preference = copy.deepcopy(votes)
        self.preference_matrix = self._create_preference_matrix(self.preference)
        self.preference_profile = self._create_preference_profile(self.preference)
        
        print(self.preference_matrix)
        print(self.preference_profile)
    
    def _create_preference_matrix(self, votes: Preference) -> PreferenceMatrix:
        if isinstance(votes, PreferenceMatrix):
            return votes
        else:
            return votes.to_preference_matrix()
    
    def _create_preference_profile(self, votes: Preference) -> PreferenceProfile:
        if isinstance(votes, PreferenceProfile):
            return votes
        else:
            return None
            
    def _has_preference_profile(self) -> bool:
        if self.preference_profile is None:
            raise WrongRepresentationException
        else:
            return True
            
    def run(self) -> VotingResult:
        raise NotImplementedError

"""End of common api"""
"""Start of voting rules"""
        
class PluralityRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
        
    def run(self) -> Candidate:
        winners_votes: Dict[str, int] = dict()
        for ranking in self.preference_profile.rankings:
            try:
                winners_votes[ranking.first_candidate().name] += ranking.first_candidate().votes
            except:
                winners_votes[ranking.first_candidate().name] = ranking.first_candidate().votes
        winning_candidate: Candidate = Candidate('ASFASF', -1)
        voting_result: VotingResult = VotingResult()
        for winner in winners_votes.keys():
            if winners_votes[winner] > winning_candidate.votes:
                winning_candidate = Candidate(winner, winners_votes[winner])
                voting_result = VotingResult().candidate(winning_candidate)
            elif winners_votes[winner] == winning_candidate.votes:
                voting_result.same().candidate(Candidate(winner, winners_votes[winner]))
        return voting_result
        
class AntiPluralityRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
    
    def run(self) -> Candidate:
        winners_votes: Dict[str, int] = dict()
        for ranking in self.preference_profile.rankings:
            try:
                winners_votes[ranking.last_candidate().name] += ranking.last_candidate().votes
            except:
                winners_votes[ranking.last_candidate().name] = ranking.last_candidate().votes
        winning_candidate: Candidate = Candidate('ASFASF', 75643211234567)
        voting_result: VotingResult = VotingResult()
        for winner in winners_votes.keys():
            if winners_votes[winner] < winning_candidate.votes:
                winning_candidate = Candidate(winner, winners_votes[winner])
                voting_result = VotingResult().candidate(winning_candidate)
            elif winners_votes[winner] == winning_candidate.votes:
                voting_result.same().candidate(Candidate(winner, winners_votes[winner]))
        return voting_result

class ApprovalRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
        
    def run(self) -> VotingResult:
        total_votes: Dict[str, int] = dict()
        for ranking in self.preference_profile.rankings:
            for candidate in ranking.candidates:
                try:
                    total_votes[candidate.name] += candidate.votes
                except:
                    total_votes[candidate.name] = candidate.votes
        voting_result: VotingResult = VotingResult()
        winning_candidate: Candidate = Candidate("gfhjkgfds", -1)
        for candidate_name, votes in total_votes.items():
            if winning_candidate.votes < votes:
                winning_candidate = Candidate(candidate_name, votes)
                voting_result = VotingResult()
                voting_result.candidate(winning_candidate)
            elif winning_candidate.votes == votes:
                voting_result.same().candidate(Candidate(candidate_name, votes))
        return voting_result

class PluralityRunOffRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
        
    def run(self) -> VotingResult:
        first_places: Dict[str, int] = dict()
        for ranking in self.preference_profile.rankings:
            try:
                first_places[ranking.first_candidate().name] += ranking.first_candidate().votes
            except:
                first_places[ranking.first_candidate().name] = ranking.first_candidate().votes
        first_places = dict(sorted(first_places.items(), key=lambda item: item[1], reverse=True))
        first: Candidate = Candidate(list(first_places)[0], 0)
        second: Candidate = Candidate(list(first_places)[1], 0)
        for ranking in self.preference_profile.rankings:
            if ranking.is_before(first, second):
                first.votes += ranking.votes
            else:
                second.votes += ranking.votes
        if(first.votes > second.votes):
            return VotingResult().candidate(first)
        elif second.votes > first.votes:
            return VotingResult().candidate(second)
        else:
            return VotingResult().candidate(first).same().candidate(second)
            
class SingleTransferableVoteRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
        
    def run(self) -> VotingResult:
        while True:
            first_places: Dict[str, int] = dict()
            for ranking in self.preference_profile.rankings:
                try:
                    first_places[ranking.first_candidate().name] += ranking.first_candidate().votes
                except:
                    first_places[ranking.first_candidate().name] = ranking.first_candidate().votes
            first_places = dict(sorted(first_places.items(), key=lambda item: item[1]))
            removed_candidate_name = list(first_places)[0]
            self.preference_profile.remove_candidate(removed_candidate_name)
            first_places: Dict[str, int] = dict()
            for ranking in self.preference_profile.rankings:
                try:
                    first_places[ranking.first_candidate().name] += ranking.first_candidate().votes
                except:
                    first_places[ranking.first_candidate().name] = ranking.first_candidate().votes
            first_places = dict(sorted(first_places.items(), key=lambda item: item[1], reverse=True))
            first_candidate_name = list(first_places)[0]
            if first_places[first_candidate_name] > self.preference_profile.total_votes // 2:
                return VotingResult().candidate(Candidate(first_candidate_name, first_places[first_candidate_name]))
            elif len(first_places) == 2:
                second_candidate_name = list(first_places)[1]
                return VotingResult().candidate(Candidate(first_candidate_name, first_places[first_candidate_name])).same().candidate(Candidate(second_candidate_name, first_places[second_candidate_name]))

class CondorceteRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        
    def run(self) -> VotingResult:
        voting_result: VotingResult = VotingResult()
        for row_idx in range(len(self.preference_matrix.votes)):
            all_won: bool = True
            for field in self.preference_matrix.votes[row_idx]:
                if field[0] <= field[1] and (field[0] != 0 and field[0] != 0):
                    all_won = False
                    break
            if all_won:
                voting_result.candidate(self.preference_matrix.candidates[row_idx]).same()
        return voting_result
                    
class CopelandRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
    
    def run(self) -> VotingResult:
        max_win_lose_difference_value: int = -1
        voting_result: VotingResult = VotingResult()
        for row_idx in range(len(self.preference_matrix.votes)):
            win_lose_difference: int = 0
            for field in self.preference_matrix.votes[row_idx]:
                if field[0] > field[1]:
                    win_lose_difference += 1
                elif field[0] < field[1]:
                    win_lose_difference -= 1
            if win_lose_difference > max_win_lose_difference_value:
                max_win_lose_difference_value = win_lose_difference
                voting_result = VotingResult()
                voting_result.candidate(self.preference_matrix.candidates[row_idx])
            elif win_lose_difference == max_win_lose_difference_value:
                voting_result.same().candidate(self.preference_matrix.candidates[row_idx])
                
        return voting_result
        
class KamenyRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
    
    def run(self) -> VotingResult:
        all_permutations: List[List[str]] = list(permutations(self.preference_profile.candidates_names))
        best_permutation: List[str] = list()
        best_permutation_score: int = -1
        for permutation in all_permutations:
            score: int = 0
            for better_candidate_idx in range(len(permutation)):
                for worse_candidate_idx in range(better_candidate_idx + 1, len(permutation)):
                    for ranking in self.preference_profile.rankings:
                        if ranking.is_before(Candidate(permutation[better_candidate_idx], 0), Candidate(permutation[worse_candidate_idx], 0)):
                            score += ranking.votes
            if score > best_permutation_score:
                best_permutation = permutation
                best_permutation_score = score
        voting_result = VotingResult()
        for candidate in best_permutation:
            voting_result.candidate(Candidate(candidate, 0)).better()
        return voting_result
                  
class CoombsRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
        
    def run(self) -> VotingResult:
        while True:
            last_places: Dict[str, int] = {}
            for ranking in self.preference_profile.rankings:
                last_candidate: Candidate = ranking.last_candidate()
                try:
                    last_places[last_candidate.name] += last_candidate.votes
                except:
                    last_places[last_candidate.name] = last_candidate.votes
            last_places = dict(sorted(last_places.items(), key=lambda item: item[1], reverse=True))
            self.preference_profile.remove_candidate(list(last_places)[0])
            first_places: Dict[str, int] = {}
            for ranking in self.preference_profile.rankings:
                try:
                    first_places[ranking.first_candidate().name] += ranking.first_candidate().votes
                except:
                    first_places[ranking.first_candidate().name] = ranking.first_candidate().votes
            first_places = dict(sorted(first_places.items(), key=lambda item: item[1], reverse=True))
            first_candidate: Candidate = Candidate(list(first_places)[0], first_places[list(first_places)[0]])
            if first_candidate.votes > self.preference_profile.total_votes // 2:
                return VotingResult().candidate(first_candidate)
            elif len(first_places) == 2:
                second_candidate: Candidate = Candidate(list(first_places)[1], first_places[list(first_places)[1]])
                return VotingResult().candidate(first_candidate).same().candidate(second_candidate)
        
class BordaRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
        
    def run(self) -> VotingResult:
        points: Dict[str, int] = {}
        for ranking in self.preference_profile.rankings:
            mult = len(self.preference_profile.candidates_names) - 1
            for candidate in ranking.candidates:
                try:
                    points[candidate.name] += candidate.votes * mult
                except:
                    points[candidate.name] = candidate.votes * mult
                mult -= 1
        points = dict(sorted(points.items(), key=lambda item: item[1], reverse=True))
        highest_points = points[list(points)[0]]
        voting_result = VotingResult()
        for candidate_name, candidate_points in points.items():
            if candidate_points == highest_points:
                voting_result.candidate(Candidate(candidate_name, candidate_points)).same()
        return voting_result
        
class BaldwinRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
        super()._has_preference_profile()
        
    def run(self) -> VotingResult:
        while True:
            points: Dict[str, int] = {}
            for ranking in self.preference_profile.rankings:
                mult = len(self.preference_profile.candidates_names) - 1
                for candidate in ranking.candidates:
                    try:
                        points[candidate.name] += candidate.votes * mult
                    except:
                        points[candidate.name] = candidate.votes * mult
                    mult -= 1
            points = dict(sorted(points.items(), key=lambda item: item[1], reverse=False))
            self.preference_profile.remove_candidate(list(points)[0])
            total_votes: Dict[str, int] = {}
            for ranking in self.preference_profile.rankings:
                try:
                    total_votes[ranking.first_candidate().name] += ranking.first_candidate().votes
                except:
                        total_votes[ranking.first_candidate().name] = ranking.first_candidate().votes
            total_votes = dict(sorted(total_votes.items(), key=lambda item: item[1], reverse=True))
            first_candidate: Candidate = Candidate(list(total_votes)[0], total_votes[list(total_votes)[0]])
            if first_candidate.votes > (self.preference_profile.total_votes // 2):
                return VotingResult().candidate(first_candidate)
            elif len(total_votes) == 2:
                second_candidate: Candidate = Candidate(list(total_votes)[1], total_votes[list(total_votes)[1]])
                return VotingResult().candidate(first_candidate).same().candidate(second_candidate)

class MaxMinRule(Rule):
    def __init__(self, votes: Preference):
        super().__init__(votes)
    
    def run(self) -> VotingResult:
        mins: Dict[str, int] = {}
        for row_idx in range(len(self.preference_matrix.votes)):
            for field in self.preference_matrix.votes[row_idx]:
                try:
                    if field[0] == 0 and field[1] == 0:
                        continue
                    if mins[self.preference_matrix.candidates[row_idx].name] > field[0]:
                        mins[self.preference_matrix.candidates[row_idx].name] = field[0]
                except:
                    mins[self.preference_matrix.candidates[row_idx].name] = field[0]
                    # print(field[0])
        maximal_votes: int = -1
        # print(mins)
        voting_result: VotingResult = VotingResult()
        for candidate_name, candidate_min_votes in mins.items():
            if candidate_min_votes > maximal_votes:
                maximal_votes = candidate_min_votes
                voting_result = VotingResult()
                voting_result.candidate(Candidate(candidate_name, candidate_min_votes))
            elif candidate_min_votes == maximal_votes:
                voting_result.same().candidate(Candidate(candidate_name, candidate_min_votes))
        return voting_result

"""End of voting rules"""
"""Start of cli implementation"""



if __name__ == "__main__":
    # Voting()
    # pp = PreferenceProfile()
    # pp.add_ranking("A > B > C  > D : 5")
    # pp.add_ranking("B > D > C > A : 7")
    # pp.add_ranking("C > B > A > D : 7")
    # pp.add_ranking("D > C > B > A : 4")
    # print(pp.to_preference_matrix())
    # pm = PreferenceMatrix()
    # pm.add_candidates("A B C")
    # pm.add_row("10/20 10/11 41/12")
    # pm.add_row("10/21 512/2 6/12")
    # pm.add_row("4/52 4/12 5/23")
    # print(BaldwinRule(pp).run())
    """ print(VotingResult().candidate(Candidate('A', 20)).better().candidate(Candidate('B', 30))) """
    Voting()