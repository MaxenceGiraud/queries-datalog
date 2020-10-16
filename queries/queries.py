# -*- coding: utf-8 -*-
import numpy as np

class Any:
    # unnamed variable
    def __init__(self):
        return

    def __repr__(self):
        return "_"


class Var:
    # named variable, with a field var_name with the variable name
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self,other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)



class Const:
    # Constants with a field const_name containing the name of the constant
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __repr__(self):
        return self.name
    
    def __eq__(self,other):
        return str(self) == str(other)
    
    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)


class Equality:
    # Equality between two terms left and right
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.args = [self.left,self.right]

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
        self.args = [self.left,self.right]

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
        self.predicate_name = str(name)
        self.args = args
        self.pos = positive
        self.arity = len(self.args)

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
        return set(self.head.get_vars())

    def get_bodyvars(self):
        '''Return all the variables contained in the body'''
        vars = []
        for c in self.body:
            vars += c.args
        return set(vars)
    
    def get_body_terms(self):
        '''Return all the terms (variable+constants) contained in the body'''
        terms = []
        for c in self.body :
            terms.append(c.args)
        terms = [[el] for el in set([item for elem in terms for item in elem])]
        return terms
    
    def is_rangerestricted(self):
        '''Check if the rule is range restricted /safe'''
        #Check if all var in head are also in Body
        return self.get_headvars() <= self.get_bodyvars() and \
         all([any([isinstance(term,Const) for term in eq]) or len(eq.intersection(self.get_var_in_positive_clauses())) for eq in self.get_eqclasses()])
        # And Check if either in each eq classes, there is : 1 constant of 1 var contained in a positive clause      
                
    def get_eqclasses(self):
        ''' Return all th equivalence classes in the rule'''
        eq = self.get_body_terms()

        for c in self.body :
            if isinstance(c,Equality):
                eq.append(set([c.left,c.right]))   
        
        return union_find(eq)
    
    def create_eqclasses(self):
        self.eq_classes = self.get_eqclasses()

    def get_predicates(self):
        pred_list_body = []
        pred_head = self.head.get_predicate()
        for c in self.body : 
            if isinstance(c,Clause)  :
                pred_list_body.append(c.get_predicate())
    
        return pred_head,pred_list_body


    def get_var_in_positive_clauses(self):
        ''' Get all the variables from all the positive clauses'''
        var_pos_clauses = set()
        for c in self.body :
            if isinstance(c,Clause) and c.pos:
                var_pos_clauses = var_pos_clauses.union(set(c.get_vars()))
        return var_pos_clauses

    def is_satisfiable(self):
        '''Check if the rule is satisfiable '''
        eq_cl = self.get_eqclasses()
        for c in self.body : # Check if negation creates conflicts with eq classes
            if isinstance(c,Different) :
                for eq in eq_cl :
                    if (c.left in eq) and (c.right in eq) :
                        return False
        
        # Check if no 2 constants in the same eq class
        for eq in eq_cl :
            const_nb = 0
            for term in eq :
                if isinstance(term,Const):
                    const_nb+=1
            if const_nb > 1 :
                return False
        return True

    def get_remove_equalities(self):
        ''' Remove all the equalities and replace the var by the representant of their equivalence classes'''
        eq_cl = self.get_eqclasses()
        repr_eq_classes = get_repr_eq_classes(eq_cl)

        new_body = [Clause(cl.predicate_name,[repr_eq_classes[x] for x in cl.args],cl.pos) \
                for cl in self.body if  isinstance(cl,Clause)] + \
                [Different(repr_eq_classes(diff.left),repr_eq_classes(diff.right)) for diff in self.body if isinstance(diff,Different)] 

        new_head = Clause(self.head.predicate_name,[repr_eq_classes[x] for x in self.head.args],self.head.pos) 

        return new_head,new_body

    def remove_equalities(self):
        self.head,self.body = self.get_remove_equalities()


    def get_predicate_namesarity(self):
        ''' Return a dict containing the arity of each predicate'''
        predicate_namesarity = [(self.head.predicate_name,self.head.arity)]
        for c in self.body : 
            if isinstance(c,Clause):
                predicate_namesarity.append((c.predicate_name,c.arity))

        return predicate_namesarity

    def check_no_negate_any(self):
        '''Check if a negation of any is stated in the rule :
        Return False if it is, True if not'''
        for c in self.body:
            if isinstance(c,Clause) and c.is_negative():
                for arg in c.args :
                    if isinstance(arg,Any):
                        return False
        return True

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
        ''' Check if program is CQ'''
        for rule in self.rules :
            for clause in rule.body :
                if isinstance(clause,Equality)  or  isinstance(clause,Different):
                    return False

        return True


    def is_rangerestricted(self):
        '''Check if the program is range restricted /safe'''
        for rule in self.rules :
            if not rule.is_rangerestricted():
                return False

        return True

    def check_predicate_arity(self):
        '''Check if the arity of each predicate does not change'''
        predicate_arity = dict()
        for r in self.rules:
            for name,arity in r.get_predicate_namesarity():
                if name in predicate_arity:
                    if predicate_arity[name] != arity:
                        return False
                else :
                    predicate_arity[name] = arity
        return True

    def check_no_negate_any(self):
        '''Check if a negation of any is stated in the program :
        Return False if it is, True if not'''
        for rule in self.rules:
            if not rule.check_no_negate_any():
                return False
        return True

    def is_recursive(self):
        pass        

    def is_satisfiable(self):
        '''Check if the program is satisfiable '''
        for r in self.rules :
            if not r.is_satisfiable():
                return False
        return True
    
    def remove_equalities(self):
        ''' Remove all the equalities of all the rulesand replace the var by the representant of their equivalence classes'''

        if self.is_satisfiable():
            for r in self.rules :
                r.remove_equalities()
        else :
            return "Not satisfiable"

    def __repr__(self):
        return "\n".join([rule.__repr__() for rule in self.rules])


