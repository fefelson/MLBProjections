import os
import unittest

import MLBProjections.MLBProjections.Environ as ENV
from MLBProjections.MLBProjections.Models.Umpire import Umpire

################################################################################
################################################################################





################################################################################
################################################################################


class UmpireTests(unittest.TestCase):

    def setUp(self):
        self.umpire = Umpire()

    def test_umpire_ends_game(self):
        
        self.assertTrue(os.path.exists(ENV.getDBPath("mlb")))



################################################################################
################################################################################

if __name__ == "__main__":
    unittest.main()
