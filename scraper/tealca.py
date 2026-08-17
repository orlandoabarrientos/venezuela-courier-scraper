import re
from scraper.base import get_http_session, clean_text, generar_link_maps, normalize_state_name


CITY_CORRECTIONS = {
    "los-chaguaramos": "Caracas",
    "el-cafetal": "Caracas",
    "ccct-2": "Caracas",
    "ccct": "Caracas",
    "los-palos-grandes": "Caracas",
    "la-candelaria": "Caracas",
    "el-cementerio": "Caracas",
    "la-candelaria-c-c-lord-center": "Caracas",
    "los-caobos": "Caracas",
    "filas-de-mariches": "Caracas",
    "prados-del-este": "Caracas",
    "el-rosal-chacao": "Caracas",
    "sabana-grande": "Caracas",
    "boleta": "Caracas",
    "montecristo": "Caracas",
    "la-california": "Caracas",
    "el-paraso": "Caracas",
    "catia": "Caracas",
    "san-martin": "Caracas",
    "la-trinidad": "Caracas",
    "yaritagua": "Yaritagua",
    "san-fernando-de-apure": "San Fernando De Apure",
    "el-tocuyo": "El Tocuyo",
    "machiques-villa-del-rosario": "Machiques",
    "puerto-piritu": "Puerto Píritu",
    "puerto-cabello-moron": "Puerto Cabello",
    "caucagua-higuerote-barlovento-tacarigua": "Higuerote",
    "san-juan-de-los-morros-villa-de-cura": "San Juan De Los Morros",
    "santa-teresa": "Santa Teresa Del Tuy",
    "catia-la-mar": "Catia La Mar",
    "bailadores-tovar-lagunillas-santa-cruz-de-mora": "Tovar",
    "merida-norte": "Mérida",
    "santa-barbara-del-zulia": "Santa Bárbara Del Zulia",
    "santa-barbara-de-barinas": "Santa Bárbara De Barinas",
    "dabajuro": "Dabajuro",
    "rubio": "Rubio",
    "el-temblador": "Temblador",
    "guasdualito": "Guasdualito",
    "socopo": "Socopó",
    "alto-barinas": "Barinas",
    "barinas-centro-comercial-barinas": "Barinas",
    "merida": "Mérida",
    "punta-de-mata": "Punta De Mata",
    "punta-cardon": "Punto Fijo",
    "tipuro": "Maturín",
    "maiquetia": "Maiquetía",
    "san-antonio-de-los-altos": "San Antonio De Los Altos",
    "tinaquillo": "Tinaquillo",
    "turmero": "Turmero",
    "las-delicias": "Maracay",
    "ciudad-bolivar": "Ciudad Bolívar",
    "higuerote": "Higuerote"
}


def parse_tealca_map(map_raw, office_name="", city="", state=""):
    if not map_raw:
        return "", "", generar_link_maps("", "", f"TEALCA {office_name} {city} {state} Venezuela")
        
    lat, lng = "", ""
    clean_map = clean_text(map_raw)
    
    if "<iframe" in map_raw or "iframe" in clean_map:
        src_match = re.search(r'src=["\']([^"\']+)["\']', map_raw)
        src_url = src_match.group(1) if src_match else map_raw
        
        lat_match = re.search(r'!3d(-?\d+\.\d+)', src_url)
        lng_match = re.search(r'!2d(-?\d+\.\d+)', src_url)
        if lat_match and lng_match:
            lat = lat_match.group(1)
            lng = lng_match.group(1)
            return lat, lng, f"https://www.google.com/maps?q={lat},{lng}"
            
        coords_match = re.search(r'q=(-?\d+\.\d+),(-?\d+\.\d+)', src_url)
        if coords_match:
            lat = coords_match.group(1)
            lng = coords_match.group(2)
            return lat, lng, f"https://www.google.com/maps?q={lat},{lng}"
            
        return "", "", generar_link_maps("", "", f"TEALCA {office_name} {city} {state} Venezuela")
        
    coords_match = re.search(r'q=(-?\d+\.\d+),(-?\d+\.\d+)', map_raw)
    if coords_match:
        lat = coords_match.group(1)
        lng = coords_match.group(2)
        return lat, lng, f"https://www.google.com/maps?q={lat},{lng}"
        
    if map_raw.startswith("http"):
        return "", "", map_raw
        
    return "", "", generar_link_maps("", "", f"TEALCA {office_name} {city} {state} Venezuela")


def scrape_tealca():
    print("[+] Extrayendo oficinas de TEALCA (Directorio Oficial)...")
    url = "https://www.tealca.com/wp-json/tealca-oficinas/v1/offices"
    session = get_http_session()
    
    try:
        response = session.get(url, timeout=25)
        response.raise_for_status()
        json_data = response.json()
        data = json_data.get("data", [])
        
        oficinas = []
        for item in data:
            post = item.get("post", {})
            fields = item.get("fields", {})
            
            nombre_raw = clean_text(post.get("name", ""))
            nombre = f"TEALCA {nombre_raw}"
            codigo = clean_text(fields.get("code", ""))
            slug = clean_text(item.get("slug", ""))
            state_raw = clean_text(item.get("state", ""))
            city_raw = clean_text(item.get("city", ""))
            
            ciudad = city_raw.title() if city_raw else ""
            if not ciudad or ciudad.lower() in ["", "d.capital", "distrito capital"]:
                if slug in CITY_CORRECTIONS:
                    ciudad = CITY_CORRECTIONS[slug]
                elif "capital" in state_raw.lower() or "d.capital" in state_raw.lower():
                    ciudad = "Caracas"
                else:
                    for k, v in CITY_CORRECTIONS.items():
                        if k in slug or slug in k:
                            ciudad = v
                            break
                if not ciudad:
                    ciudad = nombre_raw.title()
                    
            estado = normalize_state_name(state_raw, ciudad)
            
            acerca_raw = clean_text(fields.get("acerca_de", ""))
            if acerca_raw and len(acerca_raw) > 25 and not acerca_raw.startswith("http"):
                direccion = acerca_raw
                if "Envía paquetes" in direccion:
                    direccion = direccion.split("Envía paquetes")[0].strip()
                elif "Envia paquetes" in direccion:
                    direccion = direccion.split("Envia paquetes")[0].strip()
            else:
                direccion = f"Oficina TEALCA {nombre_raw}, {ciudad}, Estado {estado}"
                
            phone_match = re.search(r"(?:0412|0414|0424|0416|0426|02\d{2})[.\-\s]?\d{3}[.\-\s]?\d{2}[.\-\s]?\d{2}", acerca_raw)
            telefono = phone_match.group(0) if phone_match else ""
            
            map_raw = fields.get("url_google_map", "")
            lat, lng, maps_url = parse_tealca_map(map_raw, nombre_raw, ciudad, estado)
            
            oficinas.append({
                "Empresa": "TEALCA",
                "Codigo": codigo,
                "Nombre": nombre,
                "Estado": estado,
                "Ciudad": ciudad,
                "Direccion": direccion[:250],
                "Telefono": telefono,
                "Horario": "Lun - Vie: 08:00 AM - 05:00 PM",
                "Latitud": lat,
                "Longitud": lng,
                "Google Maps": maps_url
            })
            
        print(f"    -> Extraccion exitosa TEALCA: {len(oficinas)} oficinas procesadas.")
        return oficinas
    except Exception as e:
        print(f"    [!] Error extrayendo oficinas de TEALCA: {e}")
        return []