class Query:
    # A query is made with a program, facts (a list of clauses with constant
    # arguments only) and a clause for querying data.
    def __init__(self, program, facts, query):
        self.program = program
        self.query = query

    def is_CQ(self):
        ''' Check if query is CQ'''
        return self.program.is_CQ()

    def is_rangerestricted(self):
        ''' Check if query is range restricted/safe'''
        return self.program.is_rangerestricted()

    def is_satisfiable(self):
        ''' Check if query is satisfiable'''
        return self.program.is_satisfiable()

    def remove_equalities(self):
        ''' Remove all the equalities and replace the var by the representant of their equivalence classes'''
        return self.program.remove_equalities()
    
    def check_no_negate_any(self):
        '''Check if a negation of any is stated in the program :
        Return False if it is, True if not'''
        return self.program.check_no_negate_any()
    
    def check_predicate_arity(self):
        '''Check if the arity of each predicate does not change'''
        return self.program.check_predicate_arity()
  
    def is_recursive(self):
        pass

    def sort_rules(self):
        ''' Sort the rules/predicates in order to solver the query'''
        # Create dependencies graph
        dependencies = {}
        for r in  self.program.rules :
            head_pred,body_pred = r.get_predicates()
            dependencies.setdefault(head_pred,[]).extend(body_pred)
            [dependencies.setdefault(p,[]) for p in  body_pred]
        # Init the states
        states = {p:'white' for p in dependencies}
        start = self.query.get_predicate()
        
        # Resolve the graph problem/ sort the predicates
        def sort_graph(dependencies,states,node,sorted_list):
            if not dependencies[node]:
                sorted_list.append(node)
                states[node] = "red"
            else : 
                states[node] = "blue"
                for n in dependencies[node]:
                    if states[n] == "blue":
                        raise Exception("The Query is recursive")
                    sorted_list = sort_graph(dependencies,states,n,sorted_list)
                sorted_list.append(node)
            return sorted_list

        predicate_sorted = sort_graph(dependencies,states,start,[])
        return predicate_sorted

    def __repr__(self):
        return self.program.__repr__() + "\n? " + self.query.__repr__()


def union_find(lis):
    lis = map(set, lis)
    unions = []
    for item in lis:
        temp = []
        for s in unions:
            if not s.isdisjoint(item):
                item = s.union(item)
            else:
                temp.append(s)
        temp.append(item)
        unions = temp
    return unions

def get_repr_eq_classes(eq_classes):
    '''Get representant of an equivalent class
    -either the constant is chosen or a random var
    output a dict
    '''
    repr = []
    dict_repr = dict()
    for i in range(len(eq_classes)) :
        for term in eq_classes[i] :
            if isinstance(term,Const):
                repr.append(term)
        if len(repr) < i+1 :
            repr.append(list(eq_classes[i])[0])

        for term in eq_classes[i] :
            dict_repr[str(term)] = repr[i]

            
    return dict_repr
