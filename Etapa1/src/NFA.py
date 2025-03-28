from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        # compute the epsilon closure of a state (you will need this for subset construction)
        # see the EPSILON definition at the top of this file

        # stack to store the states I go through (starting with the state I got as parameter)
        states_stack = [state]

        # resulting set of epsilon closure states
        epsilon_cls_set = set()

        while states_stack:
            # extract a state from stack
            current_state = states_stack.pop()

            # add current state to the set
            epsilon_cls_set.add(current_state)

            # find all epsilon transitions for the current state
            epsilon_trs_set = self.d.get((current_state, EPSILON), set())

            # add the states that i can get to with epsilon trs to the stack (if not visited yet)
            states_stack.extend(state for state in epsilon_trs_set if state not in epsilon_cls_set)

        return epsilon_cls_set


    def subset_construction(self) -> DFA[frozenset[STATE]]:
        # convert this nfa to a dfa using the subset construction algorithm

        # init a new DFA instance
        new_DFA = DFA[frozenset[STATE]](
            S = self.S,
            K = set(),
            q0 = frozenset(self.epsilon_closure(self.q0)),
            d = {},
            F = set()
        )
        
        # sink state that I might need
        sink_state = frozenset({'sink'})

        # queue to store states that I need to process
        processing_states_queue = [new_DFA.q0]

        # set to store states that I finished processing
        processed_states_set = set()

        while processing_states_queue:
            current_dfa_state = processing_states_queue.pop(0)

            # add the current state to the K (states) set of DFA
            new_DFA.K.add(current_dfa_state)

            # determine the next DFA state for each transition from current DFA state
            for symbol in self.S:
                next_states_on_symbol = set()
                next_states = set()

                # for each NFA state composing the DFA state, get their next states
                # on the current symbol and their epsilon closures
                for nfa_state in current_dfa_state:
                    next_states_on_symbol = self.d.get((nfa_state, symbol), set())
                    
                    for state in next_states_on_symbol:
                        next_states.update(s for s in self.epsilon_closure(state) if s not in next_states)

                if not next_states:
                    # I need to use the sink state                    
                    if sink_state not in new_DFA.K:
                        # add the sink state to the K set and it's transitions to itself to the transitions dictionary
                        new_DFA.d.update({(sink_state, s): sink_state for s in new_DFA.S})
                        new_DFA.K.add(sink_state)

                    # set transition from current state to sink on the current symbol
                    new_DFA.d[(current_dfa_state, symbol)] = sink_state

                else:
                    # I need to create a frozenset state for the next DFA state and add the transition to it
                    next_dfa_state  = frozenset(next_states)
                    new_DFA.d[(current_dfa_state, symbol)] = next_dfa_state

                    # add the DFA state that I created to the processing queue
                    processing_states_queue.append(next_dfa_state) if next_dfa_state not in processed_states_set else None
            
            # check if the DFA state contains an NFA final state
            if any(state in self.F for state in current_dfa_state):
                new_DFA.F.add(current_dfa_state)

            # add the current DFA state to the finished states
            processed_states_set.add(current_dfa_state)

        # create and return the DFA
        return new_DFA


    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        # optional, but may be useful for the second stage of the project. Works similarly to 'remap_states'
        # from the DFA class. See the comments there for more details.
        
        new_NFA = NFA[OTHER_STATE](
            S = self.S,
            K = set(),
            q0 = f(self.q0),
            d = {},
            F = set()
        )

        new_NFA.K.add(f(state) for state in self.K)
        
        new_NFA.F.add(f(state) for state in self.F)
        
        for (state, c), next_state in self.d.items():
            # in an NFA I can have multiple next-states on the same symbol
            new_NFA.d[f(state), c].add(f(next_state))
        
        return new_NFA
