import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import mplcursors
import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox, QDateEdit, QApplication, QMessageBox
from PyQt5.QtCore import QDate
from datetime import datetime


def mostrar_graficas_consumado():
    from data import cargar_datos
    df = cargar_datos()
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

    mplcursors.cursor(hover=True)  
    plt.tight_layout()
    plt.show()

# Función para mostrar cuánto debe cada empresa
def mostrar_deudas_por_empresa():
    from data import cargar_datos
    df = cargar_datos()
    deudas_por_empresa = df.groupby('CUSTOMER')['CREDIT'].sum()

    plt.figure(figsize=(12, 8))
    ax = deudas_por_empresa.plot(kind='bar', color='salmon', edgecolor='black')
    ax.set_title('Deudas Totales por Empresa', fontsize=16, fontweight='bold')
    ax.set_xlabel('Empresa', fontsize=12)
    ax.set_ylabel('Total Deuda en US$', fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrar valores encima de las barras
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=10)

    mplcursors.cursor(hover=True)  # Añadir interactividad
    plt.tight_layout()
    plt.show()

# Función para consultar los créditos por empresa y periodo
def consultar_creditos_por_empresa():
    from data import cargar_datos
    df = cargar_datos()

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
    boton_consultar.clicked.connect(lambda: procesar_consulta(
        empresa_combo.currentText(),
        fecha_inicio_edit.date().toPyDate(),
        fecha_fin_edit.date().toPyDate()
    ))
    layout.addWidget(boton_consultar)

    dialog.setLayout(layout)
    dialog.exec_()

def procesar_consulta(empresa, fecha_inicio, fecha_fin):
    from data import cargar_datos
    df = cargar_datos()
    
    # Convertir la columna de fechas a datetime
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    # Convertir las fechas de entrada a datetime
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)
    
    df_filtrado = df[(df['CUSTOMER'] == empresa) &
                     (df['DATE'] >= fecha_inicio) &
                     (df['DATE'] <= fecha_fin)]

    if df_filtrado.empty:
        # Mostrar mensaje si no hay datos
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

        # Mostrar valores encima de las barras
        for container in ax.containers:
            ax.bar_label(container, label_type='edge', fontsize=10)

        plt.tight_layout()
        plt.show()

# Función para filtrar y graficar
def filtrar_y_graficar(cliente, fecha_inicio, fecha_fin):
    from data import cargar_datos
    df = cargar_datos()
    
    # Convertir la columna de fechas a datetime
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    # Convertir las fechas de entrada a datetime
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)
    
    df_filtrado = df[(df['CUSTOMER'] == cliente) &
                     (df['DATE'] >= fecha_inicio) &
                     (df['DATE'] <= fecha_fin)]

    if df_filtrado.empty:
        # Mostrar mensaje si no hay datos
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

        # Mostrar valores encima de las barras
        for container in ax.containers:
            ax.bar_label(container, label_type='edge', fontsize=10)

        plt.tight_layout()
        plt.show()
