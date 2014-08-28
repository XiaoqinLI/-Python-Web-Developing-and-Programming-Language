__author__ = 'daybreaklee'
# QUIZ : Frames
# Return will throw an excception
# Function Calls: new environments, catch return values

def eval_stmt(tree,environment):
    stmttype = tree[0]
    if stmttype == "assign":
        # ("assign", "x", ("binop", ..., "+",  ...)) <=== x = ... + ...
        variable_name = tree[1]
        right_child = tree[2]
        new_value = eval_exp(right_child, environment)
        env_update(environment, variable_name, new_value)
    elif stmttype == "if-then-else": # if x < 5 then A;B; else C;D;
        conditional_exp = tree[1] # x < 5
        then_stmts = tree[2] # A;B;
        else_stmts = tree[3] # C;D;
        if eval_exp(conditional_exp, environment):
            eval_stmts(then_stmts, environment)
        else:
            eval_stmts(else_stmts, environment)
        # QUIZ: Complete this code
        # Assume "eval_stmts(stmts, environment)" exists
    elif stmttype == "call": # ("call", "sqrt", [("number","2")])
        fname = tree[1] # "sqrt"
        args = tree[2] # [ ("number", "2") ]
        fvalue = env_lookup(fname, environment)
        if fvalue[0] == "function":
            # We'll make a promise to ourselves:
            # ("function", params, body, env)
            fparams = fvalue[1] # ["x"]
            fbody = fvalue[2]
            fenv = fvalue[3]
            if len(fparams) <> len(args):
                print "ERROR: wrong number of args"
            else:
                #QUIZ: Make a new environment frame
                #QUIZ(evaluate actual args, ...)
                newenv = ( fenv, {} ) # new environment
                for i in range(len(args)):
                    argval = eval_exp(args[i], environment)
                    (newenv[1])[fparams[i]] = argval
                try:
                    eval_stmts(fbody, newenv)
                    # QUIZ : Evaluate the body
                    return None
                except Exception as return_value:
                    return return_value
        else:
            print  "ERROR: call to non-function"
    elif stmttype == "return":
        retval = eval_exp(tree[1],environment)
        raise Exception(retval)
    elif stmttype == "exp":
        eval_exp(tree[1],environment)

def env_lookup(vname,env):
        if vname in env[1]:
                return (env[1])[vname]
        elif env[0] == None:
                return None
        else:
                return env_lookup(vname,env[0])

def env_update(vname,value,env):
        if vname in env[1]:
                (env[1])[vname] = value
        elif not (env[0] == None):
                env_update(vname,value,env[0])


def eval_exp(exp,env):
        etype = exp[0]
        if etype == "number":
            return float(exp[1])
        elif etype == "binop":
            a = eval_exp(exp[1],env)
            op = exp[2]
            b = eval_exp(exp[3],env)
            if op == "*":
                return a*b
            elif op == "+":
                return a + b
            elif op == "-":
                return a - b
        elif etype == "string":
                return exp[1]
        elif etype == "true":
                return True
        elif etype == "false":
                return False
        elif etype == "not":
                return not(eval_exp(exp[1], env))

        elif etype == "identifier":
            vname = exp[1]
            value = env_lookup(vname,env)
            if value == None:
                print "ERROR: unbound variable " + vname
            else:
                return value

def eval_stmts(stmts,env):
        for stmt in stmts:
            eval_stmt(stmt,env)

def eval_while(while_stmt, env):
        # Fill in your own code here. Can be done in as few as 4 lines.
        whileCondition = while_stmt[1]
        whileBody = while_stmt[2]
        if eval_exp(whileCondition,env):
            eval_stmts(whileBody,env)
            eval_while(while_stmt, env)

sqrt = ("function",("x"),(("return",("binop",("identifier","x"),"*",("identifier","x"))),),{})

environment = (None,{"sqrt":sqrt})

print eval_stmt(("call","sqrt",[("number","2")]),environment)

