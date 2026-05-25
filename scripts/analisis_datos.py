"""
Análisis de ventas simuladas.

El objetivo del script es transformar datos de ventas en información útil
para la toma de decisiones: ventas totales, producto más vendido, ventas por mes
y ventas por producto.

El código utiliza rutas relativas para poder ejecutarse correctamente.
"""

import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt


RUTA_DATOS = "datos/ventas_simuladas.csv"
CARPETA_RESULTADOS = "resultados"


def leer_ventas(ruta_archivo):
    """Lee el archivo CSV y devuelve una lista de ventas."""
    ventas = []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            venta = {
                "id": int(fila["id"]),
                "fecha": fila["fecha"],
                "producto": fila["producto"],
                "cantidad": int(fila["cantidad"]),
                "precio_unitario": float(fila["precio_unitario"]),
            }

            venta["total"] = venta["cantidad"] * venta["precio_unitario"]
            ventas.append(venta)

    return ventas


def calcular_ventas_totales(ventas):
    """Calcula el importe total vendido."""
    total = 0

    for venta in ventas:
        total += venta["total"]

    return total


def calcular_ventas_por_producto(ventas):
    """Agrupa las ventas por producto y por cantidad de unidades."""
    ventas_por_producto = defaultdict(float)
    unidades_por_producto = defaultdict(int)

    for venta in ventas:
        producto = venta["producto"]
        ventas_por_producto[producto] += venta["total"]
        unidades_por_producto[producto] += venta["cantidad"]

    return ventas_por_producto, unidades_por_producto


def calcular_ventas_por_mes(ventas):
    """Agrupa las ventas por mes usando el formato AAAA-MM."""
    ventas_por_mes = defaultdict(float)

    for venta in ventas:
        mes = venta["fecha"][:7]
        ventas_por_mes[mes] += venta["total"]

    return ventas_por_mes


def obtener_producto_mas_vendido(unidades_por_producto):
    """Devuelve el producto con mayor cantidad de unidades vendidas."""
    producto_mas_vendido = None
    mayor_cantidad = 0

    for producto, cantidad in unidades_por_producto.items():
        if cantidad > mayor_cantidad:
            producto_mas_vendido = producto
            mayor_cantidad = cantidad

    return producto_mas_vendido, mayor_cantidad


def guardar_resumen(total_ventas, producto_mas_vendido, cantidad_producto):
    """Guarda un resumen general del análisis."""
    ruta_salida = os.path.join(CARPETA_RESULTADOS, "resumen_ventas.csv")

    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["indicador", "valor"])
        escritor.writerow(["ventas_totales", round(total_ventas, 2)])
        escritor.writerow(["producto_mas_vendido", producto_mas_vendido])
        escritor.writerow(["unidades_producto_mas_vendido", cantidad_producto])


def guardar_ventas_por_producto(ventas_por_producto, unidades_por_producto):
    """Guarda las ventas agrupadas por producto."""
    ruta_salida = os.path.join(CARPETA_RESULTADOS, "ventas_por_producto.csv")

    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["producto", "unidades_vendidas", "ventas_totales"])

        for producto in sorted(ventas_por_producto.keys()):
            escritor.writerow([
                producto,
                unidades_por_producto[producto],
                round(ventas_por_producto[producto], 2)
            ])


def guardar_ventas_por_mes(ventas_por_mes):
    """Guarda las ventas agrupadas por mes."""
    ruta_salida = os.path.join(CARPETA_RESULTADOS, "ventas_por_mes.csv")

    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["mes", "ventas_totales"])

        for mes in sorted(ventas_por_mes.keys()):
            escritor.writerow([mes, round(ventas_por_mes[mes], 2)])


def generar_grafico_ventas_mensuales(ventas_por_mes):
    """Genera un gráfico simple con la evolución mensual de ventas."""
    meses = sorted(ventas_por_mes.keys())
    importes = [ventas_por_mes[mes] for mes in meses]

    plt.figure(figsize=(8, 5))
    plt.plot(meses, importes, marker="o")
    plt.title("Evolución mensual de ventas")
    plt.xlabel("Mes")
    plt.ylabel("Ventas totales")
    plt.xticks(rotation=45)
    plt.tight_layout()

    ruta_grafico = os.path.join(CARPETA_RESULTADOS, "grafico_ventas_mensuales.png")
    plt.savefig(ruta_grafico)
    plt.close()


def main():
    """Función principal del programa."""
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    ventas = leer_ventas(RUTA_DATOS)

    total_ventas = calcular_ventas_totales(ventas)
    ventas_por_producto, unidades_por_producto = calcular_ventas_por_producto(ventas)
    ventas_por_mes = calcular_ventas_por_mes(ventas)
    producto_mas_vendido, cantidad_producto = obtener_producto_mas_vendido(unidades_por_producto)

    guardar_resumen(total_ventas, producto_mas_vendido, cantidad_producto)
    guardar_ventas_por_producto(ventas_por_producto, unidades_por_producto)
    guardar_ventas_por_mes(ventas_por_mes)
    generar_grafico_ventas_mensuales(ventas_por_mes)

    print("Análisis finalizado correctamente.")
    print(f"Ventas totales: ${total_ventas:,.2f}")
    print(f"Producto más vendido: {producto_mas_vendido} ({cantidad_producto} unidades)")


if __name__ == "__main__":
    main()
