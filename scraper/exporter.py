import csv
import os

CSV_HEADERS = [
    "Empresa",
    "Codigo",
    "Nombre",
    "Estado",
    "Ciudad",
    "Direccion",
    "Telefono",
    "Horario",
    "Latitud",
    "Longitud",
    "Google Maps"
]


def export_to_csv(oficinas, file_path="agencias_venezuela.csv"):
    if not oficinas:
        print("[!] No hay oficinas para exportar.")
        return False
        
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            
        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(oficinas)
            
        print(f"[OK] Archivo CSV exportado con exito: {os.path.abspath(file_path)} ({len(oficinas)} registros)")
        return True
    except Exception as e:
        print(f"[!] Error al exportar archivo CSV: {e}")
        return False
