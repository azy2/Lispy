from parser import lispy_parser
from scope import scope
from shared import get_syn

import pprint

pp = pprint.PrettyPrinter(indent=2, width=60)



def plusBuiltin(current_scope, args):
    vals = [eval_literal(current_scope, v) for v in args]
    if 'FLOAT' in [v['type'] for v in args]:
        return get_syn('FLOAT', sum(vals))
    else:
        return get_syn('INT', sum(vals))

def difference(vals):
    d = vals[0]
    for v in vals[1:]:
        d -= v
    return d


def minusBuiltin(current_scope, args):
    vals = [eval_literal(current_scope, v) for v in args]
    if 'FLOAT' in [v['type'] for v in args]:
        return get_syn('FLOAT', difference(vals))
    else:
        return get_syn('INT', difference(vals))

def product(vals):
    p = 1
    for v in vals:
        p *= v
    return p


def timesBuiltin(current_scope, args):
    vals = [eval_literal(current_scope, v) for v in args]
    if 'FLOAT' in [v['type'] for v in args]:
        return get_syn('FLOAT', product(vals))
    else:
        return get_syn('INT', product(vals))

def quotientF(vals):
    q = vals[0]
    for v in vals[1:]:
        q /= v
    return q

def quotientI(vals):
    q = vals[0]
    for v in vals[1:]:
        q = q // v
    return q


def divideBuiltin(current_scope, args):
    vals = [eval_literal(current_scope, v) for v in args]
    if 'FLOAT' in [v['type'] for v in args]:
        return get_syn('FLOAT', quotientF(vals))
    else:
        return get_syn('INT', quotientI(vals))


def modBuiltin(current_scope, args):
	if len(args) != 2:
		#TODO ERROR HANDLING
		return None
	return get_syn('INT', eval_literal(current_scope, args[0]) % eval_literal(current_scope, args[1]))


def notBuiltin(current_scope, args):
	if len(args) != 1:
		#TODO ERROR HANDLING
		pass
	return get_syn('BOOL', not eval_literal(current_scope, args[0]))


def ltBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        return None
    return get_syn('BOOL', eval_literal(current_scope, args[0]) < eval_literal(current_scope, args[1]))


def lteBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        return None
    return get_syn('BOOL', eval_literal(current_scope, args[0]) <= eval_literal(current_scope, args[1]))


def gtBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        return None
    return get_syn('BOOL', eval_literal(current_scope, args[0]) > eval_literal(current_scope, args[1]))


def gteBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        return None
    return get_syn('BOOL', eval_literal(current_scope, args[0]) >= eval_literal(current_scope, args[1]))


def equalsBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        return None
    return get_syn('BOOL', eval_literal(current_scope, args[0]) == eval_literal(current_scope, args[1]))


def notEqualBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        return None
    return get_syn('BOOL', eval_literal(current_scope, args[0]) != eval_literal(current_scope, args[1]))


def andBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        #TODO NEED TO ONLY COMPARE BOOLS
        return None
    return get_syn('BOOL', eval_literal(current_scope, args[0]) and eval_literal(current_scope, args[1]))


def orBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        #TODO NEED TO ONLY COMPARE BOOLS
        return None
    return get_syn('BOOL', eval_literal(current_scope, args[0]) or eval_literal(current_scope, args[1]))

def carBuiltin(current_scope, args):
    if len(args) > 1:
        #TODO ERROR HANDLING
        return None
    return args[0]['value'][0]

def cdrBuiltin(current_scope, args):
    if len(args) > 1:
        #TODO ERROR HANDLING
        return None
    return get_syn('LIST', [x for x in args[0]['value'][1:]])

def consBuiltin(current_scope, args):
    if len(args) != 2:
        #TODO ERROR HANDLING
        return None
    l = [x for x in args[1]['value']]
    l.insert(0, args[0])
    return get_syn('LIST', l)


import copy

class User_func:
    def __init__(self, args, body):
        self._args = args
        self._body = body

    def __call__(self, current_scope, args):
        new_scope = copy.deepcopy(current_scope)
        for a,b in zip(self._args, args):
            #new_scope.add(a, b)
            new_scope[a] = b
        for e in self._body[:-1]:
            eval(new_scope, e)
        return eval(new_scope, self._body[-1])

