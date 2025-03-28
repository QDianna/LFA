from .NFA import NFA
from dataclasses import dataclass
import string

class Regex:
    EPSILON = ''
    def thompson(self) -> NFA[int]:
        raise NotImplementedError('the thompson method of the Regex class should never be called')

    # you should extend this class with the type constructors of regular expressions and overwrite the 'thompson' method
    # with the specific nfa patterns. for example, parse_regex('ab').thompson() should return something like:

    # >(0) --a--> (1) -epsilon-> (2) --b--> ((3))

    # extra hint: you can implement each subtype of regex as a @dataclass extending Regex


@dataclass  # creates an NFA for E1 concatenated with E2
class Concat(Regex):
    E1: Regex
    E2: Regex

    def thompson(self) -> NFA[int]:
        # get NFA of each expression & rename the states so there are no coincidences
        nfaE1 = self.E1.thompson().remap_states(lambda state: f'C_E1_{state}')
        nfaE2 = self.E2.thompson().remap_states(lambda state: f'C_E2_{state}')

        S = nfaE1.S.union(nfaE2.S)

        K = nfaE1.K.union(nfaE2.K)

        d = nfaE1.d.copy()
        d.update(nfaE2.d)
        d.update({(state, ''): {nfaE2.q0} for state in nfaE1.F})

        return NFA(S, K, nfaE1.q0, d, nfaE2.F)


@dataclass  # creates an NFA for E1 or E2
class Altern(Regex):
    E1: Regex
    E2: Regex

    def thompson(self) -> NFA[int]:
        # get NFA of each expression & rename the states so there are no coincidences
        nfaE1 = self.E1.thompson().remap_states(lambda state: f'A_E1_{state}')
        nfaE2 = self.E2.thompson().remap_states(lambda state: f'A_E2_{state}')

        S = nfaE1.S.union(nfaE2.S)

        # add new init state '0' and final state '9' to the states of the new NFA
        K = nfaE1.K.union(nfaE2.K, {0, 9})

        d = nfaE1.d.copy()
        d.update(nfaE2.d)
        d.update({(0, ''): {nfaE1.q0, nfaE2.q0}})
        d.update({(state, ''): {9} for state in nfaE1.F})
        d.update({(state, ''): {9} for state in nfaE2.F})

        return NFA(S, K, 0, d, {9})


@dataclass  # creates an NFA for E*
class Star(Regex):
    expr: Regex

    def thompson(self) -> NFA[int]:
        # get NFA of the expression & rename the states
        nfaExpr = self.expr.thompson().remap_states(lambda state: f'SE_{state}')

        # add new init state '0' and final state '9' to the states of the new NFA
        K = nfaExpr.K.union({0, 9})

        d = nfaExpr.d.copy()
        d.update({(0, ''): {nfaExpr.q0, 9}})
        d.update({(state, ''): {nfaExpr.q0, 9} for state in nfaExpr.F})

        return NFA(nfaExpr.S, K, 0, d, {9})


@dataclass  # creates an NFA for E+
class Plus(Regex):
    expr: Regex

    def thompson(self) -> NFA[int]:
        # get NFA of the expression & rename the states
        nfaExpr = self.expr.thompson().remap_states(lambda state: f'PE_{state}')
        
        # add new init state '0' and final state '9' to the states of the new NFA
        K = nfaExpr.K.union({0, 9})

        d = nfaExpr.d.copy()
        d.update({(0, ''): {nfaExpr.q0}})
        d.update({(state, ''): {nfaExpr.q0, 9} for state in nfaExpr.F})

        return NFA(nfaExpr.S, K, 0, d, {9})


@dataclass  # creates an NFA for E?
class Qmark(Regex):
    expr: Regex

    def thompson(self) -> NFA[int]:
        # get NFA of the expression & rename the states
        nfaExpr = self.expr.thompson().remap_states(lambda state: f'QE_{state}')

        # add new init state '0' and final state '9' to the states of the new NFA
        K = nfaExpr.K.union({0, 9})

        d = nfaExpr.d.copy()
        d.update({(0, ''): {nfaExpr.q0, 9}})
        d.update({(state, ''): {9} for state in nfaExpr.F})

        return NFA(nfaExpr.S, K, 0, d, {9})
        

@dataclass  # creates an NFA that accepts any lower-case letter of the alphabet
class LowerCase(Regex):

    def thompson(self) -> NFA[int]:
        S = set(string.ascii_lowercase)

        K = {0, 9}  # the initial state & the final state

        d = {}
        d.update({(0, letter): {9} for letter in string.ascii_lowercase})

        return NFA(S, K, 0, d, {9})


