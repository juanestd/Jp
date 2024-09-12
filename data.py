import pandas as pd

def cargar_datos():
    archivo_excel = 'C:\\Users\\juane\\Downloads\\CXC 2023-2024.xlsx'
    # Leer la hoja 'cxc' desde la fila 6 (indexada como 5 en Python)
    df = pd.read_excel(archivo_excel, sheet_name='CXC', header=5)
    return df
