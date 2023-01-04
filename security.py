from argon2 import PasswordHasher
import re

class password:
    def __init__(self):
        self.upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                      'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.specials = ['!', '?', '§', '$', '%', '&', '#', '@']
        self.allowed_mail_chars = self.upper + self.lower + self.numbers + ['@', '-', '.']
        self.forbidden = ['"', "--", "'", ";"]
        self.min_length = 10
        self.max_length = 20

    def check_password(self, pw):
        pw = str(pw)
        u = 0
        l = 0
        n = 0
        s = 0

        for e in pw:
            if e in self.upper:
                u += 1

            if e in self.lower:
                l += 1

            if e in self.numbers:
                n += 1

            if e in self.specials:
                s += 1

            if e in self.forbidden:
                return False

        if u >= 2 and l >= 2 and n >= 2 and s >= 2:
            if len(pw) >= self.min_length and len(pw) <= self.max_length:
                return True
            else:
                return False
        else:
            return False

class argon2:
    def __init__(self):
        self.argon =  PasswordHasher(time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)

    def hash(self, input):
        encoded = str(password).encode()
        return self.argon.hash(encoded)

    def verify(self, hash, input):
        try:
            return self.argon.verify(hash, input)
        except:
            return False

class input_validation:
    def __init__(self):
        self.min_lenght = 13

    def check_input_length(self, user_input):
        if len(user_input) < self.min_lenght:
            return True
        else:
            return False

    def check_input(self, user_input):
        user_input = user_input.upper()

        if re.match('^Y', user_input) or re.match('YES', user_input):
            return 1

        elif re.match('^N', user_input) or re.match('NO', user_input):
            return 0

        else:
            return 2

    def check_json(self,json):
        try:
            json = json.replace('False', 'false').replace(
                'True', 'true').replace('None', 'null')
            return json.loads(json)
        except:
            return False

