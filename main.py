import os
import yt_dlp
from dotenv import load_dotenv

def main():
    # 1. Cargar las variables del archivo .env
    load_dotenv()
    ruta_usb = os.getenv("RUTA_USB")

    # Validar que la ruta de la USB esté configurada
    if not ruta_usb:
        print("❌ Error: No se encontró la variable RUTA_USB en el archivo .env")
        return

    # Validar que la USB esté conectada (la ruta base debe existir)
    if not os.path.exists(ruta_usb):
        print(f"❌ Error: No se puede acceder a la ruta base de la USB ({ruta_usb}). ¿Está conectada?")
        return

    # ---------------------------------------------------------
    # NUEVA LÓGICA: Preguntar por la carpeta en la consola
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print("🎵 CONFIGURACIÓN DE CARPETA DE DESCARGA 🎵")
    print("="*50)
    nombre_carpeta = input("Escribe el nombre de la carpeta (o presiona Enter para usar la raíz de la USB): ").strip()

    # Determinar la ruta final de descarga
    if nombre_carpeta:
        ruta_descarga = os.path.join(ruta_usb, nombre_carpeta)
    else:
        ruta_descarga = ruta_usb

    # Verificar si es nueva o si ya existe
    if not os.path.exists(ruta_descarga):
        try:
            os.makedirs(ruta_descarga)
            print(f"\n✨ ¡Nueva carpeta creada exitosamente!: {ruta_descarga}")
        except Exception as e:
            print(f"\n❌ Error al crear la carpeta. Detalle: {e}")
            return
    else:
        if nombre_carpeta:
            print(f"\n📁 Usando la carpeta existente: {ruta_descarga}")
        else:
            print(f"\n📁 Usando la raíz de la USB: {ruta_descarga}")
    # ---------------------------------------------------------

    # 2. Leer los links del archivo txt
    archivo_links = "canciones.txt"
    if not os.path.exists(archivo_links):
        print(f"❌ Error: No se encontró el archivo {archivo_links}")
        return

    with open(archivo_links, "r", encoding="utf-8") as f:
        # Leemos las líneas y quitamos espacios en blanco o saltos de línea
        links = [linea.strip() for linea in f if linea.strip()]

    if not links:
        print("⚠️ El archivo de canciones está vacío.")
        return

    print(f"🎶 Se encontraron {len(links)} canciones para descargar.")

    # 3. Configurar las opciones de yt-dlp
    opciones = {
        'format': 'bestaudio/best', 
        # ATENCIÓN AQUÍ: Ahora usamos ruta_descarga en lugar de ruta_usb
        'outtmpl': os.path.join(ruta_descarga, '%(title)s.%(ext)s'), 
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
            {
                'key': 'FFmpegMetadata', 
            }
        ],
        'quiet': False, 
        'no_warnings': True
    }

    # 4. Iniciar la descarga
    print(f"\n🚀 Iniciando descargas...\n")
    with yt_dlp.YoutubeDL(opciones) as ydl:
        try:
            ydl.download(links)
            print(f"\n✅ ¡Éxito! Todas las canciones están en: {ruta_descarga}")
        except Exception as e:
            print(f"\n❌ Ocurrió un error durante la descarga: {e}")

if __name__ == "__main__":
    main()