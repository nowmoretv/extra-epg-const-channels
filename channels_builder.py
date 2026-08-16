import re
import json
import os

ARCHIVO_M3U = "lista.m3u"
ARCHIVO_SALIDA = "channels.js"

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
            # 1. Categoría (group-title)
            group_match = re.search(r'group-title="([^"]*)"', linea, re.IGNORECASE)
            category = group_match.group(1) if group_match else "General"

            # Omitir canales ocultos
            if category.lower() == "hidden":
                continue

            # 2. Dial (tvg-chno)
            chno_match = re.search(r'tvg-chno="([^"]*)"', linea)
            dial_str = chno_match.group(1) if chno_match else "0"
            try:
                dial = int(dial_str)
            except ValueError:
                dial = dial_str

            # 3. Logo (tvg-logo)
            logo_match = re.search(r'tvg-logo="([^"]*)"', linea)
            logo = logo_match.group(1) if logo_match else ""

            # 4. ID y Name (texto tras la coma)
            if "," in linea:
                nombre_canal = linea.split(",")[-1].strip()
            else:
                nombre_canal = f"Canal {dial}"

            canal_obj = {
                "dial": dial,
                "id": nombre_canal,
                "name": nombre_canal,
                "category": category,
                "logo": logo
            }
            lista_canales.append(canal_obj)

    # Ordenar por número de dial
    lista_canales.sort(key=lambda c: c["dial"] if isinstance(c["dial"], int) else 9999)

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
