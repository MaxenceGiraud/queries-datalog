# Implementation: query evaluation

In the two subfolders, you can find a parser that can analyse conjunctive query
programs. One is written in Haskell, the other in Python. The syntax is as
follows:

- relation names or constant names have to start with lower case letters and
  then can contain any sequence of letters (lower or upper case), numbers and
  hyphens "-" or underscore "\_". Or they can use any string contained between
  single quotes e.g. 'I am a relation or constant name' or double quotes "I also
  am a relation or constant name". In these cases on has, one has to escape
  single quotes or double quotes with a backslash in the corresponding case.
  
- variable names must start with an upper case letter and then may contain any
  sequence of letter (lower or upper case), numbers and hyphens "-" or
  underscore "\_".
  
- useless variables are simply written "\_"
  
- rules are then of the form:
  r(u1,...,un) <- r1(v11,...,v1n1), ..., rp(v1p,...,v1np).
  
  The commas separating the clauses in the right side or in the arguments of a
  predicate are optional.
  
  If the right side is empty, then one can simply write: r(u1,...,un).
  
  Equalities are allowed in the form of u = v.
  
- a program is a sequence of rules.

- a query is a program followed by a sentence of this form: ? r(u1,...,un).

Each version of the parser comes with data structures representing the objects
representing variables, constants, clauses, rules...

The implementations that are asked from you are to be made in one of the
proposed languages.

For Haskell, the development is using the tool stack. Here compilation is based
on the command "stack build". 

The Python implementation relies on the library "lark". It will work once you
install it: "pip install lark" or "pip3 install lark".

## Range restriction

The first thing you are asked to implement is whether a rule with possibly
equalities and negation satisfies the /range restriction/ or /safety/ property.
Check also that equalities do not generate unsatisfiable conditions.

Once this is done, also transform such rules so that they do not contain
equalities anymore.

## Recursivity of programs

Implement an algorithm that checks whether a program is recursive. When given a
query, use your algorithm so as a to obtain a sequence of predicates you need to
solve so as to answer the query.


