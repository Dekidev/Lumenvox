# Lumenvox/backend/app.py

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, send_file
from services.caption_service import CaptionService
from services.tts_service import TTSService
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# Cria as instâncias dos nossos serviços
print("Criando instâncias dos serviços...")
caption_service = CaptionService()
tts_service = TTSService()
print("Instâncias criadas.")

@app.route('/describe', methods=['POST'])
def describe_image():
    if 'image' not in request.files:
        # Este tipo de erro retorna JSON
        return {"error": "Nenhum arquivo de imagem enviado"}, 400

    image_file = request.files['image']
    if image_file.filename == '':
        # Este tipo de erro retorna JSON
        return {"error": "Arquivo de imagem inválido"}, 400

    if image_file:
        # --- LÓGICA PRINCIPAL ---
        # 1. Gera a descrição em texto
        description_text = caption_service.generate_caption(image_file.stream)
        
        # 2. Converte o texto em áudio
        audio_bytes = tts_service.synthesize_speech(description_text)
        
        # 3. Retorna o ARQUIVO DE ÁUDIO (e não mais um JSON)
        return send_file(
            io.BytesIO(audio_bytes),
            mimetype='audio/mpeg',
            as_attachment=True, # Força o download
            download_name='descricao.mp3'
        )

@app.route('/', methods=['GET'])
def health_check():
    return {"status": "API do Lumenvox está no ar e funcionando!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)