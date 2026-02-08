# 📚 Resumidor de Documentos con IA
Este es un proyecto tipo Micro SaaS que permite subir documentos PDF o pegar texto para obtener un resumen automático generado con inteligencia artificial.

Utiliza modelos de Hugging Face Transformers, optimizados para distintos tipos de entrada

## 👨‍💻 Tecnologías usadas
- Python 3.9+

- Transformers (Hugging Face)

  - facebook/bart-large-cnn
  
  - sshleifer/distilbart-cnn-12-6

- PyTorch

- Gradio

- pdfplumber

- langdetect

## 🚀 Demo en vivo
👉 [Ver la demo en Hugging Face](https://huggingface.co/spaces/Kevin-2099/resumen-documentos-ia)

## 📂 Cómo usar localmente
1.Clona el repositorio:

git clone https://github.com/Kevin-2099/resumen-documentos-ia.git

cd resumen-documentos-ia

2.Instala las dependencias:

pip install -r requirements.txt

-Si no tienes requirements.txt, puedes usar:

pip install transformers torch gradio pdfplumber langdetect

3.Ejecuta la aplicación:

python app.py


## 📌 Características
✅ Subida de archivos PDF o entrada de texto directo

✅ Extracción automática de texto (hasta 10 páginas por PDF)

✅ Generación de resúmenes con modelos BART (Hugging Face Transformers)

✅ Interfaz web amigable con Gradio

✅ Detección automática de idioma (español / inglés) 🌐

✅ Barra de progreso durante el procesamiento ⏳

✅ Estadísticas automáticas: fragmentos/páginas procesadas, palabras originales y del resumen 📊

✅ Registro interno (CSV) de resúmenes generados

✅ Tres niveles de detalle:

- 🟢 Breve — resumen corto y directo

- 🟡 Medio — equilibrio entre claridad y contexto

- 🔵 Largo — resumen detallado con más matices

✅ Múltiples formatos de salida:

- 📝 Markdown

- 📓 Markdown Avanzado (Notion / Obsidian)

- 😃 Emojis

- 🔹 Bullets estructurados (Pros / Contras / Recomendaciones / Conclusión)

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
