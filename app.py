import os
import io
import shutil
import uuid
import time
import json
from flask import (
    Flask,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    Response,
    session,
    send_from_directory,
)
from pypdf import PdfWriter, PdfReader
from werkzeug.utils import secure_filename
import fitz  

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.config["SECRET_KEY"] = "uma-chave-secreta-muito-segura-e-diferente"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --- FUNÇÃO DE UNIFICAÇÃO E COMPRESSÃO ---
def unificar_e_comprimir_pdfs(caminhos_pdf, stream_callback=None):
    relatorio = {"sucesso": [], "falha": []}

    writer = PdfWriter()
    for i, pdf_path in enumerate(caminhos_pdf):
        nome_ficheiro = os.path.basename(pdf_path)
        try:
            if stream_callback:
                stream_callback(
                    "processando", f"Lendo {nome_ficheiro}", i + 1, len(caminhos_pdf)
                )
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                writer.append(reader)
            relatorio["sucesso"].append(nome_ficheiro)
            if stream_callback:
                stream_callback("sucesso", nome_ficheiro)
        except Exception as e:
            print(f"ERRO ao ler '{nome_ficheiro}': {e}")
            relatorio["falha"].append(nome_ficheiro)
            if stream_callback:
                stream_callback("falha", nome_ficheiro)

    if not writer.pages:
        return None, relatorio

    buffer_unificado = io.BytesIO()
    writer.write(buffer_unificado)
    buffer_unificado.seek(0)

    try:
        if stream_callback:
            stream_callback(
                "processando",
                "Aplicando compressão avançada...",
                len(caminhos_pdf),
                len(caminhos_pdf),
            )
        doc_pdf = fitz.open("pdf", buffer_unificado.read())
        buffer_comprimido_bytes = doc_pdf.tobytes(garbage=4, deflate=True)
        doc_pdf.close()
        buffer_final = io.BytesIO(buffer_comprimido_bytes)
        if stream_callback:
            stream_callback("sucesso", "Compressão finalizada!")
        return buffer_final, relatorio
    except Exception as e:
        print(f"ERRO durante a compressão com PyMuPDF: {e}")
        relatorio["falha"].append("Compressão Avançada")
        if stream_callback:
            stream_callback("falha", "Compressão Avançada")
        return buffer_unificado, relatorio


# --- ROTAS FLASK ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf_files" not in request.files:
            flash("Nenhum ficheiro selecionado!")
            return redirect(request.url)
        files = request.files.getlist("pdf_files")
        if not files or all(f.filename == "" for f in files):
            flash("Nenhum ficheiro selecionado!")
            return redirect(request.url)
        session_id = str(uuid.uuid4())
        session_folder_path = os.path.join(app.config["UPLOAD_FOLDER"], session_id)
        os.makedirs(session_folder_path)
        for file in files:
            if file and file.filename.lower().endswith(".pdf"):
                filename = secure_filename(file.filename)
                file.save(os.path.join(session_folder_path, filename))
        nome_final = secure_filename(
            request.form.get("output_filename", "documento_unificado.pdf")
        )
        if not nome_final.lower().endswith(".pdf"):
            nome_final += ".pdf"
        return redirect(
            url_for("processar", session_id=session_id, nome_final=nome_final)
        )
    return render_template("index.html")


@app.route("/processar/<session_id>/<nome_final>")
def processar(session_id, nome_final):
    return render_template("process.html", session_id=session_id, nome_final=nome_final)


@app.route("/stream/<session_id>/<nome_final>")
def stream(session_id, nome_final):
    url_de_download = url_for("download", session_id=session_id, nome_final=nome_final)

    def generate_events(url_download):
        session_folder_path = os.path.join(app.config["UPLOAD_FOLDER"], session_id)
        if not os.path.isdir(session_folder_path):
            yield f'data: {json.dumps({"tipo": "erro", "mensagem": "Sessão não encontrada."})}\n\n'
            return
        caminhos_pdf = sorted(
            [
                os.path.join(session_folder_path, f)
                for f in os.listdir(session_folder_path)
                if f.lower().endswith(".pdf")
            ]
        )

        def stream_callback(tipo, nome_ficheiro, atual=0, total=0):
            data = json.dumps(
                {
                    "tipo": tipo,
                    "nome_ficheiro": nome_ficheiro,
                    "atual": atual,
                    "total": total,
                }
            )
            yield f"data: {data}\n\n"

        yield from stream_callback("inicio", "", 0, len(caminhos_pdf))
        buffer_pdf_final, relatorio = unificar_e_comprimir_pdfs(
            caminhos_pdf, stream_callback
        )
        if buffer_pdf_final:
            caminho_final = os.path.join(session_folder_path, nome_final)
            with open(caminho_final, "wb") as f:
                f.write(buffer_pdf_final.getbuffer())

            yield from stream_callback("finalizado", url_download)
        else:
            yield from stream_callback("erro_final", "Nenhum PDF pôde ser processado.")

    return Response(generate_events(url_de_download), mimetype="text/event-stream")


@app.route("/download/<session_id>/<nome_final>")
def download(session_id, nome_final):
    session_folder_path = os.path.join(app.config["UPLOAD_FOLDER"], session_id)
    try:
        return send_from_directory(session_folder_path, nome_final, as_attachment=True)
    finally:
        try:
            shutil.rmtree(session_folder_path)
            print(f"Pasta temporária {session_folder_path} removida.")
        except Exception as e:
            print(f"Erro ao remover pasta temporária: {e}")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
