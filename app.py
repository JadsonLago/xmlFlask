import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from models import NFe, create_tables
from xml_processor import process_all_xml_files, save_to_database

app = Flask(__name__)

# Pasta onde os arquivos serão temporariamente armazenados
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Certifique-se de que a pasta de uploads existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Rota para upload e processamento dos arquivos XML
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'xml_files' not in request.files:
        return "Nenhum arquivo selecionado", 400

    files = request.files.getlist('xml_files')

    # Salva cada arquivo na pasta de uploads
    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Processa todos os arquivos da pasta de uploads
    df = process_all_xml_files(app.config['UPLOAD_FOLDER'])
    save_to_database(df)

    # Exclui os arquivos após o processamento
    for file in files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

    return redirect(url_for('index'))

# Rota principal para exibir as NFes salvas
@app.route('/')
def index():
    nfes = NFe.select()
    return render_template('index.html', nfes=nfes)

if __name__ == '__main__':
    create_tables()  # Certifica-se de que as tabelas estão criadas
    app.run(debug=True)
