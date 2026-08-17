# 📦 Scraper de Agencias de Envíos en Venezuela

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()

Herramienta modular en Python para la extracción, normalización y geolocalización de sucursales activas de las principales empresas de encomiendas en Venezuela (**MRW**, **ZOOM**, **TEALCA** y **LIBERTY EXPRESS**).

---

## 🎯 Casos de Uso

- **E-commerce & Checkouts:** Alimentar selectores de agencias y modales de envío en tiendas online.
- **Logística & Despacho:** Centralizar rutas y puntos de retiro para optimización de entregas.
- **Análisis de Cobertura:** Evaluar la densidad de agencias por estado o municipio.

---

## 📋 Ejemplo de Datos Extraídos (`agencias_venezuela.csv`)

| Empresa | Estado | Nombre / Código | Dirección | Google Maps |
| :--- | :--- | :--- | :--- | :--- |
| **ZOOM** | Distrito Capital | Sede Principal La Urbina | Calle 7, Sector Sur, Edif. ZOOM | [Ver ubicación](https://maps.google.com) |
| **MRW** | Lara | 1307000 - Barquisimeto Este | Av. Lara con Calle 3, Qta AL-99 | [Ver ubicación](https://maps.google.com) |
| **TEALCA** | Miranda | 0101 - Los Ruices | Av. Diego Cisneros, Edif. Tealca | [Ver ubicación](https://maps.google.com) |
| **LIBERTY**| Carabobo | Valencia San Diego | C.C. San Diego, PB Local 12 | [Ver ubicación](https://maps.google.com) |

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/orlandoabarrientos/venezuela-courier-scraper.git
cd venezuela-courier-scraper
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el scraper
```bash
python main.py
```

El script eliminará cualquier CSV previo y generará automáticamente el archivo `agencias_venezuela.csv` actualizado con más de 800 agencias en la raíz del proyecto.

---

## 🏗️ Arquitectura del Proyecto

```text
├── main.py                 # Orquestador principal y punto de entrada CLI
├── requirements.txt        # Dependencias del proyecto (requests, urllib3, beautifulsoup4)
├── .gitignore              # Archivos y artefactos ignorados por Git
├── README.md               # Documentación y guía de instalación
├── agencias_venezuela.csv  # Archivo CSV de salida generado en la raíz
└── scraper/                # Módulos desacoplados de extracción y procesamiento
    ├── __init__.py         # Exportación del paquete scraper
    ├── base.py             # Limpieza de texto, sesiones HTTP y mapeo de 24 estados
    ├── zoom.py             # Extractor de ZOOM (373 oficinas)
    ├── mrw.py              # Extractor de MRW (250 oficinas)
    ├── tealca.py           # Extractor de TEALCA (137 oficinas)
    ├── liberty.py          # Extractor de LIBERTY EXPRESS (57 oficinas)
    └── exporter.py         # Módulo de exportación con codificación UTF-8 BOM
```
