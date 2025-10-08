# Lumenvox/backend/services/caption_service.py
"""
Este módulo contém o serviço principal de Inteligência Artificial.

A classe CaptionService é responsável por encapsular toda a lógica de
carregamento do modelo de IA e geração de legendas para as imagens.
"""
import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
from deep_translator import GoogleTranslator
import os

class CaptionService:
    """Serviço para carregar o modelo e gerar descrições de imagens."""

    # Dentro da classe CaptionService, substitua o método __init__ por este:

    def __init__(self):
        """
        Inicializa o serviço, carregando o modelo, o processador e o tradutor
        na memória uma única vez durante a inicialização do servidor.
        """
        print("Iniciando o CaptionService...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Usando dispositivo: {self.device}")

        # --- CORREÇÃO APLICADA AQUI ---
        # Construímos um caminho absoluto para o modelo para evitar ambiguidades.
        original_model_id = "Salesforce/blip-image-captioning-base"
        
        # Cria o caminho relativo de forma robusta
        relative_model_path = os.path.join("backend", "model", "modelo_final")
        # Converte para um caminho absoluto (ex: C:\Users\Hideki\Documents\Lumenvox 1.1\backend\model\modelo_final)
        finetuned_model_path = os.path.abspath(relative_model_path)
        
        print(f"Carregando PROCESSADOR de: {original_model_id}")
        self.processor = BlipProcessor.from_pretrained(original_model_id)

        print(f"Carregando MODELO TREINADO de: {finetuned_model_path}")
        self.model = BlipForConditionalGeneration.from_pretrained(finetuned_model_path).to(self.device)
        print("Modelo carregado com sucesso.")

        self.translator = GoogleTranslator(source='en', target='pt')
        print("CaptionService pronto.")

    def generate_caption(self, uploaded_image_file):
        """
        Gera uma legenda em português para um arquivo de imagem recebido.

        Args:
            uploaded_image_file: O arquivo de imagem aberto (stream de bytes).

        Returns:
            Uma string com a descrição da imagem em português.
        """
        try:
            image = Image.open(uploaded_image_file).convert("RGB")

            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            output_tokens = self.model.generate(**inputs, max_new_tokens=50)
            caption_in_english = self.processor.decode(output_tokens[0], skip_special_tokens=True)

            caption_in_portuguese = self.translator.translate(caption_in_english)

            return caption_in_portuguese

        except Exception as e:
            print(f"ERRO CRÍTICO ao gerar legenda: {e}")
            return "Desculpe, ocorreu um erro ao tentar descrever a imagem."