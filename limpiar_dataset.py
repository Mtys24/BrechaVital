# ============================================================
# LIMPIEZA DATASET GES
# Proyecto: Clasificación de diagnósticos GES
# Archivo entrada: dataset_original.csv
# Archivo salida: dataset_limpio.csv
# ============================================================

import pandas as pd
import unicodedata
import re

# ============================================================
# 1. Cargar dataset original
# ============================================================

df = pd.read_csv("dataset_original.csv")

print("===== DATASET ORIGINAL =====")
print("Filas y columnas:", df.shape)
print(df.head())

print("\nInformación general:")
print(df.info())

print("\nValores nulos por columna:")
print(df.isnull().sum())

print("\nDistribución original de GES:")
print(df["ges"].value_counts())


# ============================================================
# 2. Función para limpiar texto
# ============================================================

def limpiar_texto(texto):
    if pd.isna(texto):
        return ""

    texto = str(texto)

    # Pasar todo a mayúsculas
    texto = texto.upper()

    # Quitar tildes
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")

    # Reemplazar caracteres poco útiles por espacios
    texto = re.sub(r"[^A-Z0-9\s/+\-.]", " ", texto)

    # Quitar espacios repetidos
    texto = re.sub(r"\s+", " ", texto)

    # Quitar espacios al inicio y al final
    texto = texto.strip()

    return texto


# ============================================================
# 3. Limpiar columna diagnostic
# ============================================================

df["diagnostic"] = df["diagnostic"].apply(limpiar_texto)


# ============================================================
# 4. Limpiar columna age
# ============================================================

df["age"] = pd.to_numeric(df["age"], errors="coerce")

# Edades inválidas
df.loc[df["age"] < 0, "age"] = None
df.loc[df["age"] > 110, "age"] = None

# En este dataset aparecen edades 0.
# Se consideran como dato faltante o mal ingresado.
df.loc[df["age"] == 0, "age"] = None

# Rellenar edades faltantes con la mediana
mediana_edad = df["age"].median()
df["age"] = df["age"].fillna(mediana_edad)

# Pasar edad a número entero
df["age"] = df["age"].astype(int)


# ============================================================
# 5. Limpiar columna ges
# ============================================================

df["ges"] = df["ges"].astype(str).str.strip()

df["ges"] = df["ges"].replace({
    "True": True,
    "False": False,
    "TRUE": True,
    "FALSE": False,
    "true": True,
    "false": False,
    "1": True,
    "0": False
})

df["ges"] = df["ges"].astype(bool)


# ============================================================
# 6. Eliminar registros problemáticos
# ============================================================

filas_antes = len(df)

# Eliminar filas sin diagnóstico
df = df[df["diagnostic"] != ""]

# Eliminar duplicados exactos
df = df.drop_duplicates()

filas_despues = len(df)


# ============================================================
# 7. Revisión final
# ============================================================

print("\n===== DATASET LIMPIO =====")
print("Filas y columnas:", df.shape)
print(df.head())

print("\nFilas antes de limpieza:", filas_antes)
print("Filas después de limpieza:", filas_despues)
print("Filas eliminadas:", filas_antes - filas_despues)

print("\nValores nulos finales:")
print(df.isnull().sum())

print("\nDistribución final de GES:")
print(df["ges"].value_counts())

print("\nEdad mínima:", df["age"].min())
print("Edad máxima:", df["age"].max())
print("Edad promedio:", round(df["age"].mean(), 2))
print("Mediana de edad utilizada:", mediana_edad)

print("\nEjemplos de diagnósticos limpios:")
print(df["diagnostic"].head(20))


# ============================================================
# 8. Guardar dataset limpio
# ============================================================

df.to_csv("dataset_limpio.csv", index=False, encoding="utf-8")

print("\nArchivo generado correctamente: dataset_limpio.csv")