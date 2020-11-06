# Queries

## Queries formalism
### Examples
A list of queries can be found in the folder [query_exmaples/](./query_examples/)

###  Syntax
The syntax is as
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

## How to use 
```{python}
import queries

# Load/Parse a query
q = queries.query_parse_file("query_examples/eval2-doublejoin.query")

# Peforms check on the query 
q.is_CQ()
q.is_rangerestricted()
q.is_satisfiable()
q.check_no_negate_any()
q.check_predicate_arity()

# Remove equalities (CQE to CQ)
q.remove_equalities()

# Sort the rules in order to evaluate the query
q.sort_rules()

# Evaluate a query  
q.evalutate()
````
N.B. : The evaluate method already performs the checks and remove equalites, sort rules, no need to call those functions before evaluation. 

### unittest
to launch unittest :

```{python}
python -m unittest tests/program_test.py
````


