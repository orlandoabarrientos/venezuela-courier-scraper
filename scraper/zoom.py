import json
from scraper.base import get_http_session, clean_text, generar_link_maps, infer_state


def parse_zoom_hours(hours_raw):
    if not hours_raw or str(hours_raw).strip() in ["null", "", "{}"]:
        return ""
    try:
        data = json.loads(hours_raw)
        schedule_parts = []
        days_map = {
            "mon": "Lun", "tue": "Mar", "wed": "Mie", 
            "thu": "Jue", "fri": "Vie", "sat": "Sab", "sun": "Dom"
        }
        for d, label in days_map.items():
            val = data.get(d)
            if val and val != "0" and isinstance(val, list) and len(val) > 0:
                schedule_parts.append(f"{label}: {', '.join(val)}")
        return " | ".join(schedule_parts)
    except Exception:
        return ""


def scrape_zoom():
    print("[+] Extrayendo oficinas de ZOOM (Directorio Oficial)...")
    url = "https://zoom.red/wp-admin/admin-ajax.php?action=asl_load_stores&load_all=1"
    session = get_http_session()
    
    try:
        response = session.get(url, timeout=25)
        response.raise_for_status()
        data = response.json()
        
        oficinas = []
        for item in data:
            nombre = clean_text(item.get("title", ""))
            if not nombre.upper().startswith("ZOOM"):
                nombre = f"ZOOM {nombre}"
                
            ciudad = clean_text(item.get("city", "")).upper()
            estado_raw = clean_text(item.get("state", ""))
            estado = infer_state(ciudad, estado_raw)
            
            direccion = clean_text(item.get("street", ""))
            lat = clean_text(item.get("lat", ""))
            lng = clean_text(item.get("lng", ""))
            telefono = clean_text(item.get("phone", ""))
            codigo = clean_text(item.get("sku", item.get("id", "")))
            
            horario = parse_zoom_hours(item.get("open_hours", ""))
            dias = clean_text(item.get("days_str", ""))
            if dias and not horario:
                horario = dias
                
            maps_url = generar_link_maps(lat, lng, f"{nombre} {ciudad} Venezuela")
            
            oficinas.append({
                "Empresa": "ZOOM",
                "Codigo": codigo,
                "Nombre": nombre,
                "Estado": estado,
                "Ciudad": ciudad.title() if ciudad else "",
                "Direccion": direccion,
                "Telefono": telefono,
                "Horario": horario,
                "Latitud": lat,
                "Longitud": lng,
                "Google Maps": maps_url
            })
            
        print(f"    -> Extraccion exitosa ZOOM: {len(oficinas)} oficinas procesadas.")
        return oficinas
    except Exception as e:
        print(f"    [!] Error extrayendo oficinas de ZOOM: {e}")
        return []
