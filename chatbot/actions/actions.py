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

df_ingredients = pd.read_csv('./csv/film.csv')


class ActionCercafilm(Action):
    def name(self) -> Text:
        return "action_cerca_film"
    
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Okay, I'll provide you with a casual movie.")

        # Ottieni il numero totale di righe nel dataframe
        num_rows = df_ingredients.shape[0]
        
        # Genera un indice casuale
        random_index = random.randint(0, num_rows - 1)
        
        # Seleziona la riga corrispondente all'indice casuale
        random_film = df_ingredients.iloc[random_index]
        
        # Estrai le informazioni sul film casuale
        film_title = random_film['title']
        film_genre = random_film['genres']
        
        # Costruisci il messaggio da inviare all'utente
        message = f"Here is a casual movie for you:\nTitolo: {film_title}\nGenre: {film_genre}"
        
        # Invia il messaggio all'utente
        dispatcher.utter_message(text=message)
        
        return []