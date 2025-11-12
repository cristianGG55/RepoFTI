import re
import os
import tkinter as tk
from tkinter import filedialog

# =============================================================================
# 1. LÓGICA DE NEGOCIO (Mantenida intacta)
# =============================================================================

# Diccionario ampliado de tipos MIME comunes
MIME_TYPES = {
    # Texto y Web
    "txt": "text/plain",
    "html": "text/html",
    "htm": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "json": "application/json",
    "xml": "application/xml",
    "csv": "text/csv",
    
    # Documentos
    "pdf": "application/pdf",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    
    # Imágenes
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "svg": "image/svg+xml",
    "ico": "image/x-icon",
    "bmp": "image/bmp",
    
    # Audio
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
    "midi": "audio/midi",
    
    # Video
    "mp4": "video/mp4",
    "avi": "video/x-msvideo",
    "mpeg": "video/mpeg",
    "webm": "video/webm",
    "mov": "video/quicktime",
    
    # Archivos Comprimidos
    "zip": "application/zip",
    "rar": "application/vnd.rar",
    "7z": "application/x-7z-compressed",
    "tar": "application/x-tar",
    "gz": "application/gzip",

    # Código Fuente / Desarrollo
    "py": "text/x-python",
    "jsx": "text/jsx",  
    "ts": "application/typescript", 
    "tsx": "text/tsx",              
    "java": "text/x-java-source",
    "c": "text/x-c",
    "cpp": "text/x-c++",
    "sh": "application/x-sh",       
    
    # Documentación y Logs
    "md": "text/markdown",
    "log": "text/plain",
    "url": "application/internet-shortcut",

    # Otros
    "exe": "application/vnd.microsoft.portable-executable",
    "bin": "application/octet-stream" # Binario genérico 
    
    
}

def obtener_mime_type(nombre_archivo: str) -> str:
    """Identifica y devuelve el tipo MIME usando regex."""
    patron = r'\.([a-zA-Z0-9]+)$'
    coincidencia = re.search(patron, nombre_archivo)
    
    if coincidencia:
        extension = coincidencia.group(1).lower()
        if extension in MIME_TYPES:
            return MIME_TYPES[extension]
        else:
            return f"Extensión **no reconocida**: '.{extension}'"
    else:
        return "**El archivo no tiene una extensión reconocida.**"

# =============================================================================
# 2. CONFIGURACIÓN VISUAL 
# =============================================================================

COLOR_FONDO = "#2E2E2E"       # Gris oscuro (Fondo Ventana)
COLOR_TARJETA = "#3E3E3E"     # Gris medio (Fondo Panel)
COLOR_TEXTO = "#FFFFFF"       # Blanco
COLOR_SUBTEXTO = "#B0B0B0"    # Gris claro
COLOR_BOTON = "#007ACC"       # Azul Intenso
COLOR_BOTON_HOVER = "#005FA3" # Azul Oscuro
COLOR_EXITO = "#4CAF50"       # Verde
COLOR_ERROR = "#FFC107"       # Ámbar

FONT_TITULO = ("Segoe UI", 18, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_RESULTADO = ("Segoe UI", 14, "bold")
FONT_BOTON = ("Segoe UI", 11, "bold")

# =============================================================================
# 3. INTERFAZ GRÁFICA (Tkinter)
# =============================================================================

def seleccionar_archivo():
    """Maneja el evento del botón."""
    ruta_completa = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Todos los archivos", "*.*"),)
    )

    if ruta_completa:
        nombre_archivo = os.path.basename(ruta_completa)
        
        # 1. Actualizar nombre
        lbl_nombre_archivo.config(text=nombre_archivo, fg=COLOR_TEXTO)

        # 2. Ejecutar lógica
        resultado_bruto = obtener_mime_type(nombre_archivo)
        resultado_limpio = resultado_bruto.replace("**", "")

        # 3. Feedback visual (Color según éxito o error)
        if "no reconocida" in resultado_bruto or "no tiene" in resultado_bruto:
            color_resultado = COLOR_ERROR
        else:
            color_resultado = COLOR_EXITO

        lbl_resultado.config(text=resultado_limpio, fg=color_resultado)
        
    else:
        # Si cancela
        lbl_nombre_archivo.config(text="Ningún archivo seleccionado", fg=COLOR_SUBTEXTO)
        lbl_resultado.config(text="---", fg=COLOR_SUBTEXTO)

def main():
    """Construcción de la ventana."""
    global lbl_nombre_archivo, lbl_resultado

    root = tk.Tk()
    root.title("Detector MIME Pro")
    root.geometry("550x400")
    root.configure(bg=COLOR_FONDO)
    root.resizable(False, False)

    # --- Frame Central (Tarjeta Flotante) ---
    frame_central = tk.Frame(root, bg=COLOR_TARJETA, padx=30, pady=30)
    frame_central.place(relx=0.5, rely=0.5, anchor="center", width=480)

    # Título
    tk.Label(frame_central, text="Detector de Tipos MIME", font=FONT_TITULO, 
             bg=COLOR_TARJETA, fg=COLOR_TEXTO).pack(pady=(0, 20))

    # Botón Estilizado (Flat)
    btn = tk.Button(
        frame_central,
        text="📂  SELECCIONAR ARCHIVO",
        command=seleccionar_archivo,
        font=FONT_BOTON,
        bg=COLOR_BOTON,
        fg="white",
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=20, pady=10
    )
    btn.pack(fill=tk.X, pady=10)

    # Nombre del archivo (Label)
    lbl_nombre_archivo = tk.Label(frame_central, text="Ningún archivo seleccionado", 
                                  font=("Segoe UI", 10, "italic"), bg=COLOR_TARJETA, fg=COLOR_SUBTEXTO)
    lbl_nombre_archivo.pack(pady=5)

    # Línea divisoria simple
    tk.Frame(frame_central, height=1, bg="#555555").pack(fill=tk.X, pady=15)

    # Título Resultado
    tk.Label(frame_central, text="TIPO DETECTADO:", font=("Segoe UI", 9, "bold"), 
             bg=COLOR_TARJETA, fg=COLOR_SUBTEXTO).pack()

    # Resultado Final (Label)
    lbl_resultado = tk.Label(frame_central, text="---", font=FONT_RESULTADO, 
                             bg=COLOR_TARJETA, fg=COLOR_SUBTEXTO, wraplength=400)
    lbl_resultado.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()