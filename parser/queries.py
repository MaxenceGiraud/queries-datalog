# -*- coding: utf-8 -*-


class Any:
    # unnamed variable
    def __init__(self):
        return

    def __repr__(self):
        return "_"


class Var:
    # named variable, with a field var_name with the variable name
    def __init__(self, name):
        self.var_name = name

    def get_name(self):
        return self.var_name

    def __repr__(self):
        return self.var_name


class Const:
    # Constants with a field const_name containing the name of the constant
    def __init__(self, name):
        self.const_name = name

    def get_name(self):
        return self.const_name

    def __repr__(self):
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

    def __repr__(self):
        return self.left.__repr__() + " = " + self.right.__repr__()


class Different:
    # Specifies that two terms left and right must be different
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def __repr__(self):
        return self.left.__repr__() + " ≠ " + self.right.__repr__()


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

    def get_vars(self):
        vars = []
        for a in self.args :
            if isinstance(a,Var):
                vars.append(a)
        return vars

    def __repr__(self):
        if self.is_positive():
            neg = ""
        else:
            neg = u"¬"
        return neg + self.predicate_name + "(" + ", ".join(
            [arg.__repr__() for arg in self.args]) + ")"


class Rule:
    # Rule made with a head (positive) clause, and body of list of clauses
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def get_headvars(self):
        return self.head.get_vars()

    def get_bodyvars(self):
        vars = []
        for clause in self.body:
            vars += clause.get_vars()
        return vars

    def get_headvars_string(self):
        return set(str(v) for v in self.head.get_vars())

    def get_bodyvars_string(self):
        vars = []
        for clause in self.body:
            vars += [str(v) for v in clause.get_vars()]
        return set(vars)

    def is_rangerestricted(self):
        return self.get_headvars_string() <= self.get_bodyvars_string()

    def __repr__(self):
        if self.body == []:
            r = self.head.__repr__()
        else:
            r = self.head.__repr__() + u" ← " + " ".join(
                [clause.__repr__() for clause in self.body])
        return r + "."


class Program:
    # Programs are a non empty list of rules
    def __init__(self, rules):
        self.rules = rules

    def is_CQ(self):
        for rule in self.rules :
            for clause in rule.body :
                if isinstance(clause,Equality)  or  isinstance(clause,Different):
                    return False

        return True


    def is_rangerestricted(self):
        if self.is_CQ():
            for rule in self.rules :
                if not rule.is_rangerestricted():
                    return False

            return True
        else :
            return False




    def __repr__(self):
        return "\n".join([rule.__repr__() for rule in self.rules])


class Query:
    # A query is made with a program, facts (a list of clauses with constant
    # arguments only) and a clause for querying data.
    def __init__(self, program, facts, query):
        self.program = program
        self.query = query

    def is_CQ(self):
        return self.program.is_CQ()

    def is_rangerestricted(self):
        return self.program.is_rangerestricted()


    def __repr__(self):
        return self.program.__repr__() + "\n? " + self.query.__repr__()
