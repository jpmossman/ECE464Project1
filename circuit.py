"""
JP Mossman, Fall 2022
"""
from copy import deepcopy as copy
from node2 import Node2, NodeGraph
from typing import Dict, List, Union, Tuple

class Circuit:
    """
    A combinational circuit, composed of a graph of nodes with gate connections
    Can be evaluated for different inputs, outputs, or internal states
    """
    def __init__(self,filename:str=None, filecontent:str=None) -> None:
        self.filename = filename
        # Check that some input was given
        if filename is None and filecontent is None:
            raise FileNotFoundError

        # Set the content
        # Read in lines, remove leading and trailing whitespaces
        if filename is not None:
            lines = open(filename).readlines()    
        else:
            self.filename = ''
            lines = filecontent.split('\n')
        # Remove leading and trailing spaces from content, as well as comments
        self.content = [l.split('#')[0].strip() for l in lines]
        # Remove blank lines
        self.content = [l for l in self.content if l]

        # Determine the nodes
        self.graph:Dict[str,Node2] = NodeGraph()
        for line in self.content:
            node = Node2.from_expression(line,self.graph)

        # Get lists of nodes
        self.inputs:List[Node2] = [
            node
            for name, node in self.graph.items()
            if node.role == 'input'
        ]
        self.intern:List[Node2] = [
            node
            for name, node in self.graph.items()
            if node.role == 'intern'
        ]
        self.output:List[Node2] = [
            node
            for name, node in self.graph.items()
            if node.role == 'output'
        ]
    
    def resolve_inputs(self, inputs:Union[Dict[str,str], str]) -> Tuple[List[Node2], List[str]]:
        """
        Recursively resolve the values of the output nodes for a given input
        """
        # Set input values
        if isinstance(inputs, dict):
            for node in self.inputs:
                node.state = inputs[node.name]
        elif isinstance(inputs, str):
            for node, bit in zip(self.inputs, inputs):
                node.state = bit
        outputs = []
        for node in self.output:
            outputs.append(node.resolve())
        return self.output, outputs
    
    def __repr__(self) -> str:
        # TODO: Align input column so that longer inputs look nice
        max_node_name = max((len(name) for name, _ in self.graph.items()))
        max_num_in = max(len(node.ilist) for name, node in self.graph.items())

        # Some formatting variables
        fmt_nw = max(max_node_name,4) # Name width
        fmt_tw = 5 # Type width
        fmt_rw = 5 # Num width
        fmt_iw = (max_num_in+2) * max_node_name # Inputs width
        fmt_lw = 6 # Level width
        fmt_in = max_node_name # Width of each name in Inputs column
        
        # First line
        string = "Circuit " + self.filename + ":\n"
        
        # Inputs
        string += f"Inputs ({len(self.inputs)}):\n"
        for i in self.inputs:
            string += f"   {i.name:<{fmt_nw}s}\n"
        
        # Internal gates
        string += f"Internal Gates ({len(self.intern)}):\n"
        string += f"   {'name':<{fmt_nw}s}|"
        string += f" {'level':<{fmt_lw}s}|"
        string += f" {'type':<{fmt_tw}s}|"
        string += f" {'# In':<{fmt_rw}s}|"
        string += f"  {'Inputs':<{fmt_iw}s}"
        string += '\n'
        string += '   ' + '-'*fmt_nw+'+-' +'-'*fmt_lw+'+-' +'-'*fmt_tw+'+-' +'-'*fmt_rw+'+--' +'-'*fmt_iw + '\n'
        for i in self.intern:
            string += f"   {i.name:<{fmt_nw}s}|"
            string += f" {i.get_level():<{fmt_lw}d}|"
            string += f" {i.gtype:<{fmt_tw}s}|"
            string += f" {len(i.ilist):<{fmt_rw}d}|"
            string += '  ' + '  '.join(n.ljust(fmt_in) for n in i.ilist)
            string += '\n'
        
        # Output gates
        string += f"Outputs ({len(self.output)}):\n"
        for i in self.output:
            string += f"   {i.name:<{fmt_nw}s}|"
            string += f" {i.get_level():<{fmt_lw}d}|"
            string += f" {i.gtype:<{fmt_tw}s}|"
            string += f" {len(i.ilist):<{fmt_rw}d}|"
            string += '  ' + '  '.join(n.ljust(fmt_in) for n in i.ilist)
            string += '\n'

        return string

# If the file is called directly, run some tests
def main():
    string = \
    """
    INPUT(a)
    INPUT(b)
    c' = NOT(c)
    w = AND(a, b, c)
    e = AND(a', b, c)
    INPUT(c)
    OUTPUT(w)
    OUTPUT(x)
    x = OR(d, e, f)
    y = OR(g, h)
    z = NOT(c)
    d = AND(a, b')
    OUTPUT(y)
    OUTPUT(z)
    a' = NOT(a)
    b' = NOT(b)
    f = AND(a, b, c')
    g = AND(b', c)
    h = AND(b, c')
    """

    print("Part 1: Parsing the bench")
    # x = Circuit(filecontent=string)
    x = Circuit(filename='benches/hw1.bench')
    # x = Circuit(filename='benches/c17.bench')
    print(x)

    print("Part 2: Solving the bench")
    results = []
    for i in range(2**len(x.inputs)):
        input_vector = bin(i)[2:].zfill(len(x.inputs))
        inputs = {}
        for inp, val in zip(x.inputs, input_vector):
            inputs[inp.name] = val
        results.append((inputs,x.resolve_inputs(inputs)))
    
    # Print top line
    mid_line_format = ""
    top_line_left = ""
    for inp in x.inputs:
        top_line_left += f" {inp.name:>2s}"
        mid_line_format += " "*len(f"{inp.name:>2s}") + "{}"
    mid_line_format += " |"
    top_line_right = ""
    for out in x.output:
        top_line_right += f" {out.name:>2s}"
        mid_line_format += " "*len(f"{out.name:>2s}") + "{}"
    top_line = top_line_left + " |" + top_line_right
    print(top_line)
    print('-'*len(top_line_left) + "-+" + '-'*len(top_line_right))
    print(results)
    for r in results:
        vals = []
        for i in x.inputs:
            vals.append(r[1].nodes[i].state)
        for o in x.output:
            vals.append(r[1].nodes[o].state)
        print(mid_line_format.format(*vals))

if __name__ == '__main__':
    main()
