## Programming Language Python
## List_Comprehention_map analyzer
## Author: Xiaoqin LI
## Created Date: 03/23/2014

grammar = [ 
    ("exp", ["exp", "+", "exp"]),
    ("exp", ["exp", "-", "exp"]),
    ("exp", ["(", "exp", ")"]),
    ("exp", ["num"]),
    ]

def expand(tokens, grammar):
    for pos in range(len(tokens)):
        for rule in grammar:
            if (tokens[pos] == rule[0]):
                yield tokens[0:pos] + rule[1] + tokens[pos+1:]
                       
depth = 1
utterances = [["a","exp"]]
for x in range(depth):
    for sentence in utterances:
        utterances = utterances + [ i for i in expand(sentence, grammar)]

for sentence in utterances:
    print (sentence)
