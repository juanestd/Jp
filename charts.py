import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox, QDateEdit, QApplication, QMessageBox
from PyQt5.QtCore import QDate

# Crear la instancia de QApplication solo una vez
app = QApplication(sys.argv)

# Función para aplicar el estilo gráfico actualizado y mostrar el total en la gráfica
def estilo_grafico(ventas_por_cliente, titulo, xlabel, ylabel, total=None):
    # Ordenar de mayor a menor antes de graficar
    ventas_por_cliente = ventas_por_cliente.sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(20, 10))
    fig.patch.set_facecolor('lightgreen')
    ax.set_facecolor('lightgray')
    bars = ventas_por_cliente.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set_title(titulo, fontsize=16, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='x', rotation=85, labelsize=11)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Mostrar etiquetas en las barras
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=6, rotation=0)
    
    # Si se proporciona un total, mostrarlo en la gráfica
    if total is not None:
        ax.text(0.95, 0.95, f'Total: {total:.2f}', transform=ax.transAxes,
                fontsize=12, fontweight='bold', ha='right', va='top',
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='black'))
    
    plt.tight_layout()
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block=False)
    
def ver_consumado_por_cliente(cliente, fecha_inicio, fecha_fin):
    from data import cargar_datos_rem_nal
    df = cargar_datos_rem_nal()

    # Convertir la columna de fechas a tipo 'date' para hacer la comparación
    df['FECHA'] = df['FECHA'].dt.date

    # Filtrar los datos por cliente y rango de fechas
    df_filtrado = df[(df['CLIENTE'] == cliente) & 
                     (df['FECHA'] >= fecha_inicio) & 
                     (df['FECHA'] <= fecha_fin)]

    if df_filtrado.empty:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(f"No se encontraron ventas para {cliente} en el rango de fechas proporcionado.")
        msg.setWindowTitle("Sin datos")
        msg.exec_()
    else:
        # Agrupar y sumar ventas por cliente
        ventas_cliente = df_filtrado.groupby('CLIENTE')['US$'].sum()
        estilo_grafico(ventas_cliente, f'Ventas Totales de {cliente} desde {fecha_inicio} hasta {fecha_fin}', 
                       'Cliente', 'Total Ventas en US$')
# Función auxiliar para mostrar el gráfico de ventas
def mostrar_consumado(cliente, df):
    ventas_cliente = df[df['CLIENTE'] == cliente].groupby('CLIENTE')['US$'].sum()
    estilo_grafico(ventas_cliente, f'Ventas Totales de {cliente}', 'Cliente', 'Total Ventas en US$')

def mostrar_deudas_por_empresa():
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()
    deudas_por_empresa = df.groupby('CUSTOMER')['CREDIT'].sum()

    # Calcular el total de deudas y los porcentajes
    total_deudas = deudas_por_empresa.sum()
    porcentajes = [f'{(valor / total_deudas) * 100:.2f}%' for valor in deudas_por_empresa]
    numeros_deudas = deudas_por_empresa.values

    estilo_grafico(deudas_por_empresa, 'Deudas Totales por Empresa', 'Empresa', 'Total Deuda en US$')

    # Mostrar el total en la gráfica
    print(f"Total de Deudas: {total_deudas:.2f}")
def mostrar_ventas_por_mes(mes, año):
    from data import cargar_datos_cxc
    import pandas as pd
    import matplotlib.pyplot as plt
    
    df = cargar_datos_cxc()

    # Convertir la columna de fechas a tipo datetime
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Filtrar las ventas para el mes y año específico
    df_mes = df[(df['DATE'].dt.month == mes) & (df['DATE'].dt.year == año)]

    # Agrupar las ventas del mes por empresa y ordenarlas de mayor a menor
    ventas_por_empresa = df_mes.groupby('CUSTOMER')['TOTAL US$'].sum().sort_values(ascending=False)

    if ventas_por_empresa.empty:
        print(f"No hay ventas para {mes}/{año}")
        return

    # Crear el gráfico de torta
    fig, ax = plt.subplots(figsize=(10, 10))
    wedges, texts = ax.pie(ventas_por_empresa, labels=None, startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  # Asegura que el gráfico de torta sea circular.

    # Calcular el total de ventas y los porcentajes
    total_ventas = ventas_por_empresa.sum()
    porcentajes = [f'{(valor / total_ventas) * 100:.2f}%' for valor in ventas_por_empresa]
    numeros_ventas = ventas_por_empresa.values

    # Añadir la leyenda con los nombres de las empresas, porcentajes y números de ventas
    leyenda_textos = [f'{empresa}: {porcentaje} ({numero:.2f})' for empresa, porcentaje, numero in zip(ventas_por_empresa.index, porcentajes, numeros_ventas)]
    ax.legend(wedges, leyenda_textos, title="Empresas", loc="center left", bbox_to_anchor=(0.8, 0.5))

    # Eliminar el eje adicional y mover el texto del total de ventas dentro del gráfico
    ax.annotate(f'Total Ventas: {total_ventas:.2f}', xy=(0, -1.2), fontsize=12, ha='center', va='center')

    # Título en la parte superior de la torta
    mes_nombre = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes-1]
    plt.title(f'Ventas Totales por Empresa para {mes_nombre} {año}', fontsize=16, fontweight='bold')

    # Mostrar el gráfico
    plt.show()

