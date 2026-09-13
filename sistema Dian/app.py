import os
import re
import uuid
import time
import pandas as pd
import pymupdf
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Coordenadas X aproximadas de las columnas 45 y 46 en el formulario DIAN
# Descubiertas mediante análisis del PDF de prueba:
#   x~111.6 = Cantidad de bultos remitido (campo 45)
#   x~195.6 = Cantidad de bultos recibido (campo 46)
X_REMITIDO = 111.6
X_RECIBIDO = 195.6
X_TOLERANCE = 25  # tolerancia en puntos para la búsqueda por columna

# El valor de bultos está en una Y que es guia_y + 30 a + 90 puntos
Y_OFFSET_MIN = 30
Y_OFFSET_MAX = 90


def get_value_at(words, guide_y, target_x):
    """Busca el valor numérico más cercano a (target_x, guide_y + offset)."""
    candidates = [
        w for w in words
        if (guide_y + Y_OFFSET_MIN) <= w[1] <= (guide_y + Y_OFFSET_MAX)
        and abs(w[0] - target_x) <= X_TOLERANCE
        and re.match(r'^\d+$', w[4])
    ]
    if not candidates:
        return 0
    # Tomar el más cercano en X
    best = min(candidates, key=lambda w: abs(w[0] - target_x))
    return int(best[4])


def process_pdf(pdf_path):
    data = []
    try:
        doc = pymupdf.open(pdf_path)
        total_pages = len(doc)
        print(f"[INFO] Total de páginas: {total_pages}")
        t_start = time.time()

        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            # Extraer palabras con coordenadas: (x0, y0, x1, y1, "texto", ...)
            words = page.get_text("words")

            # Buscar todas las guías en la página
            for w in words:
                if not re.match(r'AMZPSR0\d+', w[4]):
                    continue

                guia = w[4]
                guide_y = w[1]

                remitido = get_value_at(words, guide_y, X_REMITIDO)
                recibido = get_value_at(words, guide_y, X_RECIBIDO)

                data.append({
                    "Guía": guia,
                    "Cantidad de bultos remitido": remitido,
                    "Cantidad de bultos recibido": recibido
                })

        doc.close()
        elapsed = time.time() - t_start
        print(f"[INFO] Completado en {elapsed:.1f}s — {len(data)} registros")

    except Exception as e:
        print(f"[ERROR] {e}")
        return None

    return data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(filepath)

        t0 = time.time()
        extracted_data = process_pdf(filepath)
        elapsed = round(time.time() - t0, 1)

        if os.path.exists(filepath):
            os.remove(filepath)

        if extracted_data is None:
            return jsonify({"error": "Error al procesar el archivo PDF"}), 500

        if not extracted_data:
            return jsonify({"error": "No se encontraron guías con el formato especificado."}), 404

        df = pd.DataFrame(extracted_data)
        excel_filename = f"extraccion_{uuid.uuid4().hex[:8]}.xlsx"
        excel_filepath = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)
        df.to_excel(excel_filepath, index=False)

        return jsonify({
            "message": "Archivo procesado exitosamente",
            "excel_url": f"/download/{excel_filename}",
            "records_found": len(extracted_data),
            "processing_time": elapsed
        })

    return jsonify({"error": "Archivo no permitido. Debe ser un PDF."}), 400


@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({"error": "Archivo no encontrado"}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(debug=False, host='0.0.0.0', port=port)
