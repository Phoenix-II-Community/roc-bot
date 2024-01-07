import sqlite3


# It's 31/12/2023 and Dune Part 2 still hasn't been released, so this module
# will have all formatting bits stripped leaving the sql client bits. The original bot
# was created by Jens using json files which this python rewrite continued
# using in v1 but later moved to sqlite and v2 was born. Because reasons,
# this class has a combo of formatting and data queries which is making things
# tricky when it comes to expanding functionality. It was fine for like 4~ years
# now it's time to clean it up. We could even use dataclasses which are pretty nice.

############################################################################
# was originally in data.py module but got yanked out with the v3 refactor
############################################################################

# def sql_ship_obj():
#     # connect to the sqlite database
#     conn = sqlite3.connect('rocbot.sqlite')
#     # return a class sqlite3.row object which requires a tuple input query
#     conn.row_factory = sqlite3.Row
#     # make a sqlite connection object
#     c = conn.cursor()
#     # using a defined view s_info find the ship
#     c.execute('select * from s_info where name = ?', (self.ship_name,))
#     # return the ship object including the required elemnts
#     s_obj = c.fetchone()
#     # close the database connection
#     conn.close()
#     # return the sqlite3.cursor object
#     return s_obj
#
# def sql_ship_info_obj(self):
#     conn = sqlite3.connect('rocbot.sqlite')
#     conn.row_factory = sqlite3.Row
#     c = conn.cursor()
#     if self.sub_command in ('all', 'rand'):
#         c.execute("select * from s_info")
#     else:
#         c.execute(f"select * from s_info where {self.sub_command} = ?", (self.arg1,))
#     s_obj = c.fetchall()
#     conn.close()
#     return s_obj



# category lister
def sql_ship_info_obj():
    # Possible views include
    # i_hp; inavder hp
    # m_daily; mission daily
    # s_apex; ship apexs
    # s_info; ship info
    # shortcut; list of shortcuts for auras, zens weapon affinity, and rartity
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make a sqlite connection object
    c = conn.cursor()
    # using a defined view s_info collect all table info
    c.execute('select * from s_info')
    # return the ship object including the required elemnts
    s_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return s_obj


############################################################################
# was originally in mission.py module but got yanked out with the v3 refactor
############################################################################
def sql_daily_obj(self):
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view s_info find the ship
    c.execute('select * from m_daily where day = ?', (self.day_number(),))
    # return the ship object including the required elemnts
    m_obj = c.fetchone()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return m_obj


############################################################################
# was originally in invaders.py module but got yanked out with the v3 refactor
############################################################################

def get_invaders(self):
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    invader_list = c.execute('''SELECT name FROM invaders''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return invader_list

# Grab the Invader stats for a specific ship from the SQL view
def sql_i_name_obj(self):
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view s_info find the ship
    c.execute('select * from i_hp where name = ?', (self.i_name,))
    # return the ship object including the required elemnts
    i_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return i_obj

# Grab the Invader stats for a specific affinity of invader from the SQL view
def sql_i_type_obj(self):
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view s_info find the ship
    c.execute('select * from i_hp where type = ?', (self.sc,))
    # return the ship object including the required elemnts
    i_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return i_obj

############################################################################
# was originally in img.py module but got yanked out with the v3 refactor
############################################################################

def sql_apex_num_obj():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view s_info find the ship
    c.execute('''
select
    ship.id as id,
    apex_tier.name as rank,
    apex_ships.apex_num as apex_num
from apex_ships inner join ship on apex_ships.ship_name = ship.id
inner join apexs on apex_ships.apex_id = apexs.id
inner join apex_tier on apex_ships.apex_tier = apex_tier.id;
    ''')
    # return the ship object including the required elemnts
    a_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return a_obj


############################################################################
# was originally in common.py module but got yanked out with the v3 refactor
############################################################################

# Connect to the local sqlite database `rocbot.sqlite` and generate a list of
# ship names from the `ship` table
def get_ships():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    ship_list = c.execute('''SELECT name FROM ship''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return ship_list

# return the ship name from name_list which is a list of ship names
# extracted from the databases table called ship
def ship_search(find_this):
    # using the class initiated list ship_list find one ship name that
    # matches the given string as close as possible
    found_this = process.extractOne(find_this, get_ships())
    # rapidfuzz returns the name and the ratio so strip the ratio and keep
    # the ship name
    ship_name = found_this[0]
    # return the ship name as a string
    return ship_name

# Connect to the local sqlite database `rocbot.sqlite` and generate a list of
# invader names from the invaders table
def get_invaders():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    invader_list = c.execute('''SELECT name FROM invaders''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return invader_list

def shortcut_obj(arg1):
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view shortcut collect all table info
    c.execute('select * from shortcut where shortcut =?', (arg1,))
    # return the shortcut object including the required elemnts
    # using shortc instead of sc so not to be confused with
    # sub command abbrehviations
    shortc_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return shortc_obj


def sql_dmg_brackets():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    dmg_obj = c.execute('''SELECT amount FROM ship_damage''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return dmg_obj