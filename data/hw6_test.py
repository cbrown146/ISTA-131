import unittest, sys, io, pandas as pd
from contextlib import redirect_stdout
from unittest.mock import patch
from hw6 import *
import hw6
from compare_pandas import *

''' 
Auxiliary files needed:
    compare_pandas.py
    all_countries0.pkl, all_countries1.pkl, all_countries2.pkl, all_countries3.pkl, dying.pkl
This one is needed by hw4.py and is therefore required:
    countries_of_the_world.csv
'''

class TestFns(unittest.TestCase):
    def setUp(self):
        self.regs = ['western europe', 'eastern europe', 'northern america', 'sub-saharan africa']
        self.reg_dict = {r:[] for r in self.regs}
        self.world0 = pd.read_pickle('all_countries0.pkl') # after csv_to_dataframe
        self.world1 = pd.read_pickle('all_countries1.pkl') # after format_df
        self.world2 = pd.read_pickle('all_countries2.pkl') # after life_change
        self.world3 = pd.read_pickle('all_countries3.pkl') # after years_to_extinction
        for w in [self.world0, self.world1, self.world2, self.world3]:
            for i in range(len(self.regs)):
                self.reg_dict[self.regs[i]].append(w[w['Region'].str.strip().str.lower() == self.regs[i]])
   
    def test_csv_to_dataframe(self):
        correct = pd.read_pickle('all_countries0.pkl')
        tester = csv_to_dataframe('countries_of_the_world.csv')
        self.assertTrue(compare_frames_str(correct, tester))
        
    def test_format_df(self):
        correct = pd.read_pickle('all_countries1.pkl')
        df = pd.read_pickle('all_countries0.pkl')
        self.assertIsNone(format_df(df))
        self.assertTrue(compare_frames_str(correct, df))
    
    def test_growth_rate(self):
        correct = pd.read_pickle('all_countries2.pkl')
        df = pd.read_pickle('all_countries1.pkl')
        self.assertIsNone(growth_rate(df))
        self.assertTrue(compare_frames_str(correct, df))
    
    def test_years_to_extinction(self):
        correct = pd.read_pickle('all_countries3.pkl')
        df = pd.read_pickle('all_countries2.pkl')
        self.assertIsNone(years_to_extinction(df))
        self.assertTrue(compare_frames_str(correct, df))
    
    def test_dying_countries(self):
        correct = pd.read_pickle('dying.pkl')
        df = pd.read_pickle('all_countries3.pkl')
        self.assertTrue(compare_series(correct, dying_countries(df)))
    
    def test_main(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            res = 'Botswana: 2115.0 Years to Extinction\n' +\
            'Monaco: 2602.0 Years to Extinction\n' +\
            'Ukraine: 3038.0 Years to Extinction\n' +\
            'Latvia: 3148.0 Years to Extinction\n' +\
            'Bulgaria: 3266.0 Years to Extinction\n'
            hw6.main()
            self.assertEqual(res, buf.getvalue())
    
def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + ' / 100')
    
if __name__ == "__main__":
    main()