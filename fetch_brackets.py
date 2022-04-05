#!/usr/bin/env python
from database import getNewBracketBitstring
from lib.bracket import BracketType
from lib.bracket.sample import F4_A, E_8

def bit_to_hexstring(bitstring):
    integer_val = int(bitstring, 2)
    return "{:016X}".format(integer_val)

if __name__ == '__main__':
    # TODO: Add command-line arguments for 
    # how many brackets per pool and 
    # how many pools to fetch. 
    brackets_per_pool = 100000
    num_pools = 10

    for type in ["men"]:
        print(type)
        
        for sfn_name in [None, "f4a", "e8"]:
            print(sfn_name)
            sfn = None if (not sfn_name) else (F4_A() if sfn_name == "f4a" else E_8())
            
            for pool_index in range(num_pools):
                filename = "bracket_pools/bracket_pool_{0}_{1}_{2:02d}.txt".format(type, sfn_name if sfn_name else "default", pool_index)
                with open(filename, 'w') as out_f:
                    for bracket_index in range(brackets_per_pool):
                        bitstring = getNewBracketBitstring(BracketType(type), sampling_fn=sfn)
                        out_f.write("{}\n".format(bit_to_hexstring(bitstring)))
        print()
