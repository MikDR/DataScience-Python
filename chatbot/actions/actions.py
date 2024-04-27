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
            dispatcher.utter_message(text="I didn't receive the film's name. Please provide it and try again.")
            return []
       
        # Cerca il film nel DataFrame df_ingredients
        found_films = df_film[df_film['title'].str.lower() == film_title.lower()]
 
        # Verifica se il film è stato trovato
        if found_films.empty:
            dispatcher.utter_message(text="I didn't find any movie with that name.")
            return []
 
        sorted_films = found_films.sort_values(by='vote_average', ascending=False)
 
        dispatcher.utter_message(text="Here are some films, ordered by rating.")
        
        # Cicla sui film trovati e invia le informazioni pertinenti all'utente
        for idx, film in sorted_films.iterrows():
            title = film['title']
            vote_average = film['vote_average']
            film_id = film['imdb_id']  # Ottieni l'ID del film

            # Verifica se l'ID del film è None
            if pd.isna(film_id):
                dispatcher.utter_message(text="Unfortunately, the movie is not available.")
                continue
            
            # Costruisci l'URL IMDb per il film
            imdb_url = f"https://www.imdb.com/title/{film_id}"
 
            # Costruisci il messaggio da inviare all'utente per ogni film
            message = f"Film title: {title}\nAverage Vote: {vote_average}\nIMDb URL: {imdb_url}"
 
            # Invia il messaggio all'utente
            dispatcher.utter_message(text=message)
 
        return []

#aggiustare il voto intero...
class ActionVotoMaggioreDi(Action):
    def name(self) -> Text:
        return "action_voto_maggiore_di"
   
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Ottieni il titolo del film dalla richiesta dell'utente
        voto = tracker.get_slot("vote_average")
        # .split("search the film")[1].strip()
        if voto is None:
            dispatcher.utter_message(text="Non ho ricevuto un voto. Per favore, forniscilo e riprova.")
            return [AllSlotsReset()]
       
   
        # Converti il rating in float
        try:
            voto = float(voto)
        except ValueError:
            dispatcher.utter_message(text="Il rating specificato non è valido. Per favore, forniscine uno valido e riprova.")
            return [AllSlotsReset()]
       
        # Filtra i film con un rating superiore al rating specificato
        filtered_films = df_film[df_film['vote_average'] >= voto]
       
        if filtered_films.empty:
            dispatcher.utter_message(text="Non ci sono film con un rating superiore a quello specificato.")
            return [AllSlotsReset()]
       
        # Prendi un film casuale tra quelli filtrati
        random_film = filtered_films.sample(n=1)
       
        # Estrai le informazioni del film
        title = random_film['title'].values[0]
        vote_average = random_film['vote_average'].values[0]
        runtime = random_film['runtime'].values[0]
        genres = random_film['genres'].values[0]
        id = random_film['imdb_id'].values[0]
        overview = random_film['overview'].values[0]
       
        # Costruisci il messaggio da inviare all'utente
        message = f"Ecco un film con un rating superiore a {voto}:\nTitolo: {title}\nVoto Medio: {vote_average}\nDurata: {runtime} minuti\nGenere: {genres}\nSmall overview: {overview}\nImdb Id: {id}"
       
        # Invia il messaggio all'utente
        dispatcher.utter_message(text=message)
       
        return [AllSlotsReset()]
    


class ActionFilmConAttore(Action):
    def name(self) -> Text:
        return "action_film_con_attore"
 
 
   
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # Ottieni il titolo del film dalla richiesta dell'utente
        attore = tracker.get_slot("attore")
 
        # .split("search the film")[1].strip()
 
        if attore is None:
            dispatcher.utter_message(text="I didn't receive the actor's name. Please provide it and try again.")
            return [AllSlotsReset()]
        
        #leviamo linee NaN da overview per usare str.contains
        df_film_cleaned = df_film.dropna(subset=['overview'])
       
        found_films = df_film_cleaned[df_film_cleaned['overview'].str.contains(attore, case=False)]
        print(found_films)

        # Verifica se ci sono film con quell'attore
        if found_films.empty:
            dispatcher.utter_message(text=f"I didn't find any movie with the actor {attore}.")
            return [AllSlotsReset()]

        # Ordina i film per voto medio in ordine decrescente
        sorted_films = found_films.sort_values(by='vote_average', ascending=False)

        # Prendi i primi 10 film dopo l'ordinamento
        top_10_films = sorted_films.head(10)
        
        dispatcher.utter_message(text="Here are some movies with the specified actor, sorted by average rating:")
        
        # Cicla sui primi 10 film e invia le informazioni pertinenti all'utente
        for idx, film in top_10_films.iterrows():
            title = film['title']
            vote_average = film['vote_average']
            genres = film['genres']
 
            # Costruisci il messaggio da inviare all'utente
            message = f"Film title: {title}\nAverage vote: {vote_average}\nGenre: {genres}"
 
            # Invia il messaggio all'utente
            dispatcher.utter_message(text=message)
 
        return [AllSlotsReset()]