import edge_tts
import os
from PyPDF2 import PdfReader
from docx import Document

async def read_file_by_pages(file_path):
    """
    Detecta el tipo de archivo y extrae su contenido por páginas.
    Devuelve una lista de textos donde cada elemento es una página.
    """
    _, file_extension = os.path.splitext(file_path)  # Obtiene la extensión del archivo

    try:
        if file_extension == ".pdf":
            reader = PdfReader(file_path)
            pages = [page.extract_text() for page in reader.pages]
            return pages
        elif file_extension == ".docx":
            document = Document(file_path)
            paragraphs = [paragraph.text for paragraph in document.paragraphs]
            # Divide el contenido del documento en páginas simuladas de aproximadamente 800 caracteres por página
            pages = [paragraphs[i:i+800] for i in range(0, len(paragraphs), 800)]
            return pages
        elif file_extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            # Divide el contenido en páginas simuladas de aproximadamente 800 caracteres por página
            pages = [content[i:i+800] for i in range(0, len(content), 800)]
            return pages
        else:
            return f"Error: Formato de archivo no compatible ({file_extension})."
    except Exception as e:
        return f"Error al procesar el archivo: {e}"

async def text_to_speech(text, voice, rate, pitch, output_file="output.mp3"):
    """
    Convierte texto a voz y guarda el resultado como un archivo .mp3.
    """
    if not text.strip():
        return None, "El archivo está vacío o no contiene texto válido."
    if not voice:
        return None, "Por favor, selecciona una voz."
    
    voice_short_name = voice.split(" - ")[0]  # Obtiene el nombre corto de la voz
    rate_str = f"{rate:+d}%"  # Ajusta la velocidad
    pitch_str = f"{pitch:+d}Hz"  # Ajusta el tono

    communicate = edge_tts.Communicate(text, voice_short_name, rate=rate_str, pitch=pitch_str)
    try:
        await communicate.save(output_file)  # Guarda directamente como archivo mp3
        print(f"Archivo de audio generado: {os.path.abspath(output_file)}")
        return os.path.abspath(output_file), None
    except Exception as e:
        return None, f"Error al generar el archivo de audio: {e}"

async def generate_audiobook(file_path, voice, rate, pitch, output_dir="audiobook"):
    """
    Genera un audiolibro dividiendo el contenido del archivo por páginas y
    creando un archivo de audio para cada una.
    """
    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Leer el archivo por páginas
    pages = await read_file_by_pages(file_path)
    if isinstance(pages, str):  # Si hay un error en el procesamiento
        print(pages)
        return
    
    # Procesar cada página y generar su correspondiente archivo de audio
    for i, page_content in enumerate(pages, start=1):
        output_file = os.path.join(output_dir, f"pagina_{i}.mp3")
        print(f"Procesando página {i}...")
        audio_path, warning = await text_to_speech(page_content, voice, rate, pitch, output_file)
        if warning:
            print(f"Advertencia en la página {i}: {warning}")
        else:
            print(f"Página {i} convertida a audio: {audio_path}")

async def main():
    # Archivo a convertir en audiolibro
    file_path = "HOMBRE.pdf"  # Cambia esto al archivo que deseas procesar
    
    # Configuración de voz y parámetros
    voice = "es-BO-MarceloNeural"  # Ejemplo de voz
    rate = 0  # Velocidad estándar
    pitch = 0  # Tono estándar

    # Generar el audiolibro
    await generate_audiobook(file_path, voice, rate, pitch)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
