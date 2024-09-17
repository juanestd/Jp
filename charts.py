import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox, QDateEdit, QApplication, QMessageBox
from PyQt5.QtCore import QDate
from datetime import datetime


# Funciones para Clientes Internacionales (CXC)

def mostrar_graficas_consumado():
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()
    ventas_por_cliente = df.groupby('CUSTOMER')['TOTAL US$'].sum()

    plt.figure(figsize=(12, 8))
    ax = ventas_por_cliente.plot(kind='bar', color='skyblue', edgecolor='black')
    ax.set_title('Ventas Totales por Cliente', fontsize=16, fontweight='bold')
    ax.set_xlabel('Cliente', fontsize=12)
    ax.set_ylabel('Total Ventas en US$', fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=10)

    plt.tight_layout()
    plt.show()

def mostrar_deudas_por_empresa():
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()
    deudas_por_empresa = df.groupby('CUSTOMER')['CREDIT'].sum()

    plt.figure(figsize=(12, 8))
    ax = deudas_por_empresa.plot(kind='bar', color='salmon', edgecolor='black')
    ax.set_title('Deudas Totales por Empresa', fontsize=16, fontweight='bold')
    ax.set_xlabel('Empresa', fontsize=12)
    ax.set_ylabel('Total Deuda en US$', fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=10)

    plt.tight_layout()
    plt.show()

def consultar_creditos_por_empresa():
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()

    app = QApplication([])
    dialog = QDialog()
    dialog.setWindowTitle('Consultar Créditos por Empresa')

    layout = QVBoxLayout()

    empresa_label = QLabel("Selecciona la empresa:")
    layout.addWidget(empresa_label)

    empresa_combo = QComboBox()
    empresas = df['CUSTOMER'].dropna().unique()
    empresa_combo.addItems(sorted(map(str, empresas)))
    layout.addWidget(empresa_combo)

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

    boton_consultar = QPushButton("Consultar")

    # Modificamos el clic del botón para cerrar el diálogo después de consultar
    boton_consultar.clicked.connect(lambda: (
        procesar_consulta(
            empresa_combo.currentText(),
            fecha_inicio_edit.date().toPyDate(),
            fecha_fin_edit.date().toPyDate()
        ),
        dialog.accept()  # Cierra el cuadro de diálogo
    ))
    layout.addWidget(boton_consultar)

    dialog.setLayout(layout)
    dialog.exec_()

