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
        q_rules = q.program.rules

        q.sort_rules()

        self.assertTrue(np.all(np.array(q.program.rules)==np.array(q_rules)[[1,0,2]]))
            
    def test_sort_rule_complex(self):
        file = self.folder_test+"complexrulessort.query"
        q = queries.query_parse_file(file)
        q_rules = q.program.rules
        q.sort_rules()

        self.assertTrue(np.all(np.array(q.program.rules)==np.array(q_rules)[[4,1,0,3,2,5]]))

if __name__ == '__main__':
    unittest.main()