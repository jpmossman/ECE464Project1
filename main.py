#!/usr/bin/env python3
from circuit import Circuit
import sys
import matplotlib.pyplot as plt
from random import getrandbits, seed
from time import time

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

def plot(name):
    """
    Dependending on if 'test' was passed in via the command line:
    Either save the plot or show the plot
    """
    if 'test' in sys.argv:
        plt.savefig(name)
        plt.figure()
    elif 'skip' in sys.argv:
        pass
    else:
        plt.show()

def part_A():
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

def part_B():
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
    
    # Print out all faults
    faults = bench.all_possible_faults()
    print()
    print(f"There are {len(faults)} possible faults:")
    for f in faults:
        print(f'   {f}')
    
    # Ask the user for an input vector
    print()
    tv = exit_input(f"Please enter a {insize} bit tv (e.g. abc=000): ")
    # Run testvector on all faults
    detected = []
    for f in faults:
        bench.add_fault(f)
        _, results = bench.resolve_inputs(tv)
        if "D" in results or "D'" in results:
            print(f"   HIT!  {f}")
            detected.append(f)
        else:
            print(f"   miss. {f}")
        bench.clear_fault(f.split('-')[0])
    print(f'{100*len(detected)/len(faults):02.3f}% of faults covered by the TV {tv}.')

def part_C():
    return
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

    # Print input and output size
    insize = len(bench.inputs)
    outsize = len(bench.output)
    print(f'There are {insize} input bits for {bench.filename}')
    print(f'There are {outsize} output bits for {bench.filename}')

    # Ask for random seed
    user_seed = exit_input("Enter a random seed (leave blank to use system time): ")
    if user_seed == '':
        user_seed = time()
    seed(user_seed)

    # Generate random strings
    MAX_NUM_STRINGS = 10
    rand_bit_strings = []
    print("Random strings used:")
    for _ in range(MAX_NUM_STRINGS):
        rand_bit_strings.append(bin(getrandbits(insize))[2:].zfill(insize))
        print("   "+rand_bit_strings[-1])
    
    # Run trials
    faults = bench.all_possible_faults()
    coverages = []
    for i in range(MAX_NUM_STRINGS):
        detected = 0
        for f in faults:
            bench.add_fault(f)
            for tv in rand_bit_strings[:i+1]:
                _, results = bench.resolve_inputs(tv)
                if "D" in results or "D'" in results:
                    detected += 1
                    break
            bench.clear_fault(f.split('-')[0])
        coverages.append(detected / len(faults))
    
    # Print results
    print("Here is how fault coverage % improves with the number of TVs:")
    for i, cov in enumerate(coverages):
        print(f"   {i+1: 3d}: {cov*100}%")
    
    # Plot results
    plt.plot([x+1 for x in range(MAX_NUM_STRINGS)], coverages)
    plt.xlabel('Number of TVs')
    plt.ylabel('Fault Coverage')
    plt.title(
        f'Fault Coverage vs Number of Random TVs\n'
        f'{bench.filename} with seed {user_seed}'
        )
    plot('report/testouts/'+''.join(bench.filename.split('.')[:-1]).split('/')[-1]+'.png')

def main():
    print(
        "Would you like to see:\n"
        "   A: Single TV, single fault\n"
        "   B: Single TV, all faults\n"
        "   C: Fault coverage of 1-10 TVs\n"
    )
    choice = exit_input("Choose A, B, or C: ")
    if choice == 'A':
        part_A()
    elif choice == 'B':
        part_B()
    elif choice == 'C':
        part_C()
    

if __name__ == "__main__":
    main()
