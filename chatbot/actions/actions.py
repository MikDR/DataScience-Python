# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
import pandas as pd
import random
#
#


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

df_film = pd.read_csv('./csv/film.csv')

## action cerca film, e da come risultato un film random
class ActionCercaFilm(Action):
    def name(self) -> Text:
        return "action_cerca_film"
    
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Okay, I'll provide you with a casual movie.")

        # Ottieni il numero totale di righe nel dataframe
        num_rows = df_film.shape[0]
        
        # Genera un indice casuale
        random_index = random.randint(0, num_rows - 1)
        
        # Seleziona la riga corrispondente all'indice casuale
        random_film = df_film.iloc[random_index]
        
        # Estrai le informazioni sul film casuale
        film_title = random_film['title']
        film_genre = random_film['genres']
        
        # Costruisci il messaggio da inviare all'utente
        message = f"Here is a casual movie for you:\nTitolo: {film_title}\nGenre: {film_genre}"
        
        # Invia il messaggio all'utente
        dispatcher.utter_message(text=message)
        
        return [AllSlotsReset()]


class ActionFilmPerGenere(Action):
    def name(self) -> Text:
        return "action_film_per_genere"
    
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Yes.")
        df_film_senza_nan = df_film.dropna(subset=['genres'])

        # Filtra il DataFrame per i film che corrispondono al genere specificato
        genere_selezionato = tracker.get_slot("genere")
        if genere_selezionato is not None:
            # Normalizza il genere specificato dall'utente in lettere minuscole
            genere_selezionato = genere_selezionato.lower()

            # Filtra il DataFrame per i film che corrispondono al genere specificato
            film_corrispondenti = df_film_senza_nan[df_film_senza_nan['genres'].str.lower().str.contains(genere_selezionato)]

            # Escludi i film senza genere
            film_corrispondenti = film_corrispondenti[film_corrispondenti['genres'].notna()]

            # Prendi i primi 10 film che soddisfano il criterio di filtraggio
            film_selezionati = film_corrispondenti.head(10)

            # Costruisci un messaggio contenente i dettagli dei film selezionati
            message = "Ecco alcuni film che potrebbero interessarti:\n"
            for index, row in film_selezionati.iterrows():
                message += f"Titolo: {row['title']}\nGenere: {row['genres']}\n\n"

            # Invia il messaggio all'utente
            dispatcher.utter_message(text=message)
            return []
        else:
            dispatcher.utter_message(text="Non è stato specificato un genere valido.")
            return []
            
class ActionCercaPerNome(Action):
    def name(self) -> Text:
        return "action_cerca_per_nome"
 
 
   
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # Ottieni il titolo del film dalla richiesta dell'utente
        film_title = tracker.get_slot("titolo")
 
        # .split("search the film")[1].strip()
 
        if film_title is None:
            dispatcher.utter_message(text="Non ho ricevuto il titolo del film. Per favore, forniscilo e riprova.")
            return []
       
        # Cerca il film nel DataFrame df_ingredients
        found_films = df_film[df_film['title'].str.lower() == film_title.lower()]
 
        # Verifica se il film è stato trovato
        if found_films.empty:
            dispatcher.utter_message(text="Non ho trovato nessun film con quel titolo.")
            return []
 
        # Prendi un film casuale tra quelli trovati (potrebbero essercene più di uno con lo stesso titolo)
        random_film = found_films.sample(n=1)
 
        dispatcher.utter_message(text="Okay, These are some information about the movie.")
        # Estrai le informazioni desiderate
        title = random_film['title'].values[0]
        vote_average = random_film['vote_average'].values[0]
        runtime = random_film['runtime'].values[0]
        genres = random_film['genres'].values[0]
        overview = random_film['overview'].values[0]
   
 
        # Costruisci il messaggio da inviare all'utente
        message = f"Film title: {title}\nAverage Vote: {vote_average}\nDuration: {runtime} minutes\nGenre: {genres}\nA small overview: {overview}"
 
        # Invia il messaggio all'utente
        dispatcher.utter_message(text=message)
       
        return []