@dataclass  # creates an NFA that accepts any upper-case letter of the alphabet
class UpperCase(Regex):

    def thompson(self) -> NFA[int]:
        S = set(string.ascii_uppercase)

        K = {0, 9}  # the initial state & the final state

        d = {}
        d.update({(0, letter): {9} for letter in string.ascii_uppercase})

        return NFA(S, K, 0, d, {9})


@dataclass  # creates an NFA that accepts any digit (from 0 to 9)
class Numbers(Regex):

    def thompson(self) -> NFA[int]:
        S = set(string.digits)
        
        K = {0, 9}  # the initial state & the final state
        
        d = {}
        d.update({(0, digit): {9} for digit in string.digits})

        return NFA(S, K, 0, d, {9})


@dataclass  # creates an NFA that accepts EPSILON (initial state = final state)
class Epsilon(Regex):

    def thompson(self) -> NFA[int]:
        return NFA(set(), {0}, 0, {}, {0})


@dataclass  # creates an NFA that accepts the given character 'char'
class Character(Regex):
    char: str

    def thompson(self) -> NFA[int]:
        # check if the char is prefixed with '\' and extract it if so
        self.char = self.char[1] if self.char.startswith('\\') else self.char

        S = {self.char}

        K = {0, 9}  # the initial state & the final state

        d = {(0, self.char): {9}}

        return NFA(S, K, 0, d, {9})


def parse_regex(regex: str) -> Regex:
    # create a Regex object by parsing the string

    # you can define additional classes and functions to help with the parsing process

    # the checker will call this function, then the thompson method of the generated object. the resulting NFA's
    # behaviour will be checked using your implementation form stage 1

    # extract each token from the Regex and avoid whitespaces
    i = 0
    tokens = []
    while i < len(regex):
        if regex[i] in ['[', '-', ']', '(', ')', '|', '*', '+', '?']:
            # known operations
            tokens.append(regex[i])
            i += 1
        elif regex[i:i+3] == "eps":
            # epsilon
            tokens.append("eps")
            i += 3
        elif regex[i].isalnum():
            # letters & numbers
            tokens.append(regex[i])
            i += 1
        elif regex[i] == '\\':
            # control characters prefixed with '\'
            tokens.append(regex[i:i+2])
            i += 2
        elif regex[i] != ' ':
            # non-control characters
            tokens.append(regex[i])
            i += 1
        else:
            # skip whitespaces
            i += 1

    # create specific parse functions for each operation
    # the functions call eachother in a descendent order, according to their priorities
    def parse_altern():
        regex = parse_concat()

        while tokens and tokens[0] == '|':
            tokens.pop(0)
            regex = Altern(regex, parse_concat())

        return regex
        
    def parse_concat():
        regex = parse_repeat()

        while tokens and tokens[0] not in [')', '|', '*', '+', '?']:
            regex = Concat(regex, parse_repeat())

        return regex

    def parse_repeat():
        expr = parse_expr()

        if tokens and tokens[0] == '*':
            tokens.pop(0)
            return Star(expr)
        
        elif tokens and tokens[0] == '+':
            tokens.pop(0)
            return Plus(expr)
        
        elif tokens and tokens[0] == '?':
            tokens.pop(0)
            return Qmark(expr)
        
        else:
            return expr
    
    def parse_expr():
        if tokens and tokens[0] == '(':
            tokens.pop(0)

            while tokens and tokens[0] != ')':
                regex = parse_altern()

                if tokens and tokens[0] == ')':
                    tokens.pop(0)
                    return regex

        elif tokens and tokens[0] == '[' and tokens[4] == ']':            
            if tokens[1] == 'a' and tokens[3] == 'z':
               del tokens[:5]
               return LowerCase()
            
            elif tokens[1] == 'A'and tokens[3] == 'Z':
                del tokens[:5]
                return UpperCase()
            
            elif tokens[1] == '0' and tokens[3] == '9':
                del tokens[:5]
                return Numbers()
            
        elif tokens and tokens[0] == "eps":
            tokens.pop(0)
            return Epsilon()

        elif tokens and tokens[0].startswith('\\'):
            regex = Character(tokens[0])
            tokens.pop(0)
            return regex

        elif tokens and tokens[0] not in "|*+?":
            regex = Character(tokens[0])
            tokens.pop(0)
            return regex

    return parse_altern()
