import csv
import calendar
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

# CONFIGURACIÓN GENERAL
ESCALA = 1.4  
ANCHO, ALTO = 4200, 2480
MESES_X, MESES_Y = 4, 3

# CONTROLES DE ESPACIADO
ESPACIO_ENTRE_MESES_X = 0
ESPACIO_ENTRE_MESES_Y = 0.0
ESPACIO_TITULO_MES = 2
ESPACIO_TITULO_ANIO = 1.0

# MEDIDAS BASE
CELDA_X = int(64 * ESCALA)
CELDA_Y = int(52 * ESCALA)

COLOR_FONDO = "#FFFFFF"
COLOR_TEXTO = "#111827"
COLOR_SEMANA = "#6B7280"

DIAS_SEMANA = ["L", "M", "MI", "J", "V", "S", "D"]

# Meses en español
MESES_ES = [
    "",
    "ENERO", "FEBRERO", "MARZO", "ABRIL",
    "MAYO", "JUNIO", "JULIO", "AGOSTO",
    "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
]

# PALETA
PALETA_FUERTE = [
    "#E11D48",  # rojo
    "#2563EB",  # azul
    "#16A34A",  # verde
    "#7C3AED",  # violeta
    "#EA580C",  # naranja
    "#0891B2",  # cian
    "#DB2777",  # rosa
    "#65A30D",  # lima
    "#CA8A04",  # amarillo oscuro
    "#0F766E",  # teal
]

# FUENTES
def cargar_fuente(size, bold=False):
    rutas = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for r in rutas:
        try:
            return ImageFont.truetype(r, size)
        except:
            pass
    return ImageFont.load_default()

# COLOR POR MES + NOMBRE
def color_por_mes_y_nombre(mes, nombre, nombres_del_mes):
    nombres_ordenados = sorted(nombres_del_mes)
    idx = nombres_ordenados.index(nombre)

    # rotación por mes
    rot = mes % len(PALETA_FUERTE)
    paleta_mes = PALETA_FUERTE[rot:] + PALETA_FUERTE[:rot]

    return paleta_mes[idx % len(paleta_mes)]

# CARGAR CSV
def cargar_cumpleanos(ruta):
    datos = []
    with open(ruta, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            datos.append((r["nombre"], int(r["dia"]), int(r["mes"])))
    return datos

# DIBUJAR MES
def dibujar_mes(draw, anio, mes, x0, y0,
                cumple_por_fecha, nombres_por_mes, fonts):

    font_mes, font_dia, font_small = fonts
    cal = calendar.Calendar(calendar.MONDAY)

    draw.text((x0, y0), MESES_ES[mes], font=font_mes, fill=COLOR_TEXTO)

    y_sem = y0 + int(42 * ESCALA * ESPACIO_TITULO_MES)

    for i, d in enumerate(DIAS_SEMANA):
        draw.text(
            (x0 + i * CELDA_X, y_sem),
            d,
            font=font_small,
            fill=COLOR_SEMANA
        )

    inicio_y = y_sem + int(38 * ESCALA)

    for f, semana in enumerate(cal.monthdayscalendar(anio, mes)):
        for c, dia in enumerate(semana):
            if dia == 0:
                continue

            cx = x0 + c * CELDA_X + CELDA_X // 2
            cy = inicio_y + f * CELDA_Y + CELDA_Y // 2

            if (mes, dia) in cumple_por_fecha:
                for nombre in cumple_por_fecha[(mes, dia)]:
                    color = color_por_mes_y_nombre(
                        mes, nombre, nombres_por_mes[mes]
                    )
                    r = int(18 * ESCALA)
                    w = max(2, int(3 * ESCALA))
                    draw.ellipse(
                        [cx - r, cy - r, cx + r, cy + r],
                        outline=color,
                        width=w
                    )

            draw.text(
                (cx, cy),
                str(dia),
                anchor="mm",
                font=font_dia,
                fill=COLOR_TEXTO
            )

    # Lista lateral
    lx = x0 + CELDA_X * 7 + int(20 * ESCALA)
    ly = inicio_y

    for (m, d), nombres in sorted(cumple_por_fecha.items()):
        if m == mes:
            for n in nombres:
                c = color_por_mes_y_nombre(
                    m, n, nombres_por_mes[m]
                )
                draw.ellipse(
                    [lx, ly + int(8 * ESCALA),
                     lx + int(14 * ESCALA), ly + int(22 * ESCALA)],
                    fill=c
                )
                draw.text(
                    (lx + int(22 * ESCALA), ly),
                    n,
                    font=font_small,
                    fill=COLOR_TEXTO
                )
                ly += int(26 * ESCALA)

# GENERAR CALENDARIO
def generar_calendario(anio, cumpleanos):

    cumple_por_fecha = defaultdict(list)
    nombres_por_mes = defaultdict(list)

    for n, d, m in cumpleanos:
        cumple_por_fecha[(m, d)].append(n)
        if n not in nombres_por_mes[m]:
            nombres_por_mes[m].append(n)

    img = Image.new("RGB", (ANCHO, ALTO), COLOR_FONDO)
    draw = ImageDraw.Draw(img)

    font_year = cargar_fuente(int(110 * ESCALA), bold=True)
    font_mes = cargar_fuente(int(48 * ESCALA), bold=True)
    font_dia = cargar_fuente(int(28 * ESCALA))
    font_small = cargar_fuente(int(30 * ESCALA))

    w = draw.textlength(str(anio), font=font_year)
    draw.text(
        ((ANCHO - w) / 2, int(50 * ESCALA * ESPACIO_TITULO_ANIO)),
        str(anio),
        font=font_year,
        fill=COLOR_TEXTO
    )

    caja_w = CELDA_X * 7 + int(260 * ESCALA)
    caja_h = CELDA_Y * 6 + int(160 * ESCALA)

    ox = (ANCHO - MESES_X * caja_w) // 2
    oy = (ALTO - MESES_Y * caja_h) // 2 + int(40 * ESCALA)

    for mes in range(1, 13):
        col = (mes - 1) % MESES_X
        fila = (mes - 1) // MESES_X

        x0 = ox + col * caja_w
        y0 = oy + fila * caja_h

        dibujar_mes(
            draw, anio, mes, x0, y0,
            cumple_por_fecha,
            nombres_por_mes,
            (font_mes, font_dia, font_small)
        )

    salida = f"calendario_{anio}_final_es.png"
    img.save(salida)
    print(f"Calendario generado: {salida}")

# MAIN
if __name__ == "__main__":
  for i in range(2026, 2030):
    anio = i
    datos = cargar_cumpleanos("cumpleee.csv")
    generar_calendario(anio, datos)
