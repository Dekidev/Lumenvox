import os
import uuid

class FeedbackService:
    def __init__(self, base_path='feedback_data'):
        self.base_path = base_path
        self.good_path = os.path.join(base_path, 'dados_bons', 'imagens')
        self.correction_path = os.path.join(base_path, 'precisa_de_correcao', 'imagens')
        
        # Cria as pastas se elas não existirem
        os.makedirs(self.good_path, exist_ok=True)
        os.makedirs(self.correction_path, exist_ok=True)
        print("FeedbackService pronto. Pastas de feedback garantidas.")

    def save_feedback(self, image_file_storage, generated_caption, rating, corrected_caption=None):
        # Gera um nome de arquivo único para evitar sobreposições
        unique_id = str(uuid.uuid4())
        image_filename = f"{unique_id}.jpg"
        caption_filename = f"{unique_id}.txt"

        if rating == 'good':
            save_path = self.good_path
            caption_to_save = generated_caption
        elif rating == 'bad':
            save_path = self.correction_path
            caption_to_save = corrected_caption
        else:
            return # Não faz nada se a avaliação for inválida

        # Salva o arquivo de imagem
        image_filepath = os.path.join(save_path, image_filename)
        image_file_storage.save(image_filepath)

        # Salva o arquivo de legenda (.txt)
        caption_filepath = os.path.join(save_path.replace('imagens', ''), caption_filename)
        with open(caption_filepath, 'w', encoding='utf-8') as f:
            f.write(caption_to_save)
            
        print(f"Feedback salvo para a imagem {unique_id} com avaliação '{rating}'.")