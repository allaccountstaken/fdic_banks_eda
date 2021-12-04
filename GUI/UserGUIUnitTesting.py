import unittest
import pandas as pd
from UserGui import plot

class GUI_Test(unittest.TestCase):
    def test_minMaxYears(self):

        # Setup
        ni = pd.DataFrame()
        li = pd.DataFrame()
        co = pd.DataFrame()
        fa = pd.DataFrame()
        last_generated = [0]

        minyear = '2000'
        maxyear = '2000'

        try:
            plot(ni, li, co, fa, last_generated).validateInputYears()
        except Exception as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main() 
