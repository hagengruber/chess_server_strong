"""
    Module for getting and processing input from the user
"""

from queue import Empty
import sys
import re
import database
from mail import Mail
from pieces import Pawn, Rook, Horse, Bishop, Queen, King
import security
from algorithm import AI


class Controller:
    """Class that handles everything for the module"""

    def __init__(self, view, socket, connect, games, num_of_thread, lock):
        self.socket = socket
        self.connect = connect
        self.model = None
        self.view = view
        # self.ai_player = None
        self.user_ai = None
        self.load_game = False
        self.games = games
        self.user = {'username': None, 'num_of_thread': num_of_thread,
                     'game_queue': None, 'color': '', 'enemy': ''}
        self.argon = security.ArgonHash()
        self.inpval = security.InputValidation()
        self.password = security.Password()

        self.lock = lock
        self.database_connection = database.Database(lock, self)
        self.is_logged_in = False

    def get_menu_choice(self, user_input):
        """Gets input from user and processes the input"""

        if user_input and 0 < user_input < 8:

            # If User is logged in, a different Menu will be displayed
            # User Input must be changed
            if self.is_logged_in:
                if user_input == 4:
                    user_input = 6
                elif user_input == 5:
                    user_input = 7
            else:
                if user_input == 1:
                    user_input = 4
                elif user_input == 2:
                    user_input = 5
                elif user_input == 3:
                    user_input = 7
                else:
                    user_input = -1

            if user_input == 1:
                # User vs User
                if not self.is_logged_in:
                    self.view.clear_console()
                    self.view.print_menu(self.is_logged_in, sub_message="\nLogin"
                                        "is required to play games with other players\n\n")
                    self.get_menu_choice(self.view.get_menu_choice())
                else:
                    self.join_lobby()
                    self.coop()

                    # After the Game
                    self.view.clear_console()
                    self.view.print_menu(self.is_logged_in)
                    self.get_menu_choice(self.view.get_menu_choice())

            elif user_input == 2:
                # User vs AI
                self.model.ai_player = True
                self.user_ai = AI("Black", "White", self)
                self.model.show_symbols = self.get_symbol_preference(
                    self.view.get_symbol_preference())

                self.start_game()

            elif user_input == 3:
                # load game
                cont = self.load()
                if cont:
                    self.start_game()

            elif user_input == 4:
                # login
                message = self.login()
                self.view.clear_console()
                self.view.print_menu(self.is_logged_in, sub_message="\n" + message + "\n")
                self.get_menu_choice(self.view.get_menu_choice())

            elif user_input == 5:
                # registration
                erg = self.registration()
                self.view.clear_console()

                if erg is None:
                    self.view.print_menu(
                        self.is_logged_in, sub_message="\nCode was sent to your email address\n")
                else:
                    # If something went wrong
                    self.view.print_menu(self.is_logged_in, sub_message="\n" + erg + "\n\n")

                self.get_menu_choice(self.view.get_menu_choice())

            elif user_input == 6:
                # logout
                message = self.logout()
                self.view.clear_console()
                self.view.print_menu(self.is_logged_in, sub_message="\n" + message + "\n\n")
                self.get_menu_choice(self.view.get_menu_choice())

            elif user_input == 7:
                # exit
                self.view.print("Thanks for playing")
                sys.exit()

            else:
                self.view.clear_console()
                self.view.print_menu(self.is_logged_in, sub_message=
                "\nPlease enter a valid Number\n")

        else:
            self.view.clear_console()
            self.view.print_menu(self.is_logged_in, sub_message=
            "\nPlease enter a valid Number\n")

    def registration(self):
        """Handles the registration of the user"""

        # Get the new email address and password
        res = "bla"
        mail = ""
        password = ""

        while len(res) != 0 or len(password) == 0:

            temp = self.view.get_credentials(0)

            mail = temp[0]
            password = temp[1]
            password2 = temp[2]

            try:
                valid_th_mail = mail.split("@")[1] == "stud.th-deg.de" \
                                or mail.split("@")[1] == "th-deg.de"

            except IndexError:
                valid_th_mail = False

            if len(mail) == 0 or not valid_th_mail:
                self.view.invalid_input(
                    "Your input was not a valid email address\n")
                res = "bla"
                continue

            res = self.database_connection.fetch_general_data(
                "mail", "Spieler", "WHERE mail='" + mail + "';")

            if len(res) != 0:
                self.view.invalid_input(
                    "This email address is already taken\n")
                continue

            if len(password) == 0 or len(password2) == 0:
                self.view.invalid_input(
                    "Please insert a valid Password\n")
                continue

            if not self.password.check_password(password):
                res = "bla"
                continue

            if password != password2:
                res = "bla"
                self.view.invalid_input("Your Passwords doesnt Match each other\n")

        username = mail.split(".")[0][0] + "." + mail.split(".")[1].split("@")[0]

        mail_client = Mail()

        code = Mail.create_code()

        erg = mail_client.send_mail(mail, code)

        if erg is not None:
            self.view.print(erg)
            return erg

        password =self.argon.hash(password)

        code = self.argon.hash(code)

        self.database_connection.add_player(mail, password, username, code)

        return None

    def login(self):
        """Handles the login of the user"""

        if self.is_logged_in:
            return "You are already logged in as " + str(self.user['username'])

        # Get Credentials from User
        temp = self.view.get_credentials(1)
        mail = temp[0]
        password = temp[1]

        for character in mail:
            if character not in self.password.allowed_mail_chars \
                    or character in self.password.forbidden:
                return "Wrong Credentials. Please Try again"

        res = self.database_connection.fetch_general_data(
            "*", "Spieler", "WHERE mail='" + mail + "';")

        # If the Email Address doesn't exist
        if len(res) == 0:
            self.is_logged_in = False
            return "Wrong Credentials. Please Try again"

        # If the user is locked
        if self.database_connection.get_locked(mail) == 0:
            return "Your account has been locked due to too many failed attempts.\n" \
                   "Please contact chess_dev-team@hagengruber.dev for an unlock request"

        # Check if the Password is not correct
        if not self.argon.verify(res[0][2],password):
            return "Wrong Credentials. Please Try again"

        # If the user must enter an activation Code
        if res[0][9] is not None:

            # Get Code from User
            code = self.view.get_activation_code()

            # If Code in Database (hash) is equal to the Hash from the Code the User inserted
            if self.argon.verify(res[0][9],code): #res[0][9] == self.hash_password(code):
                # Set 'aktivierungscode' to null
                self.database_connection.update_general_data(
                    'Spieler', '"aktivierungscode"', 'NULL', 'WHERE mail="' + mail + '";')
            else:
                self.database_connection.set_locked(mail)
                return "Wrong activation Code"

        self.user['username'] = res[0][3]
        self.is_logged_in = True

        self.database_connection.set_unlocked(mail)
        return "Login successful"

    def join_lobby(self):
        """User joins the lobby and waits for an Enemy"""

        self.view.print("Join Lobby...\n")

        self.lock.acquire()

        temp = None

        while temp is None:
            temp = self.get_queue_content(self.games, safe_mode=False)

        temp['lobby'].append(self.user)

        self.write_queue_content(self.games, temp, safe_mode=False)

        self.release_lock()

        self.view.print("Looking for Enemies...")

        while True:
            # Waits for an Enemy
            self.lock.acquire()

            temp = self.get_queue_content(self.games, safe_mode=False)
            join = False

            if temp is None:
                self.release_lock()
                continue

            games = temp['games']

            for i in games:
                if i['player1'] == self.user['username'] or i['player2'] == self.user['username']:
                    # Enemy found
                    join = True
                    break

            self.release_lock()

            if join:
                self.view.print("Join successful\n")
                break

    def get_room(self, temp=None):
        """Returns the content of the game queue and the index of the current Game room"""

        if temp is None:

            temp = None

            while temp is None:
                temp = self.get_queue_content(self.games)

        games = temp['games']

        for i in range(len(games)):
            if games[i]['player1'] == self.user['username'] \
                    or games[i]['player2'] == self.user['username']:
                return games, i

        return None

    def start_game(self):
        """Starts the Game and goes into the Game Loop"""

        self.model.init_board(self.load_game)

        self.model.view.update_board()
        self.get_movement_choice(self.view.get_movement_choice())

        self.model.currently_playing = 'Black'

        if self.model.ai_player:
            self.user_ai.move()
            self.model.currently_playing = 'White'
            while self.model.check_for_king():
                if self.model.currently_playing == 'Black':
                    self.user_ai.move()
                else:
                    self.get_movement_choice(self.view.get_movement_choice())

                if self.model.currently_playing == 'White':
                    self.model.currently_playing = 'Black'
                else:
                    self.model.currently_playing = 'White'

        self.view.print(self.model.currently_playing +
                        ' lost because his king died!')

        self.get_after_game_choice(self.view.get_after_game_choice())

    def get_symbol_preference(self, user_input):
        """Asks the user whether he wants to use symbols(True) or letters(False)"""

        if self.inpval.check_input_length(user_input):

            if self.inpval.check_input(user_input) == 1:
                return True

            if self.inpval.check_input(user_input) == 0:
                return False

            return self.get_symbol_preference(self.view.get_symbol_preference())

        return self.get_symbol_preference(self.view.get_symbol_preference())

    def get_movement_choice(self, move, update=True):
        """Gets input from user during a game and processes the input"""

        move = move.upper()

        if self.inpval.check_input_length(move):

            if re.match('^--', move):
                if move[2:] == "STATS":
                    pers = self.database_connection.fetch_public_userdata(
                        14)  # eid where nutzername = enemy

                    self.view.show_stats(pers)
                    self.get_movement_choice(self.view.get_movement_choice())

                if move[2:] == "SAVE":
                    if self.model.ai_player is None:
                        self.view.print("Illegal input")
                        return None

                    self.save()
                    self.view.clear_console()
                    self.view.print_menu(True, "\nSaved current Game\n\n")
                    return self.get_movement_choice(self.view.get_menu_choice())

                if move[2:] == "SURRENDER":
                    self.model.view.clear_console()
                    self.model.remove_king(self.user['color'])
                    self.finish_game()

                elif move[2:] == "DRAW":
                    draw = self.model.ask_draw()
                    if not draw:
                        self.view.print("Draw was rejected\n")
                        return None

                    self.database_connection.add_remis(
                        self.database_connection.get_id(self.user['username']))
                    self.database_connection.add_remis(
                        self.database_connection.get_id(self.user['enemy']))
                    self.database_connection.add_game(
                        self.database_connection.get_id(
                            self.user['username']),
                        self.database_connection.get_id(self.user['enemy']), None)

                    self.remove_game()

                    self.view.clear_console()
                    self.view.print_menu(True)
                    self.get_menu_choice(self.view.get_menu_choice())
                    sys.exit()

                elif move[2:] == "HELP":
                    self.view.get_help()

                else:
                    self.view.invalid_input('Please try again!')
                    return self.get_movement_choice(self.view.get_movement_choice())

            elif re.match('^[A-H][0-8][A-H][0-8]', move):

                start_pos = move[:2]
                goal_pos = move[-2:]

                return self.model.move_piece(
                    self.model.correlation[start_pos], self.model.correlation[goal_pos],
                    move=move, update=update)
            else:
                self.view.invalid_input('Please try again!')
                return self.get_movement_choice(self.view.get_movement_choice())

        else:
            self.view.invalid_input("Excuse me, Something went Wrong. Please")
            return self.get_movement_choice(self.view.get_movement_choice())

    def release_lock(self):
        """Releases the Mutex"""

        try:
            self.lock.release()
        except ValueError:
            pass

    def get_queue_content(self, queue, safe_mode=True):
        """Returns the content of the Queue"""

        if safe_mode:
            self.lock.acquire()

        try:

            temp = queue.get_nowait()
            queue.put(temp)

            if safe_mode:
                self.release_lock()

            return temp

        except Empty:
            if safe_mode:
                self.release_lock()
            return None

    def write_queue_content(self, queue, content, override=True, safe_mode=True):
        """Writes the content in the Queue"""

        if safe_mode:
            self.lock.acquire()

        if override:
            while True:
                # Removes the content in the Queue
                try:
                    queue.get_nowait()
                except Empty:
                    break

            old_content = []

        else:
            old_content = []
            while True:
                try:
                    old_content.append(queue.get_nowait())
                except Empty:
                    break

        old_content.append(content)

        for i in old_content:
            queue.put_nowait(i)

        if safe_mode:
            self.release_lock()

    def remove_game(self):
        """removes the game room from the game queue"""

        self.lock.acquire()

        temp = None
        while temp is None:
            temp = self.get_queue_content(self.games, safe_mode=False)

        games = temp['games']

        for i in games:
            if i['player1'] == self.user['username'] or i['player2'] == self.user['username']:
                # if the correct game room was found set the self.user variables
                games.remove(i)

                temp['games'] = games

                self.write_queue_content(self.games, temp, safe_mode=False)

                self.lock.release()

                break

    def coop(self):
        """handles the game between two player"""

        self.model.init_board(self.load_game)
        temp = None

        while temp is None:
            temp = self.get_queue_content(self.games)

        games = temp['games']

        for i in games:
            if i['player1'] == self.user['username'] or i['player2'] == self.user['username']:
                # if the correct game room was found set the self.user variables
                if i['White'] == self.user['username']:
                    self.user['color'] = 'White'
                else:
                    self.user['color'] = 'Black'

                # set the enemy in self.user
                if i['player1'] == self.user['username']:
                    self.user['enemy'] = i['player2']
                else:
                    self.user['enemy'] = i['player1']

        self.model.currently_playing = 'White'

        # if the variable print_wait is True, print (below) "The other player is thinking"
        print_wait = True

        while self.model.check_for_king('White') and self.model.check_for_king('Black'):

            # Loop until the game is over
            temp = None

            while temp is None:
                temp = self.get_queue_content(self.games)

            games = temp['games']

            game_alive = False

            for i in range(len(games)):
                if games[i]['player1'] == self.user['username'] \
                        or games[i]['player2'] == self.user['username']:
                    game_alive = True

            if not game_alive:
                break

            self.release_lock()

            for i in range(len(games)):
                if games[i]['player1'] == self.user['username'] \
                        or games[i]['player2'] == self.user['username']:
                    # if the correct game room was found
                    if games[i]['currently_playing'] == self.user['username']:
                        # if the user can move a piece

                        print_wait = True

                        if games[i]['last_move'] is not None:
                            # if the other payer has moved a piece

                            if games[i]['White'] == self.user['username']:
                                self.model.currently_playing = 'Black'
                            else:
                                self.model.currently_playing = 'White'

                            # move the piece of the Enemy
                            self.get_movement_choice(
                                move=games[i]['last_move'], update=False)

                        # Check if both kings are still alive
                        if not self.model.check_for_king('White') \
                                or not self.model.check_for_king('Black'):
                            self.view.clear_console()
                            self.view.print_menu(True)
                            self.get_menu_choice(self.view.get_menu_choice())
                            sys.exit()

                        self.model.currently_playing = self.user['color']

                        self.view.update_board()

                        last_move = None

                        while last_move is None:
                            # get the current move of the player and move the piece
                            last_move = self.get_movement_choice(
                                self.view.get_movement_choice())

                        self.lock.acquire()

                        new_temp = None
                        while new_temp is None:
                            new_temp = self.get_queue_content(
                                self.games, safe_mode=False)

                        games[i]['last_move'] = last_move
                        games[i]['currently_playing'] = self.user['enemy']

                        new_temp['games'][i] = games[i]

                        # update the queue with the game room
                        # since not all write operations does actually write, loop until the
                        # queue is successfully up-to-date
                        req = False
                        while not req:

                            check_content = None
                            while check_content is None:
                                check_content = self.get_queue_content(
                                    self.games, safe_mode=False)

                            try:

                                if check_content['games'][i]['currently_playing'] \
                                        == self.user['enemy']:
                                    # if the write operation was successful
                                    req = True
                                else:
                                    # if the write operation failed
                                    self.write_queue_content(
                                        self.games, new_temp, safe_mode=False)

                            except IndexError:
                                self.write_queue_content(
                                    self.games, new_temp, safe_mode=False)

                        check_content = None
                        while check_content is None:
                            check_content = self.get_queue_content(
                                self.games, safe_mode=False)

                        self.release_lock()

                    else:
                        if print_wait:
                            self.view.update_board()
                            self.view.print("The other Player is thinking...")
                            print_wait = False

                        draw = self.model.check_for_draw()

                        if not draw:
                            self.release_lock()
                        else:
                            self.view.clear_console()
                            self.view.print_menu(True)
                            self.get_menu_choice(self.view.get_menu_choice())
                            sys.exit()

                    break

        self.release_lock()
        self.finish_game()

    def finish_game(self):
        """saves stats to both users"""

        temp = None

        while temp is None:
            temp = self.get_queue_content(self.games)

        games = temp['games']

        for i in range(len(games)):
            if games[i]['player1'] == self.user['username'] \
                    or games[i]['player2'] == self.user['username']:
                # if the correct game room was found
                if games[i]['player1'] == self.user['username']:

                    if self.model.check_for_king('White'):
                        loser = games[i]['Black']
                        winner = games[i]['White']
                    else:
                        loser = games[i]['White']
                        winner = games[i]['Black']

                    self.database_connection.add_win(self.database_connection.get_id(winner))
                    self.database_connection.add_loss(self.database_connection.get_id(loser))

                    self.database_connection.add_game(
                        self.database_connection.get_id(self.user['username']),
                        self.database_connection.get_id(self.user['enemy']),
                        self.database_connection.get_id(winner))

                    self.model.recalculate_elo(
                        self.database_connection.get_id(winner),
                        self.database_connection.get_id(loser))

                    self.remove_game()

                    self.view.clear_console()
                    self.view.print_menu(True)
                    self.get_menu_choice(self.view.get_menu_choice())
                    sys.exit()

                else:

                    self.view.clear_console()
                    self.view.print_menu(True)
                    self.get_menu_choice(self.view.get_menu_choice())
                    sys.exit()

    def save(self):
        """Saves the current state to a JSON-File"""

        game_save = self.database_connection.get_game_save(self.user['username'])

        if game_save is not False:
            self.database_connection.remove_save(self.user['username'])

        game_save = {"currently_playing": str(self.model.currently_playing),
                     "show_symbols": self.model.show_symbols,
                     "board_state": {}}

        json_dict = {}
        for i in range(64):
            if self.model.board_state[i] is not None:
                lol = self.model.board_state[i].__doc__.split(" ")
                json_dict.update({str(i): {"piece": lol[2],
                                           "colour": str(self.model.board_state[i].colour),
                                           "moved": self.model.board_state[i].moved,
                                           "position": self.model.board_state[i].position}})
            else:
                json_dict.update({str(i): {"piece": None,
                                           "symbol": None,
                                           "colour": None,
                                           "moved": None,
                                           "position": None}})

        game_save["board_state"].update(json_dict)

        game_save = str(game_save).replace("'", '"')

        save_id = self.database_connection.add_save(game_save)
        self.database_connection.change_save_id(
            self.database_connection.get_id(self.user['username']), save_id)

    def load(self):
        """Loads a savestate"""

        game_save = self.database_connection.get_game_save(self.user['username'])

        if not game_save:
            self.view.clear_console()
            self.view.print_menu(True, "\nNo saved Game found\n\n")
            return False

        game_save = self.inpval.check_json(game_save)

        self.model.currently_playing = game_save['currently_playing']
        self.model.show_symbols = game_save['show_symbols']
        self.load_game = True
        self.user_ai = AI("Black", "White", self)

        self.model.ai_player = True

        for i in range(64):
            # Moved wird nicht übernommen
            if game_save['board_state'][str(i)]['piece'] == 'None':
                self.model.board_state[i] = None

            else:
                if game_save['board_state'][str(i)]['piece'] == 'Rooks':
                    self.model.board_state[i] = Rook(game_save['board_state'][str(i)]['colour'],
                                                     i, self.model, ['moved'])
                if game_save['board_state'][str(i)]['piece'] == 'Horses':
                    self.model.board_state[i] = Horse(game_save['board_state'][str(i)]['colour'],
                                                      i, self.model, ['moved'])
                if game_save['board_state'][str(i)]['piece'] == 'Bishops':
                    self.model.board_state[i] = Bishop(game_save['board_state'][str(i)]['colour'],
                                                       i, self.model, ['moved'])
                if game_save['board_state'][str(i)]['piece'] == 'Queens':
                    self.model.board_state[i] = Queen(game_save['board_state'][str(i)]['colour'],
                                                      i, self.model, ['moved'])
                if game_save['board_state'][str(i)]['piece'] == 'Kings':
                    self.model.board_state[i] = King(game_save['board_state'][str(i)]['colour'],
                                                     i, self.model, ['moved'])
                if game_save['board_state'][str(i)]['piece'] == 'Pawns':
                    self.model.board_state[i] = Pawn(game_save['board_state'][str(i)]['colour'],
                                                     i, self.model, ['moved'])

        self.view.last_board = self.model.get_copy_board_state()
        return True

    def get_after_game_choice(self, user_input):
        """Asks the player if he wants to play another game"""

        if self.inpval.check_input(user_input) == 1:
            self.view.clear_console()
            self.start_game()
        elif self.inpval.check_input(user_input) == 0:
            self.view.clear_console()
            self.view.print_menu(self.is_logged_in)
        else:
            self.get_after_game_choice(self.view.get_after_game_choice())

    def logout(self):
        """Handles the logout of the user"""

        if not self.is_logged_in:
            return "You are already logged out"

        self.user['username'] = None
        self.is_logged_in = False
        return "Logout successful"
