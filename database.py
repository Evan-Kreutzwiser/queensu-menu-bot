"""
Provides an interface for storing which channel
to post the menu in for each server using the bot
"""
import sqlite3


def connect_db() -> sqlite3.dbapi2:
    """Get a connection object representing the database"""
    return sqlite3.connect("database/database.sqlite")


def init_db():
    """Ensure the database contains the table for the channel IDs"""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Channels (Guild INTEGER PRIMARY KEY, Channel INTEGER);")
    cursor.close()
    db.commit()


def set_menu_channel(guild_id: int, channel_id: int):
    """
    Persistently store which channel in the guild the daily
    menu should be posted to.

    If a channel has already been set for the guild it will
    be overwritten.

    :param guild_id: The server containing the channel
    :param channel_id: The channel to receive daily menus in
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT OR REPLACE INTO Channels (Guild, Channel) VALUES(?, ?);",
                   (guild_id, channel_id))
    cursor.close()
    db.commit()


def forget_menu_channel(guild_id: int):
    """
    Stop receiving daily menus in the channel

    :param guild_id:
    :return:
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Channels WHERE Guild = (?)", (guild_id, ))
    cursor.close()
    db.commit()


def get_menu_channels() -> list:
    """Returns a list of every channel registered to receive daily menus"""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT Channel FROM Channels")  # Get all the registered channel IDs
    channel_ids = cursor.fetchall()
    cursor.close()
    db.commit()

    # cursor.fetchall() provides a list of single element tuples
    # Unpack those tuples into a list of integers
    channel_ids = [id_tuple[0] for id_tuple in channel_ids]
    return channel_ids
