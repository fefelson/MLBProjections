import os
import unittest

import MLBProjections.MLBProjections.Environ as ENV

################################################################################
################################################################################





################################################################################
################################################################################


class DBTests(unittest.TestCase):

    def test_db_exists(self):
        self.assertTrue(os.path.exists(ENV.getDBPath("mlb")))



################################################################################
################################################################################

if __name__ == "__main__":
    unittest.main()
