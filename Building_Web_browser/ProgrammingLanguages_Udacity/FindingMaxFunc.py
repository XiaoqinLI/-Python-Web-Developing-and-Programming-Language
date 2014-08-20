__author__ = 'daybreaklee'
# practice of Lambda function.
# maximizes the return value of f.

def findmax(f,l):
    best_element_sofar = None
    best_f_value_sofar = None
    for i in range(len(l)):
        elt = l[i]
        f_value = f(elt)
        print "elt = ", elt, "f_value = ", f_value
        if best_f_value_sofar == None or \
        f_value > best_f_value_sofar:
            best_element_sofar = elt
            best_f_value_sofar = f_value
    return best_element_sofar

l = ["Barbara", "Kingsolver", "Wrote", "The", "Poisonwood", "Bible"]

print(findmax(lambda(word): word.find("l"), l))
