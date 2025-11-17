import re
import os
import tkinter as tk
from tkinter import filedialog
import mimetypes

# =============================================================================
# 1. LÓGICA PRINCIPAL DEL PROGRAMA
# =============================================================================

def obtener_mime_type(nombre_archivo: str) -> str:
    """
    Identifica y devuelve el tipo MIME usando mimetypes (basado en IANA).
    
    NOTA: Aunque mimetypes usa internamente una base de datos más completa,
    el analisis de la expresión regular es útil para extraer la extensión 
    y dar respuesta a casos sin extensión explícita.
    """
    
    # En las siguientes instrucciones se intenta extraer la extensión mediante regex (MÉTODO 1)
    
    # Cuándo hay una r'...' significa que el contenido entre las comillas está destinado a ser una expresión regular.
    # -patron- es una str que almacenará una expresión regular.
    patron = r'\.([a-zA-Z0-9]+)$'
    # Coincidencia es un objeto de tipo Match.
    # El misma puede devolver NULL (si no hay coincidencia) o...
    # Un objeto con 3 propiedades: span (ubicación de la coincidencia), group(0) y group(1) (texto que coincide con el patrón) 
    coincidencia = re.search(patron, nombre_archivo)
    
    # Si coincidencia no es NULL (el archivo tiene extensión), se busca el MIME type correspondiente a la extensión encontrada.
    if coincidencia:
        # mimetypes.guess_type() toma la ruta completa o el nombre del archivo.
        # Devuelve una tupla (mime_type, encoding). En este caso, la segunda variable (Codificación) se ignora porque no es relevante.
        mime_type, _ = mimetypes.guess_type(nombre_archivo)
        
        if mime_type:
            # El MIME type fué encontrado por mimetypes
            return mime_type
        else:
            # mimetypes no encontró la estensión (es válida pero desconocida para Python)
            # La extensión se pasa a minuscula y se muestra un mensaje
            extension = coincidencia.group(1).lower()
            return f"Extensión **no reconocida oficialmente**: '.{extension}'"
            
    else:
        # 2. Archivo sin extensión (o la extensión no cumple el patrón)
        # Se hace una última verificación para ver si mimetypes es capaz de 
        # detectar algo, aunque es poco probable sin extensión.
        mime_type, _ = mimetypes.guess_type(nombre_archivo)
        
        if mime_type:
            return mime_type # Solo por precaución
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