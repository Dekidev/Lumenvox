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