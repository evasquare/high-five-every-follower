import sqlite3

con = sqlite3.connect("./database/data.db")
cur = con.cursor()
cur.execute(
    '''
    ALTER TABLE followers
    ADD COLUMN post_cid TEXT
    '''
)
