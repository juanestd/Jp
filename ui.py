import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QStackedWidget,
    QDialog, QComboBox, QDateEdit, QMessageBox, QSpinBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QDate
from charts import (
    mostrar_graficas_consumado, mostrar_deudas_por_empresa, 
    consultar_creditos_por_empresa, filtrar_y_graficar,
    ver_consumado_por_cliente, ver_todas_las_ventas, ver_devoluciones_por_empresa,
    mostrar_ventas_por_mes, mostrar_ventas_por_mes_rem_nal
)

def resource_path(relative_path):
    """Obtiene la ruta de los recursos."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
        self.menu_lateral.setStyleSheet("background-color: #2e2e2e; color: white;")
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
                background-color: #4a4a4a; color: white; border: 1px solid #007f00;
                padding: 10px; text-align: left; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #66bb66; color: white; border: 1px solid #00cc00;
            }
        """)
        return boton

    def mostrar_pantalla_principal(self):
        layout = QVBoxLayout()

        imagen = QLabel(self)
        pixmap = QPixmap(resource_path('descarga.jpeg'))  # Ruta de la imagen
        imagen.setPixmap(pixmap)
        imagen.setFixedSize(500, 300)
        imagen.setAlignment(Qt.AlignCenter)

        etiqueta_bienvenida = QLabel(" Bienvenidos al sistema de análisis de datos de JP FLOWERS ", self)
        etiqueta_bienvenida.setFont(QFont('Arial', 24, QFont.Bold))
        etiqueta_bienvenida.setStyleSheet("""
            QLabel {
                color: #ffffff; background-color: rgba(46, 139, 87, 204);
                border: 2px solid #ffffff; border-radius: 15px;
                padding: 10px 20px; font-size: 24px; font-family: 'Arial';
                text-shadow: 1px 1px 3px #000000;
            }
        """)
        etiqueta_bienvenida.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(imagen, alignment=Qt.AlignCenter)
        layout.addWidget(etiqueta_bienvenida, alignment=Qt.AlignCenter)
        layout.addStretch()

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

        # Botones
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

        boton_ventas_por_mes = self.crear_boton_con_icono("Mostrar Ventas por Mes", "icons/calendar_icon.png")
        boton_ventas_por_mes.clicked.connect(self.abrir_dialogo_ventas_por_mes)
        layout.addWidget(boton_ventas_por_mes)

        self.setLayout(layout)

    def crear_boton_con_icono(self, texto, icono):
        boton = QPushButton(texto)
        boton.setFont(QFont('Arial', 12))
        boton.setIcon(QIcon(icono))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a; color: #00cc66; border: 2px solid #00cc66;
                border-radius: 10px; padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333; border-color: #00ff99;
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
        dialogo.exec_()

    def procesar_filtrar_y_graficar(self, cliente, fecha_inicio, fecha_fin, dialogo):
        try:
            filtrar_y_graficar(cliente, fecha_inicio, fecha_fin)
            dialogo.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def abrir_dialogo_ventas_por_mes(self):
        # Crear un diálogo modal para seleccionar mes y año
        dialogo = QDialog(self)
        dialogo.setWindowTitle('Mostrar Ventas por Mes')

        layout = QVBoxLayout()

        # Etiqueta y combo box para seleccionar el mes
        mes_label = QLabel("Selecciona el mes:")
        layout.addWidget(mes_label)

        mes_combo = QComboBox()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", 
                "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_combo.addItems(meses)
        layout.addWidget(mes_combo)

        # Etiqueta y spin box para seleccionar el año
        año_label = QLabel("Selecciona el año:")
        layout.addWidget(año_label)

        año_spin = QSpinBox()
        año_spin.setRange(2000, 2100)
        año_spin.setValue(QDate.currentDate().year())  # Valor por defecto
        layout.addWidget(año_spin)

        # Botón para mostrar el gráfico de ventas
        boton_mostrar = QPushButton("Mostrar gráfico de ventas")
        boton_mostrar.clicked.connect(lambda: self.procesar_mostrar_ventas_por_mes(mes_combo.currentText(), año_spin.value(), dialogo))

        layout.addWidget(boton_mostrar)

        dialogo.setLayout(layout)
        dialogo.exec_()

    def procesar_mostrar_ventas_por_mes(self, mes, año, dialogo):
        try:
            # Convertir el nombre del mes a un número
            mes_numero = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                        "Julio", "Agosto", "Septiembre", "Octubre", 
                        "Noviembre", "Diciembre"].index(mes) + 1
            
            # Llamar a la función que genera el gráfico de ventas por mes y año
            from charts import mostrar_ventas_por_mes
            mostrar_ventas_por_mes(mes_numero, año)
            
        except Exception as e:
            # Mostrar mensaje de error si algo sale mal
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error al mostrar ventas por mes: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()
        finally:
            dialogo.accept()  # Cierra el diálogo una vez se ha mostrado o generado el gráfico



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
        
          # Nuevo botón para una nueva funcionalidad que desees añadir
        nuevo_boton = self.crear_boton_con_icono("Ver ventas totales por mes", "icons/new_icon.png")
        nuevo_boton.clicked.connect(self.abrir_dialogo_ventas_por_mes_remnal)
        layout.addWidget(nuevo_boton)

        self.setLayout(layout)


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
            
    def abrir_dialogo_ventas_por_mes_remnal(self):
        # Crear un diálogo modal para seleccionar mes y año
        dialogo = QDialog(self)
        dialogo.setWindowTitle('Mostrar Ventas por Mes (REMNAL)')

        layout = QVBoxLayout()

        # Etiqueta y combo box para seleccionar el mes
        mes_label = QLabel("Selecciona el mes:")
        layout.addWidget(mes_label)

        mes_combo = QComboBox()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", 
                "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_combo.addItems(meses)
        layout.addWidget(mes_combo)

        # Etiqueta y spin box para seleccionar el año
        año_label = QLabel("Selecciona el año:")
        layout.addWidget(año_label)

        año_spin = QSpinBox()
        año_spin.setRange(2000, 2100)
        año_spin.setValue(QDate.currentDate().year())  # Valor por defecto
        layout.addWidget(año_spin)

        # Botón para mostrar el gráfico de ventas
        boton_mostrar = QPushButton("Mostrar gráfico de ventas")
        boton_mostrar.clicked.connect(lambda: self.procesar_mostrar_ventas_por_mes_remnal(mes_combo.currentText(), año_spin.value(), dialogo))

        layout.addWidget(boton_mostrar)

        dialogo.setLayout(layout)
        dialogo.exec_()

    def procesar_mostrar_ventas_por_mes_remnal(self, mes, año, dialogo):
        try:
            # Convertir el nombre del mes a un número
            mes_numero = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                        "Julio", "Agosto", "Septiembre", "Octubre", 
                        "Noviembre", "Diciembre"].index(mes) + 1
            
            # Llamar a la función que genera el gráfico de ventas por mes y año
            from charts import mostrar_ventas_por_mes_rem_nal
            mostrar_ventas_por_mes_rem_nal(mes_numero, año)
            
        except Exception as e:
            # Mostrar mensaje de error si algo sale mal
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error al mostrar ventas por mes (REMNAL): {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()
        finally:
            dialogo.accept()  # Cierra el diálogo una vez se ha mostrado o generado el gráfico
            
            
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
        self.close()  # Cierra la ventana actual (pestaña)