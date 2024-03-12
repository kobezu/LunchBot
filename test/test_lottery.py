import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import user
from lottery_result import LotteryResult
from user import Language

def users_path(n: int):
    return f"test/test_users/{n}.json"

def valid_sizes(groups: "list[list[user.User]]") -> bool:
    return all((len(group) == 2) or (len(group) == 3) for group in groups)

def valid_languages(groups: "list[list[user.User]]") -> bool:
    for group in groups:
        if not all(((_user.lunch_language == Language.FIN) or (_user.lunch_language == Language.BOTH)) for _user in group):
            if not all(((_user.lunch_language == Language.ENG) or (_user.lunch_language == Language.BOTH)) for _user in group):
                return False
    return True

def print_groups(result: LotteryResult, test: int):
    def print_group(group: "list[user.User]"):
        line = ""
        for _user in group:
            line += f"{_user.name}: {_user.lunch_language.name}  "
        print(line)
    
    print(f"\nTest {test}.\nGroups:")
    n = 1
    for group in result.groups:
        print(f"{n}.")
        print_group(group)
        n+=1

    print("Users not in groups:")
    print_group(result.not_in_group)

def test(self, n: int, group_amount: int, not_group_amount: int):
    user.users.clear()
    user.load_users(users_path(n-1))
    r = LotteryResult()
    print_groups(r, n)
    self.assertTrue(valid_sizes(r.groups), "Group sizes not valid")
    self.assertTrue(valid_languages(r.groups), "Group languages not valid")
    self.assertEqual(len(r.groups), group_amount, "Unexpected amount of result groups")
    self.assertEqual(len(r.not_in_group), not_group_amount, "Unexpected amount of users not in groups")

class TestLottery(unittest.TestCase):
    
    def test_1(self):
        test(self, 1, 4, 0)

    def test_2(self):
        test(self, 2, 3, 0)
    
    def test_3(self):
        test(self, 3, 3, 0)

    def test_4(self):
        test(self, 4, 2, 0)

    def test_5(self):
        test(self, 5, 1, 1)

    def test_6(self):
        test(self, 6, 0, 2)

if __name__ == '__main__':
    unittest.main()
