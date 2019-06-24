
import operator
import re

from collections import namedtuple, OrderedDict, deque

from pycalc.ext_mod import find_attr, import_modules


# Constant ordered dictionary with tokens: regexp, operator and precedence
_tkn = namedtuple('_tkn', 're, operator, precedence')
_TOKENS = OrderedDict([
    ('FLOAT', _tkn(re.compile(r'\d*\.\d+'), float, 9)),
    ('COMPLEX', _tkn(re.compile(r'\d+[jJ](?![\w\d])'), complex, 9)),
    ('INTEGER', _tkn(re.compile(r'\d+'), int, 9)),
    ('LPARENT', _tkn(re.compile(r'\('), str, 0)),
    ('RPARENT', _tkn(re.compile(r'\)'), str, 0)),
    ('PLUS', _tkn(re.compile(r'\+'), operator.add, 4)),
    ('MINUS', _tkn(re.compile(r'-'), operator.sub, 4)),
    ('POWER', _tkn(re.compile(r'(\^)|(\*\*)'), operator.pow, 7)),
    ('TIMES', _tkn(re.compile(r'\*'), operator.mul, 5)),
    ('FDIVIDE', _tkn(re.compile(r'//'), operator.floordiv, 5)),
    ('DIVIDE', _tkn(re.compile(r'/'), operator.truediv, 5)),
    ('COMMA', _tkn(re.compile(r','), str, 8)),
    ('MODULO', _tkn(re.compile(r'%'), operator.mod, 5)),
    ('EQUALS', _tkn(re.compile(r'=='), operator.eq, 2)),
    ('LE', _tkn(re.compile(r'<='), operator.le, 3)),
    ('LT', _tkn(re.compile(r'<'), operator.lt, 3)),
    ('GE', _tkn(re.compile(r'>='), operator.ge, 3)),
    ('GT', _tkn(re.compile(r'>'), operator.gt, 3)),
    ('NE', _tkn(re.compile(r'!='), operator.ne, 2)),
    ('SPACE', _tkn(re.compile(r'\s+'), None, None)),
    ('FUNC', _tkn(re.compile(r'[\w]+\('), find_attr, 1)),
    ('CONST', _tkn(re.compile(r'[\w]+'), find_attr, 9)),
    ('ARGS', _tkn(None, bool, 1)),
    ('UMINUS', _tkn(None, lambda x: x * -1, 6)),
    ('UPLUS', _tkn(None, lambda x: x, 6)),
])


class _Token(namedtuple('token', 'index, type, value')):
    """
    Named tuple for queue in reverse polish notation algorithm
    with calculating properties from _TOKENS dictionary
    """
    @property
    def precedence(self):
        return _TOKENS[self.type].precedence

    @property
    def operator(self):
        return _TOKENS[self.type].operator


def _tokenize_expr(expr):
    """
    Walk through regexps in _TOKENS dict and cut expression in tokens
    :param expr:
    :type expr:str
    :return: list of _Token namedtuples(index, type, value)
    """
    token_expr = deque()
    while expr:
        for (_type, (_re, _, _)) in _TOKENS.items():
            if _re is not None:
                t_match = _re.match(expr)
                if t_match:
                    if _type != 'SPACE':
                        token_expr.append((_type, t_match.group()))
                    expr = expr[t_match.end():]
                    break
        else:
            raise ArithmeticError("EXPRESSION Tokenize Error")
    return [_Token(i, t, v) for i, (t, v) in enumerate(token_expr)]


def _unary_replace(token_expr):

    for token in token_expr:
        not_unary_after = {'FLOAT', 'INTEGER', 'CONST', 'COMPLEX', 'RPARENT'}
        if (token.type in {'MINUS', 'PLUS'} and
                (token.index == 0 or
                 token_expr[token.index - 1].type not in not_unary_after)):
            # Place U before token.type
            token_expr[token.index] = _Token(token.index, 'U' + token.type,
                                             token.value)


