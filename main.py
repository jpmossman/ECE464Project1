#!/usr/bin/env python3
from circuit import Circuit

def exit_input(*args, **kwargs) -> str:
    """input(), but exit the program if the text begins with exit"""
    x = input(*args, **kwargs)
    if x.startswith('exit'):
        print(x)
        exit()
    return x

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
    print(f'There are {len(bench.inputs)} input bits for {bench.filename}')
    print(f'There are {len(bench.output)} output bits for {bench.filename}')

if __name__ == "__main__":
    main()
