import sys
import os
import time
from collections import Counter

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scraper.zoom import scrape_zoom
from scraper.mrw import scrape_mrw
from scraper.tealca import scrape_tealca
from scraper.liberty import scrape_liberty
from scraper.exporter import export_to_csv


def print_summary(oficinas, elapsed_time=0.0):
    if not oficinas:
        print("[!] No se encontraron oficinas.")
        return

    print("\n" + "=" * 60)
    print("           RESUMEN ESTADISTICO DE EXTRACCION")
    print("=" * 60)

    empresa_counts = Counter(o["Empresa"] for o in oficinas)
    print("\n[+] Oficinas por Empresa:")
    for emp, count in sorted(empresa_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   * {emp:<18}: {count:>4} oficinas")
    print(f"   {'-'*30}")
    print(f"   TOTAL             : {len(oficinas):>4} oficinas")

    estado_counts = Counter(o["Estado"] for o in oficinas if o.get("Estado"))
    print("\n[+] Distribucion por Estado:")
    for edo, count in sorted(estado_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   * {edo:<25}: {count:>3} oficinas")
        
    print(f"\n[+] Tiempo total de extraccion: {elapsed_time:.2f} segundos")
    print("=" * 60 + "\n")


def main():
    csv_file = "agencias_venezuela.csv"
    
    if os.path.exists(csv_file):
        try:
            os.remove(csv_file)
        except Exception:
            pass

    print("=" * 60)
    print("  SCRAPER DE OFICINAS DE ENVIOS EN VENEZUELA")
    print("=" * 60)
    print(f"Archivo de salida: {csv_file}\n")

    start_time = time.time()
    todas_oficinas = []

    todas_oficinas.extend(scrape_zoom())
    todas_oficinas.extend(scrape_mrw())
    todas_oficinas.extend(scrape_tealca())
    todas_oficinas.extend(scrape_liberty())

    elapsed_time = time.time() - start_time

    print_summary(todas_oficinas, elapsed_time)
    export_to_csv(todas_oficinas, csv_file)

    print(f"[OK] Proceso completado exitosamente. Total procesadas: {len(todas_oficinas)}\n")


if __name__ == "__main__":
    main()
