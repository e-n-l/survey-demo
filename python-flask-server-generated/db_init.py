import sqlite3

conn = sqlite3.connect('survey.db')
c = conn.cursor()

c.execute('''ATTACH 'survey.db' AS quickpoll''')
c.execute('''
  CREATE TABLE IF NOT EXISTS quickpoll.user(
    user_id INTEGER PRIMARY KEY,
    ip_addr TEXT,
    user_agent TEXT,
    addl_info TEXT )''')
c.execute('''
  CREATE TABLE IF NOT EXISTS quickpoll.poll(
    poll_id INTEGER PRIMARY KEY,
    user_id INTEGER, -- owner
    question TEXT,
    FOREIGN KEY(user_id) REFERENCES user(user_id) )''')
c.execute('''
  CREATE TABLE IF NOT EXISTS quickpoll.answer(
    answer_id INTEGER PRIMARY KEY,
    answer TEXT,
    poll_id INTEGER,
    FOREIGN KEY(poll_id) REFERENCES poll(poll_id) )''')
c.execute('''
  CREATE TABLE IF NOT EXISTS quickpoll.vote(
    user_id INTEGER,
    answer_id INTEGER,
    poll_id INTEGER,
    ts TEXT DEFAULT(datetime()),
    FOREIGN KEY(user_id)   REFERENCES user(user_id),
    FOREIGN KEY(answer_id) REFERENCES answer(answer_id),
    FOREIGN KEY(poll_id)   REFERENCES poll(poll_id) )''')

conn.commit()

conn.close()

print('DB initialized')