from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QMenuBar, QAction, QMenu, QLabel, QStackedWidget, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize
from charts import (
    mostrar_graficas_consumado, mostrar_deudas_por_empresa, 
    consultar_creditos_por_empresa, filtrar_y_graficar,
    ver_consumado_por_cliente, ver_todas_las_ventas, ver_devoluciones_por_empresa
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JP FLOWERS - MENÚ PRINCIPAL")
        self.setGeometry(100, 100, 900, 600)
        self.initUI()

    def initUI(self):
        # Central widget
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QHBoxLayout()
        widget.setLayout(layout)

        # Menu lateral
        self.menu_lateral = QWidget()
        self.menu_lateral.setFixedWidth(200)
        self.menu_lateral.setStyleSheet("""
            background-color: #2e2e2e;
            color: white;
        """)
        menu_layout = QVBoxLayout()
        
        boton_inicio = self.crear_boton_menu("Inicio", "icons/home_icon.png")
        boton_inicio.clicked.connect(self.mostrar_pantalla_principal)
        menu_layout.addWidget(boton_inicio)

        boton_cxc = self.crear_boton_menu("Clientes Internacionales (CXC)", "icons/monitor_icon.png")
        boton_cxc.clicked.connect(self.abrir_modulo_cxc)
        menu_layout.addWidget(boton_cxc)

        boton_rem_nal = self.crear_boton_menu("Clientes Nacionales (REM NAL)", "icons/database_icon.png")
        boton_rem_nal.clicked.connect(self.abrir_modulo_rem_nal)
        menu_layout.addWidget(boton_rem_nal)

        boton_facturas_nal = self.crear_boton_menu("Facturación Nacional", "icons/invoice_icon.png")
        boton_facturas_nal.clicked.connect(self.abrir_modulo_facturas_nal)
        menu_layout.addWidget(boton_facturas_nal)

        boton_creditos_reclamos = self.crear_boton_menu("Créditos y Reclamos", "icons/gear_icon.png")
        boton_creditos_reclamos.clicked.connect(self.abrir_modulo_creditos_reclamos)
        menu_layout.addWidget(boton_creditos_reclamos)

        self.menu_lateral.setLayout(menu_layout)
        layout.addWidget(self.menu_lateral)

        # Stacked Widget
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Pantalla principal
        self.pantalla_principal = QWidget()
        self.stacked_widget.addWidget(self.pantalla_principal)
        self.mostrar_pantalla_principal()

    def crear_boton_menu(self, texto, icono):
        boton = QPushButton(texto)
        boton.setIcon(QIcon(icono))
        boton.setIconSize(QSize(24, 24))
        boton.setFont(QFont('Arial', 12))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        return boton

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

    def mostrar_pantalla_principal(self):
        layout = QVBoxLayout()
        etiqueta = QLabel("Bienvenido al menú principal")
        etiqueta.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(etiqueta)

        self.pantalla_principal.setLayout(layout)

    def abrir_modulo_cxc(self):
        self.cambiar_modulo(VentanaCXC(self.stacked_widget))

    def abrir_modulo_rem_nal(self):
        self.cambiar_modulo(VentanaREMNAL(self.stacked_widget))

    def abrir_modulo_facturas_nal(self):
        self.cambiar_modulo(VentanaFacturasNAL(self.stacked_widget))

    def abrir_modulo_creditos_reclamos(self):
        self.cambiar_modulo(VentanaCreditosReclamos(self.stacked_widget))

    def cambiar_modulo(self, modulo):
        self.stacked_widget.addWidget(modulo)
        self.stacked_widget.setCurrentWidget(modulo)


class VentanaCXC(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
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


class VentanaREMNAL(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
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


class VentanaFacturasNAL(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
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


class VentanaCreditosReclamos(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
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