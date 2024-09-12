from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QDateEdit, QMenuBar, QAction, QMenu, QDialog,
    QHBoxLayout
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
from data import cargar_datos
from charts import (
    mostrar_graficas_consumado, mostrar_deudas_por_empresa, 
    consultar_creditos_por_empresa, filtrar_y_graficar
)

# Cargamos los datos al iniciar la aplicación
df = cargar_datos()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JP FLOWERS ANALITICAS")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()

        # Menú principal
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        menu = QMenu("Opciones", self)
        menu_bar.addMenu(menu)

        # Acción para cerrar la aplicación
        action_salir = QAction("Salir", self)
        action_salir.triggered.connect(self.close)
        menu.addAction(action_salir)

        # Botón para ver el consumado de las ventas por cliente
        boton_consumado = QPushButton("Ver el consumado de las ventas por cliente")
        boton_consumado.setFont(QFont('Arial', 12))
        boton_consumado.clicked.connect(mostrar_graficas_consumado)
        layout.addWidget(boton_consumado)

        # Botón para ver el consumado de todos los créditos
        boton_creditos = QPushButton("Ver consumado de todos los créditos")
        boton_creditos.setFont(QFont('Arial', 12))
        boton_creditos.clicked.connect(self.mostrar_deudas_por_empresa)
        layout.addWidget(boton_creditos)

        # Botón para consultar los créditos por empresa
        boton_consultar_creditos = QPushButton("Consultar créditos por empresa")
        boton_consultar_creditos.setFont(QFont('Arial', 12))
        boton_consultar_creditos.clicked.connect(self.consultar_creditos_por_empresa)
        layout.addWidget(boton_consultar_creditos)

        # Botón para generar la gráfica filtrada
        boton_filtrar = QPushButton("Generar Gráfica de Ventas")
        boton_filtrar.setFont(QFont('Arial', 12))
        boton_filtrar.clicked.connect(self.mostrar_filtros_grafica)
        layout.addWidget(boton_filtrar)

        widget.setLayout(layout)

    def mostrar_filtros_grafica(self):
        dialog = QDialog()
        dialog.setWindowTitle('Filtrar Ventas para Gráfico')
        layout = QVBoxLayout()

        cliente_label = QLabel("Selecciona el cliente:")
        layout.addWidget(cliente_label)

        cliente_combo = QComboBox()
        clientes = df['CUSTOMER'].dropna().unique()
        cliente_combo.addItems(sorted(map(str, clientes)))
        layout.addWidget(cliente_combo)

        fecha_inicio_edit = QDateEdit(calendarPopup=True)
        fecha_inicio_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Selecciona la fecha de inicio:"))
        layout.addWidget(fecha_inicio_edit)

        fecha_fin_edit = QDateEdit(calendarPopup=True)
        fecha_fin_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Selecciona la fecha de fin:"))
        layout.addWidget(fecha_fin_edit)

        boton_generar = QPushButton("Generar Gráfica")
        boton_generar.clicked.connect(lambda: self.generar_grafica(cliente_combo.currentText(), fecha_inicio_edit.date().toPyDate(), fecha_fin_edit.date().toPyDate()))
        layout.addWidget(boton_generar)

        dialog.setLayout(layout)
        dialog.exec_()

    def generar_grafica(self, cliente, fecha_inicio, fecha_fin):
        filtrar_y_graficar(cliente, fecha_inicio, fecha_fin)

    def mostrar_deudas_por_empresa(self):
        mostrar_deudas_por_empresa()

    def consultar_creditos_por_empresa(self):
        consultar_creditos_por_empresa()

