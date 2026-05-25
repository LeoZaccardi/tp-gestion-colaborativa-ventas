# Revisión QA y Seguridad del Proyecto

## Rol simulado

P3 - Revisor y QA.

## Revisión de estructura

Se verifica que el repositorio respeta la estructura solicitada:

- datos/
- scripts/
- resultados/
- docs/
- evidencias/
- README.md
- .gitignore

## Revisión de seguridad

Se verifica que no se incorporaron tokens, claves ni credenciales dentro del repositorio.

El archivo .gitignore contempla archivos temporales y sensibles, como:

- __pycache__/
- .ipynb_checkpoints/
- *.log
- .env
- *.token
- *.key

## Revisión técnica

El script utiliza rutas relativas para permitir su ejecución en Google Colab sin depender de rutas locales absolutas.

También se verifica que el análisis genera resultados reproducibles:

- resumen_ventas.csv
- ventas_por_mes.csv
- ventas_por_producto.csv
- grafico_ventas_mensuales.png

## Observación final

El proyecto cumple con la trazabilidad solicitada, ya que los commits realizados se vinculan con los issues de Jira mediante los identificadores GCV-1, GCV-2 y GCV-3.
