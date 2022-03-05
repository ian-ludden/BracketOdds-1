#!/usr/bin/env python
import json
import requests

"""
Fetch a bracket JSON from BracketOdds site. 

Parameters:
===============
    type - "men" or "women"
    sfn - "f4a" for sampling Final Four seeds first, 
          "e8" for sampling Elite Eight seeds first, or
          None for the default power model

Returns:
===============
    the generated bracket as a length-63 string of 0s and 1s
"""
def fetch_bracket(type="men", sfn=None):
    bracketodds_url = "https://bracketodds.cs.illinois.edu/api/v1/bracket?type=" + type
    if sfn:
        bracketodds_url += "&sfn=" + sfn

    bracketodds_response = requests.get(bracketodds_url)
    data = json.loads(bracketodds_response.text)
    # print(data)
    return data['bitstring']


if __name__ == '__main__':
    # TODO: Add command-line arguments for 
    # how many brackets per pool and 
    # how many pools to fetch. 
    brackets_per_pool = 100000
    num_pools = 10

    for type in ["men"]:
        for sfn in [None, "f4a", "e8"]:
            for pool_index in range(num_pools):
                filename = "bracket_pools/prefix0_bracket_pool_{0:02d}.txt".format(pool_index)
                with open(filename, 'w') as out_f:
                    for bracket_index in range(brackets_per_pool):
                        bitstring = fetch_bracket(type=type, sfn=sfn)
                        prefix0_bitstring = "0" + bitstring
                        integer_val = int(prefix0_bitstring, 2)
                        out_f.write("{:016X}\n".format(integer_val))

                    