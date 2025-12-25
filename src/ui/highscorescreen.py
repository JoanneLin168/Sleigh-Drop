import pygame
from src.settings import WIDTH, HEIGHT
from src.ui.textscreen import TextScreen

class HighscoreScreen(TextScreen):
    def __init__(self, screen, highscores, buttons=None):
        highscore_text = ""
        if highscores == []:
            highscore_text = "No highscores yet!\n"
        else:
            for i, entry in enumerate(highscores):
                highscore_text += f"{i+1}. {entry['datetime']} - {entry['score']}\n"

        super().__init__(
            screen,
            "Highscores",
            highscore_text,
            buttons=buttons
        )