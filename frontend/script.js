// Espera o HTML carregar completamente antes de executar o código
document.addEventListener("DOMContentLoaded", () => {
  // 1. Pega as referências dos elementos HTML que vamos usar
  const imageUpload = document.getElementById("image-upload");
  const generateButton = document.getElementById("generate-button");
  const statusArea = document.getElementById("status-area");

  // 2. Adiciona um "ouvinte" para o evento de clique no botão
  generateButton.addEventListener("click", async () => {
    const file = imageUpload.files[0];

    // Validação: verifica se um arquivo foi selecionado
    if (!file) {
      statusArea.textContent =
        "Por favor, selecione um arquivo de imagem primeiro.";
      return;
    }

    // Prepara os dados para enviar (necessário para arquivos)
    const formData = new FormData();
    formData.append("image", file);

    // Atualiza a interface para o usuário
    statusArea.textContent =
      "Enviando imagem e gerando áudio... Por favor, aguarde.";
    generateButton.disabled = true;

    try {
      // 3. Faz a requisição POST para o nosso back-end
      const response = await fetch("http://127.0.0.1:5000/describe", {
        method: "POST",
        body: formData,
      });

      // Verifica se a resposta do servidor foi um sucesso
      if (!response.ok) {
        throw new Error(
          "Erro na resposta do servidor. Código: " + response.status
        );
      }

      // 4. Pega a resposta (áudio) e a toca
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();

      statusArea.textContent = "Audiodescrição gerada com sucesso!";
    } catch (error) {
      console.error("Erro:", error);
      statusArea.textContent =
        "Ocorreu um erro ao gerar a audiodescrição. Tente novamente.";
    } finally {
      // Reabilita o botão, independentemente do resultado
      generateButton.disabled = false;
    }
  });
});
