"""
This is where the implementation of the plugin code goes.
The ImportFromPy-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
from .parser import PyToSm

# Setup a logger
logger = logging.getLogger('ImportFromPy')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ImportFromPy(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        META = self.META
        config = self.get_current_config()
        input = self.get_file(config['file'])
        parser = PyToSm()

        descriptor = parser.getJson(input)
        smNode = core.create_child(active_node, META['StateMachine'])
        core.set_attribute(smNode, 'name', descriptor['name'])
        states = {}
        for state in descriptor['states']:
            if descriptor['regulars'][state] == True:
                node = core.create_child(smNode, META['State'])
            else:
                node = core.create_child(smNode, META['End'])
            states[state] = node
            
            core.set_attribute(node, 'name', state)
            states[core.get_path(node)] = node
        
        init = core.create_child(smNode, META['Init'])
        initTr = core.create_child(smNode, META['Transition'])
        core.set_pointer(initTr, 'src', init)
        core.set_pointer(initTr, 'dst', states[descriptor['current']])
        
        for transition in descriptor['transitions']:
            node = core.create_child(smNode, META['Transition'])
            core.set_attribute(node, 'event', transition['event'])
            core.set_pointer(node, 'src', states[transition['from']])
            core.set_pointer(node, 'dst', states[transition['to']])

        self.util.save(root_node, self.commit_hash, 'master', 'Imported StateMachine from file')
        
