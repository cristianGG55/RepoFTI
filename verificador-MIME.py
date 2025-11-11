import re
import sys

# Diccionario de extensiones de archivo a tipos MIME (MIME_TYPES)
MIME_TYPES = {
    "txt": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "json": "application/json",
    "xml": "application/xml",
    "pdf": "application/pdf",
    "zip": "application/zip",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "mp4": "video/mp4",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    # Puedes ampliarlo
}

def obtener_mime_type(nombre_archivo: str) -> str:
    """
    Identifica y devuelve el tipo MIME del archivo usando expresiones regulares.
    """
    
    # Patrón para capturar la extensión: punto seguido de uno o más caracteres 
    # alfanuméricos al final de la cadena.
    patron = r'\.([a-zA-Z0-9]+)$'
    
    coincidencia = re.search(patron, nombre_archivo)
    
    if coincidencia:
        # Extraer y normalizar a minúsculas la extensión capturada (grupo 1)
        extension = coincidencia.group(1).lower()
        
        # Buscar en el diccionario
        if extension in MIME_TYPES:
            return MIME_TYPES[extension]
        else:
            return f"Extensión **no reconocida**: '.{extension}'"
    else:
        # No se encontró una extensión siguiendo el patrón
        return "**El archivo no tiene una extensión reconocida (o carece de ella).**"

# ----------------------------------------------
## 🚀 Función Principal para Ejecución
# ----------------------------------------------

def main():
    print("--- 🔍 Detector de Tipos MIME por Consola ---")
    print("Ingrese el nombre del archivo para identificar su tipo MIME.")
    print("Escriba 'salir' o presione Ctrl+C para finalizar.\n")
    
    while True:
        try:
            # 1. Solicitar el nombre del archivo por entrada (consola)
            nombre_archivo = input("Nombre del archivo (ej: documento.pdf): ").strip()
            
            if nombre_archivo.lower() == 'salir':
                break
            
            if not nombre_archivo:
                print("Por favor, ingrese un nombre de archivo válido.")
                continue

            # 2. Obtener y mostrar el resultado
            mime = obtener_mime_type(nombre_archivo)
            
            print(f"\nArchivo ingresado: **{nombre_archivo}**")
            print(f"Resultado MIME: **{mime}**\n")
            print("-" * 40)

        except KeyboardInterrupt:
            # Captura Ctrl+C para salir limpiamente
            print("\nSaliendo del programa.")
            sys.exit(0)
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            
if __name__ == "__main__":
    main()