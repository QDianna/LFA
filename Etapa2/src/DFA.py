from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DFA[STATE]:
    S: set[str]                             # alphabet
    K: set[STATE]                           # states
    q0: STATE                               # initial state
    d: dict[tuple[STATE, str], STATE]       # transitions
    F: set[STATE]                           # final states

    def accept(self, word: str) -> bool:
        # simulate the dfa on the given word. return true if the dfa accepts the word, false otherwise
        
        current_state = self.q0

        for s in word:
            if (current_state, s) not in self.d:
                # the transition does not exist => reject the word
                return False
            
            # continue with the transition for symbol s
            current_state = self.d[(current_state, s)]

        # see if the state we ended up in is a final state
        return current_state in self.F


    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
        # optional, but might be useful for subset construction and the lexer to avoid state name conflicts.
        # this method generates a new dfa, with renamed state labels, while keeping the overall structure of the
        # automaton.

        # for example, given this dfa:

        # > (0) -a,b-> (1) ----a----> ((2))
        #               \-b-> (3) <-a,b-/
        #                   /     ⬉
        #                   \-a,b-/

        # applying the x -> x+2 function would create the following dfa:

        # > (2) -a,b-> (3) ----a----> ((4))
        #               \-b-> (5) <-a,b-/
        #                   /     ⬉
        #                   \-a,b-/

        new_DFA = DFA[OTHER_STATE](
            S = self.S,
            K = set(),
            q0 = f(self.q0),
            d = {},
            F = set()
        )

        new_DFA.K.update(f(state) for state in self.K)

        new_DFA.F.update(f(state) for state in self.F)
        
        new_DFA.d = {(f(state), symbol): f(next_state) for (state, symbol), next_state in self.d.items()}
        
        return new_DFA
