from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QMenuBar, QAction, QMenu, QLabel, QStackedWidget
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from charts import (
    mostrar_graficas_consumado, mostrar_deudas_por_empresa, 
    consultar_creditos_por_empresa, filtrar_y_graficar,
    ver_consumado_por_cliente, ver_todas_las_ventas, ver_devoluciones_por_empresa
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JP FLOWERS - MENÚ PRINCIPAL")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()

        # Cambiar el fondo de la ventana
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))  # Fondo oscuro
        self.setPalette(palette)

        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        menu = QMenu("Opciones", self)
        menu_bar.addMenu(menu)

        action_salir = QAction("Salir", self)
        action_salir.triggered.connect(self.close)
        menu.addAction(action_salir)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.pantalla_principal = QWidget()
        pantalla_layout = QVBoxLayout()

        # Botones con estilo personalizado
        boton_cxc = self.crear_boton_con_icono("Clientes Internacionales (CXC)", "icons/monitor_icon.png")
        boton_cxc.clicked.connect(self.abrir_modulo_cxc)
        pantalla_layout.addWidget(boton_cxc)

        boton_rem_nal = self.crear_boton_con_icono("Clientes Nacionales (REM NAL)", "icons/database_icon.png")
        boton_rem_nal.clicked.connect(self.abrir_modulo_rem_nal)
        pantalla_layout.addWidget(boton_rem_nal)

        boton_facturas_nal = self.crear_boton_con_icono("Facturación Nacional", "icons/invoice_icon.png")
        boton_facturas_nal.clicked.connect(self.abrir_modulo_facturas_nal)
        pantalla_layout.addWidget(boton_facturas_nal)

        boton_creditos_reclamos = self.crear_boton_con_icono("Créditos y Reclamos", "icons/gear_icon.png")
        boton_creditos_reclamos.clicked.connect(self.abrir_modulo_creditos_reclamos)
        pantalla_layout.addWidget(boton_creditos_reclamos)

        self.pantalla_principal.setLayout(pantalla_layout)
        self.stacked_widget.addWidget(self.pantalla_principal)

        widget.setLayout(layout)

    # Función para crear botones con iconos y estilo personalizado
    def crear_boton_con_icono(self, texto, icono):
        boton = QPushButton(texto)
        boton.setFont(QFont('Arial', 12))
        boton.setIcon(QIcon(icono))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        return boton

    # Funciones para cambiar de módulo sin abrir nuevas ventanas
    def abrir_modulo_cxc(self):
        self.modulo_cxc = VentanaCXC(self.stacked_widget)
        self.stacked_widget.addWidget(self.modulo_cxc)
        self.stacked_widget.setCurrentWidget(self.modulo_cxc)

    def abrir_modulo_rem_nal(self):
        self.modulo_rem_nal = VentanaREMNAL(self.stacked_widget)
        self.stacked_widget.addWidget(self.modulo_rem_nal)
        self.stacked_widget.setCurrentWidget(self.modulo_rem_nal)

    def abrir_modulo_facturas_nal(self):
        self.modulo_facturas_nal = VentanaFacturasNAL(self.stacked_widget)
        self.stacked_widget.addWidget(self.modulo_facturas_nal)
        self.stacked_widget.setCurrentWidget(self.modulo_facturas_nal)

    def abrir_modulo_creditos_reclamos(self):
        self.modulo_creditos_reclamos = VentanaCreditosReclamos(self.stacked_widget)
        self.stacked_widget.addWidget(self.modulo_creditos_reclamos)
        self.stacked_widget.setCurrentWidget(self.modulo_creditos_reclamos)


# Ventana para Clientes Internacionales (CXC)
class VentanaCXC(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()

        boton_grafica_consumado = self.crear_boton_con_icono("Mostrar Ventas por Cliente", "icons/chart_icon.png")
        boton_grafica_consumado.clicked.connect(mostrar_graficas_consumado)
        layout.addWidget(boton_grafica_consumado)

        boton_deudas_empresa = self.crear_boton_con_icono("Mostrar Deudas por Empresa", "icons/debt_icon.png")
        boton_deudas_empresa.clicked.connect(mostrar_deudas_por_empresa)
        layout.addWidget(boton_deudas_empresa)

        boton_consultar_creditos = self.crear_boton_con_icono("Consultar Créditos por Empresa", "icons/credit_icon.png")
        boton_consultar_creditos.clicked.connect(consultar_creditos_por_empresa)
        layout.addWidget(boton_consultar_creditos)

        boton_filtrar_graficar = self.crear_boton_con_icono("Filtrar y Graficar Ventas por Cliente", "icons/filter_icon.png")
        boton_filtrar_graficar.clicked.connect(filtrar_y_graficar)
        layout.addWidget(boton_filtrar_graficar)

        boton_regresar = self.crear_boton_con_icono("Regresar al Menú Principal", "icons/back_icon.png")
        boton_regresar.clicked.connect(self.regresar_menu_principal)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

    # Función para crear botones con iconos y estilo personalizado
    def crear_boton_con_icono(self, texto, icono):
        boton = QPushButton(texto)
        boton.setFont(QFont('Arial', 12))
        boton.setIcon(QIcon(icono))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        return boton

    def regresar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)


# Ventana para Clientes Nacionales (REM NAL)
class VentanaREMNAL(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()

        boton_consumado_cliente = self.crear_boton_con_icono("Ver consumado de ventas por cliente", "icons/chart_icon.png")
        boton_consumado_cliente.clicked.connect(ver_consumado_por_cliente)
        layout.addWidget(boton_consumado_cliente)

        boton_todas_ventas = self.crear_boton_con_icono("Ver todas las ventas", "icons/sales_icon.png")
        boton_todas_ventas.clicked.connect(ver_todas_las_ventas)
        layout.addWidget(boton_todas_ventas)

        boton_devoluciones_empresa = self.crear_boton_con_icono("Ver devoluciones por empresa", "icons/return_icon.png")
        boton_devoluciones_empresa.clicked.connect(ver_devoluciones_por_empresa)
        layout.addWidget(boton_devoluciones_empresa)

        boton_regresar = self.crear_boton_con_icono("Regresar al Menú Principal", "icons/back_icon.png")
        boton_regresar.clicked.connect(self.regresar_menu_principal)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

    def crear_boton_con_icono(self, texto, icono):
        boton = QPushButton(texto)
        boton.setFont(QFont('Arial', 12))
        boton.setIcon(QIcon(icono))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        return boton

    def regresar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)


# Ventana para Facturación Nacional (FACTURAS NAL)
class VentanaFacturasNAL(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta es la ventana para Facturación Nacional"))

        boton_regresar = self.crear_boton_con_icono("Regresar al Menú Principal", "icons/back_icon.png")
        boton_regresar.clicked.connect(self.regresar_menu_principal)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

    def crear_boton_con_icono(self, texto, icono):
        boton = QPushButton(texto)
        boton.setFont(QFont('Arial', 12))
        boton.setIcon(QIcon(icono))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        return boton

    def regresar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)


# Ventana para Créditos y Reclamos
class VentanaCreditosReclamos(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta es la ventana para Créditos y Reclamos"))

        boton_regresar = self.crear_boton_con_icono("Regresar al Menú Principal", "icons/back_icon.png")
        boton_regresar.clicked.connect(self.regresar_menu_principal)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

    def crear_boton_con_icono(self, texto, icono):
        boton = QPushButton(texto)
        boton.setFont(QFont('Arial', 12))
        boton.setIcon(QIcon(icono))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        return boton

    def regresar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)