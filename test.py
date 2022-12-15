import hashlib as hl
import controller as c
import view 

def registration(self):
    """Handles the registration of the user"""

    # Get the new email address and password
    res = "bla"
    mail = ""
    password = ""

    while len(res) != 0 or len(password) == 0:

        temp = ["christian.joiko@stud.th-deg.de","P@ssw0rD!'","P@ssw0rD!"]

        mail = temp[0]  # self.view.input("Enter your email address: ")
        password = temp[1]
        password2 = temp[2]

        try:

            if mail.split("@")[1] == "stud.th-deg.de" or mail.split("@")[1] == "th-deg.de":
                valid_th_mail = True
            else:
                valid_th_mail = False

        except IndexError:
            valid_th_mail = False

        if len(mail) == 0 or not valid_th_mail:
            view.View.invalid_input(
                    "Your input was not a valid email address\n")
            continue

        res = ""#c.Controller.db.fetch_general_data(
                #"mail", "Spieler", "WHERE mail='" + mail + "';")

        if len(res) != 0:
            view.View.invalid_input(
                    "This email address is already taken\n")
            continue

        if len(password) == 0:
            view.View.invalid_input(
                    "Your input was not a valid password\n")
            continue

        if not c.Controller.check_password(password):
            continue

        if password != password2:
            continue

        

        #self.db.add_player(mail, password, username, code)

        print("Hallo")

        return None


def hash_password(pw):
    encoded = pw.encode()
    hash = hl.sha3_512(encoded)
    print(hash.hexdigest())


def check_password(pw):
    u = 0
    l = 0
    n = 0
    s = 0
    upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
             'm', 'n', '0', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    specials = ['!', '?', '§', '$', '%', '&', '#']

    for e in pw:
        if e in upper:
            u += 1

        if e in lower:
            l += 1

        if e in numbers:
            n += 1

        if e in specials:
            s += 1

    if u >= 2 and l >= 2 and n >= 2 and s >= 2:
        if len(pw) >= 8:
            print("save")
        else:
            print("unsave")
    else:
        print("unsave")


#check_password("P@ssw0rD!#1")
#check_password("Hallo123")
hash_password("P@ssw0rd!#")
hash_password("P@ssw0rd!'")
#registration(1)
