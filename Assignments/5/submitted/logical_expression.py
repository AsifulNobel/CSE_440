#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Last Edited By: Asiful Haque Latif Nobel
# Last Edited on: 04/07/2016
#-------------------------------------------------------------------------------

import sys
from copy import deepcopy

var_symbols = set()
alpha_truth_values = []
#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # function's changes will actually alter the class variable. Thus, lists.
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []

def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)

    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective, result)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol, result)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target, result_instance):
    """Reads the next word of an input string and stores it in target"""
    global var_symbols

    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1
        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            # Adds expression symbol to symbol set if target is .symbol property
            if target is result_instance.symbol:
                var_symbols.add(target[0])
            break
        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here
def get_const_symbols(model, KB):
    for sub_expr in KB.subexpressions:
        if len(sub_expr.connective) == 1 and len(sub_expr.subexpressions) == 0:
            model[sub_expr.symbol[0]] = True

            if sub_expr.symbol[0] in var_symbols:
                var_symbols.remove(sub_expr.symbol[0])
        elif sub_expr.connective[0] == 'not' and len(sub_expr.subexpressions[0].subexpressions) == 0:
            model[sub_expr.subexpressions[0].symbol[0]] = False

            if sub_expr.subexpressions[0].symbol[0] in var_symbols:
                var_symbols.remove(sub_expr.subexpressions[0].symbol[0])
    return

def eval_expression(expression, model, value_stack):
    if expression.symbol[0] and expression.symbol[0] != '': # If it is a base case (symbol)
        return model[expression.symbol[0]]
    elif expression.connective[0]: # If it is a connective
        for subexpression in expression.subexpressions:
            value_stack.append(eval_expression(subexpression, model, []))

        if len(value_stack) > 0:
            first = value_stack.pop()
        else:
            if expression.connective[0] == 'and':
                return True
            elif expression.connective[0] in ['or', 'xor']:
                return False
        if expression.connective[0] == 'not':
            return (not first)

        elif expression.connective[0] == 'and':
            if first and all(value_stack):
                first = True
            else:
                first = False

            return first

        elif expression.connective[0] == 'or':
            while(len(value_stack) > 0):
                second = value_stack.pop()

                if first or second:
                    first = True
                else:
                    first = False
            return first

        elif expression.connective[0] == 'xor':
            while(len(value_stack) > 0):
                if first != value_stack.pop():
                    return True
                else:
                    return False

        elif expression.connective[0] == 'if':
            while(len(value_stack) > 0):
                first = (not value_stack.pop()) or first
            return first

        elif expression.connective[0] == 'iff':
            if first == value_stack.pop():
                return True
            else:
                return False


def pl_true(expression, model):
    return eval_expression(expression, model, [])


def tt_check_all(KB, alpha, symbols, model):
    global alpha_truth_values
    global counter

    if len(symbols) == 0:
        if pl_true(KB, model):
            alpha_truth_values.append(pl_true(alpha, model))
            return alpha_truth_values[len(alpha_truth_values) - 1]
        else:
            return True
    else:
        first_symbol = symbols[0]
        symbols.remove(first_symbol)

        # Fixed problem ---> 01/07/2016(11:16 AM)
        symbols_duplicate = deepcopy(symbols)

        model[first_symbol] = True
        true_value = tt_check_all(KB, alpha, symbols, model)

        model[first_symbol] = False
        false_value = tt_check_all(KB, alpha, symbols_duplicate, model)

        return (true_value and false_value)

def check_true_false(KB, alpha):
    global var_symbols
    global alpha_truth_values

    model = {}
    get_const_symbols(model, KB)

    symbol_list = list(var_symbols)

    return tt_check_all(KB, alpha, symbol_list, model), alpha_truth_values
