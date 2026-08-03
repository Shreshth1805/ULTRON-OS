
import os
import sys
from src.audio.recorder import Recorder
from src.audio.player import Player
from src.nlp.intent import IntentIdentifier
from src.nlp.entity import EntityExtractor
from src.utils.config import Config
from src.utils.logger import Logger

class VoicePal:
    def __init__(self):
        self.recorder = Recorder()
        self.player = Player()
        self.intent_identifier = IntentIdentifier()
        self.entity_extractor = EntityExtractor()
        self.config = Config()
        self.logger = Logger()

    def start(self):
        self.logger.info("Starting VoicePal")
        while True:
            self.logger.info("Listening for user input")
            audio = self.recorder.record()
            self.logger.info("Recognizing user input")
            text = self.recorder.recognize(audio)
            self.logger.info(f"User input: {text}")
            intent = self.intent_identifier.identify(text)
            self.logger.info(f"Intent: {intent}")
            entities = self.entity_extractor.extract(text)
            self.logger.info(f"Entities: {entities}")
            response = self.generate_response(intent, entities)
            self.logger.info(f"Response: {response}")
            self.player.play(response)

    def generate_response(self, intent, entities):
        if intent == "greeting":
            return "Hello, how can I assist you?"
        elif intent == "goodbye":
            return "Goodbye, it was nice talking to you."
        elif intent == "help":
            return "I can assist you with various tasks. What do you need help with?"
        else:
            return "I didn't understand your request. Please try again."

if __name__ == "__main__":
    voice_pal = VoicePal()
    voice_pal.start()
