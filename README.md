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

## 📄 Licencia

Este proyecto se distribuye bajo una **licencia propietaria con acceso al código (source-available)**.

El código fuente se pone a disposición únicamente para fines de **visualización, evaluación y aprendizaje**.

❌ No está permitido copiar, modificar, redistribuir, sublicenciar, ni crear obras derivadas del software o de su código fuente sin autorización escrita expresa del titular de los derechos.

❌ El uso comercial del software, incluyendo su oferta como servicio (SaaS), su integración en productos comerciales o su uso en entornos de producción, requiere un **acuerdo de licencia comercial independiente**.

📌 El texto **legalmente vinculante** de la licencia es la versión en inglés incluida en el archivo `LICENSE`. 

Se proporciona una traducción al español en `LICENSE_ES.md` únicamente con fines informativos. En caso de discrepancia, prevalece la versión en inglés.

## 🧠 Autor
Kevin-2099
