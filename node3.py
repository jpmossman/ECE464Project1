from typing import NamedTuple, Dict, List
from copy import deepcopy as copy
import re

class Node3:
    """
    Declare the class early so that the NodeGraph() function can have type hints
    """
    pass

def NodeGraph() -> Dict[str,Node3]:
    """
    Return a dictionary for representing a graph of nodes. Not actually special
    in any way but this is more to help point out the necessary structure of
    other code
    """
    return {}

class Node3:
    def __init__(self,name:str,gtype:str,ilist:list[str],role:str,parent_graph:Dict[str,Node3]) -> None:
        """
        A class for representing a node in combinational circuit.
        Second version of this class, has some major differences such as using
        a dictionary as a graph and representing it's data quite differently.
        """
        self.name = name
        self.gtype = gtype.lower()
        self.ilist = ilist
        self.role = role
        self.state = '~'
        self.level = None
        self.pg = parent_graph
        
        # Check if node has already been added to graph
        if name in self.pg:
            if self.pg[name].role == 'intern' and self.role == 'output':
                self.pg[name].role = 'output'
            elif self.pg[name].role == 'intern' and self.role == 'input':
                self.pg[name].role = 'input'
            elif self.pg[name].role == 'output' and self.role == 'intern':
                self.pg[name].ilist = ilist
                self.pg[name].gtype = gtype.lower()
            elif self.pg[name].role == 'input' and self.role == 'intern':
                self.pg[name].ilist = ilist
                self.pg[name].gtype = gtype.lower()
        # If not, add node to graph
        else:
            self.pg[name] = self

    @staticmethod
    def from_expression(expr:str,parent_graph:Dict[str,Node3]) -> Node3:
        """
        Construct a node using an expression from a bench file
        """
        # Check if input
        if match := re.search(r"input *\(([^\)]*)\)", expr, re.I|re.M):
            name = match.group(1)
            role = 'input'
            gtype, ilist = 'USER', []
        # Check if output
        elif match := re.search(r"output *\(([^\)]*)\)", expr, re.I|re.M):
            name = match.group(1)
            role = 'output'
            gtype, ilist = 'UNKNOWN', []
        # Check if internal
        elif match := re.search(r"([^\s]*) *= *(.*)", expr, re.I|re.M):
            name = match.group(1)
            role = 'intern'
            gtype, *ilist = re.findall(r"([^_\W][\w']*)",expr)[1:]
        # Else, no matching type found
        else:
            raise SyntaxError(f'{expr} does not match any known definition')
        # Instantiate Node3 object from parsed expression
        return Node3(name,gtype,ilist,role,parent_graph)


    def get_level(self) -> int:
        """
        Recursively figure out the level of the node, with inputs being level 0
        """
        if self.level is not None:
            return self.level
        if self.role == 'input':
            self.level = 0
            return self.level
        else:
            self.level = max((self.pg[n].get_level() for n in self.ilist)) + 1
            return self.level
    
    def get_inputs(self) -> List[Node3]:
        return [self.pg[n] for n in self.ilist]
    
    def resolve(self) -> str:
        # Return current state if it has been set
        if self.state != '~':
            return self.state
        # Get a list of and resolve all input states
        inputs = [self.pg[name].resolve() for name in self.ilist]
        # Resolve output state dependent on gate type and input states
        if self.gtype == 'and':
            if all(i == '1' for i in inputs):
                self.state = '1'
            elif any(i == '0' for i in inputs):
                self.state = '0'
            else:
                self.state = 'u'
        elif self.gtype == 'nand':
            if all(i == '1' for i in inputs):
                self.state = '0'
            elif any(i == '0' for i in inputs):
                self.state = '1'
            else:
                self.state = 'u'
        elif self.gtype == 'or':
            if any(i == '1' for i in inputs):
                self.state = '1'
            elif all(i == '0' for i in inputs):
                self.state = '0'
            else:
                self.state = 'u'
        elif self.gtype == 'nor':
            if any(i == '1' for i in inputs):
                self.state = '0'
            elif all(i == '0' for i in inputs):
                self.state = '1'
            else:
                self.state = 'u'
        elif self.gtype == 'xor':
            if any(i != '0' and i != '1' for i in inputs):
                self.state = 'u'
            elif inputs.count('1') % 2 == 1:
                self.state = '1'
            else:
                self.state = '0'
        elif self.gtype == 'xnor':
            if any(i != '0' and i != '1' for i in inputs):
                self.state = 'u'
            elif inputs.count('1') % 2 == 1:
                self.state = '0'
            else:
                self.state = '1'
        elif self.gtype == 'not':
            if inputs[0] == '0' or inputs[0] == '1':
                self.state = '0' if inputs[0] == '1' else '1'
            else:
                self.state = 'u'
        else:
            raise RuntimeError('Could not resolve state')
        # Return current state
        return self.state

    def __repr__(self) -> str:
        string = f"Node3: {self.name}\n"
        string += f"   {self.role}\n"
        string += f"   {self.gtype}\n"
        string += f"   {self.ilist}\n"
        return string
