import sys
from PyQt5.QtWidgets import QApplication
from ui import VentanaPrincipal  # Asegúrate de que este import sea correcto

def main():
    try:
        app = QApplication(sys.argv)
        ventana = VentanaPrincipal()  # Inicializar la ventana
        ventana.show()  # Mostrar la ventana principal
        sys.exit(app.exec())  # Iniciar el ciclo de eventos
    except Exception as e:
        print(f"Error: {e}")  # Captura cualquier error y lo muestra en la consola

if __name__ == "__main__":
    main()
