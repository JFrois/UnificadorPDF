# 📄 Unificador e Compressor de PDFs

Uma aplicação web simples e poderosa construída com Python e Flask que permite aos utilizadores fazer o upload de múltiplos ficheiros PDF, unificá-los num único documento e aplicar uma compressão avançada para reduzir significativamente o tamanho final do ficheiro.

---

## ✨ Funcionalidades Principais

* **📤 Upload de Múltiplos Ficheiros:** Selecione quantos ficheiros PDF desejar a partir do seu computador.
* **🔗 Unificação Inteligente:** Os ficheiros são unificados em ordem alfabética para garantir uma sequência previsível.
* **🗜️ Compressão de Dupla Camada:**
    1.  **Compressão Lossless:** Otimiza o conteúdo de texto e vetores de cada página.
    2.  **Compressão de Imagens:** Utiliza o poder do PyMuPDF para re-comprimir imagens e remover dados redundantes, garantindo a máxima redução de tamanho.
* **🔄 Feedback em Tempo Real:** Acompanhe todo o processo através de uma barra de progresso e um log detalhado que mostra qual ficheiro está a ser processado, os sucessos e as falhas.
* **📝 Nome de Ficheiro Personalizado:** Defina o nome que desejar para o seu documento final.
* **✨ Interface Limpa:** Uma interface de utilizador simples, intuitiva e responsiva.

---

## 🛠️ Tecnologias Utilizadas

#### **Backend**
* **Python 3**
* **Flask:** Micro-framework web para a criação das rotas e da lógica da aplicação.
* **pypdf:** Biblioteca utilizada para a unificação inicial dos documentos PDF.
* **PyMuPDF (fitz):** Biblioteca de alta performance utilizada para a compressão avançada e otimização do PDF final.

#### **Frontend**
* **HTML5**
* **CSS3:** Para uma estilização moderna e responsiva.
* **JavaScript (Vanilla):** Para a interação com o utilizador e para a comunicação em tempo real com o servidor através de *Server-Sent Events (SSE)*.

---

## 🚀 Como Executar o Projeto Localmente

Siga estes passos para configurar e executar a aplicação no seu ambiente de desenvolvimento.

**1. Pré-requisitos:**
* Ter o [Python 3](https://www.python.org/downloads/) instalado.

**2. Clone ou Descarregue o Projeto:**
   Crie uma pasta para o projeto e coloque os ficheiros `app.py`, a pasta `templates/` e a pasta `uploads/` dentro dela.

**3. Crie e Ative um Ambiente Virtual:**
   É uma boa prática isolar as dependências do projeto.

   ```bash
   # Navegue até à pasta do projeto
   cd caminho/para/unificador_web

   # Crie o ambiente virtual
   python -m venv venv

   # Ative o ambiente virtual
   # No Windows:
   .\venv\Scripts\activate
   # No macOS/Linux:
   source venv/bin/activate
   ```

**4. Instale as Dependências:**
   Crie um ficheiro chamado `requirements.txt` na pasta principal do projeto com o seguinte conteúdo:

   ```txt
   Flask
   pypdf
   PyMuPDF
   ```

   Depois, instale todas as bibliotecas de uma vez com o comando:
   ```bash
   pip install -r requirements.txt
   ```

**5. Execute a Aplicação:**
   Com o ambiente virtual ativo, inicie o servidor Flask:
   ```bash
   flask run
   ```
   A aplicação estará a ser executada em `http://127.0.0.1:5000`.

---

## 📖 Como Usar

1.  Abra o seu navegador e aceda a **http://127.0.0.1:5000**.
2.  Clique no botão **"Selecionar Ficheiros PDF"** e escolha os documentos que deseja unificar.
3.  (Opcional) Altere o nome do ficheiro final no campo **"Nome do Ficheiro Final"**.
4.  Clique em **"Unificar e Descarregar"**.
5.  Será redirecionado para a página de processamento, onde poderá acompanhar o progresso em tempo real.
6.  Quando o processo terminar, um botão de **"Download"** aparecerá. Clique nele para descarregar o seu PDF unificado e comprimido.

---

## 📂 Estrutura do Projeto

```
unificador_web/
├── venv/                 # Pasta do ambiente virtual Python
├── uploads/              # Pasta temporária para os ficheiros enviados
├── templates/
│   ├── index.html        # Página inicial de upload
│   └── process.html      # Página de progresso em tempo real
├── app.py                # Lógica principal da aplicação Flask
└── requirements.txt      # Lista de dependências Python
```
