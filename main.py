#!/usr/bin/env python3
from circuit import Circuit
import sys

def exit_input(*args, **kwargs) -> str:
    """input(), but exit the program if the text begins with exit. Mostly used for automated testing"""
    x = input(*args, **kwargs)
    if x.startswith('exit'):
        print(x)
        exit()
    if 'test' in sys.argv:
        print(x)
    return x

def run_and_print(bench:Circuit, tv:str):
    _, results = bench.resolve_inputs(tv)
    # top_row, bot_row = "", ""
    # for inp, bit in zip(bench.inputs, tv):
    #     length = len(inp.name) + 2
    #     top_row += f"{inp.name:>{length}s}"
    #     bot_row += f"{bit:>{length}s}"
    # mid_row = len(top_row)*'-' + "--|"
    # top_row += "  |"
    # bot_row += "  |"
    # for out, bit in zip(bench.output, results):
    #     length = len(out.name) + 2
    #     top_row += f"{out.name:>{length}s}"
    #     bot_row += f"{bit:>{length}s}"
    # mid_row += (len(top_row)-len(mid_row))*'-'
    # print(top_row)
    # print(mid_row)
    # print(bot_row)
    print("Inputs:")
    for inp, bit in zip(bench.inputs, tv):
        print(f"   {inp.name}: {bit}")
    print("Outputs:")
    for out, bit in zip(bench.output, results):
        print(f"   {out.name}: {bit}")
    return results

def main():
    # Open a user specified test bench
    bench_name = exit_input("Enter bench name (press enter for default circ.bench): ")
    if not bench_name:
        bench_name = "circ.bench"
    else:
        bench_name
        if not bench_name.startswith("benches/"):
            bench_name = "benches/" + bench_name
        if not bench_name.endswith(".bench"):
            bench_name = bench_name + ".bench"
    bench = Circuit(bench_name)
    
    # Print basic bench information
    print(bench)

    # Print input and output size
    insize = len(bench.inputs)
    outsize = len(bench.output)
    print(f'There are {insize} input bits for {bench.filename}')
    print(f'There are {outsize} output bits for {bench.filename}')
    print(f"The input order is:")
    for inp in bench.inputs:
        print(f'   {inp.name}')
    
    # Ask the user for an input vector
    print()
    tv = exit_input(f"Please enter a {insize} bit tv (e.g. abc=000): ")
    # Run testvector
    run_and_print(bench, tv)
    
    # Ask the user to specify a fault
    print()
    fault = exit_input("Please specify a fault (of the form a-0 or a-b-0): ")

    # Run again with the user's fault
    bench.add_fault(fault)
    results = run_and_print(bench, tv)
    if "D" in results or "D'" in results:
        print("TV is able to detect specified fault")
    else:
        print("TV is NOT able to detect specified fault")
    

if __name__ == "__main__":
    main()
