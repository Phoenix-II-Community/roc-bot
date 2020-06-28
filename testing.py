import sqlite3 

b = 'icar'
def getter():
    conn = sqlite3.connect('rocbot.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from s_info where name = ?', (b,))
    s_obj = c.fetchone()
    conn.close()
    return s_obj

a = getter()
print(a)
