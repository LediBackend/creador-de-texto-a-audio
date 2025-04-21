import edge_tts
import os

async def text_to_speech(text, voice, rate, pitch, output_file="output.mp3"):
    if not text.strip():
        return None, "Please enter text to convert."
    if not voice:
        return None, "Please select a voice."
    
    voice_short_name = voice.split(" - ")[0]  # Obtiene el nombre corto de la voz
    rate_str = f"{rate:+d}%"  # Ajusta la velocidad
    pitch_str = f"{pitch:+d}Hz"  # Ajusta el tono

    communicate = edge_tts.Communicate(text, voice_short_name, rate=rate_str, pitch=pitch_str)
    try:
        # Guarda directamente el audio como archivo mp3 en la ubicación especificada
        await communicate.save(output_file)
        print(f"Archivo guardado en: {os.path.abspath(output_file)}")
        return os.path.abspath(output_file), None
    except Exception as e:
        return None, f"Error al generar el archivo: {e}"

# Ejemplo de uso
async def main():
    text = "Hola, este es un ejemplo de generación de audio con Edge TTS."
    voice = "es-CR-JuanNeural"  # Ejemplo de voz
    rate = 5  # Velocidad estándar
    pitch = 10  # Tono estándar
    output_file = "mi_audio.mp3"  # Nombre del archivo de salida

    audio_path, warning = await text_to_speech(text, voice, rate, pitch, output_file)
    if warning:
        print(warning)
    else:
        print(f"¡Archivo de audio generado: {audio_path}!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
