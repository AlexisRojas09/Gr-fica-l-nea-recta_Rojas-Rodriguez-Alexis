"""
Interfaz gráfica para graficar funciones lineales
Basado en el estilo de la interfaz de consultas :D

Sistema de navegación entre frames:
- InputFrame: Ingreso de datos (m y b)
- GraphFrame: Muestra la gráfica de la función lineal
"""

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Tema oscuro para que se vea nice
ctk.set_appearance_mode("dark")

# Color azul para los widgets
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    """
    Clase principal de la aplicacion
    Maneja la navegacion entre diferentes frames
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Título de la ventana
        self.title("Graficador de Funciones Lineales")
        # Tamaño de la ventana
        self.geometry("1000x700")
        self.current_frame = None

        # Interceptar el cierre de la ventana para limpiar procesos en segundo plano
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Arrancamos con el frame de entrada de datos
        self.show_frame(InputFrame)

    def on_closing(self):
        """
        Maneja el evento de cierre de ventana
        Limpia las figuras de matplotlib y destruye la aplicación
        """
        plt.close('all')
        self.quit()
        self.destroy()

    def show_frame(self, frame_class, *args, **kwargs):
        """
        Método para cambiar entre frames
        Destruye el frame actual y crea el nuevo
        """
        if self.current_frame is not None:
            # Nos aseguramos de cerrar las figuras de matplotlib en memoria
            plt.close('all')
            self.current_frame.destroy()

        # Creamos el nuevo frame
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)


class InputFrame(ctk.CTkFrame):
    """
    Frame para ingresar los valores de m y b
    Valida que los datos sean numéricos
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        # Título
        self.title_label = ctk.CTkLabel(self, text="Función Lineal: f(x) = mx + b", font=("Arial", 28, "bold"))
        self.title_label.pack(pady=40)

        # Contenedor para los inputs
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=20, padx=20)

        # Etiqueta y campo para la pendiente (m)
        self.m_label = ctk.CTkLabel(self.input_frame, text="Pendiente (m):", font=("Arial", 16))
        self.m_label.grid(row=0, column=0, padx=20, pady=15)
        self.m_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ej. 2", width=150)
        self.m_entry.grid(row=0, column=1, padx=20, pady=15)

        # Etiqueta y campo para el término independiente (b)
        self.b_label = ctk.CTkLabel(self.input_frame, text="Término indep. (b):", font=("Arial", 16))
        self.b_label.grid(row=1, column=0, padx=20, pady=15)
        self.b_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ej. -3", width=150)
        self.b_entry.grid(row=1, column=1, padx=20, pady=15)

        # Botón para graficar
        self.graph_button = ctk.CTkButton(self, text="Graficar Función", command=self.validar_y_graficar, width=200, height=45, font=("Arial", 16))
        self.graph_button.pack(pady=40)

    def validar_y_graficar(self):
        """
        Valida los inputs y cambia al frame de la gráfica si son correctos
        """
        m_str = self.m_entry.get()
        b_str = self.b_entry.get()

        try:
            # Intentamos convertir a flotantes (acepta enteros y decimales)
            m = float(m_str)
            b = float(b_str)
            
            # Si es correcto, pasamos al frame de la gráfica
            self.master.show_frame(GraphFrame, m, b)
            
        except ValueError:
            # Si hay error (ej. letras, vacío), mostramos mensaje
            self.mensaje_error("Por favor, ingrese valores numéricos válidos para 'm' y 'b'.\n(No use letras ni deje los campos vacíos).")

    def mensaje_error(self, mensaje):
        """
        Muestra un mensaje de error en una ventana emergente
        """
        CTkMessagebox(title="Error de datos", message=mensaje, icon="cancel", option_1="Aceptar")


class GraphFrame(ctk.CTkFrame):
    """
    Frame que muestra la gráfica generada
    """
    def __init__(self, master, m, b, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        # Título de la gráfica
        signo_b = "+" if b >= 0 else "-"
        # Formateamos el título para que se vea bonito
        titulo_func = f"f(x) = {m}x {signo_b} {abs(b)}"
        
        self.titulo_label = ctk.CTkLabel(self, text=f"Gráfica de: {titulo_func}", font=("Arial", 24, "bold"))
        self.titulo_label.pack(pady=20)

        # Generamos la figura
        fig = self.generar_grafica(m, b)

        # Creamos un canvas para mostrar la gráfica
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=40, pady=10)

        # Botón para volver
        self.boton_volver = ctk.CTkButton(self, text="Volver", command=self.volver, width=150, height=40)
        self.boton_volver.pack(pady=20)

    def generar_grafica(self, m, b):
        """
        Genera la figura de matplotlib con la función lineal
        """
        # Valores de x (de -10 a 10)
        x = np.linspace(-10, 10, 400)
        # Ecuación de la recta
        y = m * x + b

        # Creamos la figura
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Graficamos la línea
        ax.plot(x, y, color='#1f538d', linewidth=2.5, label=f'f(x) = {m}x + {b}')
        
        # Estilo de la gráfica
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.axhline(0, color='black', linewidth=1.5) # Eje X
        ax.axvline(0, color='black', linewidth=1.5) # Eje Y
        
        ax.set_title("Función Lineal", fontsize=14)
        ax.set_xlabel("Eje X", fontsize=12)
        ax.set_ylabel("Eje Y", fontsize=12)
        ax.legend()

        # Ajustamos el layout
        fig.tight_layout()
        
        return fig

    def volver(self):
        """
        Regresa al frame de entrada de datos
        """
        self.master.show_frame(InputFrame)


# Ejecucion principal de la aplicacion (naiiiis)
if __name__ == "__main__":
    app = App()
    app.mainloop()