def _postfix_queue(token_expr):

    stack = deque()
    queue = deque()
    have_args = deque()
    for token in token_expr:
        if token.type in {'FLOAT', 'INTEGER', 'CONST', 'COMPLEX'}:
            queue.append(token)
        elif token.type == 'FUNC':
            stack.append(token)
            # If function have no arguments we append False before FUNC
            if token_expr[token.index + 1].type == 'RPARENT':
                have_args.append(False)
            else:
                have_args.append(True)
        elif not stack:
            stack.append(token)
        elif token.type == 'COMMA':
            while stack[-1].type != 'FUNC':
                queue.append(stack.pop())
            queue.append(token)
        elif token.type == 'LPARENT':
            stack.append(token)
        elif token.type == 'RPARENT':
            while stack[-1].type not in {'LPARENT', 'FUNC'}:
                queue.append(stack.pop())
                if not stack:
                    raise ArithmeticError("Parentheses error")
            if stack[-1].type == 'FUNC':
                queue.append(_Token('', 'ARGS', have_args.pop()))
                queue.append(stack.pop())
            else:
                stack.pop()
        elif token.type in {'UMINUS', 'UPLUS'} and stack[-1].type == 'POWER':

            stack.append(token)
        elif token.precedence == stack[-1].precedence and \
                token.type in {'POWER', 'UMINUS', 'UPLUS'}:
            # Right-to-Left association operations
            stack.append(token)
        elif token.precedence <= stack[-1].precedence:
            while stack:
                if token.precedence <= stack[-1].precedence:
                    queue.append(stack.pop())
                    continue
                else:
                    break
            stack.append(token)
        else:
            stack.append(token)
    while stack:
        queue.append(stack.pop())
    return queue


def _pkg_calc(queue):

    pkg_stack = deque()
    if queue:
        for element in queue:
            if element.type in ('FLOAT', 'INTEGER', 'COMPLEX',
                                'CONST', 'COMMA', 'ARGS'):
                pkg_stack.append(element.operator(element.value))
            elif element.type == 'FUNC':
                fargs = deque()
                if pkg_stack.pop() is True:
                    fargs.append(pkg_stack.pop())
                while pkg_stack and pkg_stack[-1] == ',':
                    pkg_stack.pop()
                    fargs.append(pkg_stack.pop())
                fargs.reverse()
                pkg_stack.append(element.operator(element.value[:-1])(*fargs))
            elif element.type in {'UMINUS', 'UPLUS'}:
                try:
                    operand = pkg_stack.pop()
                    pkg_stack.append(element.operator(operand))
                except IndexError:
                    raise ArithmeticError("Calculation error")
            else:
                try:
                    operand_2, operand_1 = pkg_stack.pop(), pkg_stack.pop()
                    pkg_stack.append(element.operator(operand_1, operand_2))
                except ZeroDivisionError:
                    raise ArithmeticError("Division by zero")
                except IndexError:
                    raise ArithmeticError("Calculation error")
        result = pkg_stack.pop()
        if pkg_stack:
            raise ArithmeticError("Calculation error")
        return result
    else:
        raise ArithmeticError("Empty EXPRESSION")


def _modify_expr(expr):

    expr = re.sub(r'[^\w +\-*/^%><=,.!()]', '', expr)

    expr = re.sub(r'([ +\-*/^%><=,(][\d]+)\(', r'\g<1>*(', expr)

    expr = re.sub(r'(^[\d]+)\(', r'\g<1>*(', expr)

    expr = re.sub(r',\s*\)', r')', expr)
    return expr


def calc(expr: str, modules=(), verbose: bool = False):
  
    vprint = print if verbose else lambda *args, **kwargs: None
    global _modules
    _modules = [*modules, 'math', 'builtins']
    expr = _modify_expr(expr)
    vprint("EXPR:\t", expr)
    import_modules(_modules)
    _token_expr = _tokenize_expr(expr)
    _unary_replace(_token_expr)
    vprint('TOKENS:\t', '  '.join(str(v) + ':' + t for i, t, v in _token_expr))
    _queue = _postfix_queue(_token_expr)
    vprint('RPN:\t', '  '.join(str(v) + ':' + t for i, t, v in _queue))
    _result = _pkg_calc(_queue)
    return _result
