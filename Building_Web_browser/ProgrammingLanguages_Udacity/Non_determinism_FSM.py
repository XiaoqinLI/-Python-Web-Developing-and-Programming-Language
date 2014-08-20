# Title: Simulating Non-Determinism machines directly
# In a given state, a non-deterministic machine may have *multiple*
# outgoing edges labeled with the *same* character. 
#
# To handle this ambiguity, we say that a non-deterministic finite state
# machine accepts a string if there exists *any* path through the finite
# state machine that consumes exactly that string as input and ends in an
# accepting state.

edges = { (1, 'a') : [2, 3],
          (2, 'a') : [2],
          (3, 'b') : [4, 3],
          (4, 'c') : [5] }
accepting = [2, 5] 
# It accepts both "aaa" (visiting states 1 2 2 and finally 2) and "abbc"
# (visting states 1 3 3 4 and finally 5). 

def nfsmsim(string, current, edges, accepting): 
# fill in your code here 
    if string == "":
        if type(current) is list:
            for entry in current:
                if entry in accepting:
                    return True
        else:
            if current in accepting:
                return True
        return False
    else:
        letter = string[0]
        if type(current) is not list:
            current = [current]
        for entry in current:
            if (entry, letter) in edges:
                destination = edges[(entry, letter)]
                remaining_string = string[1:]
                return nfsmsim(remaining_string, destination, edges, accepting)       
    return False

print ("Test case 1 passed: " + str(nfsmsim("abc", 1, edges, accepting) == True))
print ("Test case 2 passed: " + str(nfsmsim("aaa", 1, edges, accepting) == True)) 
print ("Test case 3 passed: " + str(nfsmsim("abbbc", 1, edges, accepting) == True)) 
print ("Test case 4 passed: " + str(nfsmsim("aabc", 1, edges, accepting) == False)) 
print ("Test case 5 passed: " + str(nfsmsim("", 1, edges, accepting) == False))

#-------------------------------------------
# Title: Reading Machine Minds
# determine if a finite state machine is
# empty or not. If it is not empty, proving that by returning a
# string that it accepts
edges = { (1, 'a') : [2, 3],
          (2, 'a') : [2],
          (3, 'b') : [4, 2],
          (4, 'c') : [5] }
accepting = [5] 
# ... accepts exactly one string: "abc". By contrast, this
# non-deterministic machine: 
edges2 = { (1, 'a') : [1],
           (2, 'a') : [2] }
accepting2 = [2]
def nfsmaccepts(current, edges, accepting, visited):
    if current in visited:
        return None
    elif current in accepting:
        return ""
    else:
        newvisited = visited + [current]
        for edge in edges:
            if edge[0] == current:
                for newstate in edges[edge]:
                    foo = nfsmaccepts(newstate,edges,accepting,newvisited)
                    if foo != None:
                        return edge[1]+foo
        return None

print ("Test 1: " + str(nfsmaccepts(1, edges, accepting, []) == "abc"))
print ("Test 2: " + str(nfsmaccepts(1, edges, [4], []) == "ab"))
print ("Test 3: " + str(nfsmaccepts(1, edges2, accepting2, []) == None))
print ("Test 4: " + str(nfsmaccepts(1, edges2, [1], []) == ""))
#-------------------------------------------------
# Title: FSM Optimization
# Lexical analyzers are implemented using finite state machines generated
# from the regular expressions of token definition rules. The performance
# of a lexical analyzer can depend on the size of the resulting finite
# state machine. If the finite state machine will be used over and over
# again (e.g., to analyze every token on every web page you visit!), It will
# be much better if it is ss small as possible (e.g., so that your webpages
# load quickly).
# (((One way to improve the performance of a finite state machine is to make
# it smaller by removing unreachable states. If such states are removed,
# the resulting FSM takes up less memory, which may make it load faster or
# fit better in a storage-constrained mobile device))). 

def nfsmtrim(edges, accepting):
    # Gather up all of the states, possibly with duplicates 
    states = []
    for e in edges:
        states = states + [e[0]] + edges[e]
    
    # a state is live if there is some way to accept starting from it
    live = []
    for s in states:
        if nfsmaccepts(s,edges,accepting,[]) != None:
            live = live + [s]
    # now that we know what is live, build up the output
    new_edges = {}
    for e in edges:
        if e[0] in live:
            new_destinations = []
            for destination in edges[e]:
                if destination in live:
                    new_destinations = new_destinations + [destination]
            if new_destinations != []:
                new_edges[e] = new_destinations
    new_accepting = []
    for s in accepting:
        if s in live:
            new_accepting = new_accepting +[s]
    return (new_edges,new_accepting)
    # this is about four lines long with list comprehensions      

edges1 = { (1,'a') : [1] ,
           (1,'b') : [2] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (8,'z') : [9] , } 
accepting1 = [ 1 ] 
(new_edges1, new_accepting1) = nfsmtrim(edges1,accepting1) 
print (new_edges1)
print (new_edges1 == {(1, 'a'): [1]})
print (new_accepting1 == [1])

(new_edges2, new_accepting2) = nfsmtrim(edges1,[]) 
print (new_edges2 == {})
print (new_accepting2 == [])

(new_edges3, new_accepting3) = nfsmtrim(edges1,[3,6]) 
print (new_edges3 == {(1, 'a'): [1], (1, 'b'): [2], (2, 'b'): [3]})
print (new_accepting3 == [3])

edges4 = { (1,'a') : [1] ,
           (1,'b') : [2,5] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (3,'c') : [2,1,4] } 
accepting4 = [ 2 ] 
(new_edges4, new_accepting4) = nfsmtrim(edges4, accepting4) 
print (new_edges4 == { 
  (1, 'a'): [1],
  (1, 'b'): [2], 
  (2, 'b'): [3], 
  (3, 'c'): [2, 1], 
})
print (new_accepting4 == [2])
