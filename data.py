connex = psycopg2.connect()

CREATE_POLLS = '''CREATE TABLE IF NOT EXISTS polls (id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);'''
CREATE_OPTIONS = '''CREATE TABLE IF NOT EXISTS options (id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER);'''
CREATE_VOTES = '''CREATE TABLE IF NOT EXISTS votes (username TEXT, option_id INTEGER);'''
SELECT_ALL_POLLS = '''
SELECT *
FROM polls;'''
SELECT_POLL_WITH_OPTION = '''SELECT polls.*
FROM polls
JOIN options
ON polls.id = options.poll_id
WHERE polls.id = %s;
'''
INSERT_OPTION = '''INSERT INTO options (option_text, poll_id) values %s;'''
INSERT_VOTE = '''INSERT INTO votes (username, option_id) VALUES (%s, %s);'''

def create_tables(connex):
    with connex:
        with connex.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)

def get_polls(connex):
    with connex:
        with connex.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()

def get_latest_poll(connex):
    with connex:
        with connex.cursor() as cursor:
            cursor.execute()

def get_polls_details(connex, poll_id):
    with connex:
        with connex.cursor() as cursor:
            cursor.execute(SELECT_POLL_WITH_OPTION, (poll_id,))
            return cursor.fetchall()

def get_poll_and_vote_results(connex, poll_id):
    with connex:
        with connex.cursor() as cursor:
            pass

def get_random_poll_vote(connex, option_id):
    with connex:
        with connex.cursor() as cursor:
            pass

def create_poll(connex, title, owner, options):
    with connex:
        with connex.cursor() as cursor:
            pass

def add_poll_vote(connex, username, option_id):
    with connex:
        with connex.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))
