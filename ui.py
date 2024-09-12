from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QMenuBar, QAction, QMenu, QLabel
)
from PyQt5.QtGui import QFont
from charts import (
    mostrar_graficas_consumado, mostrar_deudas_por_empresa, 
    consultar_creditos_por_empresa, filtrar_y_graficar
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

        boton_cxc = QPushButton("Clientes Internacionales (CXC)")
        boton_cxc.setFont(QFont('Arial', 12))
        boton_cxc.clicked.connect(self.abrir_modulo_cxc)
        layout.addWidget(boton_cxc)

        boton_rem_nal = QPushButton("Clientes Nacionales (REM NAL)")
        boton_rem_nal.setFont(QFont('Arial', 12))
        boton_rem_nal.clicked.connect(self.abrir_modulo_rem_nal)
        layout.addWidget(boton_rem_nal)

        boton_facturas_nal = QPushButton("Facturación Nacional")
        boton_facturas_nal.setFont(QFont('Arial', 12))
        boton_facturas_nal.clicked.connect(self.abrir_modulo_facturas_nal)
        layout.addWidget(boton_facturas_nal)

        boton_creditos_reclamos = QPushButton("Créditos y Reclamos")
        boton_creditos_reclamos.setFont(QFont('Arial', 12))
        boton_creditos_reclamos.clicked.connect(self.abrir_modulo_creditos_reclamos)
        layout.addWidget(boton_creditos_reclamos)

        widget.setLayout(layout)

    def abrir_modulo_cxc(self):
        self.modulo_cxc = VentanaCXC()
        self.modulo_cxc.show()

    def abrir_modulo_rem_nal(self):
        self.modulo_rem_nal = VentanaREMNAL()
        self.modulo_rem_nal.show()

    def abrir_modulo_facturas_nal(self):
        self.modulo_facturas_nal = VentanaFacturasNAL()
        self.modulo_facturas_nal.show()

    def abrir_modulo_creditos_reclamos(self):
        self.modulo_creditos_reclamos = VentanaCreditosReclamos()
        self.modulo_creditos_reclamos.show()


# Ventana para Clientes Internacionales (CXC)
class VentanaCXC(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clientes Internacionales (CXC)")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Crear los botones
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
        boton_filtrar_graficar.clicked.connect(filtrar_y_graficar)  # Conectar a la función correspondiente
        layout.addWidget(boton_filtrar_graficar)

        # Agregar el layout al widget
        widget.setLayout(layout)
        self.setCentralWidget(widget)


# Ventana para Clientes Nacionales (REM NAL)
class VentanaREMNAL(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clientes Nacionales (REM NAL)")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta es la ventana para Clientes Nacionales"))
        widget.setLayout(layout)
        self.setCentralWidget(widget)

# Ventana para Facturación Nacional (FACTURAS NAL)
class VentanaFacturasNAL(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Facturación Nacional (FACTURAS NAL)")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta es la ventana para Facturación Nacional"))
        widget.setLayout(layout)
        self.setCentralWidget(widget)

# Ventana para Créditos y Reclamos
class VentanaCreditosReclamos(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Créditos y Reclamos")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Esta es la ventana para Créditos y Reclamos"))
        widget.setLayout(layout)
        self.setCentralWidget(widget)