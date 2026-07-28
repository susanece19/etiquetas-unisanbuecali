import os
import textwrap
import math
import csv
import re
import zipfile
from io import BytesIO, StringIO
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Generador de Etiquetas de Seguridad - Colmena Seguros",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# RUTAS DE ASSETS
# ==============================================================================
ASSETS_DIR = "assets"
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo_colmena.png")
SGA_DIR = os.path.join(ASSETS_DIR, "sga")
EPP_DIR = os.path.join(ASSETS_DIR, "epp")
UN_DIR = os.path.join(ASSETS_DIR, "un")

def ensure_local_fonts():
    """Descarga automáticamente fuentes TrueType con soporte completo para tildes (á, é, í, ó, ú, ñ) en assets/fonts/ si no existen."""
    os.makedirs(FONTS_DIR, exist_ok=True)
    reg_font_path = os.path.join(FONTS_DIR, "DejaVuSans.ttf")
    bold_font_path = os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf")

    if not os.path.exists(reg_font_path) or not os.path.exists(bold_font_path):
        import urllib.request
        try:
            if not os.path.exists(reg_font_path):
                urllib.request.urlretrieve(
                    "https://cdn.jsdelivr.net/fontsource/fonts/dejavu-sans@latest/latin-400-normal.ttf",
                    reg_font_path
                )
            if not os.path.exists(bold_font_path):
                urllib.request.urlretrieve(
                    "https://cdn.jsdelivr.net/fontsource/fonts/dejavu-sans@latest/latin-700-normal.ttf",
                    bold_font_path
                )
        except Exception:
            pass

ensure_local_fonts()

# Helper para listar archivos de imagen en un directorio
def list_image_files(directory):
    if not os.path.exists(directory):
        return []
    valid_exts = ('.png', '.jpg', '.jpeg', '.webp')
    return sorted([f for f in os.listdir(directory) if f.lower().endswith(valid_exts)])

sga_files = list_image_files(SGA_DIR)
epp_files = list_image_files(EPP_DIR)
un_files = list_image_files(UN_DIR)

# ==============================================================================
# MODO DE USO: INDIVIDUAL VS LOTE (TABLA CSV)
# ==============================================================================
mode = st.sidebar.radio(
    "📌 Modo de Operación",
    options=["Etiqueta Individual", "Generación por Lote (Tabla / CSV)"],
    index=0
)

st.sidebar.divider()

font_scale = 1.0

if mode == "Etiqueta Individual":
    st.sidebar.title("🛠️ Configuración de Etiqueta")
    st.sidebar.markdown("Estructura de **Colmena Seguros (Modelo VARSOL)**")

    # Control interactivo de escala de tamaño de letra
    with st.sidebar.expander("🔤 Ajustes de Tamaño de Letra / Tipografía", expanded=True):
        font_scale = st.slider(
            "Multiplicador de Tamaño de Letra",
            min_value=0.8,
            max_value=2.0,
            value=1.1,
            step=0.1,
            help="Aumenta o disminuye proporcionalmente la letra en toda la etiqueta."
        )

    # 1. Nombre del Producto
    product_name = st.sidebar.text_input(
        "1. Nombre del Producto / Reactivo",
        value="VARSOL",
        help="Ej: VARSOL, ACETONA, ÁCIDO SULFÚRICO"
    )

    # 2. Composición
    composition_text = st.sidebar.text_area(
        "2. Composición Química",
        value="Mezcla compleja de hidrocarburos entre C9 y C12,\nparafinas: 79% CAS: 8052-41-3",
        height=80
    )

    # 3. Palabra de Advertencia
    signal_word = st.sidebar.selectbox(
        "3. Palabra de Advertencia",
        options=["Atención", "Peligro"],
        index=0
    )

    # 4. Pictogramas SGA
    selected_sga = st.sidebar.multiselect(
        "4. Pictogramas SGA / GHS",
        options=sga_files,
        default=[f for f in ["GHS02.png", "GHS07.png"] if f in sga_files] if sga_files else []
    )

    # 5. Frases H
    h_phrases_text = st.sidebar.text_area(
        "5. Indicaciones de Peligro (Frases H)",
        value="H226 Líquidos y vapores inflamables\nH302 Nocivo en caso de ingestión\nH312 Nocivo en contacto con la piel\nH332 Nocivo si se inhala\nH413 Puede ser nocivo para los organismos acuáticos",
        height=120
    )

    # 6. Frases P
    p_phrases_text = st.sidebar.text_area(
        "6. Consejos de Prudencia (Frases P)",
        value="P102 Mantener fuera del alcance de los niños\nP210 Mantener alejado del calor, chispas, llamas al descubierto\nP262 Evitar el contacto con los ojos, la piel o la ropa\nP403 Almacenar en un lugar bien ventilado\nP301+P330+P331 EN CASO DE INGESTIÓN: Enjuagarse la boca. NO provocar el vómito",
        height=140
    )

    # 7. Transporte UN
    col_un1, col_un2 = st.sidebar.columns([2, 1])
    with col_un1:
        selected_un_file = st.selectbox(
            "7a. Clase Transporte UN",
            options=un_files,
            index=un_files.index("CLASE_3.png") if "CLASE_3.png" in un_files else 0 if un_files else None
        )
    with col_un2:
        un_code = st.text_input("7b. Código UN", value="1268")

    # 8. Pictogramas EPP
    selected_epp = st.sidebar.multiselect(
        "8. Pictogramas EPP Recomendados",
        options=epp_files,
        default=epp_files if epp_files else []
    )

    # 9. Información del Proveedor
    provider_text = st.sidebar.text_area(
        "9. Información del Proveedor",
        value="CONSTELACIÓN INDUSTRIAL DEL ASEO S.A.S\n59 No. 5A - 77/85 Bogotá, Colombia\nPBX: (1) 4069777 - 3132526836",
        height=100
    )

# ==============================================================================
# LÓGICA DE DIBUJO Y CÁLCULO DINÁMICO DE ALTURA CON PIL (PILLOW)
# ==============================================================================

