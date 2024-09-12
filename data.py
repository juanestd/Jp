import pandas as pd

def cargar_datos_cxc():
    archivo_excel = 'C:\\Users\\juane\\Downloads\\CXC 2023-2024.xlsx'
    df = pd.read_excel(archivo_excel, sheet_name='CXC', header=5)
    return df

def cargar_datos_rem_nal():
    archivo_excel = 'C:\\Users\\juane\\Downloads\\CXC 2023-2024.xlsx'
    df = pd.read_excel(archivo_excel, sheet_name='REM NAL', header=5)
    return df

def cargar_datos_facturas_nal():
    archivo_excel = 'C:\\Users\\juane\\Downloads\\CXC 2023-2024.xlsx'
    df = pd.read_excel(archivo_excel, sheet_name='FACTURAS NAL', header=5)
    return df

def cargar_datos_creditos_reclamos():
    archivo_excel = 'C:\\Users\\juane\\Downloads\\CXC 2023-2024.xlsx'
    df = pd.read_excel(archivo_excel, sheet_name='Creditos-Reclamos', header=5)
    return df