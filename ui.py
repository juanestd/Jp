from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QStackedWidget,
    QDialog, QComboBox, QDateEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import QSize, QDate, Qt
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
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QHBoxLayout()
        widget.setLayout(layout)

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

        # Eliminar ajustes y ayuda
        # Aquí se eliminan los botones que ya no se necesitan

        self.menu_lateral.setLayout(menu_layout)
        layout.addWidget(self.menu_lateral)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

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
                border: 1px solid #007f00;
                padding: 10px;
                text-align: left;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #66bb66;
                color: white;
                border: 1px solid #00cc00;
            }
        """)
        return boton

    def mostrar_pantalla_principal(self):
        layout = QVBoxLayout()

        # Crear una etiqueta para mostrar la imagen de fondo
        imagen = QLabel(self)
        pixmap = QPixmap('descarga.jpeg')  # Ruta de la imagen
        imagen.setPixmap(pixmap)

        # Establecer tamaño adecuado para la imagen
        imagen.setFixedSize(500, 300)  # Cambia estos valores si prefieres otro tamaño
        imagen.setAlignment(Qt.AlignCenter)  # Centrar la imagen

        # Crear una etiqueta para el texto de bienvenida
        etiqueta_bienvenida = QLabel(" Bienvenidos al sistema de análisis de datos de JP FLOWERS ", self)
        etiqueta_bienvenida.setFont(QFont('Arial', 24, QFont.Bold))
        etiqueta_bienvenida.setStyleSheet("""
            QLabel {
                color: #ffffff;
                background-color: rgba(46, 139, 87, 204);  /* Fondo semitransparente */
                border: 2px solid #ffffff;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 24px;
                font-family: 'Arial';
                text-shadow: 1px 1px 3px #000000;
            }
        """)
        etiqueta_bienvenida.setAlignment(Qt.AlignCenter)

        # Añadir la imagen y el texto al layout, con espaciado
        layout.addStretch()  # Añadir un espacio antes de la imagen
        layout.addWidget(imagen, alignment=Qt.AlignCenter)  # Centrar la imagen
        layout.addWidget(etiqueta_bienvenida, alignment=Qt.AlignCenter)  # Centrar el texto
        layout.addStretch()  # Añadir un espacio después del texto

        self.pantalla_principal.setLayout(layout)
        self.stacked_widget.setCurrentWidget(self.pantalla_principal)



    def abrir_modulo_cxc(self):
        self.cambiar_modulo(VentanaCXC(self.stacked_widget))

    def abrir_modulo_rem_nal(self):
        self.cambiar_modulo(VentanaREMNAL(self.stacked_widget))

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
        boton_filtrar_graficar.clicked.connect(self.abrir_dialogo_filtrar_y_graficar)
        layout.addWidget(boton_filtrar_graficar)

        self.setLayout(layout)

    def crear_boton_con_icono(self, texto, icono):
        boton = QPushButton(texto)
        boton.setFont(QFont('Arial', 12))
        boton.setIcon(QIcon(icono))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #00cc66;
                border: 2px solid #00cc66;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
                border-color: #00ff99;
            }
        """)
        return boton

    def abrir_dialogo_filtrar_y_graficar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle('Filtrar y Graficar Ventas por Cliente')

        layout = QVBoxLayout()

        cliente_label = QLabel("Selecciona el cliente:")
        layout.addWidget(cliente_label)

        cliente_combo = QComboBox()
        from data import cargar_datos_cxc
        df = cargar_datos_cxc()
        clientes = df['CUSTOMER'].dropna().unique()
        cliente_combo.addItems(sorted(map(str, clientes)))
        layout.addWidget(cliente_combo)

        fecha_inicio_label = QLabel("Selecciona la fecha de inicio:")
        layout.addWidget(fecha_inicio_label)

        fecha_inicio_edit = QDateEdit(calendarPopup=True)
        fecha_inicio_edit.setDate(QDate.currentDate())
        layout.addWidget(fecha_inicio_edit)

        fecha_fin_label = QLabel("Selecciona la fecha de fin:")
        layout.addWidget(fecha_fin_label)

        fecha_fin_edit = QDateEdit(calendarPopup=True)
        fecha_fin_edit.setDate(QDate.currentDate())
        layout.addWidget(fecha_fin_edit)

        boton_generar = QPushButton("Generar gráfico")
        boton_generar.clicked.connect(lambda: self.procesar_filtrar_y_graficar(
            cliente_combo.currentText(),
            fecha_inicio_edit.date().toPyDate(),
            fecha_fin_edit.date().toPyDate(),
            dialogo
        ))
        layout.addWidget(boton_generar)

        dialogo.setLayout(layout)
        dialogo.exec()

    def procesar_filtrar_y_graficar(self, cliente, fecha_inicio, fecha_fin, dialogo):
        try:
            filtrar_y_graficar(cliente, fecha_inicio, fecha_fin)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error al filtrar y graficar: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()
        finally:
            dialogo.accept()  # Cierra el diálogo

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
        boton_consumado_cliente.clicked.connect(self.abrir_dialogo_consumado_cliente)
        layout.addWidget(boton_consumado_cliente)

        boton_todas_ventas = self.crear_boton_con_icono("Ver todas las ventas", "icons/sales_icon.png")
        boton_todas_ventas.clicked.connect(self.procesar_ver_todas_las_ventas)
        layout.addWidget(boton_todas_ventas)

        boton_devoluciones_empresa = self.crear_boton_con_icono("Ver devoluciones por empresa", "icons/return_icon.png")
        boton_devoluciones_empresa.clicked.connect(ver_devoluciones_por_empresa)
        layout.addWidget(boton_devoluciones_empresa)

        self.setLayout(layout)

    def crear_boton_con_icono(self, texto, icono):
        boton = QPushButton(texto)
        boton.setFont(QFont('Arial', 12))
        boton.setIcon(QIcon(icono))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #00cc66;
                border: 2px solid #00cc66;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
                border-color: #00ff99;
            }
        """)
        return boton

    def abrir_dialogo_consumado_cliente(self):
        self.dialogo = QDialog(self)
        self.dialogo.setWindowTitle('Ver consumado de ventas por cliente')

        layout = QVBoxLayout()

        cliente_label = QLabel("Selecciona el cliente:")
        layout.addWidget(cliente_label)

        cliente_combo = QComboBox()
        from data import cargar_datos_rem_nal
        df = cargar_datos_rem_nal()
        clientes = df['CLIENTE'].dropna().unique()
        cliente_combo.addItems(sorted(map(str, clientes)))
        layout.addWidget(cliente_combo)

        fecha_inicio_label = QLabel("Selecciona la fecha de inicio:")
        layout.addWidget(fecha_inicio_label)

        fecha_inicio_edit = QDateEdit(calendarPopup=True)
        fecha_inicio_edit.setDate(QDate.currentDate())
        layout.addWidget(fecha_inicio_edit)

        fecha_fin_label = QLabel("Selecciona la fecha de fin:")
        layout.addWidget(fecha_fin_label)

        fecha_fin_edit = QDateEdit(calendarPopup=True)
        fecha_fin_edit.setDate(QDate.currentDate())
        layout.addWidget(fecha_fin_edit)

        boton_generar = QPushButton("Generar gráfico")
        boton_generar.clicked.connect(lambda: self.procesar_ver_consumado_por_cliente(
            cliente_combo.currentText(),
            fecha_inicio_edit.date().toPyDate(),
            fecha_fin_edit.date().toPyDate(),
            self.dialogo
        ))
        layout.addWidget(boton_generar)

        self.dialogo.setLayout(layout)
        self.dialogo.exec()

    def procesar_ver_consumado_por_cliente(self, cliente, fecha_inicio, fecha_fin, dialogo):
        try:
            ver_consumado_por_cliente(cliente, fecha_inicio, fecha_fin)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error al consultar consumado por cliente: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()
        finally:
            dialogo.accept()  # Cierra el diálogo

    def procesar_ver_todas_las_ventas(self):
        try:
            ver_todas_las_ventas()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error al consultar todas las ventas: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()
        # No cambiar de vista, solo cerrar el diálogo
        self.close()  # Cierra la ventana actual (pestaña)