# 📚 Resumen Inteligente de Documentos con IA (resumen-ia-demo)
Este es un proyecto educativo tipo Micro SaaS que permite subir documentos PDF y obtener un resumen automático generado con inteligencia artificial, usando el modelo BART de Facebook (facebook/bart-large-cnn).

## 👨‍💻 Tecnologías usadas
- Python 3.9+

- Transformers (Hugging Face)

- Torch

- Gradio

- pdfplumber

- langdetect

## 🚀 Demo en vivo
👉 [Ver la demo en Hugging Face](https://huggingface.co/spaces/Kevin-2099/resumen-documentos-ia)

## 📂 Cómo usar localmente
1.Clona el repositorio:

git clone https://github.com/Kevin-2099/resumen-documentos-ia.git

cd resumen-ia-demo

2.Instala las dependencias:

pip install -r requirements.txt

-Si no tienes requirements.txt, puedes usar:

pip install transformers pdfplumber gradio

3.Ejecuta la aplicación:

python app.py


## 📌 Características
✅ Subida de archivos PDF

✅ Extracción automática de texto (hasta 10 páginas)

✅ Generación de resumen con modelo BART (Hugging Face Transformers)

✅ Interfaz amigable con Gradio

✅ Detección automática de idioma (español / inglés) 🌐

✅ Barra de progreso durante el procesamiento ⏳

✅ Estadísticas automáticas: páginas procesadas, palabras originales y del resumen 📊

✅ Registro interno (CSV) de resúmenes generados

✅ Tres niveles de detalle:

- 🟢 Breve — resumen corto y directo

- 🟡 Medio — balance entre claridad y contexto

- 🔵 Largo — resumen detallado con matices

✅ Tres formatos de salida:

- 📝 Markdown

- 😃 Emojis

- 🔹 Bullets

✅ Fácil de ejecutar localmente o en la nube (Hugging Face Spaces)

## 🧠 Autor
Kevin-2099