def mostrar_graficas_consumado():
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()
    ventas_por_cliente = df.groupby('CUSTOMER')['TOTAL US$'].sum()

    # Calcular el total de ventas
    total_ventas = ventas_por_cliente.sum()

    # Mostrar el gráfico incluyendo el total
    estilo_grafico(ventas_por_cliente, 'Ventas Totales por Cliente', 'Cliente', 'Total Ventas en US$', total=total_ventas)

def consultar_creditos_por_empresa():
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()
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
    boton_consultar.clicked.connect(lambda: (
        procesar_consulta(
            empresa_combo.currentText(),
            fecha_inicio_edit.date().toPyDate(),
            fecha_fin_edit.date().toPyDate()
        ),
        dialog.accept()
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

        # Calcular el total de créditos
        total_creditos = creditos_por_fecha.sum()

        # Mostrar el gráfico incluyendo el total
        estilo_grafico(creditos_por_fecha, f'Créditos de {empresa} ({fecha_inicio.date()} a {fecha_fin.date()})', 'Fecha', 'Total Créditos en US$', total=total_creditos)

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

        # Calcular el total de ventas
        total_ventas = ventas_por_fecha.sum()

        # Mostrar el gráfico incluyendo el total
        estilo_grafico(ventas_por_fecha, f'Ventas de {cliente} ({fecha_inicio.date()} a {fecha_fin.date()})', 'Fecha', 'Total Ventas en US$', total=total_ventas)

def mostrar_consumado(cliente, df):
    ventas_cliente = df[df['CLIENTE'] == cliente].groupby('CLIENTE')['US$'].sum()

    # Calcular el total de ventas
    total_ventas = ventas_cliente.sum()

    # Mostrar el gráfico incluyendo el total
    estilo_grafico(ventas_cliente, f'Ventas Totales de {cliente}', 'Cliente', 'Total Ventas en US$', total=total_ventas)

def ver_todas_las_ventas():
    from data import cargar_datos_rem_nal
    df = cargar_datos_rem_nal()
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
        df,
        dialog
    ))
    layout.addWidget(boton_generar)
    dialog.setLayout(layout)
    dialog.exec_()

def mostrar_ventas_periodo(fecha_inicio, fecha_fin, df, dialog):
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)
    df_filtrado = df[(df['FECHA'] >= fecha_inicio) & (df['FECHA'] <= fecha_fin)]
    ventas_por_cliente = df_filtrado.groupby('CLIENTE')['US$'].sum()

    # Calcular el total de ventas
    total_ventas = ventas_por_cliente.sum()

    # Mostrar el gráfico incluyendo el total
    estilo_grafico(ventas_por_cliente, f'Ventas entre {fecha_inicio.date()} y {fecha_fin.date()}', 'Cliente', 'Total Ventas en US$', total=total_ventas)
    dialog.accept()  # Cierra el diálogo después de generar el gráfico

def ver_devoluciones_por_empresa():
    from data import cargar_datos_rem_nal
    df = cargar_datos_rem_nal()
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
        devoluciones_por_fecha = devoluciones_cliente.groupby('FECHA')['DEVOLUCION US$'].sum()
        estilo_grafico(devoluciones_por_fecha, f'Devoluciones de {cliente}', 'Fecha', 'Total Devoluciones en US$')

def mostrar_ventas_por_mes_rem_nal(mes, año):
    from data import cargar_datos_rem_nal
    import pandas as pd
    import matplotlib.pyplot as plt
    
    df = cargar_datos_rem_nal()  # Cargar datos de REM NAL
    df['FECHA'] = pd.to_datetime(df['FECHA'])  # Convertir la columna de fechas a tipo datetime
    
    # Filtrar las ventas para el mes y año específico
    df_mes = df[(df['FECHA'].dt.month == mes) & (df['FECHA'].dt.year == año)]
    
    # Agrupar las ventas del mes por cliente o empresa y ordenarlas de mayor a menor
    ventas_por_cliente = df_mes.groupby('CLIENTE')['US$'].sum().sort_values(ascending=False)
    
    if ventas_por_cliente.empty:
        print(f"No hay ventas para {mes}/{año}")
        return
    
    # Crear el gráfico de torta
    fig, ax = plt.subplots(figsize=(10, 10))
    wedges, texts = ax.pie(ventas_por_cliente, labels=None, startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  # Asegura que el gráfico de torta sea circular.
    
    # Calcular el total de ventas y los porcentajes
    total_ventas = ventas_por_cliente.sum()
    porcentajes = [f'{(valor / total_ventas) * 100:.2f}%' for valor in ventas_por_cliente]
    numeros_ventas = ventas_por_cliente.values
    
    # Añadir la leyenda con los nombres de las empresas, porcentajes y números de ventas
    leyenda_textos = [f'{cliente}: {porcentaje} ({numero:.2f})' for cliente, porcentaje, numero in zip(ventas_por_cliente.index, porcentajes, numeros_ventas)]
    ax.legend(wedges, leyenda_textos, title="Clientes", loc="center left", bbox_to_anchor=(0.8, 0.5))
    
    # Mostrar el total de ventas dentro del gráfico
    ax.annotate(f'Total Ventas: {total_ventas:.2f}', xy=(0, -1.2), fontsize=12, ha='center', va='center')
    
    # Título del gráfico
    mes_nombre = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes-1]
    plt.title(f'Ventas Totales por Cliente para {mes_nombre} {año}', fontsize=16, fontweight='bold')
    
    # Mostrar el gráfico
    plt.show()




if __name__ == '__main__':
    sys.exit(app.exec_())