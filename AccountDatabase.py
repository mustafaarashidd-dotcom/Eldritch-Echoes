import sqlite3

conn = sqlite3.connect("EldritchEchoesAccounts.db")  # Set up connection to database file

c = conn.cursor()  # Create cursor to execute SQL statements

#c.execute("""CREATE TABLE AccountInfo (
#            username text PRIMARY KEY,
#            password text,
#            checkpoint integer,
#            HPLost integer,
#            HP integer,
#            AT integer,
#            DF integer,
#            SPEED integer,
#            EXP integer,
#            damage integer,
#            gold integer,
#            maxHP integer,
#            b1_looted boolean,
#            b2_looted boolean,
#            b3_looted boolean,
#            b4_looted boolean,
#            b5_looted boolean,
#            b6_looted boolean,
#            c1_looted boolean,
#            c2_looted boolean,
#            c3_looted boolean,
#            c4_looted boolean,
#            c5_looted boolean,
#            c6_looted boolean,
#            c7_looted boolean,
#            m1_complete boolean,
#            m2_complete boolean,
#            m3_complete boolean,
#            m4_complete boolean,
#            o1_defeated boolean,
#            o2_defeated boolean,
#            o3_defeated boolean,
#            o4_defeated boolean,
#            o5_defeated boolean,
#            o1_killed boolean,
#            o2_killed boolean,
#            o3_killed boolean,
#            o4_killed boolean,
#            o5_killed boolean,
#            o1_spared boolean,
#            o2_spared boolean,
#            o3_spared boolean,
#            o4_spared boolean,
#            o5_spared boolean
#            )""")

#c.execute("DROP TABLE AccountInfo")  # if u need to delete table and remake it again

conn.commit()  # must commit after doing anything
conn.close()  # Close SQL statements

def check_for_accounts():
    conn = sqlite3.connect("EldritchEchoesAccounts.db")
    c = conn.cursor()

    if c.execute("SELECT * FROM AccountInfo WHERE o5_defeated = 1"):
        results = c.fetchall()
    else:
        results = None

    conn.commit()
    c.close()

    return results

def addAccount(username, password):  # Create function to add accounts and set up database variables within there
    conn = sqlite3.connect("EldritchEchoesAccounts.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO AccountInfo VALUES (?, ?, 1, 0, 50, 10, 0, 5, 0, 0, 0, 50, False, False, False, False,"
              "False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,"
              "False, False, False, False, False, False, False, False, False, False, False, False, False)", (username, password))  # Add values for new record in table

    conn.commit()
    conn.close()