def procesar_consulta(empresa, fecha_inicio, fecha_fin):
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()

    df['DATE'] = pd.to_datetime(df['DATE'])
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    df_filtrado = df[(df['CUSTOMER'] == empresa) &
                     (df['DATE'] >= fecha_inicio) &
                     (df['DATE'] <= fecha_fin)]

    if df_filtrado.empty:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"La empresa {empresa} no tiene créditos en este periodo de tiempo.")
        msg.setWindowTitle("Sin Datos")
        msg.exec_()
    else:
        creditos_por_fecha = df_filtrado.groupby('DATE')['CREDIT'].sum()

        plt.figure(figsize=(12, 8))
        ax = creditos_por_fecha.plot(kind='bar', color='purple', edgecolor='black')
        ax.set_title(f'Créditos de {empresa} ({fecha_inicio.date()} a {fecha_fin.date()})', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Total Créditos en US$', fontsize=12)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        for container in ax.containers:
            ax.bar_label(container, label_type='edge', fontsize=10)

        plt.tight_layout()
        plt.show()

def filtrar_y_graficar(cliente, fecha_inicio, fecha_fin):
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()

    df['DATE'] = pd.to_datetime(df['DATE'])
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    df_filtrado = df[(df['CUSTOMER'] == cliente) &
                     (df['DATE'] >= fecha_inicio) &
                     (df['DATE'] <= fecha_fin)]

    if df_filtrado.empty:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"No hay ventas para el cliente {cliente} en este periodo de tiempo.")
        msg.setWindowTitle("Sin Datos")
        msg.exec_()
    else:
        ventas_por_fecha = df_filtrado.groupby('DATE')['TOTAL US$'].sum()

        plt.figure(figsize=(12, 8))
        ax = ventas_por_fecha.plot(kind='bar', color='green', edgecolor='black')
        ax.set_title(f'Ventas de {cliente} ({fecha_inicio.date()} a {fecha_fin.date()})', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Total Ventas en US$', fontsize=12)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        for container in ax.containers:
            ax.bar_label(container, label_type='edge', fontsize=10)

        plt.tight_layout()
        plt.show()

        
def ver_consumado_por_cliente():  # Función restaurada
    from data import cargar_datos_rem_nal
    df = cargar_datos_rem_nal()
    app = QApplication([])

    dialog = QDialog()
    dialog.setWindowTitle('Ver consumado de ventas por cliente')

    layout = QVBoxLayout()

    cliente_label = QLabel("Selecciona el cliente:")
    layout.addWidget(cliente_label)

    cliente_combo = QComboBox()
    clientes = df['CLIENTE'].dropna().unique()
    cliente_combo.addItems(sorted(map(str, clientes)))
    layout.addWidget(cliente_combo)

    boton_mostrar = QPushButton("Mostrar consumado")
    boton_mostrar.clicked.connect(lambda: mostrar_consumado(cliente_combo.currentText(), df))
    layout.addWidget(boton_mostrar)

    dialog.setLayout(layout)
    dialog.exec_()

def mostrar_consumado(cliente, df):
    ventas_cliente = df[df['CLIENTE'] == cliente].groupby('CLIENTE')['US$'].sum()

    plt.figure(figsize=(8, 6))
    ax = ventas_cliente.plot(kind='bar', color='skyblue', edgecolor='black')
    ax.set_title(f'Ventas Totales de {cliente}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Cliente', fontsize=12)
    ax.set_ylabel('Total Ventas en US$', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=10)

    plt.tight_layout()
    plt.show()

def ver_todas_las_ventas():
    from data import cargar_datos_rem_nal
    df = cargar_datos_rem_nal()
    app = QApplication([])

    dialog = QDialog()
    dialog.setWindowTitle('Ver todas las ventas')

    layout = QVBoxLayout()

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
    boton_generar.clicked.connect(lambda: mostrar_ventas_periodo(
        fecha_inicio_edit.date().toPyDate(),
        fecha_fin_edit.date().toPyDate(),
        df
    ))
    layout.addWidget(boton_generar)

    dialog.setLayout(layout)
    dialog.exec_()
    
def mostrar_ventas_periodo(fecha_inicio, fecha_fin, df):
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    df_filtrado = df[(df['FECHA'] >= fecha_inicio) & (df['FECHA'] <= fecha_fin)]
    ventas_por_cliente = df_filtrado.groupby('CLIENTE')['US$'].sum()

    plt.figure(figsize=(12, 8))
    ax = ventas_por_cliente.plot(kind='bar', color='lightgreen', edgecolor='black')
    ax.set_title(f'Ventas entre {fecha_inicio.date()} y {fecha_fin.date()}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Cliente', fontsize=12)
    ax.set_ylabel('Total Ventas en US$', fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=10)

    plt.tight_layout()
    plt.show()

def ver_devoluciones_por_empresa():
    from data import cargar_datos_rem_nal
    df = cargar_datos_rem_nal()
    app = QApplication([])

    dialog = QDialog()
    dialog.setWindowTitle('Ver devoluciones por empresa')

    layout = QVBoxLayout()

    cliente_label = QLabel("Selecciona la empresa:")
    layout.addWidget(cliente_label)

    cliente_combo = QComboBox()
    clientes = df['CLIENTE'].dropna().unique()
    cliente_combo.addItems(sorted(map(str, clientes)))
    layout.addWidget(cliente_combo)

    boton_mostrar = QPushButton("Mostrar devoluciones")
    boton_mostrar.clicked.connect(lambda: mostrar_devoluciones(cliente_combo.currentText(), df))
    layout.addWidget(boton_mostrar)

    dialog.setLayout(layout)
    dialog.exec_()

def mostrar_devoluciones(cliente, df):
    devoluciones_cliente = df[df['CLIENTE'] == cliente][['FECHA', 'DEVOLUCION US$']].dropna()

    if devoluciones_cliente.empty:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"La empresa {cliente} no tiene devoluciones registradas.")
        msg.setWindowTitle("Sin Devoluciones")
        msg.exec_()
    else:
        plt.figure(figsize=(12, 8))
        ax = devoluciones_cliente.set_index('FECHA')['DEVOLUCION US$'].plot(kind='bar', color='orange', edgecolor='black')
        ax.set_title(f'Devoluciones de {cliente}', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Total Devoluciones en US$', fontsize=12)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        for container in ax.containers:
            ax.bar_label(container, label_type='edge', fontsize=10)

        plt.tight_layout()
        plt.show()
