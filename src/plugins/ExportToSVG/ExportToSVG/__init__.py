"""
This is where the implementation of the plugin code goes.
The ExportToSVG-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
import graphviz

# Setup a logger
logger = logging.getLogger('ExportToSVG')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ExportToSVG(PluginBase):
    def main(self):
        core = self.core
        active_node = self.active_node
        META = self.META

        #initializing our graph
        modelfile = self.commit_hash.replace('#','_') + '_' + core.get_path(active_node).replace('/','_') 
        g = graphviz.Digraph(core.get_attribute(active_node, 'name'), format='svg', filename= modelfile)
        g.attr(rankdir='LR', size='8,5')

        # Loading all nodes for easy iteration
        nodes = core.load_sub_tree(active_node)

        for node in nodes:
            if core.is_type_of(node, META['State']):
                if core.is_type_of(node, META['Init']):
                    g.attr('node', shape='point')
                    g.node(core.get_attribute(node, 'name'))
                else:
                    g.attr('node', shape='circle')
                    g.node(core.get_attribute(node, 'name'))
        for node in nodes:
            if core.is_type_of(node, META['Transition']):
                current_state = core.load_pointer(node, 'src')
                current_state_name = core.get_attribute(current_state, 'name')
                event_name = core.get_attribute(node, 'event')
                next_state = core.load_pointer(node, 'dst')
                next_state_name = core.get_attribute(next_state, 'name')
                g.edge(current_state_name, next_state_name, label=event_name)

        
        # Printing execution initiation code
        g.render(directory='./src/common/svg')           
