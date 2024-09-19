import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui import VentanaPrincipal, resource_path  

def main():
    try:
        app = QApplication(sys.argv)
        ventana = VentanaPrincipal()
        
        # Establecer el icono de la ventana
        ventana.setWindowIcon(QIcon(resource_path('descarga.jpeg')))  # Ruta a tu imagen
        
        ventana.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
