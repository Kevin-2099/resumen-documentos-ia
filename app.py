# ============================================
# Importar librerías
# ============================================
import gradio as gr
import pdfplumber
import csv
import os
import re
from datetime import datetime
from transformers import pipeline
from langdetect import detect

# ============================================
# Cargar modelos Hugging Face
# ============================================
resumidor_pdf = pipeline("summarization", model="facebook/bart-large-cnn")
resumidor_texto = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# ============================================
# Guardar registros de resúmenes
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
# Función para extraer texto de PDF
# ============================================
def extraer_texto_desde_pdf(archivo_pdf):
    texto = ""
    try:
        with pdfplumber.open(archivo_pdf.name) as pdf:
            for pagina in pdf.pages[:10]:  # limitar a primeras 10 páginas
                contenido = pagina.extract_text()
                if contenido:
                    texto += contenido + "\n"
    except:
        return None, "❌ Error al procesar el PDF."
    return texto.replace("\n", " ").strip(), None

# ============================================
# Función para resumir texto o PDF
# ============================================
def resumir_general(tipo_entrada, archivo_pdf, texto_input, nivel, formato, progreso=gr.Progress()):
    if tipo_entrada == "PDF":
        if archivo_pdf is None:
            return "❌ Sube un PDF.", None
        texto, error = extraer_texto_desde_pdf(archivo_pdf)
        if error:
            return error, None
        nombre_archivo = archivo_pdf.name
    else:
        texto = texto_input.strip()
        if len(texto) < 300:
            return "❌ El texto es demasiado corto para resumir.", None
        nombre_archivo = "entrada_texto.txt"

    try:
        idioma = detect(texto)
    except:
        idioma = "desconocido"

    if nivel == "Breve":
        max_len, min_len = 80, 30
    elif nivel == "Medio":
        max_len, min_len = 150, 60
    else:
        max_len, min_len = 250, 100

    fragmentos = [texto[i:i+700] for i in range(0, len(texto), 700)][:5]
    res = resumidor_pdf(fragmentos, max_length=max_len, min_length=min_len, do_sample=False)
    resumen_total = " ".join([r["summary_text"] for r in res]).strip()

    palabras_originales = len(texto.split())
    palabras_resumen = len(resumen_total.split())

    # ==============================
    # Formatos de salida
    # ==============================
    if formato == "Markdown":
        resumen_formateado = f"""
## 🧠 Resumen ({nivel})
🌐 **Idioma detectado:** `{idioma.upper()}`
---
{resumen_total}
---
### 📊 Estadísticas
- **Fragmentos procesados:** {len(fragmentos)}
- **Palabras originales:** {palabras_originales}
- **Palabras en resumen:** {palabras_resumen}
"""
    elif formato == "Emojis":
        resumen_formateado = (
            f"🧠 Resumen ({nivel})\n"
            f"🌐 Idioma: {idioma.upper()}\n\n"
            f"📄 {resumen_total}\n\n"
            f"📊 Fragmentos: {len(fragmentos)}\n"
            f"🔠 Original: {palabras_originales}\n"
            f"📝 Resumen: {palabras_resumen}"
        )
    elif formato == "Markdown Avanzado":
        # Formato compatible con Notion/Obsidian
        resumen_formateado = f"""# Resumen ({nivel})
Idioma detectado: `{idioma.upper()}`
---
## Contenido
{resumen_total}
---
## Estadísticas
- Fragmentos procesados: {len(fragmentos)}
- Palabras originales: {palabras_originales}
- Palabras en resumen: {palabras_resumen}
*Este resumen está optimizado para Notion/Obsidian.*
"""
    else:
        resumen_formateado = (
            f"• Nivel: {nivel}\n"
            f"• Idioma: {idioma.upper()}\n"
            f"• Fragmentos: {len(fragmentos)}\n"
            f"• Palabras originales: {palabras_originales}\n"
            f"• Palabras resumen: {palabras_resumen}\n\n"
            f"Contenido:\n{resumen_total}"
        )

    with open("resumen_salida.txt", "w", encoding="utf-8") as f:
        f.write(resumen_formateado)

    guardar_log(nombre_archivo, resumen_total, idioma, nivel)
    return resumen_formateado, "resumen_salida.txt"

