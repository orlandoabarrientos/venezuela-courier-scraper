import re
import urllib.parse
from html import unescape
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_http_session(retries=3, backoff_factor=0.5):
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/html, */*",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
    })
    return session


def clean_text(text):
    if not text:
        return ""
    
    text = unescape(str(text))
    text = re.sub(r"<[^>]+>", " ", text)
    
    word_fixes = {
        r"\bPANAM-\b": "PANAMÁ",
        r"\bPASTELER-A\b": "PASTELERÍA",
        r"\bFARMAC-A\b": "FARMACIA",
        r"\bPANADER-A\b": "PANADERÍA",
        r"\bPELUQUER-A\b": "PELUQUERÍA",
        r"\bLICORER-A\b": "LICORERÍA",
        r"\bFERRETER-A\b": "FERRETERÍA",
        r"\bINMOBILIAR-A\b": "INMOBILIARIA",
        r"\bCARPINTER-A\b": "CARPINTERÍA",
        r"\bJOYER-A\b": "JOYERÍA",
        r"\bLIBRER-A\b": "LIBRERÍA",
        r"\bAGENC-A\b": "AGENCIA",
        r"\bCOMPA-IA\b": "COMPAÑÍA",
        r"\bCOMPAIA\b": "COMPAÑÍA",
        r"\bMU-ECO\b": "MUÑECO",
        r"\bMUECO\b": "MUÑECO",
        r"\bPE-A\b": "PEÑA",
    }
    for pattern, repl in word_fixes.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
        
    text = re.sub(r"(\d+)\ufffd(\d+\')", r"\1°\2", text)
    
    replacements = {
        "a\ufffdo": "año",
        "A\ufffdO": "AÑO",
        "espa\ufffda": "españa",
        "Espa\ufffda": "España",
        "ESPA\ufffdA": "ESPAÑA",
        "abri\ufffd": "abrió",
        "est\ufffd": "está",
        "atenci\ufffdn": "atención",
        "ATENCI\ufffdN": "ATENCIÓN",
        "AUVISI\ufffdN": "AUVISIÓN",
        "auvisi\ufffdn": "auvisión",
        "env\ufffda": "envía",
        "ENV\ufffdA": "ENVÍA",
        "panam\ufffd": "panamá",
        "PANAM\ufffd": "PANAMÁ",
        "pa\ufffds": "país",
        "pa\ufffdes": "países",
        "f\ufffdcil": "fácil",
        "r\ufffdpida": "rápida",
        "soluci\ufffdn": "solución",
        "SOLUCI\ufffdN": "SOLUCIÓN",
        "jur\ufffd": "jurí",
        "JUR\ufffd": "JURÍ",
        "trav\ufffds": "través",
        "m\ufffds": "más",
        "M\ufffdS": "MÁS",
        "informaci\ufffdn": "información",
        "INFORMACI\ufffdN": "INFORMACIÓN",
        "adquiri\ufffd": "adquirió",
        "opci\ufffdn": "opción",
        "OPCI\ufffdN": "OPCIÓN",
        "direcci\ufffdn": "dirección",
        "DIRECCI\ufffdN": "DIRECCIÓN",
        "ubicaci\ufffdn": "ubicación",
        "UBICACI\ufffdN": "UBICACIÓN",
        "tel\ufffdfono": "teléfono",
        "TEL\ufffdFONO": "TELÉFONO",
        "Pante\ufffdn": "Panteón",
        "PANTE\ufffdN": "PANTEÓN",
        "Para\ufffdso": "Paraíso",
        "PARA\ufffdSO": "PARAÍSO",
        "\ufffd": "",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
        
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_state_name(state_raw, city=""):
    if city:
        city_norm = clean_text(city).upper()
        if city_norm in VENEZUELA_CITY_STATE_MAP:
            return VENEZUELA_CITY_STATE_MAP[city_norm]
            
    if not state_raw:
        return "Venezuela"
        
    st = clean_text(state_raw).strip()
    st_upper = st.upper()
    
    canonical_map = {
        "AMAZONAS": "Amazonas",
        "ANZOATEGUI": "Anzoátegui",
        "ANZOÁTEGUI": "Anzoátegui",
        "APURE": "Apure",
        "ARAGUA": "Aragua",
        "BARINAS": "Barinas",
        "BOLIVAR": "Bolívar",
        "BOLÍVAR": "Bolívar",
        "CARABOBO": "Carabobo",
        "COJEDES": "Cojedes",
        "DELTA AMACURO": "Delta Amacuro",
        "DISTRITO CAPITAL": "Distrito Capital",
        "D.CAPITAL": "Distrito Capital",
        "D. CAPITAL": "Distrito Capital",
        "GRAN CARACAS": "Distrito Capital",
        "FALCON": "Falcón",
        "FALCÓN": "Falcón",
        "GUARICO": "Guárico",
        "GUÁRICO": "Guárico",
        "LA GUAIRA": "La Guaira",
        "VARGAS": "La Guaira",
        "LARA": "Lara",
        "MERIDA": "Mérida",
        "MÉRIDA": "Mérida",
        "MIRANDA": "Miranda",
        "MONAGAS": "Monagas",
        "NUEVA ESPARTA": "Nueva Esparta",
        "PORTUGUESA": "Portuguesa",
        "SUCRE": "Sucre",
        "TACHIRA": "Táchira",
        "TÁCHIRA": "Táchira",
        "TRUJILLO": "Trujillo",
        "YARACUY": "Yaracuy",
        "ZULIA": "Zulia",
        "DEPENDENCIAS FEDERALES": "Dependencias Federales",
        "INTERNACIONAL (EE.UU.)": "Internacional (EE.UU.)",
        "INTERNACIONAL (PANAMÁ)": "Internacional (Panamá)"
    }
    
    if st_upper in canonical_map:
        return canonical_map[st_upper]
        
    for k, v in canonical_map.items():
        if k in st_upper:
            return v
            
    return st.title() if st else "Venezuela"


def generar_link_maps(lat, lng, query=""):
    lat_s = str(lat).strip() if lat is not None else ""
    lng_s = str(lng).strip() if lng is not None else ""
    
    if lat_s and lng_s and lat_s not in ["0", "", "None", "null"] and lng_s not in ["0", "", "None", "null"]:
        return f"https://www.google.com/maps?q={lat_s},{lng_s}"
    
    if query:
        encoded = urllib.parse.quote_plus(query.strip())
        return f"https://www.google.com/maps/search/?api=1&query={encoded}"
    
    return ""


VENEZUELA_CITY_STATE_MAP = {
    "CARACAS": "Distrito Capital",
    "MARACAIBO": "Zulia",
    "VALENCIA": "Carabobo",
    "BARQUISIMETO": "Lara",
    "MARACAY": "Aragua",
    "CIUDAD GUAYANA": "Bolívar",
    "PUERTO ORDAZ": "Bolívar",
    "SAN CRISTOBAL": "Táchira",
    "SAN CRISTÓBAL": "Táchira",
    "BARCELONA": "Anzoátegui",
    "PUERTO LA CRUZ": "Anzoátegui",
    "MATURIN": "Monagas",
    "MATURÍN": "Monagas",
    "MERIDA": "Mérida",
    "MÉRIDA": "Mérida",
    "CIUDAD BOLIVAR": "Bolívar",
    "CIUDAD BOLÍVAR": "Bolívar",
    "CUMANA": "Sucre",
    "CUMANÁ": "Sucre",
    "BARINAS": "Barinas",
    "CABIMAS": "Zulia",
    "PUNTO FIJO": "Falcón",
    "LOS TEQUES": "Miranda",
    "CORO": "Falcón",
    "GUATIRE": "Miranda",
    "GUARENAS": "Miranda",
    "SAN FELIPE": "Yaracuy",
    "ACARIGUA": "Portuguesa",
    "CARORA": "Lara",
    "EL TIGRE": "Anzoátegui",
    "EL TIGRITO": "Anzoátegui",
    "GUASDUALITO": "Apure",
    "SAN CARLOS": "Cojedes",
    "VALERA": "Trujillo",
    "SAN FERNANDO": "Apure",
    "SAN FERNANDO DE APURE": "Apure",
    "PORLAMAR": "Nueva Esparta",
    "LA GUAIRA": "La Guaira",
    "MAIQUETIA": "La Guaira",
    "MAIQUETÍA": "La Guaira",
    "PUERTO CABELLO": "Carabobo",
    "TUCUPITA": "Delta Amacuro",
    "PUERTO AYACUCHO": "Amazonas",
    "CHARALLAVE": "Miranda",
    "SAN ANTONIO DE LOS ALTOS": "Miranda",
    "SAN ANTONIO DEL TACHIRA": "Táchira",
    "SAN ANTONIO DEL TÁCHIRA": "Táchira",
    "CAGUA": "Aragua",
    "TURMERO": "Aragua",
    "LA VICTORIA": "Aragua",
    "VILLA DE CURA": "Aragua",
    "CALABOZO": "Guárico",
    "SAN JUAN DE LOS MORROS": "Guárico",
    "VALLE DE LA PASCUA": "Guárico",
    "ANACO": "Anzoátegui",
    "CARUPANO": "Sucre",
    "CARÚPANO": "Sucre",
    "EL VIGIA": "Mérida",
    "EL VIGÍA": "Mérida",
    "CABUDARE": "Lara",
    "CIUDAD OJEDA": "Zulia",
    "SANTA BARBARA DEL ZULIA": "Zulia",
    "MACHIQUES": "Zulia",
    "SANTA ELENA DE UAIREN": "Bolívar",
    "UPATA": "Bolívar",
    "TINAQUILLO": "Cojedes",
    "TRUJILLO": "Trujillo",
    "BOCONO": "Trujillo",
    "BOCONÓ": "Trujillo",
    "GUANARE": "Portuguesa",
    "ARAURE": "Portuguesa",
    "CHIVACOA": "Yaracuy",
    "NIRGUA": "Yaracuy",
    "YARITAGUA": "Yaracuy",
    "SAN JUAN DE COLON": "Táchira",
    "RUBIO": "Táchira",
    "TARIBA": "Táchira",
    "TARIBA NUEVA": "Táchira",
    "TÁRIBA": "Táchira",
    "LA FRIA": "Táchira",
    "LA FRÍA": "Táchira",
    "LA GRITA": "Táchira",
    "SANTA RITA": "Zulia",
    "ROSARIO DE PERIJA": "Zulia",
    "VILLA DEL ROSARIO": "Zulia",
    "MENE GRANDE": "Zulia",
    "SAN FRANCISCO": "Zulia",
    "HIGUEROTE": "Miranda",
    "RIO CHICO": "Miranda",
    "RÍO CHICO": "Miranda",
    "OCUMARE DEL TUY": "Miranda",
    "SANTA TERESA DEL TUY": "Miranda",
    "SANTA LUCIA": "Miranda",
    "CATIA LA MAR": "La Guaira",
    "CARABALLEDA": "La Guaira",
    "CARAYACA": "La Guaira",
    "GUASIPATI": "Bolívar",
    "TUMEREMO": "Bolívar",
    "EL CALLAO": "Bolívar",
    "CAICARA DEL ORINOCO": "Bolívar",
    "LECHERIA": "Anzoátegui",
    "LECHERIAS": "Anzoátegui",
    "LECHERÍA": "Anzoátegui",
    "PARIAGUAN": "Anzoátegui",
    "CANTAURA": "Anzoátegui",
    "PUERTO PIRITU": "Anzoátegui",
    "PUERTO PÍRITU": "Anzoátegui",
    "CLARINES": "Anzoátegui",
    "ZARAZA": "Guárico",
    "ALTAGRACIA DE ORITUCO": "Guárico",
    "CHAGUARAMAS": "Guárico",
    "EL SOCORRO": "Guárico",
    "SANTA MARIA DE IPIRE": "Guárico",
    "TUCUPIDO": "Guárico",
    "EL SOMBRERO": "Guárico",
    "SOCOPO": "Barinas",
    "SOCOPÓ": "Barinas",
    "SANTA BARBARA DE BARINAS": "Barinas",
    "SABANETA": "Barinas",
    "PEDRAZA": "Barinas",
    "BARINITAS": "Barinas",
    "CIUDAD BOLIVIA": "Barinas",
    "TOVAR": "Mérida",
    "BAILADORES": "Mérida",
    "EJIDO": "Mérida",
    "MUCUCHIES": "Mérida",
    "NUEVA BOLIVIA": "Mérida",
    "LAGUNILLAS": "Mérida",
    "SANTA ELENA DE ARENALES": "Mérida",
    "SANTA ELENA DE ARENALES (EDO. MERIDA)": "Mérida",
    "CAJA SECA": "Zulia",
    "BACHAQUERO": "Zulia",
    "LA CONCEPCION": "Zulia",
    "LOS PUERTOS DE ALTAGRACIA": "Zulia",
    "EL VENADO": "Zulia",
    "CHURUGUARA": "Falcón",
    "DABAJURO": "Falcón",
    "MENE DE MAUROA": "Falcón",
    "MORON": "Carabobo",
    "GUACARA": "Carabobo",
    "LOS GUAYOS": "Carabobo",
    "SAN JOAQUIN": "Carabobo",
    "MARIARA": "Carabobo",
    "NAGUANAGUA": "Carabobo",
    "SAN DIEGO": "Carabobo",
    "TOCUYITO": "Carabobo",
    "BEJUMA": "Carabobo",
    "MONTALBAN": "Carabobo",
    "GUIGUE": "Carabobo",
    "PALO NEGRO": "Aragua",
    "SANTA CRUZ": "Aragua",
    "SANTA CRUZ DE ARAGUA": "Aragua",
    "SAN MATEO": "Aragua",
    "EL LIMON": "Aragua",
    "SAN CASIMIRO": "Aragua",
    "COLONIA TOVAR": "Aragua",
    "SANTA RITA - ARAGUA": "Aragua",
    "LA ASUNCION": "Nueva Esparta",
    "JUAN GRIEGO": "Nueva Esparta",
    "PAMPATAR": "Nueva Esparta",
    "EL VALLE": "Nueva Esparta",
    "PUNTA DE MATA": "Monagas",
    "TEMBLADOR": "Monagas",
    "TUREN": "Portuguesa",
    "TURÉN": "Portuguesa",
    "QUIBOR": "Lara",
    "QUÍBOR": "Lara",
    "EL TOCUYO": "Lara",
    "LA PASTORA": "Lara",
    "ACHAGUAS": "Apure",
    "BIRUACA": "Apure",
    "CAPACHO": "Táchira",
    "COLON": "Táchira",
    "COLONCITO": "Táchira",
    "EL PINAL": "Táchira",
    "LA TENDIDA": "Táchira",
    "PALMIRA": "Táchira",
    "URENA": "Táchira",
    "UREÑA": "Táchira",
    "CARRIZAL": "Miranda",
    "CUA": "Miranda",
    "CUÁ": "Miranda",
    "SAN FELIX": "Bolívar",
    "MIAMI": "Internacional (EE.UU.)",
    "PANAMA": "Internacional (Panamá)"
}


def infer_state(city, default_state=""):
    if default_state and clean_text(default_state) not in ["", "Venezuela"]:
        return normalize_state_name(default_state, city)
    
    if not city:
        return "Venezuela"
    
    city_norm = clean_text(city).upper()
    if city_norm in VENEZUELA_CITY_STATE_MAP:
        return VENEZUELA_CITY_STATE_MAP[city_norm]
    
    for c_k, s_v in VENEZUELA_CITY_STATE_MAP.items():
        if c_k == city_norm or (len(c_k) > 4 and c_k in city_norm):
            return s_v
            
    return normalize_state_name(default_state, city) if default_state else "Venezuela"
