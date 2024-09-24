import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox, QDateEdit, QApplication, QMessageBox
from PyQt5.QtCore import QDate

# Crear la instancia de QApplication solo una vez
app = QApplication(sys.argv)

def formato_dolares(x, pos):
    """Formatear valores en dólares con puntos de miles y dos decimales."""
    return f'${x:,.2f}'

def estilo_grafico(data, titulo, xlabel, ylabel, total=None):
    # Ordenar y crear la figura
    data = data.sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))  # Cambiar tamaño en función del número de barras
    fig.patch.set_facecolor('lightgray')  # Color de fondo de la figura
    ax.set_facecolor('white')  # Color de fondo del gráfico
    
    # Graficar las barras
    data.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax, width=0.6)
    
    # Ajustes de fuente según la cantidad de datos
    fontsize = max(8, min(14, 280 // len(data)))  # Ajustar el tamaño de la letra
    ax.set_title(titulo, fontsize=fontsize, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    
    ax.tick_params(axis='x', rotation=90, labelsize=fontsize)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Formatear los ejes y las etiquetas en formato de dólares
    ax.yaxis.set_major_formatter(FuncFormatter(formato_dolares))
    
    # Mostrar etiquetas en las barras con formato de dólares
    for container in ax.containers:
        labels = [f'${v:,.2f}' for v in container.datavalues]
        ax.bar_label(container, labels=labels, label_type='edge', fontsize=fontsize - 2, rotation=0)
    
    # Mostrar total si está disponible
    if total:
        ax.text(0.95, 0.95, f'Total: ${total:,.2f}', transform=ax.transAxes,
                fontsize=fontsize, fontweight='bold', ha='right', va='top',
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='black'))
    
    plt.tight_layout()
    plt.show(block=False)



def ajustar_dialogo(dialog):
    dialog.setFixedSize(400, 300)  # Ajustar tamaño del diálogo
    
def ver_consumado_por_cliente(cliente, fecha_inicio, fecha_fin):
    from data import cargar_datos_rem_nal
    import pandas as pd
    import matplotlib.pyplot as plt
    from PyQt5.QtWidgets import QMessageBox

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

        # Crear gráfico de torta
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(ventas_cliente, labels=ventas_cliente.index, autopct='%1.1f%%',
                                           startangle=90, colors=plt.cm.Paired.colors)
        ax.axis('equal')  # Asegura que el gráfico de torta sea circular.

        # Título del gráfico
        plt.title(f'Ventas Totales de {cliente} desde {fecha_inicio} hasta {fecha_fin}', fontsize=16, fontweight='bold')

        # Mostrar el gráfico
        plt.show()



        
        
def mostrar_consumado(cliente, df):
    ventas_cliente = df[df['CLIENTE'] == cliente].groupby('CLIENTE')['US$'].sum()
    estilo_grafico(ventas_cliente, f'Ventas Totales de {cliente}', 'Cliente', 'Total Ventas en US$')

def mostrar_deudas_por_empresa():
    from data import cargar_datos_cxc
    import pandas as pd
    import matplotlib.pyplot as plt

    df = cargar_datos_cxc()
    deudas_por_empresa = df.groupby('CUSTOMER')['OPEN BALANCE'].sum()

    # Filtrar las deudas para ignorar las que son 0 y ordenar de mayor a menor
    deudas_por_empresa = deudas_por_empresa[deudas_por_empresa > 0].sort_values(ascending=False)

    if deudas_por_empresa.empty:
        print("No hay deudas para mostrar.")
        return

    # Limitar la cantidad de empresas en la leyenda a 40
    top_n = 36  # Número de empresas que aparecerán en la leyenda
    deudas_top_empresas = deudas_por_empresa[:top_n]
    otros = deudas_por_empresa[top_n:].sum()

    # Añadir un grupo "Otros" para el resto de las empresas
    if otros > 0:
        deudas_top_empresas['Otros'] = otros

    # Crear el gráfico de torta con un tamaño ajustado
    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts = ax.pie(deudas_top_empresas, labels=None, startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  # Asegura que el gráfico de torta sea circular

    # Calcular el total de deudas y los porcentajes
    total_deudas = deudas_top_empresas.sum()
    porcentajes = [(valor / total_deudas) * 100 for valor in deudas_top_empresas]
    numeros_deudas = deudas_top_empresas.values

    # Formato de dólares
    def formato_dolares(x):
        return f'${x:,.2f}'

    # Añadir la leyenda con los nombres de las empresas, porcentajes y números de deudas
    leyenda_textos = [
        f'{empresa}: {porcentaje:.2f}% ({formato_dolares(numero)})'
        for empresa, porcentaje, numero in zip(deudas_top_empresas.index, porcentajes, numeros_deudas)
    ]

    # Colocar la leyenda a la derecha del gráfico y moverla a la izquierda
    ax.legend(wedges, leyenda_textos, title="Empresas", loc="center left", bbox_to_anchor=(0.9, 0.5), fontsize=8)

    # Mover el texto del total de deudas más a la izquierda
    ax.annotate(f'Total Deuda: {formato_dolares(total_deudas)}', xy=(-1.8, 0), fontsize=12, ha='center', va='center')

    # Título en la parte superior de la torta
    plt.title('Deudas Totales por Empresa', fontsize=16, fontweight='bold')

    # Ajustar el layout para que no se corte la leyenda
    plt.subplots_adjust(right=0.75, top=0.85)  # Ajusta márgenes según sea necesario

    # Mostrar el gráfico
    plt.show()


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

    # Crear el gráfico de torta con un tamaño ajustado
    fig, ax = plt.subplots(figsize=(10, 8))  # Ajusta el tamaño de la figura según sea necesario

    wedges, texts = ax.pie(ventas_por_empresa, labels=None, startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  # Asegura que el gráfico de torta sea circular.

    # Calcular el total de ventas y los porcentajes
    total_ventas = ventas_por_empresa.sum()
    porcentajes = [(valor / total_ventas) * 100 for valor in ventas_por_empresa]
    numeros_ventas = ventas_por_empresa.values

    # Formato de dólares
    def formato_dolares(x):
        return f'${x:,.2f}'

    # Añadir la leyenda con los nombres de las empresas, porcentajes y números de ventas
    leyenda_textos = [
        f'{empresa}: {porcentaje:.2f}% ({formato_dolares(numero)})'
        for empresa, porcentaje, numero in zip(ventas_por_empresa.index, porcentajes, numeros_ventas)
    ]

    # Colocar la leyenda a la derecha del gráfico
    ax.legend(wedges, leyenda_textos, title="Empresas", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)

    # Mover el texto del total de ventas más a la izquierda
    ax.annotate(f'Total Ventas: {formato_dolares(total_ventas)}', xy=(-1.8, 0), fontsize=12, ha='center', va='center')

    # Título en la parte superior de la torta
    mes_nombre = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes-1]
    plt.title(f'Ventas Totales por Empresa para {mes_nombre} {año}', fontsize=16, fontweight='bold')

    # Ajustar el layout para que no se corte la leyenda
    plt.subplots_adjust(right=0.75, top=0.85)  # Ajusta márgenes según sea necesario

    # Mostrar el gráfico
    plt.show()




def mostrar_graficas_consumado():
    from data import cargar_datos_cxc
    import pandas as pd
    import matplotlib.pyplot as plt

    df = cargar_datos_cxc()

    # Agrupar las ventas por cliente
    ventas_por_cliente = df.groupby('CUSTOMER')['TOTAL US$'].sum().sort_values(ascending=False)

    # Filtrar para eliminar valores de 0
    ventas_por_cliente = ventas_por_cliente[ventas_por_cliente > 0]

    if ventas_por_cliente.empty:
        print("No hay ventas disponibles para mostrar.")
        return

    # Limitar la cantidad de clientes en la leyenda a 40
    top_n = 35  # Número de clientes que aparecerán en la leyenda
    ventas_top_clientes = ventas_por_cliente[:top_n]
    otros = ventas_por_cliente[top_n:].sum()

    # Añadir un grupo "Otros" para el resto de los clientes
    if otros > 0:
        ventas_top_clientes['Otros'] = otros

    # Crear el gráfico de torta con un tamaño ajustado
    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts = ax.pie(ventas_top_clientes, labels=None, startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  # Asegura que el gráfico de torta sea circular

    # Calcular el total de ventas y los porcentajes
    total_ventas = ventas_top_clientes.sum()
    porcentajes = [(valor / total_ventas) * 100 for valor in ventas_top_clientes]
    numeros_ventas = ventas_top_clientes.values

    # Formato de dólares
    def formato_dolares(x):
        return f'${x:,.2f}'

    # Añadir la leyenda con los nombres de los clientes, porcentajes y números de ventas
    leyenda_textos = [
        f'{cliente}: {porcentaje:.2f}% ({formato_dolares(numero)})'
        for cliente, porcentaje, numero in zip(ventas_top_clientes.index, porcentajes, numeros_ventas)
    ]

    # Colocar la leyenda a la derecha del gráfico
    ax.legend(wedges, leyenda_textos, title="Clientes", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)

    # Mover el texto del total de ventas más a la izquierda
    ax.annotate(f'Total Ventas: {formato_dolares(total_ventas)}', xy=(-1.8, 0), fontsize=12, ha='center', va='center')

    # Título en la parte superior de la torta
    plt.title('Ventas Totales por Cliente', fontsize=16, fontweight='bold')

    # Ajustar el layout para que no se corte la leyenda
    plt.subplots_adjust(right=0.7, top=0.85)

    # Mostrar el gráfico
    plt.show()



def consultar_creditos_por_empresa():
    from data import cargar_datos_cxc
    df = cargar_datos_cxc()
    dialog = QDialog()
    dialog.setWindowTitle('Consultar Créditos por Empresa')
    dialog.setFixedSize(400, 300)  # Ajusta el tamaño máximo del diálogo

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
    import pandas as pd
    df = cargar_datos_cxc()
    df['DATE'] = pd.to_datetime(df['DATE'])
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)
    
    df_filtrado = df[(df['CUSTOMER'] == empresa) &
                     (df['DATE'] >= fecha_inicio) &
                     (df['DATE'] <= fecha_fin)]

    # Verificar si hay créditos
    if df_filtrado.empty:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"La empresa {empresa} no tiene créditos en este periodo de tiempo.")
        msg.setWindowTitle("Sin Datos")
        msg.exec_()
    else:
        creditos_por_fecha = df_filtrado.groupby('DATE')['CREDIT'].sum()

        # Filtrar para eliminar valores en 0
        creditos_por_fecha = creditos_por_fecha[creditos_por_fecha > 0]

        # Verificar si después de filtrar hay datos para graficar
        if creditos_por_fecha.empty:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"La empresa {empresa} no tiene créditos mayores a 0 en este periodo de tiempo.")
            msg.setWindowTitle("Sin Datos")
            msg.exec_()
        else:
            # Calcular el total de créditos
            total_creditos = creditos_por_fecha.sum()

            # Mostrar el gráfico incluyendo el total
            estilo_grafico(creditos_por_fecha, f'Créditos de {empresa} ({fecha_inicio.date()} a {fecha_fin.date()})', 'Fecha', 'Total Créditos en US$', total=total_creditos)


def filtrar_y_graficar(cliente, fecha_inicio, fecha_fin):
    from data import cargar_datos_cxc
    import pandas as pd
    from matplotlib import pyplot as plt
    from matplotlib.ticker import FuncFormatter

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
        # Agrupar las ventas por mes y año
        df_filtrado['Mes-Año'] = df_filtrado['DATE'].dt.to_period('M')
        ventas_por_mes = df_filtrado.groupby('Mes-Año')['TOTAL US$'].sum()

        # Ignorar valores nulos o cero
        ventas_por_mes = ventas_por_mes[ventas_por_mes > 0]

        # Verificar si hay datos para graficar
        if ventas_por_mes.empty:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"No hay ventas mayores a 0 para el cliente {cliente} en este periodo.")
            msg.setWindowTitle("Sin Datos")
            msg.exec_()
            return

        # Calcular el total de ventas
        total_ventas = ventas_por_mes.sum()

        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(10, 6))  # Tamaño ajustado
        fig.patch.set_facecolor('white')  # Fondo blanco
        ax.set_facecolor('lightgray')

        # Graficar las barras con un tamaño reducido
        ventas_por_mes.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax, width=0.4)

        # Ajustes de fuente
        ax.set_title(f'Ventas de {cliente} ({fecha_inicio.date()} a {fecha_fin.date()})', fontsize=10, fontweight='bold')
        ax.set_xlabel('Mes', fontsize=9)
        ax.set_ylabel('Total Ventas en US$', fontsize=9)

        # Cambiar los nombres de los meses a español
        meses_esp = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                     7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}

        # Usar el índice original (sin ordenar) para las etiquetas
        ax.set_xticklabels([f'{meses_esp[mes.month]} {mes.year}' for mes in ventas_por_mes.index.to_timestamp()], rotation=45)

        ax.tick_params(axis='x', labelsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Formatear los ejes y las etiquetas en formato de dólares
        ax.yaxis.set_major_formatter(FuncFormatter(formato_dolares))

        # Mostrar etiquetas en las barras ajustando la posición
        for container in ax.containers:
            labels = [f'${v:,.2f}' for v in container.datavalues]
            ax.bar_label(container, labels=labels, label_type='edge', fontsize=8, rotation=0, padding=3)  # Ajustar el padding

        # Mostrar total en la esquina superior derecha
        ax.text(0.95, 0.95, f'Total: ${total_ventas:,.2f}', transform=ax.transAxes,
                fontsize=9, fontweight='bold', ha='right', va='top',
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='black'))

        plt.tight_layout()
        plt.show(block=False)




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
        msg.setText(f"No hay devoluciones para el cliente {cliente}.")
        msg.setWindowTitle("Sin Datos")
        msg.exec_()
        return

    # Agrupar y sumar devoluciones por fecha
    devoluciones_por_fecha = devoluciones_cliente.groupby('FECHA')['DEVOLUCION US$'].sum()

    # Calcular el total de devoluciones
    total_devoluciones = devoluciones_por_fecha.sum()

    # Mostrar el gráfico incluyendo el total
    estilo_grafico(devoluciones_por_fecha, f'Devoluciones de {cliente}', 'Fecha', 'Total Devoluciones en US$', total=total_devoluciones)


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