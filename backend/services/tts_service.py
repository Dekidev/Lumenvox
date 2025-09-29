# Lumenvox/backend/services/tts_service.py

from google.cloud import texttospeech
import os

class TTSService:
    def __init__(self):
        # A biblioteca do Google usa automaticamente as credenciais
        # da variável de ambiente que definimos no arquivo .env
        self.client = texttospeech.TextToSpeechClient()
        print("TTSService pronto.")

    def synthesize_speech(self, text):
        """Converte um texto em áudio (bytes de um arquivo MP3)."""
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Configura a voz. Você pode experimentar outras vozes!
        # Lista de vozes: https://cloud.google.com/text-to-speech/docs/voices
        voice = texttospeech.VoiceSelectionParams(
            language_code="pt-BR",
            name="pt-BR-Wavenet-B" # Uma voz masculina de alta qualidade
        )

        # Seleciona o tipo de áudio (MP3)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Realiza a requisição de conversão de texto em fala
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Retorna o conteúdo de áudio em bytes
        return response.audio_content