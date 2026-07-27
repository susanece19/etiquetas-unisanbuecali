import os
import textwrap
import math
import csv
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
        options=["Atención", "Peligro","Ninguna"],
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
    """Ajusta líneas de texto al ancho máximo exactamente con Pillow para evitar desbordamientos."""
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
        
        words = raw_line.split(' ')
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_w = bbox[2] - bbox[0]
            
            if line_w <= max_width or not current_line:
                current_line.append(word)
            else:
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
    font_prod_name    = load_font(42 * scale, is_bold=True)  # Nombre del Producto (ej: VARSOL)
    font_signal       = load_font(30 * scale, is_bold=True)  # Palabra "ATENCIÓN" o "PELIGRO"
    font_body         = load_font(19 * scale, is_bold=False) # Frases H y Frases P
    font_body_bold    = load_font(17 * scale, is_bold=True)  # Encabezados de sección
    font_small        = load_font(15 * scale, is_bold=False) # Texto de Composición
    font_provider     = load_font(15 * scale, is_bold=False) # Datos del Proveedor
    
    col_left_w = 290
    col_right_w = WIDTH - col_left_w

    # Ancho máximo seguro para que el texto nunca toque las líneas verticales
    comp_max_w = col_left_w - (PADDING_INNER * 2)
    right_col_max_w = col_right_w - (PADDING_INNER * 2)
    mid_col_w = WIDTH - 2 * col_left_w  # Ancho de la celda central del Nombre del Producto
    
    comp_lines, comp_h, _ = wrap_and_measure_text(draw, c_text, font_small, comp_max_w)
    prod_lines, prod_h, _ = wrap_and_measure_text(draw, p_name.upper(), font_prod_name, mid_col_w - (PADDING_INNER * 2))
    
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
    p_adv_bbox = draw.textbbox((0, 0), "PALABRA DE ADVERTENCIA", font=font_body_bold)
    p_adv_h = p_adv_bbox[3] - p_adv_bbox[1]
    draw.text((PADDING_INNER, y_curr + (row2_h - p_adv_h) // 2), "PALABRA DE ADVERTENCIA", fill="black", font=font_body_bold)
    
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
    st.title("📊 Generación por Lote / Tabla (CSV)")
    st.markdown("Adjunta un archivo CSV para generar las etiquetas de múltiples reactivos a la vez en un solo paquete ZIP.")

    sample_csv_data = (
        "Nombre,Composicion,Palabra Advertencia,Pictogramas SGA,Frases H,Frases P,Clase UN,Codigo UN,Pictogramas EPP,Proveedor\n"
        "VARSOL,\"Mezcla de hidrocarburos C9-C12, 79%\",Atención,\"GHS02.png, GHS07.png\",\"H226 Líquidos inflamables\nH302 Nocivo\",\"P102 Mantener fuera del alcance\nP210 Alejado del calor\",CLASE_3.png,1268,\"BOTAS.png, GAFAS.png, GUANTES.png, MASCARILLA.png\",\"CONSTELACIÓN INDUSTRIAL S.A.S\"\n"
        "ACETONA PURA,\"Propan-2-ona >99.5%\",Peligro,\"GHS02.png, GHS07.png\",\"H225 Líquido muy inflamable\nH319 Irritación ocular\",\"P210 Alejado de chispas\nP233 Recipiente cerrado\",CLASE_3.png,1090,\"GAFAS.png, GUANTES.png, MASCARILLA GAS.png\",\"QUÍMICOS BOGOTÁ S.A.S\"\n"
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        st.download_button(
            label="📥 Descargar Plantilla CSV de Ejemplo",
            data=sample_csv_data,
            file_name="Plantilla_Reactivos_SGA.csv",
            mime="text/csv",
            use_container_width=True
        )

    uploaded_file = st.file_uploader("Adjunta tu archivo CSV con la tabla de reactivos", type=["csv", "txt"])

    if uploaded_file is not None:
        try:
            content = uploaded_file.getvalue().decode("utf-8")
            reader = csv.DictReader(StringIO(content))
            rows = list(reader)

            st.success(f"Se cargaron exitosamente {len(rows)} reactivos del archivo CSV.")
            
            if st.button("🚀 Generar Todas las Etiquetas y Descargar ZIP", type="primary", use_container_width=True):
                zip_buf = BytesIO()
                with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for idx, r in enumerate(rows):
                        p_name = r.get("Nombre", f"REACTIVO_{idx+1}")
                        c_text = r.get("Composicion", "Sin composición")
                        s_word = "Peligro" if "peligro" in r.get("Palabra Advertencia", "").lower() else "Atención"
                        
                        sga_raw = r.get("Pictogramas SGA", "GHS02.png")
                        sga_list = [s.strip() for s in sga_raw.split(",") if s.strip() in sga_files]
                        if not sga_list:
                            sga_list = [sga_files[0]] if sga_files else []

                        h_text = r.get("Frases H", "")
                        p_text = r.get("Frases P", "")
                        
                        un_raw = r.get("Clase UN", "CLASE_3.png").strip()
                        un_file = un_raw if un_raw in un_files else (un_files[0] if un_files else "")
                        un_num = r.get("Codigo UN", "1268")

                        epp_raw = r.get("Pictogramas EPP", "")
                        epp_list = [e.strip() for e in epp_raw.split(",") if e.strip() in epp_files] if epp_raw else epp_files

                        prov_text = r.get("Proveedor", "CONSTELACIÓN INDUSTRIAL S.A.S")

                        img = generate_chemical_label_custom(
                            p_name, c_text, s_word, sga_list, h_text, p_text, un_file, un_num, epp_list, prov_text,
                            scale=1.1
                        )
                        
                        img_byte_arr = BytesIO()
                        img.save(img_byte_arr, format="PNG")
                        clean_item_name = p_name.replace(" ", "_")
                        zip_file.writestr(f"{idx+1}_Etiqueta_{clean_item_name}.png", img_byte_arr.getvalue())

                st.download_button(
                    label="📦 DESCARGAR PAQUETE ZIP (Todas las Etiquetas PNG)",
                    data=zip_buf.getvalue(),
                    file_name="Etiquetas_SGA_Colmena_Lote.zip",
                    mime="application/zip",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error al leer el archivo CSV: {str(e)}")
