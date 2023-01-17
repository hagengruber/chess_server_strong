    def get_menu_choice(self, user_input):
        """Gets input from user and processes the input"""

        if int(user_input) and 0 < user_input < 8:

            # If User is logged in, a different Menu will be displayed
            # User Input must be changed
            if self.is_logged_in:
                if user_input == '4':
                    user_input = '6'
                elif user_input == '5':
                    user_input = '7'
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
                    self.view.print_menu(self.is_logged_in,
                                         sub_message="\nLogin is required to play games with other players\n\n")
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
                self.model.ai = True
                self.user_ai = AI(self.model, self.view, "Black", "White", self)
                self.model.show_symbols = self.get_symbol_preference(self.view.get_symbol_preference())

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
                        self.is_logged_in, sub_message="\nCode was sent to your email address\n\n")
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
                self.view.print_menu(self.is_logged_in, sub_message="\nPlease enter a valid Number\n")

        else:
            self.view.clear_console()
            self.view.print_menu(self.is_logged_in, sub_message="\nPlease enter a valid Number\n")