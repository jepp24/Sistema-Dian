import re
import time
import pymupdf

X_REMITIDO = 111.6
X_RECIBIDO = 195.6
X_TOLERANCE = 25
Y_OFFSET_MIN = 30
Y_OFFSET_MAX = 90

def get_value_at(words, guide_y, target_x):
    candidates = [
        w for w in words
        if (guide_y + Y_OFFSET_MIN) <= w[1] <= (guide_y + Y_OFFSET_MAX)
        and abs(w[0] - target_x) <= X_TOLERANCE
        and re.match(r'^\d+$', w[4])
    ]
    if not candidates:
        return 0
    best = min(candidates, key=lambda w: abs(w[0] - target_x))
    return int(best[4])

t0 = time.time()
results = []
with pymupdf.open("prueba.pdf.pdf") as doc:
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        words = page.get_text("words")
        for w in words:
            if not re.match(r'AMZPSR0\d+', w[4]):
                continue
            guia = w[4]
            guide_y = w[1]
            remitido = get_value_at(words, guide_y, X_REMITIDO)
            recibido = get_value_at(words, guide_y, X_RECIBIDO)
            results.append((page_num, guia, remitido, recibido))

elapsed = time.time() - t0
print(f"Tiempo: {elapsed:.1f}s | Total registros: {len(results)}")
print("\nPrimeros 20 resultados:")
for r in results[:20]:
    print(f"  Pag {r[0]:3d} | {r[1]} | remitido={r[2]} | recibido={r[3]}")
