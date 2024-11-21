class State:
    def __init__(self, name):
        self.name = name

class Event:
    def __init__(self, name) -> None:
        self.name = name

class Transition:
    def __init__(self, current, event, next):
        self.current_state = current
        self.next_state = next
        self.event = event

class StateMachine:
    def __init__(self):
        self.states = {}
        self.events = {}
        self.transitions = []
        self.current_state = None

    def add_state(self, state_name):
        if state_name not in self.states:
            self.states[state_name] = State(state_name)

    def add_event(self, event_name):
        if event_name not in self.events:
            self.events[event_name] = Event(event_name)

    def set_current_state(self, state_name):
        if state_name in self.states:
            self.current_state = self.states[state_name]
        else:
            raise ValueError(f"State '{state_name}' does not exist.") 

    def add_transition(self, current_state_name, event_name, next_state_name):
        if current_state_name not in self.states:
            raise ValueError(f"Current state '{current_state_name}' does not exist.")
        if event_name not in self.events:
            raise ValueError(f"Event '{event_name}' does not exist.")
        if next_state_name not in self.states:
            raise ValueError(f"Next state '{next_state_name}' does not exist.")

        current_state = self.states[current_state_name]
        event = self.events[event_name]
        next_state = self.states[next_state_name]
        self.transitions.append(Transition(current_state, event, next_state))
    
    def transition(self, event_name):
        if self.current_state is None:
            raise ValueError("Current state is not set.")
        if event_name not in self.events:
            raise ValueError(f"Event '{event_name}' does not exist.")
 
        event = self.events[event_name]
        for transition in self.transitions:
            if transition.current_state == self.current_state and transition.event == event:
                self.current_state = transition.next_state
                print(f"Transitioned to {self.current_state.name}")
                return

        raise ValueError(f"No valid transition for event '{event_name}' from state '{self.current_state.name}'.")
    
    def is_deterministic(self):
        # Must have exactly one current state
        if self.current_state is None:
            return False
        
        # Given a state and an event, not more than one next state cen be defined
        for i, transition1 in enumerate(self.transitions):
            for j, transition2 in enumerate(self.transitions):
                if i != j and transition1.current_state == transition2.current_state:
                    if transition1.event == transition2.event and transition1.next_state != transition2.next_state:
                        return False
        
        return True

    def print_current(self):
        print(f"Current state is [{self.current_state.name}]")
        print('Valid events from current state:')
        for transition in self.transitions:
            if(transition.current_state == self.current_state):
                print(transition.event.name)
    
    def await_input(self):
        print("Please enter the next event's name:")
        event_name = input()
        self.transition(event_name)

    def is_finished(self):
        outgoing = 0
        for transition in self.transitions:
            if(transition.current_state == self.current_state):
                outgoing += 1
        return outgoing == 0

    def run(self):
        print('Start machine execution')
        if not self.is_deterministic():
            raise ValueError('The state machine is non-deterministic!!!')
        
        is_finished = self.is_finished()
        while not is_finished:
            self.print_current()
            self.await_input()
            is_finished = self.is_finished()
        
        
