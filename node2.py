from typing import NamedTuple, Dict, List
from copy import deepcopy as copy
import re
import state5 as s5

class Node2:
    """
    Declare the class early so that the NodeGraph() function can have type hints
    """
    pass

def NodeGraph() -> Dict[str,Node2]:
    """
    Return a dictionary for representing a graph of nodes. Not actually special
    in any way but this is more to help point out the necessary structure of
    other code
    """
    return {}

class Node2:
    def __init__(self,name:str,gtype:str,ilist:List[str],role:str,parent_graph:Dict[str,Node2]) -> None:
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
        self.faults = []

        # Figure out which function to use for resolution
        if self.gtype == 'and':
            self.func = s5.S5_AND
        elif self.gtype == 'nand':
            self.func = s5.S5_NAND
        elif self.gtype == 'or':
            self.func = s5.S5_OR
        elif self.gtype == 'nor':
            self.func = s5.S5_NOR
        elif self.gtype == 'xor':
            self.func = s5.S5_XOR
        elif self.gtype == 'xnor':
            self.func = s5.S5_XNOR
        elif self.gtype == 'not':
            self.func = s5.S5_NOT
        
        # Check if node has already been added to graph
        if name in self.pg:
            if self.pg[name].role == 'intern' and self.role == 'output':
                self.pg[name].role = 'output'
            elif self.pg[name].role == 'intern' and self.role == 'input':
                self.pg[name].role = 'input'
            elif self.pg[name].role == 'output' and self.role == 'intern':
                self.pg[name].ilist = ilist
                self.pg[name].gtype = gtype.lower()
                self.pg[name].func = self.func
            elif self.pg[name].role == 'input' and self.role == 'intern':
                self.pg[name].ilist = ilist
                self.pg[name].gtype = gtype.lower()
                self.pg[name].func = self.func
        # If not, add node to graph
        else:
            self.pg[name] = self

    @staticmethod
    def from_expression(expr:str,parent_graph:Dict[str,Node2]) -> Node2:
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
        # Instantiate Node2 object from parsed expression
        return Node2(name,gtype,ilist,role,parent_graph)


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
    
    def get_inputs(self) -> List[Node2]:
        return [self.pg[n] for n in self.ilist]
    
    def resolve(self) -> str:
        # Return current state if it has been set
        if self.state != '~':
            return self.state
        # Get a list of and resolve all input states
        inputs = [self.pg[name].resolve() for name in self.ilist]
        # Search for faults and perform 5 state algebra
        for f in self.faults:
            if f[0] == 'input':
                pass
        # Resolve output state dependent on gate type and input states
        self.state = self.func(*inputs)
        # Return current state
        return self.state

    def add_fault(self, fault:str) -> bool:
        """
        Attach a fault to the node. Faults are of the form a-b-0 or a-0
        """
        # Determine form of fault
        if fault.count('-') > 2: # Fault formatted incorrectly
            pass # Raise some sort of format error
        elif fault.count('-') == 2: # Input SA fault
            parent, child, val = fault.split('-')
            if parent != self.name:
                pass # Raise some sort of error?
            else:
                self.faults.append(("input", child, val))
        elif fault.count('-') == 1: # Output SA fault
            parent, val = fault.split('-') 
            if parent != self.name:
                pass # Raise some sort of error?
            else:
                self.faults.append(("output",val))
        else: # Fault formatted incorrectly
            pass # Raise some sort of format erro

    def clear_faults(self) -> int:
        """
        Remove all faults
        """
        count = len(self.faults)
        self.faults = []
        return count

    def doubly_link(self) -> bool:
        """
        Doubly link the graph for fault tv generation purposes
        """
    
    def __repr__(self) -> str:
        string = f"Node2: {self.name}\n"
        string += f"   {self.role}\n"
        string += f"   {self.gtype}\n"
        string += f"   {self.ilist}\n"
        return string