# ============================================
# App bullets: Pros / Contras / Recomendaciones / Conclusión
# ============================================
patron_conclusion = re.compile(r'\b(in conclusion|en conclusión|en general|overall)\b', re.IGNORECASE)

def es_conclusion(frase: str) -> bool:
    return bool(patron_conclusion.search(frase))

def buscar_conclusion_original(texto: str):
    m = re.search(r'(?i)\b(in conclusion|en conclusión|en general|overall)\b.*?(?:[.!?]|$)', texto, flags=re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0).strip().rstrip('.') + '.'
    return None

def unique_preserve_order(lst):
    seen = set()
    out = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def resumir_bullets(tipo_entrada, archivo_pdf, texto_input):
    try:
        if tipo_entrada == "PDF":
            if archivo_pdf is None:
                return "❌ Sube un PDF."
            texto, error = extraer_texto_desde_pdf(archivo_pdf)
            if error:
                return error
        else:
            texto = texto_input.strip()
            if len(texto) < 300:
                return "❌ El texto es demasiado corto para analizar."

        idioma = detect(texto)
        lang = "es" if idioma == "es" else "en"

        conclusion_original = buscar_conclusion_original(texto)

        resumen = resumidor_texto(texto, max_length=300, min_length=120, do_sample=False)
        resumen_text = resumen[0]["summary_text"]

        frases = []
        for f in re.split(r'\.\s+|\.\n+', resumen_text):
            f_strip = f.strip()
            if not f_strip:
                continue
            if es_conclusion(f_strip):
                frases.append(f_strip)
                continue
            if conclusion_original and conclusion_original.lower().split()[0] in f_strip.lower():
                frases.append(f_strip)
                continue
            subfrases = re.split(r', | y |; | pero | sin embargo | and | but | however | such as ', f_strip)
            frases.extend([s.strip() for s in subfrases if s.strip()])

        pros, cons, recomendaciones, conclusion = [], [], [], []

        # Clasificación por idioma
        if lang == "es":
            for s in frases:
                s_low = s.lower()
                if es_conclusion(s):
                    conclusion.append(s)
                    continue
                if any(word in s_low for word in [
                    "recomienda","sugerencia","aconseja","debe",
                    "es recomendable","es aconsejable","fundamental",
                    "es fundamental","necesario","es necesario","conviene",
                    "se recomienda","debería","es importante"
                ]):
                    recomendaciones.append(s)
                    continue
                if any(word in s_low for word in [
                    "mejora","beneficio","ventaja","eficiente",
                    "facilita","permitir","permite","optimiza",
                    "colaboración","transformando","adoptando",
                    "ofrecer","incrementa","aumenta","potencia",
                    "reduce costos","mejora la calidad","ahorra tiempo"
                ]):
                    pros.append(s)
                    continue
                if any(word in s_low for word in [
                    "problema","limitación","desventaja","pérdida",
                    "inconveniente","desafíos","desafío","limitaciones",
                    "riesgo","riesgos","preocupación","preocupaciones",
                    "costoso","difícil","complejo","barrera","obstáculo"
                ]):
                    cons.append(s)
                    continue
        else:
            for s in frases:
                s_low = s.lower()
                if es_conclusion(s):
                    conclusion.append(s)
                    continue
                if any(word in s_low for word in [
                    "to fully leverage","it is critical","should","must",
                    "recommend","invest","train","educate","policy",
                    "it is important","best practice","adopt","implement"
                ]):
                    recomendaciones.append(s)
                    continue
                if any(word in s_low for word in [
                    "risk","risks","challenge","problem","loss","issue",
                    "concern","concerns","lack","limitation","threat",
                    "danger","side effect","ethical","bias","privacy","security","costly","complex"
                ]):
                    cons.append(s)
                    continue
                if any(word in s_low for word in [
                    "improve","benefit","advantage","allow","efficient",
                    "productivity","personalized","leverage","enable",
                    "adopt","transform","deliver","opportunity",
                    "collaboration","optimize","enhance","save time",
                    "reduce cost","increase"
                ]):
                    pros.append(s)
                    continue

        # Conclusión original prioritaria
        if conclusion_original:
            conclusion = [conclusion_original]
            cons = [c for c in cons if conclusion_original.lower() not in c.lower()]

        pros = unique_preserve_order(pros)
        cons = unique_preserve_order(cons)
        recomendaciones = unique_preserve_order(recomendaciones)
        conclusion = unique_preserve_order(conclusion)

        if not pros:
            pros = ["No se identificaron pros claros." if lang == "es" else "No clear pros found."]
        if not cons:
            cons = ["No hay contras importantes identificadas." if lang == "es" else "No clear cons found."]
        if not recomendaciones:
            recomendaciones = ["No se encontraron recomendaciones específicas." if lang == "es" else "No recommendations found."]
        if not conclusion:
            conclusion = ["No se pudo determinar una conclusión clara." if lang == "es" else "No clear conclusion found."]

        bullets = [
            "✅ **Pros**: " + "; ".join(pros),
            "⚠️ **Contras**: " + "; ".join(cons),
            "🔧 **Recomendaciones**: " + "; ".join(recomendaciones),
            "📌 **Conclusión**: " + "; ".join(conclusion),
        ]

        return "\n".join(bullets)

    except Exception as e:
        return f"❌ No se pudo generar el resumen. Error: {str(e)}"

