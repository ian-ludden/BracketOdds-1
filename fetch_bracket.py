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
def fetch_brackets(type="men", sfn=None, count=1):
    bracketodds_url = "https://bracketodds.cs.illinois.edu/api/v1/bracket/multiplebrackets?type=" + type
    bracketodds_url += "&count=" + str(count)
    if sfn:
        bracketodds_url += "&sfn=" + sfn

    bracketodds_response = requests.get(bracketodds_url)
    data = json.loads(bracketodds_response.text)
    return data['bitstrings']


if __name__ == '__main__':
    # TODO: Add command-line arguments for 
    # how many brackets per pool and 
    # how many pools to fetch. 
    brackets_per_request = 200
    requests_per_pool = 500
    num_pools = 10

    for type in ["men"]:
        print(type)
        for sfn in [None, "f4a", "e8"]:
            print(sfn)
            for pool_index in range(num_pools):
                filename = "bracket_pools/bracket_pool_{0}_{1}_{2:02d}.txt".format(type, sfn if sfn else "default", pool_index)
                with open(filename, 'w') as out_f:
                    for request_index in range(requests_per_pool):
                        bitstrings = fetch_brackets(type=type, sfn=sfn, count=brackets_per_request)
                        for bitstring in bitstrings:
                            integer_val = int(bitstring, 2)
                            out_f.write("{:016X}\n".format(integer_val))
        print()
                    