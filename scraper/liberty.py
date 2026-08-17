from scraper.base import get_http_session, clean_text, generar_link_maps, normalize_state_name


def parse_liberty_hours(horario_dict):
    if not horario_dict or not isinstance(horario_dict, dict):
        return "Lun - Vie: 08:30 AM - 05:30 PM"
    
    days_map = {
        "monday": "Lun",
        "tuesday": "Mar",
        "wednesday": "Mie",
        "thursday": "Jue",
        "friday": "Vie",
        "saturday": "Sab",
        "sunday": "Dom"
    }
    
    parts = []
    for day_en, day_es in days_map.items():
        intervals = horario_dict.get(day_en)
        if intervals and isinstance(intervals, list):
            time_strs = []
            for item in intervals:
                in_t = item.get("in", "")
                out_t = item.get("out", "")
                if in_t and out_t:
                    time_strs.append(f"{in_t} - {out_t}")
            if time_strs:
                parts.append(f"{day_es}: {', '.join(time_strs)}")
                
    return " | ".join(parts) if parts else "Lun - Vie: 08:30 AM - 05:30 PM"


def scrape_liberty():
    print("[+] Extrayendo oficinas de LIBERTY EXPRESS (Directorio Oficial)...")
    url = "https://libertyexpress.com/wp-json/konocimiento/v1/sucursales?region=venezuela"
    session = get_http_session()
    
    try:
        response = session.get(url, timeout=25)
        response.raise_for_status()
        data = response.json()
        
        oficinas = []
        for item in data:
            title = clean_text(item.get("title", ""))
            slug = clean_text(item.get("slug", ""))
            nombre = f"LIBERTY EXPRESS {title}" if not title.upper().startswith("LIBERTY") else title
            
            datos = item.get("datos", {}) or {}
            location = datos.get("location", {}) or {}
            address = datos.get("address", {}) or {}
            contact = datos.get("contact", {}) or {}
            
            estado_raw = clean_text(location.get("state", ""))
            ciudad = clean_text(location.get("city", "")).title()
            estado = normalize_state_name(estado_raw, ciudad)
            
            direccion = clean_text(address.get("full", address.get("short", "")))
            
            phone_list = contact.get("phone", [])
            phones = [clean_text(p) for p in phone_list if clean_text(p)]
            telefono = ", ".join(phones) if phones else ""
            
            horario = parse_liberty_hours(datos.get("horario", {}))
            
            pluscode = location.get("pluscode", "")
            maps_url = generar_link_maps("", "", f"{nombre} {direccion} {ciudad} Venezuela") if not pluscode else f"https://www.google.com/maps/search/?api=1&query={pluscode.replace(' ', '+')}"
            
            oficinas.append({
                "Empresa": "LIBERTY EXPRESS",
                "Codigo": slug,
                "Nombre": nombre,
                "Estado": estado,
                "Ciudad": ciudad,
                "Direccion": direccion,
                "Telefono": telefono,
                "Horario": horario,
                "Latitud": "",
                "Longitud": "",
                "Google Maps": maps_url
            })
            
        print(f"    -> Extraccion exitosa LIBERTY EXPRESS: {len(oficinas)} oficinas procesadas.")
        return oficinas
    except Exception as e:
        print(f"    [!] Error extrayendo oficinas de LIBERTY EXPRESS: {e}")
        return []
