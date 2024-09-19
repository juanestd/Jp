import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui import VentanaPrincipal  # Asegúrate de que este import sea correcto

def main():
    try:
        app = QApplication(sys.argv)
        ventana = VentanaPrincipal()  # Inicializar la ventana
        
        # Establecer el icono de la ventana
        ventana.setWindowIcon(QIcon('descarga.jpeg'))  # Ruta a tu imagen
        
        ventana.show()  # Mostrar la ventana principal
        sys.exit(app.exec())  # Iniciar el ciclo de eventos
    except Exception as e:
        print(f"Error: {e}")  # Captura cualquier error y lo muestra en la consola

if __name__ == "__main__":
    main()
