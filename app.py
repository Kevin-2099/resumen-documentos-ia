# ============================================
# Importar librerías
# ============================================

from transformers import pipeline
import pdfplumber
import gradio as gr
import csv
import os
from datetime import datetime
from langdetect import detect

# ============================================
# Cargar modelo Hugging Face
# ============================================

resumidor = pipeline("summarization", model="facebook/bart-large-cnn")

# ============================================
# Guardar registros de resúmenes generados
# ============================================

def guardar_log(nombre_archivo, resumen, idioma, nivel):
    nombre_log = "resumenes_log.csv"
    resumen_corto = resumen[:120].replace("\n", " ")
    fila = [datetime.now().isoformat(), nombre_archivo, idioma, nivel, resumen_corto]
    existe = os.path.isfile(nombre_log)
    
    with open(nombre_log, mode="a", newline='', encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if not existe:
            escritor.writerow(["fecha", "archivo", "idioma", "nivel", "resumen"])
        escritor.writerow(fila)

# ============================================
# Función principal para resumir PDF
# ============================================

def resumir_archivo(archivo, nivel, formato, progreso=gr.Progress()):
    texto = ""
    num_paginas = 0
    try:
        with pdfplumber.open(archivo.name) as pdf:
            limite = min(10, len(pdf.pages))
            for i, pagina in enumerate(pdf.pages[:limite]):
                contenido = pagina.extract_text()
                if contenido:
                    texto += contenido + "\n"
                progreso((i + 1) / limite)
            num_paginas = limite
    except:
        return "❌ Error: No se pudo procesar el archivo PDF.", None

    texto = texto.replace("\n", " ").strip()
    if len(texto) < 300:
        return "❌ El documento es demasiado corto para generar un resumen.", None

    # Detectar idioma
    try:
        idioma = detect(texto)
    except:
        idioma = "desconocido"

    # Configurar longitud del resumen según el nivel
    if nivel == "Breve":
        max_len, min_len = 80, 30
    elif nivel == "Medio":
        max_len, min_len = 150, 60
    else:
        max_len, min_len = 250, 100

    # Fragmentar texto y resumir
    fragmentos = [texto[i:i+700] for i in range(0, len(texto), 700)][:5]
    resúmenes = resumidor(fragmentos, max_length=max_len, min_length=min_len, do_sample=False)
    resumen_total = " ".join([r["summary_text"] for r in resúmenes]).strip()

    # Limpiar texto
    resumen_total = " ".join(resumen_total.split())

    # Crear formato de salida
    palabras_originales = len(texto.split())
    palabras_resumen = len(resumen_total.split())

    if formato == "Markdown":
        resumen_formateado = f"""
## 🧠 Resumen ({nivel})
🌐 **Idioma detectado:** `{idioma.upper()}`

---

{resumen_total}

---

### 📊 Estadísticas
- **Páginas procesadas:** {num_paginas}
- **Palabras originales:** {palabras_originales}
- **Palabras en resumen:** {palabras_resumen}
"""
    elif formato == "Emojis":
        resumen_formateado = (
            f"🧠 *Resumen ({nivel})*\n"
            f"🌐 Idioma detectado: {idioma.upper()}\n\n"
            f"📄 {resumen_total}\n\n"
            f"📊 **Estadísticas:**\n"
            f"➡️ Páginas procesadas: {num_paginas}\n"
            f"🔠 Palabras originales: {palabras_originales}\n"
            f"📝 Palabras en resumen: {palabras_resumen}\n"
        )
    else:  # Bullets
        resumen_formateado = (
            f"• **Nivel:** {nivel}\n"
            f"• **Idioma:** {idioma.upper()}\n"
            f"• **Páginas:** {num_paginas}\n"
            f"• **Original:** {palabras_originales} palabras\n"
            f"• **Resumen:** {palabras_resumen} palabras\n\n"
            f"🧾 **Contenido:**\n{resumen_total}"
        )

    # Guardar archivo de salida
    with open("resumen_salida.txt", "w", encoding="utf-8") as f:
        f.write(resumen_formateado)

    guardar_log(archivo.name, resumen_total, idioma, nivel)

    return resumen_formateado, "resumen_salida.txt"

# ============================================
# Interfaz visual con Gradio
# ============================================

interfaz = gr.Interface(
    fn=resumir_archivo,
    inputs=[
        gr.File(label="📄 Sube tu documento PDF (en español o inglés)"),
        gr.Radio(["Breve", "Medio", "Largo"], label="🧩 Nivel de detalle", value="Medio"),
        gr.Radio(["Markdown", "Emojis", "Bullets"], label="🎨 Formato de salida", value="Markdown")
    ],
    outputs=[
        gr.Markdown(label="🧠 Resumen generado por IA"),
        gr.File(label="⬇️ Descargar resumen")
    ],
    title="📚 Resumen Inteligente de Documentos con IA (v2)",
    description=(
        "Sube un documento PDF y obtén un resumen automático de alta calidad usando el modelo BART de Facebook. "
        "Selecciona el nivel de detalle y el formato de salida (Markdown, Emojis o Bullets)."
    ),
    theme="compact"
)

# ============================================
# Lanzar la aplicación
# ============================================

if __name__ == "__main__":
    interfaz.launch(share=True)
