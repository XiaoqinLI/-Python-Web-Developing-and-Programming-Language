__author__ = 'daybreaklee'

def addtochart(chart, index, state):
    # Insert code here!
    if not state in chart[index]:
        chart[index] = [state] + chart[index]
        return True
    else:
        return False

# Writing Closure
# We are currently looking at chart[i] and we see x => ab . cd from j
# Write the Python procedure, closure, that takes five parameters:
#   grammar: the grammar using the previously described structure
#   i: a number representing the chart state that we are currently looking at
#   x: a single nonterminal
#   ab and cd: lists of many things

# The closure function should return all the new parsing states that we want to
# add to chart position i
# Hint: This is tricky. If you are stuck, do a list comphrension over the grammar rules.

# def closure (grammar, i, x, ab, cd):
#     return [[] if cd == [] else(rule[0],[],rule[1],i) for rule in grammar if rule[0] == cd[0]]
def closure (grammar, i, x, ab, cd):
    next_states = [ (rule[0],[],rule[1],i)\
        for rule in grammar if cd != [] and cd[0] == rule[0] ]
    return next_states


# Writing Shift
# We are currently looking at chart[i] and we see x => ab . cd from j. The input is tokens.
# Your procedure, shift, should either return None, at which point there is
# nothing to do or will return a single new parsing state that presumably
# involved shifting over the c if c matches the ith token.

def shift (tokens, i, x, ab, cd, j):
    if len(tokens) <= i or cd == []:
        return None
    else:
        if cd[0] == tokens[i]:
            return (x, ab+[cd[0]], cd[1:], j)
        else:
            return None

# Writing Reductions
# We are looking at chart[i] and we see x => ab . cd from j.
# Hint: Reductions are tricky, so as a hint, remember that you only want to do
# reductions if cd == []
# Hint: You'll have to look back previously in the chart.

# def reductions(chart, i, x, ab, cd, j):
#     # Insert code here!
#     if len(cd) != 0:
#         return None
#     else:
#         for rule1 in chart[j]:
#             if rule1[2] == ab:
#                 return [(rule[0], rule[1] + [x], rule[2][1:], rule[3])
#                         for rule in chart[j] if rule[2][0] == x]
#         #return None

def reductions(chart,i,x,ab,cd,j):
    return [ (jstate[0], jstate[1] + [x], (jstate[2])[1:], jstate[3] )
             for jstate in chart[j]
             if cd == [] and jstate[2] != [] and (jstate[2])[0] == x]



chart = {0: [('exp', ['exp'], ['+', 'exp'], 0),
             ('exp', [], ['num'], 0),
             ('exp', [], ['(', 'exp', ')'], 0),
             ('exp', [], ['exp', '-', 'exp'], 0),
             ('exp', [], ['exp', '+', 'exp'], 0)],
         1: [('exp', ['exp', '+'], ['exp'], 0)],
         2: [('exp', ['exp', '+', 'exp'], [], 0)]}

print reductions(chart,2,'exp',['exp','+','exp'],[],0)
print reductions(chart,2,'exp',['exp','+','exp'],[],0) == [('exp', ['exp'], ['-', 'exp'], 0),
                                                               ('exp', ['exp'], ['+', 'exp'], 0)]

grammar = [
    ("exp", ["exp", "+", "exp"]),
    ("exp", ["exp", "-", "exp"]),
    ("exp", ["(", "exp", ")"]),
    ("exp", ["num"]),
    ("t",["I","like","t"]),
    ("t",[""])
    ]

print closure(grammar,0,"exp",["exp","+"],["exp"]) == [('exp', [], ['exp', '+', 'exp'], 0), ('exp', [], ['exp', '-', 'exp'], 0), ('exp', [], ['(', 'exp', ')'], 0), ('exp', [], ['num'], 0)]
print closure(grammar,0,"exp",[],["exp","+","exp"]) == [('exp', [], ['exp', '+', 'exp'], 0), ('exp', [], ['exp', '-', 'exp'], 0), ('exp', [], ['(', 'exp', ')'], 0), ('exp', [], ['num'], 0)]
print closure(grammar,0,"exp",["exp"],["+","exp"]) == []

print shift(["exp","+","exp"],2,"exp",["exp","+"],["exp"],0) == ('exp', ['exp', '+', 'exp'], [], 0)
print shift(["exp","+","exp"],0,"exp",[],["exp","+","exp"],0) == ('exp', ['exp'], ['+', 'exp'], 0)
print shift(["exp","+","exp"],3,"exp",["exp","+","exp"],[],0) == None
print shift(["exp","+","ANDY LOVES COOKIES"],2,"exp",["exp","+"],["exp"],0) == None


grammar1 = [
    ("S", ["P" ]),
    ("P", ["(" , "P", ")" ]),
    ("P", []) ,
]
tokens = ["(", "(", ")", ")" ]

def parse(tokens, grammar):
    tokens = tokens + ["end_of_input_marker"]
    chart = {}
    start_rule = grammar[0]
    for i in range(len(tokens)+1):
        chart[i] = []
    start_state = (start_rule[0], [], start_rule[1], 0)
    chart[0] = [ start_state ]
    for i in range(len(tokens)):
        while True:
            changes = False
            for state in chart[i]:
                x = state[0]
                ab = state[1]
                cd = state[2]
                j = state[3]

                #if closure
                next_states = closure(grammar,i,x,ab,cd)
                for next_state in next_states:
                    changes = addtochart(chart,i,next_state) or changes

                #if shifting
                next_state = shift(tokens,i,x,ab,cd,j)
                if next_state != None:
                    changes = addtochart(changes,i+1,next_state) or changes

                #if reductions
                next_states = reductions(chart,i,x,ab,cd,j)
                for next_state in next_states:
                    changes = addtochart(chart,i,next_state) or changes

            # we are done if nothing changed!
            if not changes:
                break
    for i in range(len(tokens)):
        print "== chart " + str(i)
        for state in chart[i]:
            x = state[0]
            ab = state[1]
            cd = state[2]
            j = state[3]
            print "   " + x + " ->",
            for sym in ab:
                print " " + sym,
            print " ."
            for sym in cd:
                print " " + sym,
            print "  from " + str(j)

    accepting_state = (start_rule[0], start_rule[1], [], 0)
    return accepting_state in chart[len(tokens)-1]

result = parse(tokens,grammar1)