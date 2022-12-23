"""
    Module that manages operations on the database
"""
import sqlite3


class Database:
    """Class that handles everything for the module"""

    def __init__(self):
        self.con = None
        self.cur = None

    def open_connection(self):
        """Creates a new connection and a cursor"""
        self.con = sqlite3.connect("Chess_Online_DB.db")
        self.cur = self.con.cursor()

    def close_connection(self):
        """Closes the connection and saves changes"""
        self.con.close()

    def add_player(self, mail, password, username, code):
        """Adds a player to the 'Spieler' table"""
        self.open_connection()
        self.cur.executescript("""INSERT INTO Spieler
                            (mail, passwort, nutzername, aktivierungscode) VALUES
                            ('%s', '%s', '%s', '%s')""" % (mail, password, username, code))
        self.con.commit()
        self.close_connection()

    def add_game(self, player1_id, player2_id, victor_id):
        """Adds a completed game to the 'Spiele' table"""
        self.open_connection()
        self.cur.execute("""INSERT INTO Spiele (spieler1id, spieler2id, siegerid) VALUES
                            ('%s', '%s', '%s')""" % (player1_id, player2_id, victor_id))
        self.con.commit()
        self.close_connection()

    def add_save(self, data_name):
        """Adds a savestate to the 'Speicherstände' table"""
        self.open_connection()
        self.cur.execute(
            """INSERT INTO Speicherstände (name) VALUES ('%s')""" % data_name)
        self.con.commit()
        primary_key = self.cur.lastrowid
        self.close_connection()
        return primary_key

    def remove_save(self, username):
        """Removes the Save state from the user"""

        self.open_connection()

        res = self.cur.execute(
            """SELECT saveid FROM Spieler WHERE id = '%s'""" % self.get_id(username))

        save_id = res.fetchall()[0][0]

        self.change_save_id(self.get_id(username), 0, end_connection=False)

        self.cur.execute(
            """DELETE FROM Speicherstände WHERE id='%s'""" % save_id)
        self.con.commit()
        self.close_connection()

    def add_win(self, player_id):
        """Increases the number of wins by one for a given player"""
        self.open_connection()
        self.cur.execute(
            """UPDATE Spieler SET siege = siege + 1 WHERE id = '%s'""" % player_id)
        self.con.commit()
        self.close_connection()

    def add_loss(self, player_id):
        """Increases the number of losses by one for a given player"""
        self.open_connection()
        self.cur.execute(
            """UPDATE Spieler SET niederlagen = niederlagen + 1 WHERE id = '%s'""" % player_id)
        self.con.commit()
        self.close_connection()

    def add_remis(self, player_id):
        """Increases the number of remis by one for a given player"""
        self.open_connection()
        self.cur.execute(
            """UPDATE Spieler SET remis = remis + 1 WHERE id = '%s'""" % player_id)
        self.con.commit()
        self.close_connection()

    def change_save_id(self, player_id, save_id, end_connection=True):
        """Changes the save_id of a given player to the id of a given savestate"""
        self.open_connection()
        self.cur.execute(
            """UPDATE Spieler SET saveid = '%s' WHERE id = '%s'""" % (save_id, player_id))
        self.con.commit()
        if end_connection:
            self.close_connection()

    def change_elo(self, victor_id, loser_id, elo):
        """Changes the elo of a given player"""
        self.add_elo(victor_id, elo)
        self.remove_elo(loser_id, elo)

    def add_elo(self, player_id, elo):
        """Increase a players elo"""
        self.open_connection()
        self.cur.execute(
            """UPDATE Spieler SET elo = elo + '%s' WHERE id = '%s'""" % (elo, player_id))
        self.con.commit()
        self.close_connection()

    def remove_elo(self, player_id, elo):
        """Decrease a players elo"""
        self.open_connection()
        self.cur.execute(
            """UPDATE Spieler SET elo = elo - '%s' WHERE id = '%s'""" % (elo, player_id))
        self.con.commit()
        self.close_connection()

    def fetch_public_userdata(self, player_id):
        """Returns a players public data"""
        self.open_connection()
        res = self.cur.execute("""SELECT nutzername, siege, niederlagen, remis, elo
                                  FROM Spieler WHERE id = '%s'""" % player_id)
        data = res.fetchall()
        self.close_connection()
        return data

    def fetch_full_userdata(self, player_id):
        """Returns a players full data"""
        self.open_connection()
        res = self.cur.execute(
            """SELECT * FROM Spieler WHERE id = '%s'""" % player_id)
        data = res.fetchall()
        self.close_connection()
        return data

    def fetch_general_data(self, table_filter, database, sql_exec=""):
        """Executes SQL statements for general purpose"""
        self.open_connection()
        res = self.cur.execute("SELECT " + table_filter + " FROM " + database + " " + sql_exec)
        data = res.fetchall()
        self.close_connection()
        return data

    def get_id(self, username):
        """Gets the id from Username"""
        self.open_connection()
        res = self.cur.execute("""SELECT id
                                  FROM Spieler WHERE nutzername = '%s'""" % username)
        data = res.fetchall()
        self.close_connection()

        data = int(data[0][0])

        return data

    def update_general_data(self, table, column, content, sql_exec=""):
        """Executes SQL statements for general update purpose"""
        self.open_connection()
        self.cur.execute("UPDATE " + table + " SET " +
                         column + "=" + content + " " + sql_exec)
        self.con.commit()
        self.close_connection()

    def get_game_save(self, username):
        """returns the json formatted game save"""

        self.open_connection()
        res = self.cur.execute(
            """SELECT saveid FROM Spieler WHERE nutzername = '%s'""" % username)
        save_game = res.fetchall()[0][0]

        res = self.cur.execute(
            """SELECT name FROM Speicherstände WHERE id = '%s'""" % save_game)

        data = res.fetchall()
        self.close_connection()

        try:
            data = data[0][0]
        except IndexError:
            return False

        return data

    def set_locked(self, mail):
        """Updates Blocked in Userdata"""
        self.open_connection()
        self.cur.execute(
            """update Spieler set authversuche = authversuche - 1 WHERE mail = ?""", (mail,))
        self.con.commit()
        self.close_connection()

    def get_locked(self, mail):
        """Gets the id from Username"""
        self.open_connection()
        res = self.cur.execute("""SELECT authversuche
                                  FROM Spieler WHERE mail = ?""", (mail,))
        data = res.fetchall()
        self.close_connection()

        data = int(data[0][0])

        return data

    def set_unlocked(self, mail):
        """Updates Blocked in Userdata"""
        self.open_connection()
        self.cur.execute(
            """update Spieler set authversuche = 3 WHERE mail = ?""", (mail,))
        self.con.commit()
        self.close_connection()
