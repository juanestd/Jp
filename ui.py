from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QMenuBar, QAction, QMenu, QLabel, QStackedWidget
)
from PyQt5.QtGui import QFont
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

        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        menu = QMenu("Opciones", self)
        menu_bar.addMenu(menu)

        action_salir = QAction("Salir", self)
        action_salir.triggered.connect(self.close)
        menu.addAction(action_salir)

        self.stacked_widget = QStackedWidget()  # Widget para contener las diferentes vistas
        layout.addWidget(self.stacked_widget)

        self.pantalla_principal = QWidget()
        pantalla_layout = QVBoxLayout()

        # Botones para Clientes Internacionales (CXC)
        boton_cxc = QPushButton("Clientes Internacionales (CXC)")
        boton_cxc.setFont(QFont('Arial', 12))
        boton_cxc.clicked.connect(self.abrir_modulo_cxc)
        pantalla_layout.addWidget(boton_cxc)

        # Botones para Clientes Nacionales (REM NAL)
        boton_rem_nal = QPushButton("Clientes Nacionales (REM NAL)")
        boton_rem_nal.setFont(QFont('Arial', 12))
        boton_rem_nal.clicked.connect(self.abrir_modulo_rem_nal)
        pantalla_layout.addWidget(boton_rem_nal)

        boton_facturas_nal = QPushButton("Facturación Nacional")
        boton_facturas_nal.setFont(QFont('Arial', 12))
        boton_facturas_nal.clicked.connect(self.abrir_modulo_facturas_nal)
        pantalla_layout.addWidget(boton_facturas_nal)

        boton_creditos_reclamos = QPushButton("Créditos y Reclamos")
        boton_creditos_reclamos.setFont(QFont('Arial', 12))
        boton_creditos_reclamos.clicked.connect(self.abrir_modulo_creditos_reclamos)
        pantalla_layout.addWidget(boton_creditos_reclamos)

        self.pantalla_principal.setLayout(pantalla_layout)
        self.stacked_widget.addWidget(self.pantalla_principal)

        widget.setLayout(layout)

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

        boton_grafica_consumado = QPushButton("Mostrar Ventas por Cliente")
        boton_grafica_consumado.setFont(QFont('Arial', 12))
        boton_grafica_consumado.clicked.connect(mostrar_graficas_consumado)
        layout.addWidget(boton_grafica_consumado)

        boton_deudas_empresa = QPushButton("Mostrar Deudas por Empresa")
        boton_deudas_empresa.setFont(QFont('Arial', 12))
        boton_deudas_empresa.clicked.connect(mostrar_deudas_por_empresa)
        layout.addWidget(boton_deudas_empresa)

        boton_consultar_creditos = QPushButton("Consultar Créditos por Empresa")
        boton_consultar_creditos.setFont(QFont('Arial', 12))
        boton_consultar_creditos.clicked.connect(consultar_creditos_por_empresa)
        layout.addWidget(boton_consultar_creditos)

        boton_filtrar_graficar = QPushButton("Filtrar y Graficar Ventas por Cliente")
        boton_filtrar_graficar.setFont(QFont('Arial', 12))
        boton_filtrar_graficar.clicked.connect(filtrar_y_graficar)
        layout.addWidget(boton_filtrar_graficar)

        # Botón para regresar al menú principal
        boton_regresar = QPushButton("Regresar al Menú Principal")
        boton_regresar.setFont(QFont('Arial', 12))
        boton_regresar.clicked.connect(self.regresar_menu_principal)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

    def regresar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)


# Ventana para Clientes Nacionales (REM NAL)
class VentanaREMNAL(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()

        boton_consumado_cliente = QPushButton("Ver consumado de ventas por cliente")
        boton_consumado_cliente.setFont(QFont('Arial', 12))
        boton_consumado_cliente.clicked.connect(ver_consumado_por_cliente)
        layout.addWidget(boton_consumado_cliente)

        boton_todas_ventas = QPushButton("Ver todas las ventas")
        boton_todas_ventas.setFont(QFont('Arial', 12))
        boton_todas_ventas.clicked.connect(ver_todas_las_ventas)
        layout.addWidget(boton_todas_ventas)

        boton_devoluciones_empresa = QPushButton("Ver devoluciones por empresa")
        boton_devoluciones_empresa.setFont(QFont('Arial', 12))
        boton_devoluciones_empresa.clicked.connect(ver_devoluciones_por_empresa)
        layout.addWidget(boton_devoluciones_empresa)

        boton_regresar = QPushButton("Regresar al Menú Principal")
        boton_regresar.setFont(QFont('Arial', 12))
        boton_regresar.clicked.connect(self.regresar_menu_principal)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

    def regresar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)


# Ventana para Facturación Nacional (FACTURAS NAL)
class VentanaFacturasNAL(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta es la ventana para Facturación Nacional"))

        boton_regresar = QPushButton("Regresar al Menú Principal")
        boton_regresar.setFont(QFont('Arial', 12))
        boton_regresar.clicked.connect(self.regresar_menu_principal)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

    def regresar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)


# Ventana para Créditos y Reclamos
class VentanaCreditosReclamos(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta es la ventana para Créditos y Reclamos"))

        boton_regresar = QPushButton("Regresar al Menú Principal")
        boton_regresar.setFont(QFont('Arial', 12))
        boton_regresar.clicked.connect(self.regresar_menu_principal)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

    def regresar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)