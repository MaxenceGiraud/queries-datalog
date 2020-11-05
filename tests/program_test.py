import unittest
import queries
import numpy as np

'''Careful : This test file is meant to be run at the root of the project'''

class ProgramTestCase(unittest.TestCase):
    def setUp(self):
        self.folder_test = 'query_examples/'

    def test_isCQ(self):
        file = self.folder_test+"CQnotRR.query"
        iscq = queries.program_parse_file(file)
        self.assertTrue(iscq.is_CQ())

    #def test_isnotCQ(self):

    def test_not_rangerestricted(self):
        file = self.folder_test+"CQnotRR.query"
        notrr = queries.program_parse_file(file)
        self.assertFalse(notrr.is_rangerestricted())

    def test_rangerestricted(self):
        file = self.folder_test+"RR.query"
        rr = queries.program_parse_file(file)
        self.assertTrue(rr.is_rangerestricted())
    
    def test_safe(self):
        file = self.folder_test+"safe.query"
        rr = queries.program_parse_file(file)
        self.assertTrue(rr.is_rangerestricted())
    
    def test_safe2(self):
        file = self.folder_test+"safe2.query"
        rr = queries.program_parse_file(file)
        self.assertTrue(rr.is_rangerestricted())

    def test_not_safe(self):
        file = self.folder_test+"notsafe.query"
        q = queries.program_parse_file(file)
        self.assertFalse(q.is_rangerestricted())

    def test_not_satisfiable(self):
        file = self.folder_test+"inconsistant.query"
        q = queries.program_parse_file(file)
        self.assertFalse(q.is_satisfiable())
    
    def test_not_satisfiable2(self):
        file = self.folder_test+"inconsistant.query"
        q = queries.program_parse_file(file)
        self.assertFalse(q.is_satisfiable())
    
    def test_not_satisfiable3(self):
        file = self.folder_test+"inconsistant.query"
        q = queries.program_parse_file(file)
        self.assertFalse(q.is_satisfiable())
    
    def test_any_negation(self):
        file = self.folder_test+"anynegation.query"
        q = queries.program_parse_file(file)
        self.assertFalse(q.check_no_negate_any())
    
    def test_no_any_negation(self):
        file = self.folder_test+"safe.query"
        q = queries.program_parse_file(file)
        self.assertTrue(q.check_no_negate_any())

        file = self.folder_test+"safe2.query"
        q = queries.program_parse_file(file)
        self.assertTrue(q.check_no_negate_any())

        file = self.folder_test+"aritypredicatechanging.query"
        q = queries.program_parse_file(file)
        self.assertTrue(q.check_no_negate_any())

        file = self.folder_test+"RR.query"
        q = queries.program_parse_file(file)
        self.assertTrue(q.check_no_negate_any())
    
    def test_changingpredicatearity(self):
        file = self.folder_test+"aritypredicatechanging.query"
        q = queries.program_parse_file(file)
        self.assertFalse(q.check_predicate_arity())
    
    def test_no_changingpredicatearity(self):
        file = self.folder_test+"safe2.query"
        q = queries.program_parse_file(file)
        self.assertTrue(q.check_predicate_arity())

        file = self.folder_test+"RR.query"
        q = queries.program_parse_file(file)
        self.assertTrue(q.check_predicate_arity())

        file = self.folder_test+"inconsistant.query"
        q = queries.program_parse_file(file)
        self.assertTrue(q.check_predicate_arity())

        file = self.folder_test+"inconsistent2.query"
        q = queries.program_parse_file(file)
        self.assertTrue(q.check_predicate_arity())

    def test_sort_rule_simple(self):
        file = self.folder_test+"rulestosort.query"
        q = queries.query_parse_file(file)
        sorted_rules = q.get_sorted_predicate()

        self.assertListEqual(sorted_rules,['f', 'q'])
            
    def test_sort_rule2(self):
        file = self.folder_test+"complexrulessort.query"
        q = queries.query_parse_file(file)
        sorted_rules = q.get_sorted_predicate()

        self.assertListEqual(sorted_rules,['f', 'q'])
    
    def test_recursive_program(self):
        file = self.folder_test+"recursive.query"
        q = queries.query_parse_file(file)
        self.assertRaises(Exception,q.sort_rules)

    def test_eval_simple(self):
        file = self.folder_test+"eval0.query"
        q = queries.query_parse_file(file)
        eval = list(np.unique([str(a) for a in q.evaluate()]))
        self.assertListEqual(["'Actor0'","'Actor1'"],eval)
    
    def test_eval_singlejoint(self):
        file = self.folder_test+"eval1.query"
        q = queries.query_parse_file(file)
        eval = list(np.unique(q.evaluate()))
        self.assertListEqual(["Theatre0","Theatre1","Theatre2"],eval)
    
    def test_eval_doublejoint(self):
        file = self.folder_test+"eval2.query"
        q = queries.query_parse_file(file)
        eval = list(np.unique(q.evaluate()))
        self.assertListEqual(["Movie0","Movie1","Movie2"],eval)

if __name__ == '__main__':
    unittest.main()