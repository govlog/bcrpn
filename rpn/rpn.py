# -*- coding: UTF-8

import math


class Infix(object):
    """Class to convert from INFIX notation to RPN notation with a RPN parser
       Include variables, bitwise operator and some trig functions"""

    LEFT_ASSOC = 0
    RIGHT_ASSOC = 1
    OTHER = 2

    op_order = {'^': (10, RIGHT_ASSOC),
                '*': (5, LEFT_ASSOC),
                '/': (5, LEFT_ASSOC),
                '%': (3, LEFT_ASSOC),
                '+': (1, LEFT_ASSOC),
                '-': (1, LEFT_ASSOC),
                ')': (0, OTHER),
                '(': (0, OTHER),
                '&': (0, OTHER)}

    valid_ops = {'+', '-', '/', '*', '%', '^', '&', '|', '!'}

    paren = {'(': 1,
             ')': 1}

    logic = {'&', '|', '!', ''}

    func = {'sin': (5, LEFT_ASSOC),
            'cos': (5, LEFT_ASSOC),
            'acos': (5, LEFT_ASSOC)}

    def __init__(self, infix_expr, variables, debug=False):
        __sanitize = infix_expr.strip(' \t\n\r').replace(' ', '')

        self.infix = list(__sanitize)

        if variables:
            self.variables = variables
        else:
            self.variables = {}

        self.scale = 9
        self.form = ''

        if debug:
            print "(input) ", infix_expr
            print "(clean) ", self.infix
            self.debug = True
        else:
            self.debug = False

        self.token_list = []
        self.rpn = []
        self.result = 0
        self.set_scale(self.scale)


    def __debug(self, msg):
        if self.debug:
            print msg


    @staticmethod
    def __error(msg):
        print msg

    def __format_num(self, num):
        return self.form.format(num).rstrip('0').rstrip('.')


    def __get_word(self, word):
        if word in Infix.func:
            return word
        elif word in self.variables:
            return float(self.variables[word])
        else:
            self.__error("(warn)   unknown func/var '" + word + "'")
            return 0

    @staticmethod
    def __is_int(i):
        if '.' not in str(i).rstrip('0').rstrip('.'):
            return True
        else:
            return False


    def __get_stuff(self, num, word):
        if num == '-' and word != '':
            self.token_list.append(float(-self.__get_word(word)))
        elif (word and num) or num == '-' or num == '.':
            self.__error('(error) error in expression')
            return False

        elif num != '':
            self.token_list.append(float(num))

        elif word != '':
            self.token_list.append(self.__get_word(word))

        return True


    def set_scale(self, scale):
        self.scale = scale
        self.form = '{0:.' + str(scale) + 'f}'


    @staticmethod
    def is_assoc(o1, direction):
        if Infix.op_order[o1][1] == direction:
            return True
        else:
            return False


    def to_tokens(self):
        """This method convert the sanitized self input into an array of token"""
        num = ''
        word = ''
        last = ''

        par_count = {'(': 0, ')': 0}

        for i, c in enumerate(self.infix):

            if c in self.paren:
                par_count[c] += 1

            if self.token_list:
                last = self.token_list[-1]

            if c.isdigit() or c == '.' or (c == '-' and (i == 0 or num == '' and word == '' and last != ')')):
                num += c

            elif c.isalpha():
                word += c

            elif c in self.op_order:

                if not self.__get_stuff(num, word):
                    return False

                num = ''
                word = ''

                if i < len(self.infix) - 1 or c == ')':
                    self.token_list.append(c)
                else:
                    self.__error("(error) last char can't be an operator")
                    return False

            else:

                self.__error("(error) wrong char '" + c + "' at pos " + str(i))
                return False

        if par_count['('] != par_count[')']:
            self.__error("(error) missing parenthesis")
            return False

        if not self.__get_stuff(num, word):
            return False

        self.__debug('(tokens) ' + str(self.token_list))

        return True


    def to_rpn(self):
        """This method convert an array of tokens to a RPN output stack"""
        stack = []
        for t in self.token_list:

            if t in self.func:
                stack.append(t)

            elif t == '(':
                stack.append(t)

            elif t in Infix.valid_ops:

                while stack:
                    if self.is_assoc(t, self.LEFT_ASSOC) and Infix.op_order[t] <= Infix.op_order[stack[-1]] \
                            or self.is_assoc(t, self.RIGHT_ASSOC) and Infix.op_order[t] < Infix.op_order[stack[-1]]:
                        self.rpn.append(stack.pop())
                    else:
                        break

                stack.append(t)

            elif t == ')':

                while stack[-1] != '(':
                    self.rpn.append(stack.pop())

                if stack:
                    stack.pop()
                    if stack and stack[-1] in Infix.func:
                        self.rpn.append(stack.pop())

            else:
                self.rpn.append(t)

        while stack:
            self.rpn.append(stack.pop())

        if not self.rpn:
            self.rpn.append(0)

        self.__debug('(rpn)    ' + str(self.rpn))

        return True


    def to_result(self):
        """This method parse/compute the RPN stack and store result in self.result"""
        stack = []

        for t in self.rpn:

            if t in Infix.valid_ops and t not in Infix.logic:
                if len(stack) >= 2:

                    b = float(stack.pop())
                    a = float(stack.pop())

                    if t == '*':
                        stack.append(a * b)
                    elif t == '/':
                        if not a or not b:
                            self.__error('(error)  division by zero!')
                            return False
                        else:
                            stack.append(a / b)
                    elif t == '+':
                        stack.append(a + b)
                    elif t == '-':
                        stack.append(a - b)
                    elif t == '%':
                        stack.append(a % b)
                    elif t == '^':
                        if a == 1:
                            stack.append(1)
                        else:
                            if self.__is_int(b):
                                stack.append(a ** b)
                            else:
                                self.__debug('(error) exponent must be an integer')
                                return False

                else:
                    self.__error('(error) operand missing')
                    return False

            elif t in Infix.logic:
                a = stack.pop()
                b = stack.pop()
                if self.__is_int(a) and self.__is_int(b):
                    a = int(a)
                    b = int(b)
                    if t == '&':
                        stack.append(a & b)
                    if t == '|':
                        stack.append(a | b)
                else:
                    self.__debug('(error) must use integer for bitwise')
                    return False

            elif t in Infix.func:
                a = float(stack.pop())
                if t == 'sin':
                    stack.append(math.sin(a))
                elif t == 'cos':
                    stack.append(math.cos(a))
                else:
                    self.__error('(error) functions need parameters')
                    return False

            else:
                stack.append(t)

        self.result = self.__format_num(stack[-1])

        return True


    def evaluate(self):
        """This method evaluate, convert user input INFIX to POSTFIX, then to RPN and compute RPN output stack"""
        if self.to_tokens() and self.to_rpn() and self.to_result():
            return True
        else:
            return False


    def get_result(self):
        """This method return the computed result"""
        if self.evaluate():
            return self.result
        else:
            return 0
