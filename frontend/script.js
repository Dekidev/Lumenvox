// CONTEÚDO PARA O frontend/script.js

class AudioDescricaoApp {
  constructor() {
    this.initializeElements();
    this.bindEvents();

    this.lastFile = null;
    this.lastGeneratedCaption = "";
    this.lastAudio = null;
    this.axiosController = null;
  }

  initializeElements() {
    // Componentes de Upload
    this.uploadZone = document.getElementById("uploadZone");
    this.fileInput = document.getElementById("fileInput");
    this.uploadBtn = document.getElementById("uploadBtn");
    this.uploadBtnText = this.uploadBtn.querySelector(".upload-btn__text");
    this.fileList = document.getElementById("fileList");
    this.statusArea = document.getElementById("status-area");

    // Componentes de Resultado
    this.resultDisplayArea = document.getElementById("result-display-area");
    this.descriptionTextContent = document.getElementById(
      "description-text-content"
    );

    // Componentes de Feedback
    this.feedbackSection = document.getElementById("feedback-section");
    this.goodFeedbackBtn = document.getElementById("good-feedback-btn");
    this.badFeedbackBtn = document.getElementById("bad-feedback-btn");
    this.correctionArea = document.getElementById("correction-area");
    this.correctionText = document.getElementById("correction-text");
    this.submitCorrectionBtn = document.getElementById("submit-correction-btn");
  }

  bindEvents() {
    this.uploadZone.addEventListener("click", () => this.fileInput.click());
    this.uploadZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      this.uploadZone.classList.add("upload-zone--dragover");
    });
    this.uploadZone.addEventListener("dragleave", () =>
      this.uploadZone.classList.remove("upload-zone--dragover")
    );
    this.uploadZone.addEventListener("drop", (e) => this.handleFileDrop(e));

    this.fileInput.addEventListener("change", (e) => this.handleFileSelect(e));

    this.uploadBtn.addEventListener("click", () => {
      const currentAction = this.uploadBtnText.textContent;
      if (currentAction === "CANCELAR") {
        this.cancelGeneration();
      } else if (currentAction.startsWith("OUVIR NOVAMENTE")) {
        this.replayAudio();
      }
    });

    this.goodFeedbackBtn.addEventListener("click", () =>
      this.sendFeedback("good")
    );
    this.badFeedbackBtn.addEventListener("click", () =>
      this.correctionArea.classList.remove("hidden")
    );
    this.submitCorrectionBtn.addEventListener("click", () => {
      const userCorrection = this.correctionText.value;
      if (userCorrection.trim() === "")
        return alert("Por favor, escreva sua descrição.");
      this.sendFeedback("bad", userCorrection);
    });
  }

  handleFileDrop(e) {
    e.preventDefault();
    this.uploadZone.classList.remove("upload-zone--dragover");
    if (e.dataTransfer.files.length) {
      this.addAndProcessFile(e.dataTransfer.files[0]);
    }
  }

  handleFileSelect(e) {
    if (e.target.files.length) {
      this.addAndProcessFile(e.target.files[0]);
    }
  }

  addAndProcessFile(file) {
    if (!file.type.startsWith("image/")) {
      alert("Por favor, envie apenas arquivos de imagem.");
      return;
    }
    this.lastFile = file;
    this.renderFileList();

    this.feedbackSection.classList.add("hidden");
    this.resultDisplayArea.classList.add("hidden");
    this.statusArea.textContent = "";
    this.lastAudio = null;

    this.uploadBtn.disabled = true;
    this.uploadBtnText.textContent = "GERAR AUDIODESCRIÇÃO";

    this.generateDescription();
  }

  renderFileList() {
    if (!this.lastFile) {
      this.fileList.innerHTML = "";
      return;
    }
    this.fileList.innerHTML = `
            <div class="file-item">
                <div class="file-info">
                    <div class="file-preview">🖼️</div>
                    <div class="file-details">
                        <h4>${this.lastFile.name}</h4>
                        <p>${(this.lastFile.size / 1024 / 1024).toFixed(
                          2
                        )} MB</p>
                    </div>
                </div>
            </div>`;
  }

  replayAudio() {
    if (this.lastAudio) {
      this.lastAudio.currentTime = 0;
      this.lastAudio.play();
    }
  }

  async generateDescription() {
    if (!this.lastFile) return;

    const formData = new FormData();
    formData.append("image", this.lastFile);

    this.statusArea.textContent = "Enviando imagem e gerando áudio...";
    this.uploadBtn.disabled = false;
    this.uploadBtnText.textContent = "CANCELAR";
    this.uploadBtn.classList.add("upload-btn--loading");

    this.axiosController = new AbortController();

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/describe",
        formData,
        {
          responseType: "blob",
          signal: this.axiosController.signal,
        }
      );

      this.lastGeneratedCaption = decodeURIComponent(
        response.headers["x-generated-caption"]
      );
      const audioBlob = response.data;
      const audioUrl = URL.createObjectURL(audioBlob);
      this.lastAudio = new Audio(audioUrl);
      this.lastAudio.play();

      this.descriptionTextContent.textContent = this.lastGeneratedCaption;
      this.statusArea.textContent = "Audiodescrição gerada! O que você achou?";

      this.uploadBtnText.textContent = "OUVIR NOVAMENTE 🔊";
      this.uploadBtn.classList.remove("upload-btn--loading");

      this.resultDisplayArea.classList.remove("hidden");
      this.feedbackSection.classList.remove("hidden");
    } catch (error) {
      if (axios.isCancel(error)) {
        this.statusArea.textContent =
          "Geração cancelada. Selecione um ficheiro para começar.";
      } else {
        console.error("Erro:", error);
        this.statusArea.textContent =
          "Ocorreu um erro ao gerar a audiodescrição. Tente novamente.";
      }
      this.uploadBtnText.textContent = "GERAR AUDIODESCRIÇÃO";
      this.uploadBtn.disabled = true;
      this.uploadBtn.classList.remove("upload-btn--loading");
    } finally {
      this.axiosController = null;
    }
  }

  cancelGeneration() {
    if (this.axiosController) {
      this.axiosController.abort();
    }
  }

  async sendFeedback(rating, correctedCaption = null) {
    this.statusArea.textContent = "Obrigado pelo seu feedback!";
    this.feedbackSection.classList.add("hidden");
    this.correctionArea.classList.add("hidden");
    this.correctionText.value = "";

    const feedbackFormData = new FormData();
    feedbackFormData.append("image", this.lastFile);
    feedbackFormData.append("generated_caption", this.lastGeneratedCaption);
    feedbackFormData.append("rating", rating);
    if (correctedCaption) {
      feedbackFormData.append("corrected_caption", correctedCaption);
    }

    try {
      await axios.post("http://127.0.0.1:5000/feedback", feedbackFormData);
    } catch (error) {
      console.error("Erro ao enviar feedback:", error);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.app = new AudioDescricaoApp();
});
