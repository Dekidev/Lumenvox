from dotenv import load_dotenv
load_dotenv()

from urllib.parse import quote
from flask import Flask, request, send_file, jsonify
from services.caption_service import CaptionService
from services.tts_service import TTSService
from flask_cors import CORS
import io

app = Flask(__name__)
# Diz ao navegador para permitir que o JavaScript leia o nosso cabeçalho customizado
CORS(app, expose_headers=['X-Generated-Caption'])


print("Criando instâncias dos serviços...")
caption_service = CaptionService()
tts_service = TTSService()
print("Serviços prontos para operar.")


@app.route('/describe', methods=['POST'])
def describe_image_endpoint():
    if 'image' not in request.files: return jsonify({"error": "Nenhum arquivo de imagem enviado."}), 400
    uploaded_image = request.files['image']
    if not uploaded_image or uploaded_image.filename == '': return jsonify({"error": "O arquivo enviado é inválido."}), 400
    
    try:
        description_text = caption_service.generate_caption(uploaded_image.stream)
        audio_bytes = tts_service.synthesize_speech(description_text)
        
        response = send_file(io.BytesIO(audio_bytes), mimetype='audio/mpeg')
        
        # --- MELHORIA APLICADA AQUI ---
        # Usamos quote() para garantir que caracteres especiais (como acentos)
        # sejam enviados corretamente no cabeçalho.
        response.headers['X-Generated-Caption'] = quote(description_text)
        
        return response
    except Exception as e:
        print(f"ERRO INESPERADO NA ROTA /describe: {e}")
        return jsonify({"error": "Um erro inesperado ocorreu no servidor."}), 500

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    return jsonify({"status": "Feedback recebido com sucesso!"})

@app.route('/', methods=['GET'])
def health_check_endpoint():
    return jsonify({"status": "API do Lumenvox está no ar e funcionando!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)