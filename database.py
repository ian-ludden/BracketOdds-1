#!/usr/bin/env python
from lib.bracket import Bracket, BracketType
from lib.bracket.sample import Sample

def getNewBracketBitstring(bracket_type: Bracket=BracketType.MEN,
        sampling_fn: Sample=None) -> dict:
    
    b = Bracket(bracket_type, sampling_fn)
    b.run()
    return b.bits()
