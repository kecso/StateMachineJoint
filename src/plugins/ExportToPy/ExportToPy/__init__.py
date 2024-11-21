"""
This is where the implementation of the plugin code goes.
The ExportToPy-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
import os


# Setup a logger
logger = logging.getLogger('ExportToPy')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
dirpath = os.path.dirname(os.path.abspath(__file__))
domainCode = open(os.path.join(dirpath,'domainSM.py'), 'r').read()

class ExportToPy(PluginBase):
    def main(self):
        core = self.core
        active_node = self.active_node
        META = self.META

        # Printing static imports and SM creation command
        model_code = "from .domainSM import StateMachine\n\n"
        model_name = core.get_attribute(active_node, 'name')
        model_code += model_name + " = StateMachine()\n"
        
        # Loading all nodes for easy iteration
        nodes = core.load_sub_tree(active_node)

        for node in nodes:
            if core.is_type_of(node, META['State']) and not core.is_type_of(node, META['Init']):
                model_code += model_name + ".add_state(\"" + core.get_attribute(node, 'name') + "\")\n"

        events = []
        transitions = []
        for node in nodes:
            if core.is_type_of(node, META['Transition']):
                current_state = core.load_pointer(node, 'src')
                current_state_name = core.get_attribute(current_state, 'name')
                event_name = core.get_attribute(node, 'event')
                next_state = core.load_pointer(node, 'dst')
                next_state_name = core.get_attribute(next_state, 'name')

                if core.is_type_of(current_state, META['Init']):
                    model_code += model_name + ".set_current_state(\"" + next_state_name + "\")\n"  
                else:
                    transitions.append({'from': current_state_name, 'event': event_name, 'to': next_state_name})
                    if not event_name in events:
                        events.append(event_name)
                        model_code += model_name + ".add_event(\"" + event_name + "\")\n"
        
        for transition in transitions:
            model_code += model_name + ".add_transition(\"" + transition['from'] + "\", \"" + transition['event'] + "\", \"" + transition['to'] + "\")\n"

        # Printing execution initiation code
        model_code += "\n" + model_name + ".run()\n"
        logger.debug(model_code)

        artifact = {}
        artifact['domainSM.py'] = domainCode
        artifact[model_name + '.py'] = model_code
        self.add_artifact('SmToPy_' + model_name, artifact)           

                


