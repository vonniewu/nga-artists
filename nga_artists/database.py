import sqlite3
import sys


TABLE_NAME = "Artist"
CREATE_TABLE_SQL = f"CREATE TABLE {TABLE_NAME}(" \
                       "id int, " \
                       "FirstName varchar(100), " \
                       "LastName varchar(100), " \
                       "Biography varchar(250), " \
                       "Link varchar(250))"
INSERT_SQL = f"INSERT INTO {TABLE_NAME} VALUES (?,?,?,?,?);"
SELECT_SQL = f"SELECT * from {TABLE_NAME}"
DELETE_SQL = f"DROP TABLE IF EXISTS {TABLE_NAME}"


class ArtistDB:

    def __init__(self, database):
        self.database = database
        self.connection = None
        self.cursor = None

        self._initialize()

    def _initialize(self):
        self.connect()
        self._create_table(CREATE_TABLE_SQL)

    def _create_table(self, create_table_sql):
        with self.connection:
            while True:
                try:
                    self.cursor.execute(create_table_sql)
                except sqlite3.OperationalError as e:
                    self.cursor.execute(DELETE_SQL)
                    continue
                break

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.database)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

    def add_entry(self, artist):
        self.cursor.execute(INSERT_SQL,
                            (artist.artist_id, artist.first_name, artist.last_name, artist.biography, artist.link))

    def print_entries(self):
        self.cursor.execute(SELECT_SQL)
        query_results = self.cursor.fetchall()

        for result in query_results:
            print(result)

    def close(self):
        self.connection.commit()
        self.connection.close()
