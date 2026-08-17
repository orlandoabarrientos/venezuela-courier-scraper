from scraper.base import get_http_session, clean_text, generar_link_maps, normalize_state_name


def scrape_mrw():
    print("[+] Extrayendo oficinas de MRW (Localizador Oficial)...")
    url = "https://mrwve.com/api/agencias"
    session = get_http_session()
    
    try:
        response = session.get(url, timeout=25)
        response.raise_for_status()
        data = response.json()
        
        oficinas = []
        for item in data:
            nombre_raw = clean_text(item.get("nombre", ""))
            if not nombre_raw.upper().startswith("MRW"):
                nombre = f"MRW {nombre_raw}"
            else:
                nombre = nombre_raw
                
            estado_raw = clean_text(item.get("estado", ""))
            estado = normalize_state_name(estado_raw)
            
            codigo = clean_text(item.get("codigo", ""))
            direccion = clean_text(item.get("direccion", ""))
            lat = clean_text(item.get("latitud", ""))
            lng = clean_text(item.get("longitud", ""))
            
            ciudad = nombre_raw.title()
            
            maps_url = generar_link_maps(lat, lng, f"{nombre} {estado} Venezuela")
            
            oficinas.append({
                "Empresa": "MRW",
                "Codigo": codigo,
                "Nombre": nombre,
                "Estado": estado,
                "Ciudad": ciudad,
                "Direccion": direccion,
                "Telefono": "",
                "Horario": "Lun - Vie: 08:00 AM - 05:00 PM",
                "Latitud": lat,
                "Longitud": lng,
                "Google Maps": maps_url
            })
            
        print(f"    -> Extraccion exitosa MRW: {len(oficinas)} agencias procesadas.")
        return oficinas
    except Exception as e:
        print(f"    [!] Error extrayendo agencias de MRW: {e}")
        return []
