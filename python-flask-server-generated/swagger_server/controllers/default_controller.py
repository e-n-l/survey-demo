import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.poll import Poll  # noqa: E501
from swagger_server.models.poll_answer import PollAnswer  # noqa: E501
from swagger_server.models.polls import Polls  # noqa: E501
from swagger_server import util

DB_NAME = 'survey.db'

import sqlite3

def user_get(user_id):    
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c  = conn.cursor()

    c.execute("SELECT * FROM user WHERE user_id=?",[ user_id ])
    row = c.fetchone()

    user = {}

    for key in row.keys():
        user[key] = row[key]

    return user


def this_user():
    user = {
        'user_agent': connexion.request.headers["User-Agent"],
        'ip_addr':    connexion.request.remote_addr,
        'info':       ''
    }

    conn = sqlite3.connect(DB_NAME)
    c  = conn.cursor()

    c.execute("SELECT user_id FROM user WHERE user_agent=? AND ip_addr=?",
        [ user['user_agent'],user['ip_addr'] ])
    user_id = c.fetchone()

    if user_id is None:
        c.execute("INSERT INTO user (user_agent,ip_addr) VALUES (?,?)",
            [ user['user_agent'],user['ip_addr'] ])
        conn.commit()
        user['id'] = c.lastrowid
        print('new user added!')
    else:
        user['id'] = user_id[0]
        print('hello user '+str(user_id[0]))

    return user


def create_answer(poll_id, answer):  # noqa: E501
    """add a new answer

     # noqa: E501

    :param poll_id: 
    :type poll_id: int
    :param answer: 
    :type answer: str

    :rtype: PollAnswer
    """ 
    user = this_user()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT question FROM poll WHERE poll_id = ? AND user_id = ?",
        [poll_id,user['id']])
    question_text = c.fetchone()

    if question_text:
        print('authorized!')
        c.execute("INSERT OR REPLACE INTO answer (poll_id,answer) VALUES (?,?)",
                [poll_id,answer])        
        conn.commit()
    else:
        return { 'error':'Wrong user' }, 301

    answer_data = { 
        "poll_id":   poll_id, 
        "answer_id": c.lastrowid, 
        "answer":    answer }
    conn.close()

    return answer_data, 201

def create_poll(question):  # noqa: E501
    """create a poll

    create polls using this endpoint. # noqa: E501

    :param question: 
    :type question: str

    :rtype: Poll
    """

    poll_data = { 
        "question": question, 
        "poll_id": '',
        "editable": False,
        "answers": [] }

    user = this_user()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT poll_id FROM poll WHERE question=?",
        [question])
    poll_exists = c.fetchone()
    
    if poll_exists is None:
        c.execute("INSERT INTO poll (question,user_id) VALUES (?,?)",
            [question, user['id'] ])
        conn.commit()
        poll_data['poll_id'] = c.lastrowid
        poll_data['editable'] = True
    else:
        owner = poll_exists[0]
        poll_data['poll_id'] = poll_exists[0]
        if user['id'] == owner:
            poll_data['editable'] = True


    json = connexion.request.json

    if 'answers' in json and type(json['answers']) is list and poll_data['editable']:
        for answer in json['answers']:
            new_answer = create_answer(poll_data['poll_id'],answer)
            poll_data["answers"].append(new_answer[0])
    elif poll_data['editable']:
        c.execute('DELETE FROM poll WHERE poll_id = ?',poll_data['poll_id'])
        return { 'error':'Poll must have options to vote on' },422

    conn.close()

    return poll_data, 201

def get_poll(poll_id):  # noqa: E501
    """get_poll

     # noqa: E501

    :param poll_id: 
    :type poll_id: int

    :rtype: Poll
    """
    user = this_user()
    this_poll = {}

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c  = conn.cursor()
    c2 = conn.cursor()

    c.execute('''
        SELECT question,
               poll_id,
               user_id, -- owner
               CASE WHEN user_id = ? THEN 1 ELSE 0 END AS editable
        FROM   poll
        WHERE  poll_id = ?''', 
        [ user['id'], poll_id ])


    row = c.fetchone()

    if type(row) is not sqlite3.Row:
        conn.close()
        return { "error": "Poll not found" }, 422


    # load query into poll dict
    for key in row.keys():
        this_poll[key] = row[key]


    # add an array of answers / votes
    c2.execute( '''
        SELECT answer, answer_id, user_id
        FROM   answer 
          LEFT JOIN vote USING (answer_id)
          LEFT JOIN user USING (user_id)
        WHERE  answer.poll_id = ?''',
        [poll_id] )

    this_poll['voted'] = 0
    this_poll['options'] = []
    this_poll['taken'] = 0
    this_answer = { 'answer_id': -1 }
    winner = [0,0]

    for row in c2.fetchall():
        if row['answer_id'] != this_answer['answer_id']:
            if this_answer['answer_id'] != -1:
                this_poll['options'].append(this_answer)
                this_answer_votes = len(this_answer['votes'])
                if this_answer_votes > winner[0]:
                    winner = [this_answer_votes, len(this_poll['options'])-1 ]

            this_answer = { 
                'answer_id': row['answer_id'],
                'answer': row['answer'],
                'votes': []
            }

        if row['user_id']:
            this_poll['voted'] += 1
            this_voter = user_get(row['user_id'])
            this_answer['votes'].append(this_voter)
            if this_voter['user_id'] == user['id']:
                this_answer['active'] = 1
                this_poll['taken'] = 1


    # activate most_votes flag, if possible:
    if winner[0]:
        this_poll['options'][winner[1]]['most_votes'] = 1

    
    conn.close()
    return this_poll, 200

def create_vote(poll_id, answer_id):  # noqa: E501
    """submit answers to poll questions

     # noqa: E501

    :param poll_id: 
    :type poll_id: int
    :param answer_id: 
    :type answer_id: int

    :rtype: None
    """
    user = this_user()

    conn = sqlite3.connect(DB_NAME)
    c  = conn.cursor()

    c.execute("DELETE FROM vote WHERE user_id = ? AND poll_id = ?",
        [user['id'],poll_id])

    c.execute("INSERT OR REPLACE INTO vote (user_id, answer_id, poll_id) VALUES (?,?,?)",
        [user['id'],answer_id,poll_id])
    conn.commit()
    conn.close()

    return {}, 201

def polls_get():  # noqa: E501
    """display all available polls

     # noqa: E501


    :rtype: Polls
    """
    user = this_user()
    polls = []

    conn = sqlite3.connect(DB_NAME)
    c  = conn.cursor()
    c.execute("SELECT poll_id FROM poll ORDER BY poll_id")

    for row in c.fetchall():
        # get votes / voters
        polls.append( get_poll( row[0] )[0] )

    conn.close()
    return polls, 200