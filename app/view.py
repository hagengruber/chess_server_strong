"""
    Module for displaying the current state of the game to the user
"""

from pyfiglet import figlet_format
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


class View:
    """Class that handles everything for the module"""

    def __init__(self):
        self.socket = None
        self.model = None
        self.last_board = None
        self.count = 1

    def init_socket(self, socket):
        """init the socket"""
        self.socket = socket

    def clear_console(self):
        """Clear the console of unnecessary stuff"""
        self.socket.sendall("\033[H\033[J".encode())

    def input(self, text=None):
        """gets the input of the user"""
        if text is not None:
            self.print(text)

        return self.socket.recv(1024).decode()

    def print(self, text):
        """sends a text to the user"""
        self.socket.sendall(text.encode())

    def invalid_input(self, user_input):
        """print error message"""
        self.print('Invalid input!')
        self.print(user_input)

    def update_board(self, state=""):
        """Updates the board to show recent movement"""

        self.count += 1
        self.clear_console()

        if state == "":
            state = self.model.board_state

        box_top = ' \u250C' + '\u2500\u2500\u2500\u252C' * 7 + '\u2500\u2500\u2500\u2510'
        box_middle = ' \u251C' + '\u2500\u2500\u2500\u253C' * 7 + '\u2500\u2500\u2500\u2524'
        box_bottom = ' \u2514' + '\u2500\u2500\u2500\u2534' * 7 + '\u2500\u2500\u2500\u2518'

        temp = None

        while temp is None:
            temp = self.model.controller.get_queue_content(
                self.model.controller.games)

        games = temp['games']

        for i in range(len(games)):
            if games[i]['player1'] == self.model.controller.user['username'] \
                    or games[i]['player2'] == self.model.controller.user['username']:
                self.print(games[i]['currently_playing'] +
                           ' is currently playing!\n')

        self.print('   1   2   3   4   5   6   7   8\n')
        self.print(box_top + '\n')
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(8):
            row = letters[i]
            for j in range(8):
                if state[i * 8 + j] is not None:
                    if state[i * 8 + j] != self.last_board[i * 8 + j]:
                        row += '\u2502\x1b[6;30;42m' + ' ' + \
                               state[i * 8 + j].symbol + ' \x1b[0m'
                    else:
                        row += '\u2502' + ' ' + state[i * 8 + j].symbol + ' '
                else:
                    if state[i * 8 + j] != self.last_board[i * 8 + j]:
                        row += '\u2502\x1b[6;30;42m' + '   \x1b[0m'
                    else:
                        row += '\u2502' + '   '

            row += '\u2502'
            self.print(row + '\n')
            if i != 7:
                self.print(box_middle + '\n')
        self.print(box_bottom + '\n')

        self.last_board = self.model.get_copy_board_state()

    def print_menu(self, login, sub_message=None):
        """Display the starting menu and tell 'model' to ask the user what he wants to do"""

        message = figlet_format("Chess Online")
        self.socket.sendall(message.encode())

        message = '\n\n-Enter a move by giving the coordinates of the ' \
                  'starting point and the goal point\n'
        self.socket.sendall(message.encode())
        message = '-During a match you can either enter a legal Move or ' \
                  '"--Help" for further commands\n'
        self.socket.sendall(message.encode())

        if login:
            message = '(1)PlayerVsPlayer   (2)PlayerVsBot   (3)LoadGame   ' \
                      '(4)Logout   (5)Exit\n'
        else:
            message = '(1)Login   (2)Registration   (3)Exit\n'

        self.socket.sendall(message.encode())

        if sub_message is not None:

            # Error message in red
            colorama_init()
            sub_message = f"{Fore.RED}" + sub_message + f"{Style.RESET_ALL}"

            self.socket.sendall(sub_message.encode())

        self.model.controller.get_menu_choice(self.get_menu_choice())

    def get_after_game_choice(self):
        """get the user input after the game"""

        self.print('\nDo you want to play another round? (Y/N): ')
        return input()

    def get_menu_choice(self):
        """get the users choice"""

        while True:

            self.print('\nPlease enter the number that corresponds to your desired menu: ')

            try:
                user_input = int(self.input())

            except ValueError:
                self.clear_console()
                self.print_menu(self.model.controller.is_logged_in,
                                sub_message="\nPlease enter an Integer\n")
                continue

            if user_input < 0 or user_input > 6:
                self.clear_console()
                self.print_menu(self.model.controller.is_logged_in,
                                sub_message="\nPlease enter a valid Number\n")

            else:
                return user_input

    def get_symbol_preference(self):
        """get the users preference"""

        self.print(
            '\nDo you want to use symbols? If not, letters will be used instead. (Y/N): ')
        return self.input()

    def get_movement_choice(self):
        """get the move of the user"""

        self.print('Please enter your desired Move: ')
        return self.input()

    def show_stats(self, data):
        """prints the stats  of the opponent"""

        self.print('Stats of the opponent: ' + str(data) + '\n')

    def get_help(self):
        """print help for user"""

        self.print("legal move or\n")
        self.print("--stats - show opponent Stats\n")
        self.print("--save - Save and Quit Game\n")
        self.print("--remis - offer Remis\n")
        self.print("--surrender - Surrender\n")

    def accept_remis(self):
        """asks if the user wants to accept the draw"""

        self.print('Do you want to accept Draw? ')
        return self.input()

    def get_activation_code(self):
        """get the activation code from the user"""

        self.print("\nEnter your activation Code: ")
        return self.input()

    def get_credentials(self, i):
        """get the credentials of the user"""

        temp = []
        self.print('\nE-mail address:')
        temp.append(self.input())
        self.print('\nPassword (2x "A-Z", 2x "a-z", 2x "0-9", '
                   '2x ("!" "?" "$" "&" "%" "#" "@")) min. 10, max. 20 character: ')
        temp.append(self.input())

        if i == 0:
            self.print('Repeat password:')
            temp.append(self.input())
        return temp
