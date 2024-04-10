from lib.bracket import Bracket, BracketType
from lib.bracket.sample import F4_A, E_8

# perfect_bitstring = "011010000000000101101010010010000111111101000001110101111001101" # 2022
perfect_bitstring = "000100011100000000000000010010100001111011110011100010110000001"

def hex_to_bitstring(hex_string):
    integer_val = int(hex_string, 16)
    return "{:064b}".format(integer_val)


def score_bitstring_directly(bitstring):
    b = [int(bit) for bit in bitstring]
    p = [int(bit) for bit in perfect_bitstring]
    current_round = 6
    current_idx = 0
    gamesCorrectList = [0] * 6

    # rnd64_bitstring = b[:32]
    # rnd64_perf_bitstring = p[:32]
    # rnd64_correct = [rnd64_bitstring[i] == rnd64_perf_bitstring[i] for i in range(32)]
    # print(sum(rnd64_correct), rnd64_correct)

    # rnd32_bitstring = b[32:48]
    # rnd32_perf_bitstring = p[32:48]
    # rnd32_correct = [(rnd32_bitstring[i] == rnd32_perf_bitstring[i]) and rnd64_correct[2 * i + rnd32_perf_bitstring[i]] for i in range(16)]
    # print(sum(rnd32_correct), rnd32_correct)

    prev_round_correct = [True for i in range(64)]
    start = 0
    end = 32
    total_score = 0
    for rnd in range(6):
        # print(rnd, start, end)
        round_bitstring = b[start:end]
        round_perf_bitstring = p[start:end]
        round_correct = [(round_bitstring[i] == round_perf_bitstring[i]) and prev_round_correct[2 * i + round_perf_bitstring[i]] for i in range(end - start)]
        gamesCorrectList[rnd] = sum(round_correct)
        total_score += 10 * 2**rnd * gamesCorrectList[rnd]
        start = end
        end += 2**(5 - rnd - 1)
        prev_round_correct = round_correct

    # print(gamesCorrectList)
    return total_score



def score_bitstring(bitstring, bracket_type):
    # Compares a bitstring for a generated bracket to a perfect bitstring
    # Returns a tuple (score, numCorrect, gamesCorrectList), where score is the bracket score
    # and numCorrect is the number of games that were correct in the bitstring.
    perfect_bracket_matches = Bracket.from_bitstring(bracket_type, perfect_bitstring).matches()
    test_matches = Bracket.from_bitstring(bracket_type, bitstring).matches()
    current_round = 6
    current_idx = 0
    # The score value of a correct game in each round
    # Doubles for each sequential round
    value = 10
    totalScore = 0
    gamesCorrectList = [0] * 6
    # change the value
    newValue = [31, 47, 55, 59, 61, 62]
    rnd = 0
    # Calculates the number of games in the round
    for perfGame, testGame in zip(perfect_bracket_matches, test_matches):
        if perfGame.winner.name == testGame.winner.name:
            gamesCorrectList[rnd] += 1
            totalScore += value
            # print(totalScore)
        if current_idx == newValue[rnd]:
            value *= 2
            rnd += 1
        if newValue[current_round - 1] == current_idx:
            break
        current_idx += 1

    return totalScore#, sum(gamesCorrectList), gamesCorrectList


if __name__ == '__main__':
    # TODO: Add command-line arguments for 
    # how many brackets per pool and 
    # how many pools. 
    brackets_per_pool = 100000
    num_pools = 10

    for type in ["men"]:
        bracket_type = BracketType.MEN
        print(type)
        
        for sfn_name in [None, "f4a", "e8"]:
            print(sfn_name)
            
            for pool_index in range(num_pools):
                filename = "bracket_pools/bracket_pool_{0}_{1}_{2:02d}.txt".format(type, sfn_name if sfn_name else "default", pool_index)
                with open(filename, 'r') as in_f:
                    for bracket_index in range(brackets_per_pool):
                        # if (bracket_index % 10000) == 0:
                        #     print("index =", bracket_index // 10000)
                        hexstring = in_f.readline()
                        bitstring = hex_to_bitstring(hexstring)[:-1]
                        score = score_bitstring_directly(bitstring)
                        if score >= 1460: # ESPN cutoff, or some other reasonable threshold
                            print("{},{}".format(score, bitstring))
        print()