# ============================================
# Interfaz Gradio Unificada
# ============================================
with gr.Blocks(title="🧠 Resumidor de Documentos con IA") as app:

    gr.Markdown("# 🤖 Resumidor de documentos con IA")
    gr.Markdown("Resumen de PDF o Texto con dos herramientas en una.")

    with gr.Tabs():

        with gr.Tab("📄 Resumir General (PDF o Texto)"):
            tipo_entrada = gr.Radio(["Texto", "PDF"], value="Texto", label="Tipo de entrada")
            texto_input = gr.Textbox(label="Pega tu texto", lines=12)
            archivo_pdf = gr.File(label="Sube un PDF (opcional)")
            nivel = gr.Radio(["Breve", "Medio", "Largo"], value="Medio", label="Nivel de detalle")
            formato = gr.Radio(["Markdown", "Markdown Avanzado", "Emojis", "Bullets"], value="Markdown", label="Formato de salida")
            salida_pdf = gr.Markdown(label="Resumen generado")
            descarga = gr.File(label="Descargar resumen")
            boton_pdf = gr.Button("Generar resumen")
            boton_pdf.click(resumir_general, [tipo_entrada, archivo_pdf, texto_input, nivel, formato], [salida_pdf, descarga])

        with gr.Tab("📝 Resumir Texto en Bullets"):
            tipo_entrada_bullets = gr.Radio(["Texto", "PDF"], value="Texto", label="Tipo de entrada")
            texto_input_bullets = gr.Textbox(label="Pega tu texto", lines=12)
            archivo_pdf_bullets = gr.File(label="Sube un PDF (opcional)")
            salida_texto = gr.Textbox(label="Resumen en bullets", lines=12)
            boton_texto = gr.Button("Generar resumen en bullets")
            boton_texto.click(resumir_bullets, [tipo_entrada_bullets, archivo_pdf_bullets, texto_input_bullets], salida_texto)

# ============================================
# Lanzar app
# ============================================
if __name__ == "__main__":
    app.launch(share=True)
