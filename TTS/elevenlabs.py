import random
from elevenlabs import save
from elevenlabs.client import ElevenLabs as ElevenLabsClient
from utils import settings

class ElevenLabs:
    def __init__(self):
        self.max_chars = 2500
        self.client: ElevenLabsClient = None

    def run(self, text, filepath, random_voice: bool = False):
        if self.client is None:
            self.initialize()
        try:
            if random_voice:
                voice = self.randomvoice()
            else:
                voice = str(settings.config["settings"]["tts"]["elevenlabs_voice_name"]).capitalize()
            
            audio = self.client.generate(text=text, voice=voice, model="eleven_multilingual_v1")
            save(audio=audio, filename=filepath)
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            raise

    def initialize(self):
        if settings.config["settings"]["tts"]["elevenlabs_api_key"]:
            api_key = settings.config["settings"]["tts"]["elevenlabs_api_key"]
        else:
            raise ValueError(
                "You didn't set an Elevenlabs API key! Please set the config variable ELEVENLABS_API_KEY to a valid API key."
            )

        self.client = ElevenLabsClient(api_key=api_key)

    def randomvoice(self):
        if self.client is None:
            self.initialize()
        voices = self.client.voices.get_all()
        if isinstance(voices, tuple) and len(voices) > 1 and isinstance(voices[1], list):
            voice_list = voices[1]  # The list of voices is the second item in the tuple
        else:
            voice_list = list(voices)  # Fallback to the previous method
        
        if not voice_list:
            raise ValueError("No voices available")
        
        chosen_voice = random.choice(voice_list)
        
        # Debug print
        print(f"Chosen voice object: {chosen_voice}")
        
        if isinstance(chosen_voice, str):
            return chosen_voice
        elif hasattr(chosen_voice, 'name'):
            return chosen_voice.name
        elif isinstance(chosen_voice, dict) and 'name' in chosen_voice:
            return chosen_voice['name']
        else:
            raise ValueError(f"Unable to determine voice name from object: {chosen_voice}")

elevenlabs = ElevenLabs