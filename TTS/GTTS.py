from gtts import gTTS
from utils import settings

class GTTS:
    def __init__(self):
        self.max_chars = 5000  # gTTS doesn't have a strict limit, but let's set a reasonable one

    def run(self, text: str, filepath: str, random_voice: bool = False):
        # The 'random_voice' parameter is ignored for gTTS as it doesn't support voice selection
        lang = settings.config["reddit"]["thread"]["post_lang"] or "en"
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filepath)

    @staticmethod
    def random_voice() -> str:
        # gTTS doesn't support voice selection, so this method does nothing
        return "default"