def check_player_pos(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute('SELECT * FROM AccountInfo')
    results = c.fetchall()

    for index, account in enumerate(results):
        username = account[0]
        if username == username_entered:
            checkpoint = account[2]

            if checkpoint == 1:
                pos = 'island1'
                return pos
            elif checkpoint == 2:
                pos = 'island2'
                return pos
            elif checkpoint == 3:
                pos = 'island3'
                return pos
            elif checkpoint == 4:
                pos = 'island4'
                return pos
            else:
                pos = 'unknown'
                return pos

    conn.commit()
    conn.close()

def change_checkpoint(username_entered, checkpoint):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    update_query = """
    UPDATE AccountInfo
    SET checkpoint = ?
    WHERE username = ?
    """

    c.execute(update_query, (checkpoint, username_entered))

    conn.commit()
    conn.close()

def change_damage_taken(username_entered, damage):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    update_query = """
    UPDATE AccountInfo
    SET damage = ?
    WHERE username = ?
    """

    c.execute(update_query, (damage, username_entered))

    conn.commit()
    conn.close()

def get_leaderboard_info():
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT username, damage FROM AccountInfo WHERE o5_defeated = 1 ORDER BY damage ASC")

    results = c.fetchall()

    conn.close()

    return results

def save_data_1(b1_looted, b2_looted, c1_looted, m1_complete, o1_defeated, o2_defeated, o1_killed, o2_killed, o1_spared, o2_spared, username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    update_query = """
        UPDATE AccountInfo
        SET b1_looted = ?, b2_looted = ?, c1_looted = ?, m1_complete = ?, o1_defeated = ?, o2_defeated = ?, o1_killed = ?,
         o2_killed = ?, o1_spared = ?, o2_spared = ?
        WHERE username = ?
        """

    c.execute(update_query, (b1_looted, b2_looted, c1_looted, m1_complete, o1_defeated, o2_defeated, o1_killed, o2_killed,
                             o1_spared, o2_spared, username_entered))

    conn.commit()
    conn.close()

def save_data_2(b1_looted, b2_looted, c1_looted, c2_looted, m1_complete, m2_complete, o1_defeated, o2_defeated, o3_defeated,
                o1_killed, o2_killed, o3_killed, o1_spared, o2_spared, o3_spared, username_entered):

    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    update_query = """
            UPDATE AccountInfo
            SET b1_looted = ?, b2_looted = ?, c1_looted = ?, c2_looted = ?, m1_complete = ?, m2_complete = ?, o1_defeated = ?,
             o2_defeated = ?, o3_defeated = ?, o1_killed = ?, o2_killed = ?, o3_killed = ?, o1_spared = ?, o2_spared = ?, o3_spared = ?
            WHERE username = ?
            """

    c.execute(update_query, (b1_looted, b2_looted, c1_looted, c2_looted, m1_complete, m2_complete, o1_defeated, o2_defeated,
                             o3_defeated, o1_killed, o2_killed, o3_killed, o1_spared, o2_spared, o3_spared, username_entered))

    conn.commit()
    conn.close()

def save_data_3(b1_looted, b2_looted, b3_looted, b4_looted, b5_looted, b6_looted, c1_looted, c2_looted, c3_looted, c4_looted,
                c5_looted, c6_looted, m1_complete, m2_complete, m3_complete, o1_defeated, o2_defeated, o3_defeated,
                o4_defeated, o1_killed, o2_killed, o3_killed, o4_killed, o1_spared, o2_spared, o3_spared, o4_spared,
                username_entered):

    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    update_query = """
            UPDATE AccountInfo
            SET b1_looted = ?, b2_looted = ?, b3_looted = ?, b4_looted = ?, b5_looted = ?, b6_looted = ?, c1_looted = ?, 
             c2_looted = ?, c3_looted = ?, c4_looted = ?, c5_looted = ?, c6_looted = ?, m1_complete = ?, m2_complete = ?,
             m3_complete = ?, o1_defeated = ?, o2_defeated = ?, o3_defeated = ?, o4_defeated = ?, o1_killed = ?, o2_killed = ?, 
             o3_killed = ?, o4_killed = ?, o1_spared = ?, o2_spared = ?, o3_spared = ?, o4_spared = ?
            WHERE username = ?
            """

    c.execute(update_query,
              (b1_looted, b2_looted, b3_looted, b4_looted, b5_looted, b6_looted, c1_looted, c2_looted, c3_looted, c4_looted,
               c5_looted, c6_looted, m1_complete, m2_complete, m3_complete, o1_defeated, o2_defeated, o3_defeated,
               o4_defeated, o1_killed, o2_killed, o3_killed, o4_killed, o1_spared, o2_spared, o3_spared, o4_spared, username_entered))

    conn.commit()
    conn.close()

def save_data_4(b1_looted, b2_looted, b3_looted, b4_looted, b5_looted, b6_looted, c1_looted, c2_looted, c3_looted, c4_looted,
                c5_looted, c6_looted, c7_looted, m1_complete, m2_complete, m3_complete, m4_complete, o1_defeated, o2_defeated,
                o3_defeated, o4_defeated, o5_defeated, o1_killed, o2_killed, o3_killed, o4_killed, o5_killed, o1_spared,
                o2_spared, o3_spared, o4_spared, o5_spared, username_entered):

    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    update_query = """
            UPDATE AccountInfo
            SET b1_looted = ?, b2_looted = ?, b3_looted = ?, b4_looted = ?, b5_looted = ?, b6_looted = ?, c1_looted = ?, 
             c2_looted = ?, c3_looted = ?, c4_looted = ?, c5_looted = ?, c6_looted = ?, c7_looted = ?, m1_complete = ?, 
             m2_complete = ?, m3_complete = ?, m4_complete = ?, o1_defeated = ?, o2_defeated = ?, o3_defeated = ?, 
             o4_defeated = ?, o5_defeated = ?, o1_killed = ?, o2_killed = ?, o3_killed = ?, o4_killed = ?, o5_killed = ?,
             o1_spared = ?, o2_spared = ?, o3_spared = ?, o4_spared = ?, o5_spared = ?
            WHERE username = ?
            """

    c.execute(update_query,
              (b1_looted, b2_looted, b3_looted, b4_looted, b5_looted, b6_looted, c1_looted, c2_looted, c3_looted, c4_looted,
               c5_looted, c6_looted, c7_looted, m1_complete, m2_complete, m3_complete, m4_complete, o1_defeated, o2_defeated,
               o3_defeated, o4_defeated, o5_defeated, o1_killed, o2_killed, o3_killed, o4_killed, o5_killed, o1_spared,
               o2_spared, o3_spared, o4_spared, o5_spared, username_entered))

    conn.commit()
    conn.close()

def check_b1_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT b1_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_b2_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT b2_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_b3_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT b3_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_b4_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT b4_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_b5_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT b5_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_b6_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT b6_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_c1_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT c1_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_c2_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT c2_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_c3_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT c3_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_c4_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT c4_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_c5_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT c5_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_c6_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT c6_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_c7_looted(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT c7_looted FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_m1_complete(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT m1_complete FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_m2_complete(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT m2_complete FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_m3_complete(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT m3_complete FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_m4_complete(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT m4_complete FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o1_defeated(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o1_defeated FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o2_defeated(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o2_defeated FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o3_defeated(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o3_defeated FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o4_defeated(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o4_defeated FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o5_defeated(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o5_defeated FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o1_killed(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o1_killed FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o2_killed(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o2_killed FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o3_killed(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o3_killed FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o4_killed(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o4_killed FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o5_killed(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o5_killed FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o1_spared(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o1_spared FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o2_spared(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o2_spared FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o3_spared(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o3_spared FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o4_spared(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o4_spared FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_o5_spared(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT o5_spared FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    if results[0][0] == 1:
        return True
    else:
        return False

def check_HP(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT HP FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    return results[0][0]

def check_AT(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT AT FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    return results[0][0]

def check_DF(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT DF FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    return results[0][0]

def check_SPEED(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT SPEED FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    return results[0][0]

def check_EXP(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT EXP FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    return results[0][0]

def check_damage(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT damage FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    return results[0][0]

def change_HP(username_entered, HP):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    query = """
    UPDATE AccountInfo
            SET HP = ?
            WHERE username = ?
    """

    c.execute(query, (HP, username_entered))

    conn.commit()
    conn.close()

def change_AT(username_entered, AT):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    query = """
        UPDATE AccountInfo
                SET AT = ?
                WHERE username = ?
        """

    c.execute(query, (AT, username_entered))

    conn.commit()
    conn.close()

def change_DF(username_entered, DF):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    query = """
        UPDATE AccountInfo
                SET DF = ?
                WHERE username = ?
        """

    c.execute(query, (DF, username_entered))

    conn.commit()
    conn.close()

def change_SPEED(username_entered, SPEED):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    query = """
        UPDATE AccountInfo
                SET SPEED = ?
                WHERE username = ?
        """

    c.execute(query, (SPEED, username_entered))

    conn.commit()
    conn.close()

def change_EXP(username_entered, EXP):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    query = """
        UPDATE AccountInfo
                SET EXP = ?
                WHERE username = ?
        """

    c.execute(query, (EXP, username_entered))

    conn.commit()
    conn.close()

def change_damage(username_entered, damage):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    query = """
        UPDATE AccountInfo
                SET damage = ?
                WHERE username = ?
        """

    c.execute(query, (damage, username_entered))

    conn.commit()
    conn.close()

def change_gold(username_entered, gold):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    query = """
    UPDATE AccountInfo
    SET gold = ?
    WHERE username = ?
    """

    c.execute(query, (gold, username_entered))

    conn.commit()
    conn.close()

def check_gold(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT gold FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    return results[0][0]

def change_maxHP(username_entered, maxHP):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    query = """
            UPDATE AccountInfo
                    SET maxHP = ?
                    WHERE username = ?
            """

    c.execute(query, (maxHP, username_entered))

    conn.commit()
    conn.close()

def check_maxHP(username_entered):
    conn = sqlite3.connect('EldritchEchoesAccounts.db')
    c = conn.cursor()

    c.execute("SELECT maxHP FROM AccountInfo WHERE username = ?", (username_entered,))
    results = c.fetchall()

    conn.commit()
    conn.close()

    return results[0][0]
