__author__ = 'xiaoqin.li'
# Reading Machine Minds 2
#
# We say that a finite state machine is "empty" if it accepts no strings.
# Similarly, we say that a context-free grammar is "empty" if it accepts no
# strings. In this problem, you will write a Python procedure to determine
# if a context-free grammar is empty.
#
# A context-free grammar is "empty" starting from a non-terminal symbol S
# if there is no _finite_ sequence of rewrites starting from S that
# yield a sequence of terminals.
#
# For example, the following grammar is empty:
#
# grammar1 = [
#       ("S", [ "P", "a" ] ),           # S -> P a
#       ("P", [ "S" ]) ,                # P -> S
#       ]
#
# Because although you can write S -> P a -> S a -> P a a -> ... that
# process never stops: there are no finite strings in the language of that
# grammar.
#
# By contrast, this grammar is not empty:
#
# grammar2 = [
#       ("S", ["P", "a" ]),             # S -> P a
#       ("S", ["Q", "b" ]),             # S -> Q b
#       ("P", ["P"]),                   # P -> P
#       ("Q", ["c", "d"]),              # Q -> c d
#
# And ["c","d","b"] is a witness that demonstrates that it accepts a
# string.
#
# Write a procedure cfgempty(grammar,symbol,visited) that takes as input a
# grammar (encoded in Python) and a start symbol (a string). If the grammar
# is empty, it must return None (not the string "None", the value None). If
# the grammar is not empty, it must return a list of terminals
# corresponding to a string in the language of the grammar. (There may be
# many such strings: you can return any one you like.)
#
# To avoid infinite loops, you should use the argument 'visited' (a list)
# to keep track of non-terminals you have already explored.
#
# Hint 1: Conceptually, in grammar2 above, starting at S is not-empty with
# witness [X,"a"] if P is non-empty with witness X and is non-empty with
# witness [Y,"b"] if Q is non-empty with witness Y.
#
# Hint 2: Recursion! A reasonable base case is that if your current
# symbol is a terminal (i.e., has no rewrite rules in the grammar), then
# it is non-empty with itself as a witness.
#
# Hint 3: all([True,False,True]) = False
#         any([True,True,False]) = True

#--------------recursive solution-------------------
def cfgempty(grammar,symbol,visited):
    if symbol in visited:
        return None
    elif not any([ rule[0] == symbol for rule in grammar]): # checking if this symbol is a terminal
        return[symbol]

    else:
        new_visited = visited + [symbol] # update visited
        #consider every rewrite rule "Symbol" => RHS(right hand side)
        for rhs in [rule[1] for rule in grammar if rule[0] == symbol]:
            #check if every part of RHS is non-empty
            if all([None != cfgempty(grammar, ele, new_visited) for ele in rhs]):
                result = [] #gather up results
                for r in rhs:
                    result =  result + cfgempty(grammar, r, new_visited)
                return result
    return None

#---------------non recursive solution: brutal force-----------------
# def expand(tokens, grammar):
#     for pos in range(len(tokens)):
#         for rule in grammar:
#             if tokens[pos] == rule[0]:
#                 yield tokens[0:pos] + rule[1] + tokens[pos + 1:]
#
# def make_grammar(depth, utterances, grammar):
#     for x in range(depth):
#         for sentence in utterances:
#             utterances = utterances + [ i for i in expand(sentence, grammar)]
#
#     return utterances
#
# def cfgempty(grammar, symbol, visited):
#
#     production = make_grammar(len(grammar), [[symbol]], grammar)
#
#     cases = []
#     for rule in grammar:
#         cases.append(rule[0])
#     for issue in production:
#         flag = False
#         for case in cases:
#             if case in issue:
#                 flag = True
#                 break
#         if not flag:
#             return issue
#     return None

# We have provided a few test cases for you. You will likely want to add
# more of your own.

grammar1 = [
      ("S", [ "P", "a" ] ),
      ("P", [ "S" ]) ,
      ]

print cfgempty(grammar1,"S",[]) == None

grammar2 = [
      ("S", ["P", "a" ]),
      ("S", ["Q", "b" ]),
      ("P", ["P"]),
      ("Q", ["c", "d"]),
      ]

print cfgempty(grammar2,"S",[]) == ['c', 'd', 'b']

grammar3 = [  # some Spanish provinces
        ("S", [ "Barcelona", "P", "Huelva"]),
        ("S", [ "Q" ]),
        ("Q", [ "S" ]),
        ("P", [ "Las Palmas", "R", "Madrid"]),
        ("P", [ "T" ]),
        ("T", [ "T", "Toledo" ]),
        ("R", [ ]) ,
        ("R", [ "R"]),
        ]

print cfgempty(grammar3,"S",[]) == ['Barcelona', 'Las Palmas', 'Madrid', 'Huelva']
