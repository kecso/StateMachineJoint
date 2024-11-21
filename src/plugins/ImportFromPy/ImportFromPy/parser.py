from lark import Lark
from lark.visitors import Interpreter

grammar = r"""
code: instruction+
instruction: definition
    | importing
    | state
    | event
    | current
    | transition
    | run

importing: "from" "domainSM" "import" "StateMachine"
definition: WORD "= StateMachine()"
state: WORD ".add_state('" WORD "')"
event: WORD ".add_event('" WORD "')"
current: WORD ".set_current_state('" WORD "')"
transition: WORD ".add_transition('" WORD "'" "," "'" WORD "'" "," "'" WORD "')"
run: WORD ".run()"
WORD: /[a-zA-Z0-9_]+/
%import common.NEWLINE
%import common.WS
%ignore WS
"""
class PyToSmInterpreter(Interpreter):
    def __init__(self):
        self.json = {'name':'', 'current': None, 'events': [], 'states': [], 'transitions': [], 'regulars':{}}

    def definition(self, tree):
        #print('DEF', tree)
        self.json['name'] = tree.children[0].value
    def state(self, tree):
        #print('STATE', tree)
        #print(tree.children[1])
        self.json['states'].append(tree.children[1].value)
    def event(self, tree):
        #print('EVENT', tree)
        #print(tree.children[1])
        self.json['events'].append(tree.children[1].value)
    def transition(self, tree):
        #print('TRANSITION', tree)
        self.json['transitions'].append({'from': tree.children[1].value, 'event': tree.children[2].value, 'to': tree.children[3].value})
        self.json['regulars'][tree.children[1].value] = True
    def current(self, tree):
        #print('CURRENT', tree)
        self.json['current'] = tree.children[1].value


class PyToSm():
    def __init__(self):
        self.interpreter = PyToSmInterpreter()
        self.parser = parser = Lark(grammar=grammar,start='code', parser="lalr")
    
    def getJson(self, text):
        tree = self.parser.parse(text)
        self.interpreter.visit(tree)
        return self.interpreter.json

