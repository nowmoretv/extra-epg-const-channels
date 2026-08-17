import re
import json
import os

ARCHIVO_M3U = "lista.m3u"
ARCHIVO_SALIDA = "channels.js"

def obtener_categoria_por_dial(dial):
    """
    Determina la categoría del canal según el número de dial (tvg-chno).
    """
    if not isinstance(dial, int):
        return "Otros"

    if 4 <= dial <= 199:
        return "Deportes"
    elif 200 <= dial <= 260:
        return "Cine"
    elif 261 <= dial <= 299:
        return "Series"
    elif 300 <= dial <= 399:
        return "Entretenimiento"
    elif 400 <= dial <= 499:
        return "Nacionales"
    elif 500 <= dial <= 599:
        return "Regionales"
    elif 600 <= dial <= 998:
        return "Locales"
    elif 1000 <= dial <= 1020:
        return "Portugal"
    elif 1021 <= dial <= 1100:
        return "Reino Unido"
    elif 1101 <= dial <= 1200:
        return "Francia"
    elif 1201 <= dial <= 1300:
        return "Italia"
    elif 1301 <= dial <= 1400:
        return "Alemania"
    elif 1401 <= dial <= 1500:
        return "Europa Occidental"
    elif 1501 <= dial <= 1600:
        return "Europa del Norte"
    elif 1601 <= dial <= 1700:
        return "Europa Central"
    elif 1701 <= dial <= 1999:
        return "Europa Oriental"
    elif 2000 <= dial <= 2299:
        return "Norteamérica"
    elif 2300 <= dial <= 2499:
        return "Centroamérica"
    elif 2500 <= dial <= 2999:
        return "Sudamérica"
    elif 3000 <= dial <= 3999:
        return "Asia"
    elif 4000 <= dial <= 4999:
        return "África"
    elif 5000 <= dial <= 5999:
        return "Oceanía"
    elif 7000 <= dial <= 7999:
        return "Música"
    elif 9000 <= dial <= 9999:
        return "Otros"
    else:
        return "Otros"


def generar_channels_js():
    if not os.path.exists(ARCHIVO_M3U):
        print(f"❌ Error: No se encontró el archivo {ARCHIVO_M3U}")
        return

    lista_canales = []
    print("--> Procesando lista .m3u...")

    with open(ARCHIVO_M3U, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("#EXTINF:"):
            # 1. Filtro: Si contiene "hidden", se ignora el canal por completo
            if re.search(r'\bhidden\b', linea, re.IGNORECASE):
                continue

            # 2. Dial (tvg-chno)
            chno_match = re.search(r'tvg-chno="([^"]*)"', linea)
            dial_str = chno_match.group(1) if chno_match else "0"
            try:
                dial = int(dial_str)
            except ValueError:
                dial = dial_str

            # 3. Categoría calculada según el Dial
            category = obtener_categoria_por_dial(dial)

            # 4. Logo (tvg-logo)
            logo_match = re.search(r'tvg-logo="([^"]*)"', linea)
            logo = logo_match.group(1) if logo_match else ""

            # 5. ID desde tvg-id (si no existe, queda como "")
            tvg_id_match = re.search(r'tvg-id="([^"]*)"', linea)
            canal_id = tvg_id_match.group(1) if tvg_id_match else ""

            # 6. Name (exclusivamente el texto tras la última coma)
            if "," in linea:
                nombre_canal = linea.split(",")[-1].strip()
            else:
                nombre_canal = f"Canal {dial}"

            canal_obj = {
                "dial": dial,
                "id": canal_id,
                "name": nombre_canal,
                "category": category,
                "logo": logo
            }
            lista_canales.append(canal_obj)

    # Ordenar por número de dial ascendente
    lista_canales.sort(key=lambda c: c["dial"] if isinstance(c["dial"], int) else 99999)

    print(f"--> Generando {ARCHIVO_SALIDA} con {len(lista_canales)} canales...")
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f_js:
        f_js.write("// Archivo generado automáticamente por GitHub Actions\n")
        f_js.write("const CHANNELS = [\n")
        for c in lista_canales:
            f_js.write(
                f'  {{ dial: {json.dumps(c["dial"])}, id: {json.dumps(c["id"], ensure_ascii=False)}, '
                f'name: {json.dumps(c["name"], ensure_ascii=False)}, '
                f'category: {json.dumps(c["category"], ensure_ascii=False)}, '
                f'logo: {json.dumps(c["logo"], ensure_ascii=False)} }},\n'
            )
        f_js.write("];\n")

    print(f"✔ {ARCHIVO_SALIDA} creado con éxito.")


if __name__ == "__main__":
    generar_channels_js()
