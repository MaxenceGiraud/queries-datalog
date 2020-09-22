# -*- coding: utf-8 -*-

from lark import Lark, Transformer

from . import queries

grammar = r"""
NEG:  "~" | "¬" | "!"
IMPL: "<-" | "<=" | "←" | ":-"
ASK: "?" | "?-"
DOT: "."
UPPER: /[A-Z]/
LOWER: /[a-z]/
SYMBOLS: /[a-zA-Z0-9\-_]/
VAR: UPPER SYMBOLS*
NAME: LOWER SYMBOLS* | /'([^']|\')+'/ | /"([^"]|\")+"/
ANY: "_"
NEQ: "<>" | "~=" | "!=" | "≠"

query: program the_query

program: rule          -> one_rule_program
       | rule program  -> rec_program

rule: head IMPL body DOT -> act_rule
    | head DOT           -> fact

head: pred "(" args ")"

?pred: VAR
| NAME

term: VAR -> t_var
| NAME    -> t_name
| ANY     -> t_any

tterm: VAR -> t_var
| NAME     -> t_name

?args:              -> empty_arg
| nargs

nargs: term      -> one_arg
| term "," nargs -> args_term
| term nargs     -> args_term

body:              -> empty_body
| clause "," body  -> clause_body
| clause body      -> clause_body

clause: tterm "=" tterm  -> eq_clause
| NEG tterm "=" tterm    -> neq_clause1
| tterm NEQ tterm        -> neq_clause2
| NEG pred "(" args ")"  -> neg_clause
| pred "(" args ")"      -> pos_clause

the_query: ASK head DOT ->the_query_dot
| ASK head -> the_query

%import common.WS
%ignore WS
"""


class BuildQuery(Transformer):
    """Class for compiling parse trees to query data structures"""
    def query(self, ch):
        [program, theQuery] = ch
        return queries.Query(program, [], theQuery)

    def one_rule_program(self, rule):
        return queries.Program(rule)

    def rec_program(self, ch):
        [rule, program] = ch
        return queries.Program([rule] + program.rules)

    def act_rule(self, ch):
        [head, _, body, _] = ch
        return queries.Rule(head, body)

    def fact(self, ch):
        [head, _] = ch
        return queries.Rule(head, [])

    def head(self, ch):
        [pred, args] = ch
        return queries.Clause(pred, args, True)

    def pred(self, v):
        [n] = v
        return n

    def empty_args(self):
        return []

    def one_arg(self, ch):
        [t] = ch
        return [t]

    def args_term(self, ch):
        [t, args] = ch
        return [t] + args

    def t_var(self, ch):
        [x] = ch
        return queries.Var(x)

    def t_name(self, ch):
        [n] = ch
        return queries.Const(n)

    def t_any(self, ch):
        return queries.Any()

    def empty_body(self, _):
        return []

    def clause_body(self, ch):
        [clause, body] = ch
        return [clause] + body

    def eq_clause(self, ch):
        [left, right] = ch
        return queries.Equality(left, right)

    def neq_clause1(self, ch):
        [_, left, right] = ch
        return queries.Different(left, right)

    def neq_clause2(self, ch):
        [left, _, right] = ch
        return queries.Different(left, right)

    def neg_clause(self, ch):
        [_, pred, args] = ch
        return queries.Clause(pred, args, False)

    def pos_clause(self, ch):
        [pred, args] = ch
        return queries.Clause(pred, args, True)

    def the_query_dot(self, ch):
        [ask, head, dot] = ch
        return head

    def the_query(self, ch):
        [ask, head] = ch
        return head


query_parser = Lark(grammar,
                    start='query',
                    parser='lalr',
                    transformer=BuildQuery()).parse
program_parser = Lark(grammar,
                      start='program',
                      parser='lalr',
                      transformer=BuildQuery()).parse


def program_parse_file(file_name):
    """Function helper that parses a file containing a program and return a queries.Program object."""
    with open(file_name,encoding='utf8') as f:
        return program_parser(f.read())


def query_parse_file(file_name):
    """Function helper that parses a file containing a program and return a queries.Query object."""
    with open(file_name,encoding='utf8') as f:
        return query_parser(f.read())

if __name__ == 'main':
    print(query_parse_file("../example.query"))
