from selectors import EpollSelector

CREATE_POLLS = '''CREATE TABLE IF NOT EXISTS polls (id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);'''
CREATE_OPTIONS = '''CREATE TABLE IF NOT EXISTS options (id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER);'''
CREATE_VOTES = '''CREATE TABLE IF NOT EXISTS votes (username TEXT, option_id INTEGER);'''
SELECT_ALL_POLLS = '''
SELECT *
FROM polls;'''

SELECT_POLL_WITH_OPTION = '''
SELECT *
FROM polls
JOIN options
ON polls.id = options.poll_id
WHERE polls.id = (
    SELECT id
    FROM polls
    ORDER BY polls.id DESC
    LIMIT 1);
'''
INSERT_POLL_RETURN_ID = "INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"
INSERT_OPTION = '''INSERT INTO options (option_text, poll_id) values %s;'''
INSERT_VOTE = '''INSERT INTO votes (username, option_id) VALUES (%s, %s);'''
OBTAIN_LAST_POLL = '''
SELECT *
FROM polls
JOIN options
ON polls.id = options.poll_id
WHERE polls.id = (
    SELECT id
    FROM polls
    ORDER BY polls DESC
    LIMIT 1
    );
'''
OBTAIN_LAST_POLL_V2 = '''
WITH last_id AS (
    SELECT id FROM polls ORDER BY id DESC LIMIT 1
    )
SELECT *
FROM polls
JOIN options
ON polls.id = options.poll_id
WHERE polls.id = (SELECT * FROM last_id);
'''
SELECT_RANDOM_VOTE = '''
SELECT *
FROM votes
WHERE option_id = %s
ORDER BY RANDOM()
LIMIT 1;
'''
SELECT_POLL_VOTE_DETAILS = '''
option_id, option_text, COUNT(votes.option_id) AS vote_count, COUNT(votes.option_id) * 100 / sum(count(votes.option_id)) AS pourcentage
FROM options
LEFT JOIN votes
ON options.id = votes.option_id
WHERE options.poll_id = %s
GROUP BY options.option_id;
'''

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
            cursor.execute(SELECT_POLL_VOTE_DETAILS, (poll_id,))
            return cursor.fetchall()

def get_random_poll_vote(connex, option_id):
    with connex:
        with connex.cursor() as cursor:
            cursor.execute(SELECT_RANDOM_VOTE, option_id)
            return cursor.fetchone()

def create_poll(connex, title, owner, options):
    with connex:
        with connex.cursor() as cursor:
            cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))
            poll_id = cursor.fetchone()[0]
            options_values = [(option_text, poll_id) for option_text in options]
            for option in options_values:
                cursor.execute(INSERT_OPTION, option)

                ## Il aurait été possible d'utiliser une fn de psycopg2 à la place de cette dernière boucle :
                ## execute_values(cursor, INSERT_OPTION, option_values)
                ## La fonction execute_values prend trois arguments :
                # Le curseur qui exécutera les requêtes.
                # La requête qui sera exécutée pour chaque valeur.
                # Une liste de tup, où chaque tup correspond à ce qui est entré dans l’une des requêtes.

def add_poll_vote(connex, username, option_id):
    with connex:
        with connex.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))
