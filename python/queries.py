# -*- coding: utf-8 -*-


class Any:
    # unnamed variable
    def __init__(self):
        return

    def toString(self):
        return "_"


class Var:
    # named variable, with a field var_name with the variable name
    def __init__(self, name):
        self.var_name = name

    def get_name(self):
        return self.var_name

    def toString(self):
        return self.var_name


class Const:
    # Constants with a field const_name containing the name of the constant
    def __init__(self, name):
        self.const_name = name

    def get_name(self):
        return self.const_name

    def toString(self):
        return self.const_name


class Equality:
    # Equality between two terms left and right
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def toString(self):
        return self.left.toString() + " = " + self.right.toString()


class Different:
    # Specifies that two terms left and right must be different
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def toString(self):
        return self.left.toString() + " ≠ " + self.right.toString()


class Clause:
    # Clause with a predicate name, the list of terms (args), and whether it is
    # negated or not.
    def __init__(self, name, args, positive):
        self.predicate_name = name
        self.args = args
        self.pos = positive

    def get_predicate(self):
        return self.predicate_name

    def get_args(self):
        return self.args

    def is_negative(self):
        return not self.pos

    def is_positive(self):
        return self.pos

    def toString(self):
        if self.is_positive():
            neg = ""
        else:
            neg = u"¬"
        return neg + self.predicate_name + "(" + ", ".join(
            [arg.toString() for arg in self.args]) + ")"


class Rule:
    # Rule made with a head (positive) clause, and body of list of clauses
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def get_head(self):
        return self.head

    def get_body(self):
        return self.body

    def toString(self):
        if self.body == []:
            r = self.head.toString()
        else:
            r = self.head.toString() + u" ← " + " ".join(
                [clause.toString() for clause in self.body])
        return r + "."


class Program:
    # Programs are a non empty list of rules
    def __init__(self, rules):
        self.rules = rules

    def get_rules(self):
        return self.rules

    def toString(self):
        return "\n".join([rule.toString() for rule in self.rules])


class Query:
    # A query is made with a program, facts (a list of clauses with constant
    # arguments only) and a clause for querying data.
    def __init__(self, program, facts, query):
        self.program = program
        self.query = query

    def get_program(self):
        return self.program

    def get_query(self):
        return self.query

    def toString(self):
        return self.program.toString() + "\n? " + self.query.toString()
