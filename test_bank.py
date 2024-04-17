

import unittest
from unittest import TestCase
from banking_system_imp import BankingSystemImp


class Tests(TestCase):
    """
    The test suit below includes 3 tests .
    """

    failureException = Exception


    @classmethod
    def setUp(cls):
        cls.system = BankingSystemImp()


    def test_case_01(self):
        self.assertEqual(self.system.create_account('account1'),0)
        self.assertEqual(self.system.create_account('account2'),0)
        self.assertEqual(self.system.create_account('account3',10),10)
        self.assertEqual(self.system.create_account('account2',10),False)


    def test_case_02(self):
        self.assertEqual(self.system.create_account('account1',100),100)
        self.assertEqual(self.system.create_account('account2'),0)
        self.assertEqual(self.system.deposit('account1', 2500), 2600)
        self.assertEqual(self.system.deposit('account1', 500), 3100)
        self.assertEqual(self.system.deposit('account2', 1000), 1000)
        self.assertEqual(self.system.deposit('account3', 100), False)


    def test_case_03(self):
        self.assertEqual(self.system.create_account('account1'),0)
        self.assertEqual(self.system.create_account('account2'),0)
        self.assertEqual(self.system.deposit('account1', 2000), 2000)
        self.assertEqual(self.system.deposit('account2', 1000), 1000)
        self.assertEqual(self.system.transfer('account1', 'account2', 500), (1500,1500))
        self.assertEqual(self.system.withdraw('account1', 100), 1400)
        self.assertEqual(self.system.withdraw('account2', 300), 1200)
        self.assertEqual(self.system.withdraw('account1', 1500), False)

if __name__=='__main__':
    unittest.main(exit=False)        
