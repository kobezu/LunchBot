from user import User, Language, users
import random

#class for generating lottery result 
class LotteryResult:
    def __init__(self) -> None:
        #list for groups
        self.groups: list[list[User]] = []
        #list for users not in group
        self.not_in_group: list[User] = []
        self.generate_groups()

    def generate_groups(self):
        #users filtered by language
        eng = [user for user in users.values() if (user.lunch_language == Language.ENG) & user.joined]
        fin = [user for user in users.values() if (user.lunch_language == Language.FIN) & user.joined]
        both = [user for user in users.values() if (user.lunch_language == Language.BOTH) & user.joined]

        def form_group(group: "list[User]"):
            #add group to groups
            self.groups.append(group.copy())
            #remove users from pools
            for user in group:
                language = user.lunch_language
                if language == Language.BOTH:
                    both.remove(user)
                elif language == Language.FIN:
                    fin.remove(user)
                else:
                    eng.remove(user)
        #form eng groups:
        if len(eng) > 0:
            #make pool
            pool = eng + both
            #shuffle pools
            random.shuffle(pool)
            random.shuffle(eng)
            #form groups of two while pools are big enough
            while len(eng) > 0 and len(pool) > 3:
                #choose one user from eng pool and remove it from general pool
                choice = eng[0]
                pool.remove(choice)
                #form group by choosing remaining users from general pool
                form_group([choice, pool.pop()])
            #form group of three if there is still 3 left in pool and they are all eng
            if len(eng) == 3:
                form_group(eng)
            #if there is two eng, form group of them
            elif len(eng) == 2:
                form_group(eng)
            #if one eng, try to form group from general pool 
            elif len(eng) == 1:
                #if at least 2 users in pool, form group
                if len(pool) > 1:
                    choice = eng[0]
                    pool.remove(choice)
                    form_group([choice, pool.pop()])
                #else not enough users to form group 
                else: 
                    self.not_in_group.append(eng.pop())
        #form fin groups
        pool = fin + both
        if len(pool) > 1:
            random.shuffle(pool)
            while len(pool) > 3:
                form_group([pool.pop(), pool.pop()])
            form_group(pool)
        else:
            if len(fin) == 1:
                self.not_in_group.append(fin.pop())
            elif len(both) == 1:
                self.not_in_group.append(both.pop())