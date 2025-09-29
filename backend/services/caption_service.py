# Lumenvox/backend/services/caption_service.py

import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
from deep_translator import GoogleTranslator
import os

class CaptionService:
    def __init__(self):
        """
        Construtor da classe.
        Este método é chamado apenas uma vez, quando o servidor inicia.
        É aqui que carregamos o modelo pesado para a memória.
        """
        print("Iniciando o CaptionService...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Usando dispositivo: {self.device}")

        # --- CORREÇÃO APLICADA AQUI ---
        # Definimos o nome do modelo original para carregar o processador
        original_model_name = "Salesforce/blip-image-captioning-base"

        # Encontra o caminho para o modelo treinado
        model_dir = "./backend/model/blip-flickr8k-finetuned"
        latest_checkpoint = max([d for d in os.listdir(model_dir) if d.startswith("checkpoint-")])
        self.model_path = os.path.join(model_dir, latest_checkpoint)
        
        print(f"Carregando PROCESSADOR de: {original_model_name}")
        # Carrega o PROCESSADOR do modelo original, pois ele não foi alterado
        self.processor = BlipProcessor.from_pretrained(original_model_name)

        print(f"Carregando MODELO de: {self.model_path}")
        # Carrega o MODELO do nosso checkpoint treinado
        self.model = BlipForConditionalGeneration.from_pretrained(self.model_path).to(self.device)
        print("Modelo carregado com sucesso.")

        # Inicializa o tradutor
        self.translator = GoogleTranslator(source='en', target='pt')
        print("CaptionService pronto.")

    def generate_caption(self, image_stream):
        """
        Recebe um stream de imagem, gera e traduz a legenda.
        Este método será chamado a cada requisição da API.
        """
        try:
            # Abre a imagem a partir do stream de dados
            image = Image.open(image_stream).convert("RGB")

            # Processa a imagem e gera a legenda em inglês
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            output = self.model.generate(**inputs, max_new_tokens=50)
            english_caption = self.processor.decode(output[0], skip_special_tokens=True)

            # Traduz a legenda para português
            portuguese_caption = self.translator.translate(english_caption)

            return portuguese_caption

        except Exception as e:
            print(f"Erro ao gerar legenda: {e}")
            return "Erro ao processar a imagem."