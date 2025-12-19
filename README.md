# Proyectitos
Repositorio con proyectos personales desarrollados para práctica y automatización de tareas. El código puede reutilizarse como referencia.
# Calendario 
## Descripción

Script en Python que genera calendarios anuales en alta resolución y en español a partir de un archivo CSV con cumpleaños.  
La función principal es `generar_calendario(anio, datos)`, donde `anio` es un entero y `datos` se cargan desde un CSV usando `cargar_cumpleanos`.  
El proyecto fue desarrollado en Google Colab, por lo que la ruta de los archivos puede variar y es necesario subir manualmente el CSV y las fuentes `DejaVuSans.ttf` y `DejaVuSans-Bold.ttf` al entorno de ejecución.
El archivo CSV debe contener tres columnas con encabezados:
- `nombre`: nombre de la persona es str
- `dia`: día del mes (número entero)
- `mes`: mes (número entero del 1 al 12)

Ejemplo:
```csv
nombre,dia,mes
Luz,5,3
Kari,18,7
Dani,22,12