def print_lispy(scope, lispy):
    if lispy['type'] not in ['INT', 'FLOAT', 'BOOL', 'STRING', 'LIST']:
        e = eval(scope, lispy)
        print_lispy(scope, e)
    if lispy['type'] in ['INT', 'FLOAT']:
        print(eval_literal(scope, lispy))
    if lispy['type'] == 'BOOL':
        b = eval_literal(scope, lispy)
        if b:
            print('#t')
        else:
            print('#f')
    if lispy['type'] == 'STRING':
        s = eval_literal(scope, lispy)
        print('"' + s + '"')
    if lispy['type'] == 'LIST':
        print("'(", end='')
        lis = eval_literal(scope, lispy)
        for l in lis[:-1]:
            print(eval_literal(scope, l), end=' ')
        print(str(eval_literal(scope, lis[-1])) + ')')


def eval_literal(current_scope, ast):
    if ast['type'] in ['INT', 'FLOAT', 'STRING', 'BOOL', 'LIST']:
        return ast['value']
    else:
        return None



def eval(current_scope, ast):
    ast = copy.deepcopy(ast)
    if ast['type'] in ['INT', 'FLOAT', 'STRING', 'BOOL', 'LIST']:
        return ast

    if ast['type'] == 'ID':
        #return current_scope.get(ast['value'])
        return current_scope[ast['value']]

    if ast['type'] == 'LET':
        name = ast['value']['name']['value']
        value = ast['value']['value']
        if value['type'] in ['FUNC_CALL', 'ID']:
            value = eval(current_scope, value)
        #current_scope.add(name, value)
        current_scope[name] = value
        return value

    if ast['type'] == 'DEFUN':
        function_name = ast['value']['name']['value']
        args = ast['value']['args'] # TODO if any of these aren't IDs crash
        args = [a['value'] for a in args]
        body = ast['value']['body']['value']
        #current_scope.add(function_name, User_func(args, body))
        current_scope[function_name] = User_func(args, body)

    if ast['type'] == 'IF':
        arg = ast['value']['cond']
        if arg['type'] in ['FUNC_CALL', 'ID']:
            arg = eval(current_scope, arg)
        cond = eval(current_scope, arg)
        if cond:
            ret = ast['value']['then']
            if ret['type'] in ['FUNC_CALL', 'ID', 'DEFUN', 'LET', 'IF']:
                ret = eval(current_scope, ret)
            return ret
        else:
            ret = ast['value']['else']
            if ret['type'] in ['FUNC_CALL', 'ID', 'DEFUN', 'LET', 'IF']:
                ret = eval(current_scope, ret)
            return ret

    if ast['type'] == 'PRINT':
        for val in ast['value']['value']:
            print_lispy(current_scope, val)

    if ast['type'] == 'FUNC_CALL':
        args = ast['value']['arg_exprs']['value']
        for (i, a) in enumerate(args):
            if a['type'] in ['FUNC_CALL', 'ID']:
                args[i] = eval(current_scope, args[i])
        #return current_scope.get(ast['value']['name']['value'])(current_scope, args)
        return current_scope[ast['value']['name']['value']](current_scope, args)


global_scope = {
    '+': plusBuiltin,
    '-': minusBuiltin,
    '*': timesBuiltin,
    '/': divideBuiltin,
    '%': modBuiltin,
    '<': ltBuiltin,
    '<=': lteBuiltin,
    '>': gtBuiltin,
    '>=': gteBuiltin,
    '=': equalsBuiltin,
    '!=': notEqualBuiltin,
    'and': andBuiltin,
    'or': orBuiltin,
    'not': notBuiltin,
    'car': carBuiltin,
    'cdr': cdrBuiltin,
    'cons': consBuiltin
}

if __name__ == '__main__':
    lispy = lispy_parser()
    while(True):
        ast = lispy.parse(input())
        pp.pprint(eval(global_scope, ast))
