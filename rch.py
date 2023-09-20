import openai
import sys
import panel as pn  # GUI
pn.extension()

openai.api_key = "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"


class rch:
    def __init__(self):
        self.api = openai.api_key
        