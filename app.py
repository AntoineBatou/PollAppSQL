import os
import psycopg2
from psycopg2.errors import DivisionByZero
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import data

DATABASE_PROMPT = "Saisissez la valeur DATABASE_URI ou laissez-la vide pour charger le fichier .env : "
MENU_PROMPT = """-- Menu --
1) Créer un nouveau sondage
2) Lister les sondages ouverts
3) Voter sur un sondage
4) Afficher les votes du sondage
5) Sélectionner un gagnant au hasard à partir d'une option du sondage
6) Quitter
Saisir votre choix : """
NEW_OPTION_PROMPT = "Saisissez le texte de la nouvelle option (ou laissez-le vide pour ne plus ajouter d'options) : "

def prompt_create_poll(connex):
    poll_title = input("Veuillez entrer un titre pour le sondage : ")
    poll_owner = input("QUel propriétaire du sondage ? ")
    options = []
    while new_option := input(NEW_OPTION_PROMPT):
        options.append(new_option)
    data.create_poll(connex, poll_title, poll_owner, options)

def list_open_polls(connex):
    polls = data.get_polls(connex)

    for _id, title, owner in polls:
        print(f"{_id}, - {title}, crée par {owner}.")

def prompt_vote_poll(connex):
    poll_id = input("Pour quel sondage voulez-vous voter (id) ? ")
    poll_options = data.get_polls_details(connex, poll_id)
    _print_poll_options(connex, poll_options)
    option_id = input("Pour quelle option voulez-vous voter ?")
    username = input("Quel utilisateur êtes-vous ?")
    data.add_poll_vote(connex, username, option_id)

def _print_poll_options(connex, poll_with_options):
    for option in poll_with_options:
        print(f"{option[3]}: {option[4]}")

def show_poll_vote(connex):
    list_open_polls(connex)
    poll_id = input("Pour quel sondage?")
    try:
        poll_and_votes = data.get_poll_and_vote_results(connex, poll_id)
    except DivisionByZero:
        print("Pas de vote pour ce sondage !")
    else:
        for _id, option_text, count, percentage in poll_and_votes:
            print(f"{option_text} a obtenu {count} votes ({percentage:.2f}% du total)")

def randomize_poll_winner(connex):
    list_open_polls(connex)
    poll_id = input("Séléctionnez un sondage pour lequel vous souhaitez désigner un gagnant !")
    poll_with_options = data.get_polls_details(connex, poll_id)
    _print_poll_options(connex, poll_with_options)
    option_id = input("Séléctionnez l'ID de la réponse gagnante, nous séléctionnerons un gagant au hasard !")
    winner = data.get_random_poll_vote(connex, option_id)
    print(f"Le gagnant est {winner[0]}")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_vote,
    "5": randomize_poll_winner
}

def menu():
    database_uri = input(DATABASE_PROMPT)
    if not database_uri:
        load_dotenv()
        database_uri = os.environ["DATABASE_URL"]
    connex = psycopg2.connect(database_uri)
    data.create_tables(connex)


    while (user_choice := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[user_choice](connex)
        except KeyError:
            print("Choix inconnu !")

menu()