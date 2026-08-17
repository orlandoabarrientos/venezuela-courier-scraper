import re
from scraper.base import get_http_session, clean_text, generar_link_maps, normalize_state_name


CITY_CORRECTIONS = {
    "los-chaguaramos": "Caracas",
    "el-cafetal": "Caracas",
    "ccct-2": "Caracas",
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
    "merida": "Mérida"
}


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
            
            map_url = fields.get("url_google_map", "")
            lat, lng = "", ""
            if map_url:
                coords_match = re.search(r"q=(-?\d+\.\d+),(-?\d+\.\d+)", map_url)
                if coords_match:
                    lat = coords_match.group(1)
                    lng = coords_match.group(2)
                    
            maps_url = generar_link_maps(lat, lng, f"{nombre} {ciudad} {estado} Venezuela") if not map_url else map_url
            
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
