import os
from mysql import connector
from control.Musician import Musician


class DatabaseConnection:
    def __init__(self) -> None:
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.database = "musicbot"
        self.password = "hurensohn"
        if self.is_windows():
            self.password = ""
        self.connection = None
        self.check_connection()

    def is_windows(self):
        print("OS: " + os.name)
        if os.name == 'nt':
            return True
        return False

    def is_connected(self) -> bool:
        if self.connection.is_connected():
            return True
        return False

    def check_connection(self):
        if self.connection is None or not self.is_connected():
            self.connection = connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

    def get_token(self, host_type: str) -> str or None:
        self.check_connection()
        sql_statement = """SELECT token FROM host WHERE name='%s'"""
        cursor = self.connection.cursor()
        cursor.execute(sql_statement % host_type)
        for row in cursor.fetchall():
            return row[0]
        return None

    def get_youtube_api_key(self, host_type: str) -> str or None:
        self.check_connection()
        sql_statement = """SELECT youtube_key FROM host WHERE name='%s'"""
        cursor = self.connection.cursor()
        cursor.execute(sql_statement % host_type)
        for row in cursor.fetchall():
            return row[0]
        return None

    def get_spotify_api_secrets(self, host_type: str) -> tuple or None:
        self.check_connection()
        sql_statement = """SELECT spotify_id, spotify_secret FROM host WHERE name='%s'"""
        cursor = self.connection.cursor()
        cursor.execute(sql_statement % host_type)
        for row in cursor.fetchall():
            return row[0], row[1]
        return None

    def get_responses(self) -> list:
        self.check_connection()
        sql_statement = """SELECT * FROM responses"""
        cursor = self.connection.cursor()
        cursor.execute(sql_statement)
        responses = []
        for row in cursor.fetchall():
            columns = []
            for column in row:
                columns.append(column)
            responses.append(columns)
        return responses

    def create_musician(self, server_id, server_name, nickname, prefix, bound_channel, language_id) -> None:
        self.check_connection()
        sql_statement = """INSERT INTO guilds (id, server_id, server_name, nickname, prefix, bound_channel, language_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor = self.connection.cursor()
        cursor.execute(sql_statement, [0, server_id, server_name, nickname, prefix, bound_channel, language_id])
        self.connection.commit()
        print("Inserted ", cursor.rowcount, " rows.")

    def get_musicians(self, client_name: str) -> list:
        musicians = []
        self.check_connection()
        sql_statement = """SELECT *  FROM guilds"""
        cursor = self.connection.cursor()
        cursor.execute(sql_statement)
        for row in cursor.fetchall():
            musicians.append(
                Musician(row[1], row[2], client_name, nickname=row[3], prefix=row[4], bind=row[5], language_id=row[6])
            )
        return musicians

    def save_musicians(self, musicians: list) -> None:
        # Creating mysql sql_statement
        sql_statement = """INSERT INTO guilds (id, server_id, server_name, nickname, prefix, bound_channel, language_id) 
        VALUES 
        """
        for i, musician in enumerate(musicians):
            if i == len(musicians) - 1:
                sql_statement += "('%s', '%s', '%s', '%s', '%s', '%s', '%s') " % (0, musician.guild_id, musician.guild_name, musician.nickname, musician.prefix, musician.bound_channel, musician.language_id)
            else:
                sql_statement += "('%s', '%s', '%s', '%s', '%s', '%s', '%s'), " % (0, musician.guild_id, musician.guild_name, musician.nickname, musician.prefix, musician.bound_channel, musician.language_id)
        sql_statement += """ON DUPLICATE KEY UPDATE
            server_name=VALUES(server_name),
            nickname=VALUES(nickname),
            prefix=VALUES(prefix),
            bound_channel=VALUES(bound_channel),
            language_id=VALUES(language_id);
        """
        # Send data
        cursor = self.connection.cursor()
        cursor.execute(sql_statement)
        self.connection.commit()
        print("Updated/Inserted ", cursor.rowcount, " rows.")