def load_font(size, is_bold=False):
    """Carga una fuente Truetype buscando en la carpeta local assets/fonts o en el sistema para garantizar soporte de tildes (á, é, í, ó, ú, ñ)."""
    size = int(size)
    local_ttf = os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf" if is_bold else "DejaVuSans.ttf")
    
    font_paths = [
        # 1. Fuentes descargadas localmente en assets/fonts/
        local_ttf,
        # 2. Fuentes en el directorio de trabajo local
        "DejaVuSans-Bold.ttf" if is_bold else "DejaVuSans.ttf",
        "arialbd.ttf" if is_bold else "arial.ttf",
        "LiberationSans-Bold.ttf" if is_bold else "LiberationSans-Regular.ttf",
        # 3. Rutas completas comunes en Linux / Streamlit Cloud / Ubuntu / Debian
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if is_bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if is_bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if is_bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    
    # Intento de carga directa si el sistema resuelve el nombre
    for name in ["DejaVuSans-Bold.ttf" if is_bold else "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue

    # Intenta usar la fuente por defecto escalable de Pillow (Pillow >= 10.1)
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()

def wrap_and_measure_text(draw, text, font, max_width):
    """Ajusta líneas de texto al ancho máximo exactamente con Pillow, dividiendo palabras largas si sobrepasan el ancho."""
    lines = []
    line_heights = []
    total_height = 0
    font_size = getattr(font, "size", 16)
    
    for raw_line in text.split('\n'):
        if not raw_line.strip():
            lines.append("")
            h = font_size + 6
            line_heights.append(h)
            total_height += h
            continue
        
        # Primero dividimos por espacios
        words = raw_line.split(' ')
        
        # Si alguna palabra individual es más ancha que max_width, la dividimos por guiones, comas, o caracteres
        split_words = []
        for w in words:
            bbox = draw.textbbox((0, 0), w, font=font)
            if (bbox[2] - bbox[0]) > max_width:
                # Intentar dividir por guiones, guion bajo, comas o barras inclinadas primero
                sub_parts = re.split(r'(-|_|,|\/)', w)
                sub_parts = [p for p in sub_parts if p]
                
                temp_w = ""
                for part in sub_parts:
                    test_sub = temp_w + part
                    b_sub = draw.textbbox((0, 0), test_sub, font=font)
                    if (b_sub[2] - b_sub[0]) <= max_width:
                        temp_w = test_sub
                    else:
                        if temp_w:
                            split_words.append(temp_w)
                        # Si part sigue siendo demasiado largo, dividir por caracteres
                        b_part = draw.textbbox((0, 0), part, font=font)
                        if (b_part[2] - b_part[0]) > max_width:
                            char_buf = ""
                            for ch in part:
                                test_ch = char_buf + ch
                                b_ch = draw.textbbox((0, 0), test_ch, font=font)
                                if (b_ch[2] - b_ch[0]) <= max_width:
                                    char_buf = test_ch
                                else:
                                    split_words.append(char_buf)
                                    char_buf = ch
                            if char_buf:
                                temp_w = char_buf
                        else:
                            temp_w = part
                if temp_w:
                    split_words.append(temp_w)
            else:
                split_words.append(w)
                
        current_line = []
        for word in split_words:
            test_line = ' '.join(current_line + [word]) if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_w = bbox[2] - bbox[0]
            
            if line_w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    line_str = ' '.join(current_line)
                    lines.append(line_str)
                    bbox_line = draw.textbbox((0, 0), line_str, font=font)
                    h = (bbox_line[3] - bbox_line[1]) + 6
                    line_heights.append(h)
                    total_height += h
                current_line = [word]
                
        if current_line:
            line_str = ' '.join(current_line)
            lines.append(line_str)
            bbox_line = draw.textbbox((0, 0), line_str, font=font)
            h = (bbox_line[3] - bbox_line[1]) + 6
            line_heights.append(h)
            total_height += h
        
    return lines, total_height, line_heights

# ==============================================================================
# 🧩 FUNCIONES COMPLEMENTARIAS DE PARSEO Y NORMALIZACIÓN DE BASE DE DATOS
# ==============================================================================

def format_phrases(text, prefix="H"):
    """Formatea frases H y P garantizando un salto de línea por cada código H o P o combinación de códigos (ej: P301 + P312 o P305 + P351 + P338)."""
    if not text or not str(text).strip() or any(w in str(text).lower() for w in ["sin ", "ningun", "ningún", "n/a", "none"]):
        return text.strip() if (text and str(text).strip() and "sin " in str(text).lower()) else ("Sin indicaciones de peligro." if prefix == "H" else "Sin consejos de prudencia.")
    
    cleaned = str(text).strip()
    
    # 1. Normalizar cualquier espacio o salto de línea alrededor del signo "+" para evitar saltos de línea tras "+"
    cleaned = re.sub(r'\s*\+\s*', ' + ', cleaned)
    
    # 2. Unir saltos de línea internos que no correspondan al inicio de un nuevo código H/P
    cleaned = re.sub(r'\n(?!\s*[HP]\d{3})', ' ', cleaned)
    
    # 3. Formatear para que cada nuevo código o combinación de códigos (ej: P305 + P351 + P338) empiece en su propia línea
    formatted = re.sub(r'(\.|\;)?\s*([HP]\d{3}(?:\s*\+\s*[HP]\d{3})*)', r'\n\2', cleaned)
    
    # 4. Limpiar espacios sobrantes y eliminar líneas vacías
    lines = [re.sub(r'\s+', ' ', line).strip() for line in formatted.split('\n') if line.strip()]
    return '\n'.join(lines)

def parse_sga_pictograms(sga_raw, sga_files):
    """Mapea pictogramas SGA (GHS) desde la base de datos a los archivos disponibles en assets/sga."""
    if not sga_raw or not str(sga_raw).strip() or any(w in str(sga_raw).lower() for w in ["ningun", "ningún", "n/a", "sin"]):
        return []
    
    found = []
    sga_upper = str(sga_raw).upper()
    
    for i in range(1, 10):
        code = f"GHS0{i}"
        short_code = f"GHS{i}"
        if code in sga_upper or short_code in sga_upper or f"0{i}" in sga_upper:
            fname = f"{code}.png"
            if fname in sga_files and fname not in found:
                found.append(fname)
                
    if not found:
        for f in sga_files:
            base_f = os.path.splitext(f)[0].upper()
            if base_f in sga_upper and f not in found:
                found.append(f)
                
    return found

def parse_un_class(un_raw, un_files):
    """Mapea la Clase UN de transporte a los archivos en assets/un."""
    if not un_raw or not str(un_raw).strip() or any(w in str(un_raw).lower() for w in ["n/a", "ningun", "ningún", "sin", "none", "-"]):
        return ""
    
    un_clean = str(un_raw).upper().strip()
    if un_clean in un_files:
        return un_clean
    if f"{un_clean}.png" in un_files:
        return f"{un_clean}.png"
    if f"CLASE_{un_clean}.png" in un_files:
        return f"CLASE_{un_clean}.png"
    
    match = re.search(r'(\d+(\.\d+)?)', un_clean)
    if match:
        num_str = match.group(1)
        candidate = f"CLASE_{num_str}.png"
        if candidate in un_files:
            return candidate
            
    return ""

def parse_un_code(un_code_raw):
    """Formatea la Identificación UN a formato estándar 'UN XXXX'."""
    if not un_code_raw or not str(un_code_raw).strip() or any(w in str(un_code_raw).lower() for w in ["n/a", "ningun", "ningún", "sin", "none", "-"]):
        return "N/A"
    clean = str(un_code_raw).strip()
    if clean.isdigit():
        return f"UN{clean}"
    return clean

def parse_epp_pictograms(epp_raw, epp_files):
    """Mapea los nombres de EPP desde el CSV a las imágenes circulares en assets/epp."""
    if not epp_raw or not str(epp_raw).strip() or any(w in str(epp_raw).lower() for w in ["ningun", "ningún", "n/a", "sin"]):
        return []
        
    epp_lower = str(epp_raw).lower()
    found = []
    
    mappings = [
        (["gafas", "lentes", "ojos", "anteparaparos"], "GAFAS.png"),
        (["guantes", "manos"], "GUANTES.png"),
        (["prenda", "ropa", "overol", "traje", "bata"], "PRENDA.png"),
        (["mascarilla gas", "gas", "respirador gas"], "MASCARILLA GAS.png"),
        (["mascarilla", "tapabocas", "respirador"], "MASCARILLA.png"),
        (["careta", "visor", "facial"], "CARETA.png"),
        (["botas", "calzado", "zapatos"], "BOTAS.png"),
    ]
    
    for keywords, fname in mappings:
        if fname in epp_files and fname not in found:
            for kw in keywords:
                if kw in epp_lower:
                    found.append(fname)
                    break
                    
    for ef in epp_files:
        base_name = os.path.splitext(ef)[0].lower()
        if base_name in epp_lower and ef not in found:
            found.append(ef)
            
    return found

def parse_chemical_db(content_str, sga_files, epp_files, un_files):
    """
    Parsea de forma ultra-robusta la base de datos de reactivos (CSV/TSV/delimitado por punto y coma ; o tabuladores).
    Soporta estructuras multicolumna o con separador personalizado, preservando saltos de línea multilínea dentro de comillas.
    """
    if not content_str or not content_str.strip():
        return []

    # Detectar delimitador analizando la primera línea no vacía
    first_line = content_str.replace('\r\n', '\n').replace('\r', '\n').strip().split('\n')[0]
    delimiters = [';', '\t', ',', '|']
    delimiter = ';'
    max_cnt = -1
    for d in delimiters:
        cnt = first_line.count(d)
        if cnt > max_cnt:
            max_cnt = cnt
            delimiter = d

    try:
        f = StringIO(content_str)
        reader = csv.reader(f, delimiter=delimiter)
        all_rows = list(reader)
    except Exception:
        # Fallback si falla la lectura estricta
        lines = [line for line in content_str.replace('\r\n', '\n').replace('\r', '\n').split('\n') if line.strip()]
        all_rows = [line.split(delimiter) for line in lines]

    if not all_rows:
        return []

    # Normalizar encabezado
    headers = [str(h).strip() for h in all_rows[0]]
    data_rows = all_rows[1:]

    hdr_map = {}
    for idx, h in enumerate(headers):
        clean_h = str(h).strip().lower()
        clean_h = clean_h.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
        
        if any(w in clean_h for w in ["nombre", "sustancia", "reactivo", "producto"]):
            hdr_map["nombre"] = idx
        elif any(w in clean_h for w in ["comp", "formula", "ingrediente"]):
            hdr_map["composicion"] = idx
        elif any(w in clean_h for w in ["palabra", "advertencia", "signal"]):
            hdr_map["palabra"] = idx
        elif "sga" in clean_h or "ghs" in clean_h:
            hdr_map["sga"] = idx
        elif any(w in clean_h for w in ["frase_h", "frase h", "fraseh", "indicacion", "frases h", "indicaciones"]):
            hdr_map["frase_h"] = idx
        elif any(w in clean_h for w in ["frase_p", "frase p", "frasep", "consejo", "prudencia", "frases p", "consejos"]):
            hdr_map["frase_p"] = idx
        elif "clase" in clean_h:
            hdr_map["clase_un"] = idx
        elif any(w in clean_h for w in ["codigo", "identificacion", "numero un"]) or clean_h == "un":
            hdr_map["codigo_un"] = idx
        elif "epp" in clean_h or "proteccion" in clean_h:
            hdr_map["epp"] = idx
        elif "proveedor" in clean_h or "fabricante" in clean_h:
            hdr_map["proveedor"] = idx

    parsed_results = []

    for row_idx, row in enumerate(data_rows):
        if not row:
            continue

        clean_row = [str(cell).strip() for cell in row]
        # Limpiar celdas vacías sobrantes al final
        while len(clean_row) > len(headers) and clean_row[-1] == "":
            clean_row.pop()

        if not clean_row or not any(clean_row):
            continue

        num_cols = len(clean_row)

        def get_val_by_map(key, default_pos):
            idx = hdr_map.get(key, default_pos)
            if idx is not None and idx < num_cols:
                return clean_row[idx]
            return ""

        p_name = get_val_by_map("nombre", 0)
        
        # Si la fila tiene más columnas que los encabezados (composición con delimitadores no escapados)
        comp_idx = hdr_map.get("composicion", 1)
        if num_cols > len(headers) and comp_idx is not None:
            extra_cols = num_cols - len(headers)
            comp_parts = clean_row[comp_idx : comp_idx + 1 + extra_cols]
            c_text = " ".join(comp_parts).replace("|", "\n")
        else:
            c_text = get_val_by_map("composicion", 1).replace("|", "\n")

        signal_raw = get_val_by_map("palabra", 2)
        sga_raw = get_val_by_map("sga", 3)
        h_raw = get_val_by_map("frase_h", 4)
        p_raw = get_val_by_map("frase_p", 5)
        un_class_raw = get_val_by_map("clase_un", 6)
        un_code_raw = get_val_by_map("codigo_un", 7)
        epp_raw = get_val_by_map("epp", 8)
        prov_text = get_val_by_map("proveedor", 9)

        if not p_name or p_name.upper() in ["NOMBRE", "SUSTANCIA", "REACTIVO", "NOMBRE_DEL_PRODUCTO"]:
            continue

        s_word = "Atención"
        sig_lower = signal_raw.lower()
        if "peligro" in sig_lower:
            s_word = "Peligro"
        elif "atencion" in sig_lower or "atención" in sig_lower:
            s_word = "Atención"
        elif any(w in sig_lower for w in ["ningun", "ningún", "n/a", "sin"]):
            s_word = "Ninguna"

        sga_list = parse_sga_pictograms(sga_raw, sga_files)
        h_text = format_phrases(h_raw, "H")
        p_text = format_phrases(p_raw, "P")
        un_file = parse_un_class(un_class_raw, un_files)
        un_num = parse_un_code(un_code_raw)
        epp_list = parse_epp_pictograms(epp_raw, epp_files)

        if not prov_text or prov_text.upper() in ["N/A", "NINGUNO", "NONE", ""]:
            prov_text = "Sin información del proveedor"

        parsed_results.append({
            "product_name": p_name,
            "composition": c_text if c_text else "Sin composición especificada",
            "signal_word": s_word,
            "sga_list": sga_list,
            "h_phrases": h_text,
            "p_phrases": p_text,
            "un_file": un_file,
            "un_code": un_num,
            "epp_list": epp_list,
            "provider": prov_text,
            "sga_raw": sga_raw,
            "epp_raw": epp_raw
        })

    return parsed_results

def generate_chemical_label_custom(
    p_name, c_text, s_word, sga_list, h_text, p_text, un_file, un_num, epp_list, prov_text, scale=1.2
):
    """Genera la imagen PNG de la etiqueta ajustada dinámicamente según el contenido."""
    WIDTH = 1000
    LINE_THICKNESS = 2
    PADDING_INNER = 20  # Margen de seguridad interno para que el texto no toque los bordes
    
    scale = scale if scale is not None else 1.2
    
    temp_img = Image.new("RGB", (WIDTH, 3000), "white")
    draw = ImageDraw.Draw(temp_img)
    
    # ==============================================================================
    # 🔤 CONFIGURACIÓN DE TAMAÑOS DE FUENTE
    # ==============================================================================
    font_header_title = load_font(22 * scale, is_bold=True)  # Título "COLMENA SEGUROS"
    font_signal       = load_font(30 * scale, is_bold=True)  # Palabra "ATENCIÓN" o "PELIGRO"
    font_body         = load_font(19 * scale, is_bold=False) # Frases H y Frases P
    font_body_bold    = load_font(17 * scale, is_bold=True)  # Encabezados de sección
    font_small        = load_font(15 * scale, is_bold=False) # Texto de Composición
    font_provider     = load_font(15 * scale, is_bold=False) # Datos del Proveedor
    
    col_left_w = 300
    col_right_w = WIDTH - col_left_w
    
    # Ancho máximo seguro para que el texto nunca toque las líneas verticales
    comp_max_w = col_left_w - (PADDING_INNER * 2)
    right_col_max_w = col_right_w - (PADDING_INNER * 2)
    mid_col_w = WIDTH - 2 * col_left_w  # Ancho de la celda central del Nombre del Producto
    
    comp_lines, comp_h, _ = wrap_and_measure_text(draw, c_text, font_small, comp_max_w)
    
    # Ajuste dinámico de tamaño de fuente para el Nombre del Producto
    max_prod_w = mid_col_w - (PADDING_INNER * 2)
    font_size_prod = int(38 * scale)
    min_font_size_prod = int(18 * scale)
    font_prod_name = load_font(font_size_prod, is_bold=True)
    prod_lines, prod_h, _ = wrap_and_measure_text(draw, p_name.upper(), font_prod_name, max_prod_w)
    
    while font_size_prod > min_font_size_prod and (len(prod_lines) > 2 or prod_h > 80):
        font_size_prod -= 2
        font_prod_name = load_font(font_size_prod, is_bold=True)
        prod_lines, prod_h, _ = wrap_and_measure_text(draw, p_name.upper(), font_prod_name, max_prod_w)
    
    row1_h = max(110, comp_h + 45, prod_h + 30)
    row2_h = int(55 * scale)
    
    h_lines, h_text_h, _ = wrap_and_measure_text(draw, h_text, font_body, right_col_max_w)
    p_lines, p_text_h, _ = wrap_and_measure_text(draw, p_text, font_body, right_col_max_w)
    
    h_box_h = max(90, h_text_h + 45)
    p_box_h = max(110, p_text_h + 45)
    right_col_total_h = h_box_h + p_box_h
    
    sga_count = len(sga_list)
    sga_min_h = 180 if sga_count <= 2 else 240 if sga_count <= 4 else 300
    middle_section_h = max(sga_min_h, right_col_total_h)
    
    # Anchos equilibrados para Fila 5 (UN | EPP | Proveedor)
    w_col1 = 260
    w_col2 = 410
    w_col3 = WIDTH - w_col1 - w_col2  # 330
    
    provider_lines, prov_h, _ = wrap_and_measure_text(draw, prov_text, font_provider, w_col3 - (PADDING_INNER * 2))
    
    # Cálculo de espacio para EPP (filas dinámicas)
    epp_icon_size = 46
    epp_gap_x = 10
    epp_gap_y = 10
    cols_epp = max(1, (w_col2 - 20) // (epp_icon_size + epp_gap_x))
    rows_epp = math.ceil(len(epp_list) / cols_epp) if epp_list else 1
    epp_req_h = 36 + rows_epp * epp_icon_size + (rows_epp - 1) * epp_gap_y + 15
    
    un_id_lines, un_id_h, _ = wrap_and_measure_text(draw, f"Identificación UN: {un_num}", font_body_bold, w_col1 - (PADDING_INNER * 2))
    un_req_h = 120 + un_id_h
    
    row5_h = max(140, prov_h + 50, epp_req_h, un_req_h)
    
    TOTAL_HEIGHT = row1_h + row2_h + middle_section_h + row5_h
    
    img = Image.new("RGBA", (WIDTH, TOTAL_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, WIDTH - 1, TOTAL_HEIGHT - 1], outline="black", width=LINE_THICKNESS * 2)
    
    # FILA 1
    y_curr = 0
    draw.line([(0, y_curr + row1_h), (WIDTH, y_curr + row1_h)], fill="black", width=LINE_THICKNESS)
    draw.line([(col_left_w, y_curr), (col_left_w, y_curr + row1_h)], fill="black", width=LINE_THICKNESS)
    draw.line([(WIDTH - col_left_w, y_curr), (WIDTH - col_left_w, y_curr + row1_h)], fill="black", width=LINE_THICKNESS)
    
    if os.path.exists(LOGO_PATH):
        try:
            logo_img = Image.open(LOGO_PATH).convert("RGBA")
            logo_img.thumbnail((col_left_w - 20, row1_h - 15), Image.Resampling.LANCZOS)
            lx = (col_left_w - logo_img.width) // 2
            ly = y_curr + (row1_h - logo_img.height) // 2
            img.paste(logo_img, (lx, ly), logo_img)
        except Exception:
            draw.text((20, y_curr + row1_h // 2 - 10), "COLMENA SEGUROS", fill="black", font=font_header_title)
    else:
        draw.text((20, y_curr + row1_h // 2 - 10), "COLMENA SEGUROS", fill="black", font=font_header_title)
        
    # Nombre del producto o reactivo perfectamente centrado en su recuadro central
    py_prod = y_curr + (row1_h - prod_h) // 2
    for pline in prod_lines:
        prod_bbox = draw.textbbox((0, 0), pline, font=font_prod_name)
        pw = prod_bbox[2] - prod_bbox[0]
        center_x = col_left_w + (mid_col_w - pw) // 2
        draw.text((center_x, py_prod), pline, fill="black", font=font_prod_name)
        py_prod += font_prod_name.size + 4
    
    comp_x_start = WIDTH - col_left_w
    draw.rectangle([comp_x_start, y_curr, WIDTH - 1, y_curr + 30], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    
    # Título "COMPOSICIÓN" centrado dinámicamente
    c_hdr_bbox = draw.textbbox((0, 0), "COMPOSICIÓN", font=font_body_bold)
    c_hdr_w = c_hdr_bbox[2] - c_hdr_bbox[0]
    c_hdr_x = comp_x_start + (col_left_w - c_hdr_w) // 2
    draw.text((c_hdr_x, y_curr + 6), "COMPOSICIÓN", fill="black", font=font_body_bold)
    
    cy = y_curr + 36
    for line in comp_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_small)
        lw = line_bbox[2] - line_bbox[0]
        lx = max(comp_x_start + PADDING_INNER, comp_x_start + (col_left_w - lw) // 2)
        draw.text((lx, cy), line, fill="#1F2937", font=font_small)
        cy += font_small.size + 4
        
    y_curr += row1_h
    
    # FILA 2
    draw.line([(0, y_curr + row2_h), (WIDTH, y_curr + row2_h)], fill="black", width=LINE_THICKNESS)
    draw.line([(col_left_w, y_curr), (col_left_w, y_curr + row2_h)], fill="black", width=LINE_THICKNESS)
    p_adv_bbox = draw.textbbox((0, 0), "Palabra de Advertencia", font=font_body_bold)
    p_adv_h = p_adv_bbox[3] - p_adv_bbox[1]
    draw.text((PADDING_INNER, y_curr + (row2_h - p_adv_h) // 2), "Palabra de Advertencia", fill="black", font=font_body_bold)
    
    sig_color = "#DC2626" if s_word == "Peligro" else "#D97706"
    sig_bbox = draw.textbbox((0, 0), s_word.upper(), font=font_signal)
    sw = sig_bbox[2] - sig_bbox[0]
    sx = max(col_left_w + PADDING_INNER, col_left_w + (col_right_w - sw) // 2)
    draw.text((sx, y_curr + (row2_h - (sig_bbox[3] - sig_bbox[1])) // 2), s_word.upper(), fill=sig_color, font=font_signal)
    
    y_curr += row2_h
    
    # FILA 3 Y 4 UNIFICADA
    draw.line([(0, y_curr + middle_section_h), (WIDTH, y_curr + middle_section_h)], fill="black", width=LINE_THICKNESS)
    draw.line([(col_left_w, y_curr), (col_left_w, y_curr + middle_section_h)], fill="black", width=LINE_THICKNESS)
    
    draw.rectangle([0, y_curr, col_left_w, y_curr + 28], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    sga_hdr_bbox = draw.textbbox((0, 0), "PICTOGRAMAS SGA", font=font_body_bold)
    sga_hdr_w = sga_hdr_bbox[2] - sga_hdr_bbox[0]
    draw.text(((col_left_w - sga_hdr_w) // 2, y_curr + 5), "PICTOGRAMAS SGA", fill="black", font=font_body_bold)
    
    if sga_list:
        sga_count = len(sga_list)
        box_y_start = y_curr + 30
        box_h_avail = middle_section_h - 36
        box_w_avail = col_left_w - 24  # 12px de margen a cada lado
        
        # Determinar número de columnas y filas óptimas según la cantidad
        if sga_count == 1:
            cols, rows = 1, 1
        elif sga_count == 2:
            cols, rows = 2, 1
        elif sga_count in (3, 4):
            cols, rows = 2, 2
        elif sga_count in (5, 6):
            cols, rows = 3, 2
        elif sga_count in (7, 8, 9):
            cols, rows = 3, 3
        else:
            cols = 3
            rows = math.ceil(sga_count / cols)

        gap_x = 10
        gap_y = 10

        max_w_per_icon = (box_w_avail - (cols - 1) * gap_x) // cols
        max_h_per_icon = (box_h_avail - (rows - 1) * gap_y) // rows

        # Tamaño del ícono ajustado dinámicamente al espacio máximo disponible
        icon_size = max(35, min(max_w_per_icon, max_h_per_icon, 120))

        # Ancho y alto total de la cuadrícula para centrado vertical y horizontal perfecto
        grid_w = cols * icon_size + (cols - 1) * gap_x
        grid_h = rows * icon_size + (rows - 1) * gap_y

        start_y = box_y_start + max(4, (box_h_avail - grid_h) // 2)

        for idx, sga_file in enumerate(sga_list):
            r = idx // cols
            c = idx % cols
            
            # Si la última fila tiene menos elementos, centrar esos elementos en esa fila
            items_in_this_row = sga_count - r * cols if (r == rows - 1 and sga_count % cols != 0) else cols
            row_w = items_in_this_row * icon_size + (items_in_this_row - 1) * gap_x
            row_start_x = (col_left_w - row_w) // 2

            px = row_start_x + c * (icon_size + gap_x)
            py = start_y + r * (icon_size + gap_y)

            sga_path = os.path.join(SGA_DIR, sga_file)
            if os.path.exists(sga_path):
                try:
                    s_img = Image.open(sga_path).convert("RGBA")
                    s_img = s_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                    img.paste(s_img, (int(px), int(py)), s_img)
                except Exception:
                    pass

    h_block_height = int(middle_section_h * (h_box_h / right_col_total_h))
    
    draw.rectangle([col_left_w, y_curr, WIDTH - 1, y_curr + 28], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    h_hdr_bbox = draw.textbbox((0, 0), "INDICACIONES DE PELIGRO (FRASES H)", font=font_body_bold)
    h_hdr_w = h_hdr_bbox[2] - h_hdr_bbox[0]
    draw.text((col_left_w + (col_right_w - h_hdr_w) // 2, y_curr + 5), "INDICACIONES DE PELIGRO (FRASES H)", fill="black", font=font_body_bold)
    
    hy = y_curr + 36
    for line in h_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_body)
        lw = line_bbox[2] - line_bbox[0]
        lx = max(col_left_w + PADDING_INNER, col_left_w + (col_right_w - lw) // 2)
        draw.text((lx, hy), line, fill="black", font=font_body)
        hy += font_body.size + 4
        
    p_start_y = y_curr + h_block_height
    draw.line([(col_left_w, p_start_y), (WIDTH, p_start_y)], fill="black", width=LINE_THICKNESS)
    
    draw.rectangle([col_left_w, p_start_y, WIDTH - 1, p_start_y + 28], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    p_hdr_bbox = draw.textbbox((0, 0), "CONSEJOS DE PRUDENCIA (FRASES P)", font=font_body_bold)
    p_hdr_w = p_hdr_bbox[2] - p_hdr_bbox[0]
    draw.text((col_left_w + (col_right_w - p_hdr_w) // 2, p_start_y + 5), "CONSEJOS DE PRUDENCIA (FRASES P)", fill="black", font=font_body_bold)
    
    py = p_start_y + 36
    for line in p_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_body)
        lw = line_bbox[2] - line_bbox[0]
        lx = max(col_left_w + PADDING_INNER, col_left_w + (col_right_w - lw) // 2)
        draw.text((lx, py), line, fill="black", font=font_body)
        py += font_body.size + 4
        
    y_curr += middle_section_h
    
    # FILA 5
    draw.line([(w_col1, y_curr), (w_col1, y_curr + row5_h)], fill="black", width=LINE_THICKNESS)
    draw.line([(w_col1 + w_col2, y_curr), (w_col1 + w_col2, y_curr + row5_h)], fill="black", width=LINE_THICKNESS)
    
    font_hdr_un = load_font(10.5 * scale, is_bold=True)
    font_hdr_epp = load_font(11 * scale, is_bold=True)
    font_hdr_prov = load_font(11 * scale, is_bold=True)
    
    # 1. COLUMNA UN
    draw.rectangle([0, y_curr, w_col1, y_curr + 26], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    un_hdr_bbox = draw.textbbox((0, 0), "PICTOGRAMAS NACIONES UNIDAS", font=font_hdr_un)
    un_hdr_w = un_hdr_bbox[2] - un_hdr_bbox[0]
    un_hdr_x = (w_col1 - un_hdr_w) // 2
    draw.text((un_hdr_x, y_curr + 5), "PICTOGRAMAS NACIONES UNIDAS", fill="black", font=font_hdr_un)
    
    if un_file:
        un_path = os.path.join(UN_DIR, un_file)
        if os.path.exists(un_path):
            try:
                un_img = Image.open(un_path).convert("RGBA")
                un_img.thumbnail((70, 70), Image.Resampling.LANCZOS)
                img.paste(un_img, (w_col1 // 2 - un_img.width // 2, y_curr + 30), un_img)
            except Exception:
                pass
                
    # Dibujar la identificación UN ajustada dentro del recuadro
    un_id_y = y_curr + row5_h - un_id_h - 10
    for uline in un_id_lines:
        ubbox = draw.textbbox((0, 0), uline, font=font_body_bold)
        uw = ubbox[2] - ubbox[0]
        ux = (w_col1 - uw) // 2
        draw.text((ux, un_id_y), uline, fill="black", font=font_body_bold)
        un_id_y += font_body_bold.size + 4
    
    # 2. COLUMNA EPP
    draw.rectangle([w_col1, y_curr, w_col1 + w_col2, y_curr + 26], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    epp_hdr_bbox = draw.textbbox((0, 0), "EPP (ELEMENTOS PROTECCIÓN PERSONAL A USAR)", font=font_hdr_epp)
    epp_hdr_w = epp_hdr_bbox[2] - epp_hdr_bbox[0]
    epp_hdr_x = w_col1 + (w_col2 - epp_hdr_w) // 2
    draw.text((epp_hdr_x, y_curr + 5), "EPP (ELEMENTOS PROTECCIÓN PERSONAL A USAR)", fill="black", font=font_hdr_epp)
    
    if epp_list:
        epp_box_x_start = w_col1
        epp_box_y_start = y_curr + 32
        
        for idx, epp_file in enumerate(epp_list):
            r = idx // cols_epp
            c = idx % cols_epp
            
            items_in_this_row = len(epp_list) - r * cols_epp if (r == (len(epp_list) - 1) // cols_epp and len(epp_list) % cols_epp != 0) else cols_epp
            row_w = items_in_this_row * epp_icon_size + (items_in_this_row - 1) * epp_gap_x
            row_start_x = epp_box_x_start + (w_col2 - row_w) // 2
            
            ex = row_start_x + c * (epp_icon_size + epp_gap_x)
            ey = epp_box_y_start + r * (epp_icon_size + epp_gap_y)
            
            epp_path = os.path.join(EPP_DIR, epp_file)
            if os.path.exists(epp_path):
                try:
                    e_img = Image.open(epp_path).convert("RGBA")
                    circle_bg = Image.new("RGBA", (epp_icon_size, epp_icon_size), (0, 0, 0, 0))
                    c_draw = ImageDraw.Draw(circle_bg)
                    c_draw.ellipse([0, 0, epp_icon_size - 1, epp_icon_size - 1], fill="#0055A5")
                    
                    e_img.thumbnail((epp_icon_size - 10, epp_icon_size - 10), Image.Resampling.LANCZOS)
                    circle_bg.paste(e_img, ((epp_icon_size - e_img.width) // 2, (epp_icon_size - e_img.height) // 2), e_img)
                    
                    img.paste(circle_bg, (int(ex), int(ey)), circle_bg)
                except Exception:
                    pass

    # 3. COLUMNA PROVEEDOR
    draw.rectangle([w_col1 + w_col2, y_curr, WIDTH - 1, y_curr + 26], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    prov_hdr_bbox = draw.textbbox((0, 0), "INFORMACIÓN DEL PROVEEDOR", font=font_hdr_prov)
    prov_hdr_w = prov_hdr_bbox[2] - prov_hdr_bbox[0]
    prov_hdr_x = w_col1 + w_col2 + (w_col3 - prov_hdr_w) // 2
    draw.text((prov_hdr_x, y_curr + 5), "INFORMACIÓN DEL PROVEEDOR", fill="black", font=font_hdr_prov)
    
    p_y = y_curr + 35
    for line in provider_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_provider)
        lw = line_bbox[2] - line_bbox[0]
        lx = max(w_col1 + w_col2 + 10, w_col1 + w_col2 + (w_col3 - lw) // 2)
        draw.text((lx, p_y), line, fill="#111827", font=font_provider)
        p_y += font_provider.size + 4

    return img

# ==============================================================================
# INTERFAZ STREAMLIT
# ==============================================================================

if mode == "Etiqueta Individual":
    st.title("🏷️ Generador de Etiquetas SGA - Colmena Seguros")
    st.markdown("Genera automáticamente etiquetas de seguridad química en alta resolución basadas en la norma NTC 4435 / SGA Colmena.")
    
    generated_label_img = generate_chemical_label_custom(
        product_name, composition_text, signal_word, selected_sga,
        h_phrases_text, p_phrases_text, selected_un_file, un_code, selected_epp, provider_text,
        scale=font_scale
    )
    
    buf = BytesIO()
    generated_label_img.save(buf, format="PNG")
    png_bytes = buf.getvalue()
    
    st.image(generated_label_img, use_container_width=True, caption="Vista Previa de Etiqueta Generada Dinámicamente")
    
    st.divider()
    clean_filename = f"Etiqueta_SGA_Colmena_{(product_name or 'producto').replace(' ', '_')}.png"
    st.download_button(
        label="📥 Descargar Etiqueta en formato PNG",
        data=png_bytes,
        file_name=clean_filename,
        mime="image/png",
        type="primary",
        use_container_width=True
    )

else:
    st.title("📊 Generación por Lote / Base de Datos (CSV / Semicolon)")
    st.markdown("Carga tu archivo de base de datos (delimitado por `;`, `,` o tabulaciones) para procesar múltiples sustancias y generar todas sus etiquetas en formato PNG o en un único paquete ZIP.")

    sample_db_49 = (
        "Nombre;Composicion;Palabra_Advertencia;Pictogramas_SGA;Frases_H;Frases_P;Clase_UN;Codigo_UN;Pictogramas_EPP;Proveedor\n"
        "3,4-DIHIDROXIFENIL-L-FENILALANINA;59-92-7 Levodopa <= 100 %;Atencion;GHS07;H302: Nocivo en caso de ingestión. H315: Provoca irritación cutánea. H319: Provoca irritación ocular grave. H335: Puede irritar las vías respiratorias.;P261: Evitar respirar el polvo. P264: Lavarse la piel concienzudamente. P280: Llevar guantes de protección.;N/A;N/A;gafas, guantes, prenda, mascarilla;Sigma-Aldrich Inc. 3050 SPRUCE ST ST. LOUIS MO 63103\n"
        "ACEITE DE INMERSION;120-51-4 Benzoato de bencilo >= 30 - < 50 %;Atencion;GHS09;H410: Muy tóxico para los organismos acuáticos, con efectos nocivos duraderos.;P273: Evitar su liberación al medio ambiente. P391: Recoger el vertido.;9;UN3082;gafas, guantes, prenda;MERCK S.A. Av.Carrera 9a No. 101-67 Bogotá\n"
        "ACEITE DE PINO;8021-29-2 Fir needle oil <= 100 %;Atencion;GHS02, GHS07;H226: Líquidos y vapores inflamables. H315: Provoca irritación cutánea.;P210: Mantener alejado del calor, chispas, llamas abiertas.;3;UN1993;gafas, guantes, prenda, mascarilla;Sigma-Aldrich Inc. 3050 SPRUCE ST ST. LOUIS MO 63103\n"
        "ÁCIDO 2-TIOBARBITÚRICO;5217-47-0 1,3-Diethyldihydro-2-thioxopyrimidine-4,6(1H,5H)-dione <= 100 %;Peligro;GHS06, GHS08;H301: Tóxico en caso de ingestión. H317: Puede provocar una reacción alérgica en la piel.;P280: Llevar guantes de protección. P301 + P310: Llamar a toxicología.;6.1;UN2811;gafas, guantes, prenda, mascarilla;Sigma-Aldrich Inc. 3050 SPRUCE ST ST. LOUIS MO 63103\n"
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        st.download_button(
            label="📥 Descargar Plantilla / Modelo de Base de Datos (;)",
            data=sample_db_49,
            file_name="Modelo_Base_Datos_Sustancias.csv",
            mime="text/csv",
            use_container_width=True
        )

    uploaded_file = st.file_uploader("Adjunta tu archivo CSV o TXT con la base de datos de reactivos", type=["csv", "txt"])

    if uploaded_file is not None:
        try:
            raw_bytes = uploaded_file.getvalue()
            try:
                content = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                content = raw_bytes.decode("latin-1")

            parsed_items = parse_chemical_db(content, sga_files, epp_files, un_files)

            if not parsed_items:
                st.error("No se pudieron extraer reactivos válidos del archivo. Verifica que las columnas contengan datos y no estén vacías.")
            else:
                st.success(f"✅ ¡Base de datos cargada con éxito! Se procesaron {len(parsed_items)} sustancias/reactivos.")

                df_summary = [
                    {
                        "Substancia / Nombre": item["product_name"],
                        "Palabra Advertencia": item["signal_word"],
                        "SGA Encontrados": ", ".join(item["sga_list"]) if item["sga_list"] else "Ninguno",
                        "Clase UN": item["un_file"].replace(".png", "") if item["un_file"] else "N/A",
                        "Código UN": item["un_code"],
                        "EPP Recomendados": ", ".join([e.replace(".png", "") for e in item["epp_list"]]) if item["epp_list"] else "Ninguno",
                        "Proveedor": item["provider"]
                    }
                    for item in parsed_items
                ]
                
                with st.expander("📋 Ver Tabla Completa de Sustancias Detectadas", expanded=True):
                    st.dataframe(df_summary, use_container_width=True)

                st.divider()
                st.subheader("👁️ Vista Previa Individual e Inspección de Etiquetas")
                
                selected_idx = st.selectbox(
                    "Selecciona una sustancia de la base de datos para previsualizar su etiqueta:",
                    options=list(range(len(parsed_items))),
                    format_func=lambda i: f"{i+1}. {parsed_items[i]['product_name']} ({parsed_items[i]['signal_word']})"
                )

                if selected_idx is not None:
                    item_preview = parsed_items[selected_idx]
                    prev_img = generate_chemical_label_custom(
                        item_preview["product_name"],
                        item_preview["composition"],
                        item_preview["signal_word"],
                        item_preview["sga_list"],
                        item_preview["h_phrases"],
                        item_preview["p_phrases"],
                        item_preview["un_file"],
                        item_preview["un_code"],
                        item_preview["epp_list"],
                        item_preview["provider"],
                        scale=font_scale
                    )
                    
                    st.image(prev_img, caption=f"Etiqueta Generada para: {item_preview['product_name']}", use_container_width=True)

                    buf_single = BytesIO()
                    prev_img.save(buf_single, format="PNG")
                    st.download_button(
                        label=f"📥 Descargar solo la etiqueta de {item_preview['product_name']} (PNG)",
                        data=buf_single.getvalue(),
                        file_name=f"Etiqueta_{item_preview['product_name'].replace(' ', '_')}.png",
                        mime="image/png"
                    )

                st.divider()
                st.subheader("📦 Descargar Todas las Etiquetas en un Archivo ZIP")
                
                if st.button("🚀 Generar y Empaquetar Todas las Etiquetas en ZIP", type="primary", use_container_width=True):
                    with st.spinner(f"Generando {len(parsed_items)} etiquetas en alta resolución..."):
                        zip_buf = BytesIO()
                        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zip_file:
                            for idx, item in enumerate(parsed_items):
                                img = generate_chemical_label_custom(
                                    item["product_name"],
                                    item["composition"],
                                    item["signal_word"],
                                    item["sga_list"],
                                    item["h_phrases"],
                                    item["p_phrases"],
                                    item["un_file"],
                                    item["un_code"],
                                    item["epp_list"],
                                    item["provider"],
                                    scale=font_scale
                                )
                                
                                img_byte_arr = BytesIO()
                                img.save(img_byte_arr, format="PNG")
                                safe_name = "".join(c if c.isalnum() else "_" for c in item["product_name"])
                                zip_file.writestr(f"{idx+1:02d}_Etiqueta_{safe_name}.png", img_byte_arr.getvalue())

                        st.success("🎉 ¡Todas las etiquetas han sido generadas y empaquetadas exitosamente!")
                        st.download_button(
                            label=f"📦 DESCARGAR PAQUETE ZIP ({len(parsed_items)} ETIQUETAS PNG)",
                            data=zip_buf.getvalue(),
                            file_name="Etiquetas_SGA_Colmena_Lote_Completo.zip",
                            mime="application/zip",
                            use_container_width=True,
                            type="primary"
                        )
        except Exception as e:
            st.error(f"Error al procesar la base de datos: {str(e)}")
