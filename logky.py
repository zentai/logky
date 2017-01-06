import pprint
import operator
import json

global state_markov
# state_markov = {'1719': 7.522190461862494e-05,
#  '1126': 7.522190461862494e-05,
#  '2111': 7.522190461862494e-05,
#  '2017': 7.522190461862494e-05,
#  '1726': 7.522190461862494e-05,
#  '1926': 0.00015044380923724988,
#  '1918': 0.00015044380923724988,
#  '2020': 0.00015044380923724988,
#  '1921': 0.00022566571385587483,
#  '2621': 0.00030088761847449976,
#  '2119': 0.00045133142771174966,
#  '1118': 0.0006769971415676245,
#  '1119': 0.0011283285692793741,
#  '1711': 0.001203550473897999,
#  '1117': 0.0012787723785166241,
#  '1911': 0.0025575447570332483,
#  '1920': 0.03354896945990672,
#  '2018': 0.03415074469685572,
#  '1819': 0.0349781856476606,
#  '2011': 0.4439596810591244,
#  '1120': 0.444636678200692}

def feature_abstract(line, delimeter):
    return line.split(delimeter)[-1]

def state_retrieval(fname, delimeter):
    state = []
    f = open(fname, "r")
    lines = f.read().splitlines()
    for line in lines:
        state.append(feature_abstract(line, delimeter))
    f.close()
    return state

def build_markov_table(fname, delimeter):
    p_state = {}
    state = state_retrieval(fname, delimeter)

    for i in range(len(state)-1):
        index = state[i]+state[i+1]
        p_state[index] = 1 if index not in p_state else p_state[index] + 1

    for key, count in p_state.items():
        p_state[key] = float(count)/len(state)
        print key, p_state[key]

    output = open(fname+".markov", "w")
    output.write(json.dumps(p_state, sort_keys=True, indent=4))
    output.close()

def load_markov_table(fname):
    global state_markov
    print "=== Load markov ==="
    json_str = open(fname, "r").read()
    state_markov = json.loads(json_str)
    pprint.pprint(state_markov)
    print "=============================="

def run_data(fname, delimeter):
    global state_markov
    print "run_data"
    state = []
    lines = open(fname, "r").read().splitlines()
    last_log = ""
    for line in lines:
        state.append(line.split(delimeter)[-1])
        if len(state) < 2:
            continue
        key = "%s%s" % (state[-2], state[-1])
        if key not in state_markov:
            # print "key not found: %s" % key
            continue
        if state_markov[key] < 0.003:
            print state_markov[key]
            print last_log
            print line
            print "==========================="
        last_log = line
    print "run_data end"

if __name__ == '__main__':
    msg = raw_input('Enter message to send : ')
    if msg == "markov":
        build_markov_table("/tmp/state.log", " ")
    elif msg == "run":
        load_markov_table("/tmp/state.log.markov")
        run_data("/tmp/state.log", " ")

