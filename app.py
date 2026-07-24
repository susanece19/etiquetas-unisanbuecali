import os
import textwrap
from io import BytesIO
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
LOGO_PATH = os.path.join(ASSETS_DIR, "logo_colmena.png")
SGA_DIR = os.path.join(ASSETS_DIR, "sga")
EPP_DIR = os.path.join(ASSETS_DIR, "epp")
UN_DIR = os.path.join(ASSETS_DIR, "un")

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
# BARRA LATERAL (SIDEBAR): ENTRADAS DEL USUARIO
# ==============================================================================
st.sidebar.title("🛠️ Configuración de Etiqueta")
st.sidebar.markdown("Basado en la estructura de **Colmena Seguros (Modelo VARSOL)**")

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
    """Carga una fuente Truetype del sistema o fuente por defecto de Pillow."""
    font_names = [
        "DejaVuSans-Bold.ttf" if is_bold else "DejaVuSans.ttf",
        "arialbd.ttf" if is_bold else "arial.ttf",
        "LiberationSans-Bold.ttf" if is_bold else "LiberationSans-Regular.ttf",
    ]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()

def wrap_and_measure_text(draw, text, font, max_width):
    """Ajusta líneas de texto al ancho máximo dado y calcula la altura requerida."""
    lines = []
    for raw_line in text.split('\n'):
        if not raw_line.strip():
            lines.append("")
            continue
        wrapped = textwrap.wrap(raw_line, width=max(15, int(max_width / (font.size * 0.55))))
        lines.extend(wrapped)
    
    total_height = 0
    line_heights = []
    for line in lines:
        if line:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1] + 4
        else:
            h = font.size + 4
        line_heights.append(h)
        total_height += h
        
    return lines, total_height, line_heights

def generate_chemical_label():
    """Genera la imagen PNG de la etiqueta ajustada dinámicamente según el contenido."""
    WIDTH = 1000
    PADDING = 12
    LINE_THICKNESS = 2
    
    # Crear canvas temporal para mediciones
    temp_img = Image.new("RGB", (WIDTH, 2000), "white")
    draw = ImageDraw.Draw(temp_img)
    
    # Fuentes con jerarquía visual proporcional
    font_header_title = load_font(18, is_bold=True)
    font_prod_name = load_font(32, is_bold=True)
    font_signal = load_font(22, is_bold=True)
    font_body = load_font(15, is_bold=False)
    font_body_bold = load_font(15, is_bold=True)
    font_small = load_font(13, is_bold=False)
    font_provider = load_font(14, is_bold=False)
    
    # Anchos de columnas
    col_left_w = 260
    col_right_w = WIDTH - col_left_w  # 740px
    
    # --- CÁLCULO DE ALTURAS DINÁMICAS ---
    # Fila 1: Encabezado (Logo | Nombre | Composición)
    comp_lines, comp_h, _ = wrap_and_measure_text(draw, composition_text, font_small, col_left_w - 20)
    row1_h = max(110, comp_h + 40)
    
    # Fila 2: Palabra de advertencia
    row2_h = 50
    
    # Secciones Frases H y Frases P (Columna Derecha)
    h_lines, h_text_h, _ = wrap_and_measure_text(draw, h_phrases_text, font_body, col_right_w - 40)
    p_lines, p_text_h, _ = wrap_and_measure_text(draw, p_phrases_text, font_body, col_right_w - 40)
    
    h_box_h = max(80, h_text_h + 40)
    p_box_h = max(100, p_text_h + 40)
    right_col_total_h = h_box_h + p_box_h
    
    # Seccion Pictogramas SGA (Columna Izquierda)
    sga_count = len(selected_sga)
    sga_min_h = 180 if sga_count <= 2 else 240 if sga_count <= 4 else 300
    
    # Fila 3 y 4 Unificada (Sección Central)
    middle_section_h = max(sga_min_h, right_col_total_h)
    
    # Fila 5: UN | EPP | Proveedor
    provider_lines, prov_h, _ = wrap_and_measure_text(draw, provider_text, font_provider, 300)
    row5_h = max(140, prov_h + 45)
    
    # Altura Total Dinámica
    TOTAL_HEIGHT = row1_h + row2_h + middle_section_h + row5_h
    
    # Inicialización de la imagen final
    img = Image.new("RGBA", (WIDTH, TOTAL_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # DIBUJAR BORDES EXTERIORES
    draw.rectangle([0, 0, WIDTH - 1, TOTAL_HEIGHT - 1], outline="black", width=LINE_THICKNESS * 2)
    
    # ==========================================================================
    # FILA 1: Encabezado (Logo Colmena | Nombre Producto | Composición)
    # ==========================================================================
    y_curr = 0
    # Línea horizontal inferior Fila 1
    draw.line([(0, y_curr + row1_h), (WIDTH, y_curr + row1_h)], fill="black", width=LINE_THICKNESS)
    # Divisores verticales
    draw.line([(col_left_w, y_curr), (col_left_w, y_curr + row1_h)], fill="black", width=LINE_THICKNESS)
    draw.line([(WIDTH - col_left_w, y_curr), (WIDTH - col_left_w, y_curr + row1_h)], fill="black", width=LINE_THICKNESS)
    
    # Columna 1 (Logo Colmena)
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
        
    # Columna 2 (Nombre del Producto)
    prod_bbox = draw.textbbox((0, 0), product_name.upper(), font=font_prod_name)
    pw = prod_bbox[2] - prod_bbox[0]
    ph = prod_bbox[3] - prod_bbox[1]
    center_x = col_left_w + (col_right_w - col_left_w) // 2 - pw // 2
    center_y = y_curr + (row1_h - ph) // 2
    draw.text((center_x, center_y), product_name.upper(), fill="black", font=font_prod_name)
    
    # Columna 3 (Composición)
    comp_x_start = WIDTH - col_left_w
    draw.rectangle([comp_x_start, y_curr, WIDTH - 1, y_curr + 30], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    draw.text((comp_x_start + 45, y_curr + 6), "COMPOSICIÓN", fill="black", font=font_body_bold)
    
    cy = y_curr + 36
    for line in comp_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_small)
        lw = line_bbox[2] - line_bbox[0]
        lx = comp_x_start + (col_left_w - lw) // 2
        draw.text((lx, cy), line, fill="#1F2937", font=font_small)
        cy += font_small.size + 4
        
    y_curr += row1_h
    
    # ==========================================================================
    # FILA 2: Palabra de Advertencia
    # ==========================================================================
    draw.line([(0, y_curr + row2_h), (WIDTH, y_curr + row2_h)], fill="black", width=LINE_THICKNESS)
    draw.line([(col_left_w, y_curr), (col_left_w, y_curr + row2_h)], fill="black", width=LINE_THICKNESS)
    
    # Título Izquierda
    draw.text((20, y_curr + 14), "Palabra de Advertencia", fill="black", font=font_body_bold)
    
    # Valor Derecha
    sig_color = "#DC2626" if signal_word == "Peligro" else "#D97706"
    sig_bbox = draw.textbbox((0, 0), signal_word.upper(), font=font_signal)
    sw = sig_bbox[2] - sig_bbox[0]
    sx = col_left_w + (col_right_w - sw) // 2
    draw.text((sx, y_curr + 12), signal_word.upper(), fill=sig_color, font=font_signal)
    
    y_curr += row2_h
    
    # ==========================================================================
    # FILA 3 Y 4 UNIFICADA: SGA (Izq) | Frases H y Frases P (Der)
    # ==========================================================================
    # Línea inferior de la sección central
    draw.line([(0, y_curr + middle_section_h), (WIDTH, y_curr + middle_section_h)], fill="black", width=LINE_THICKNESS)
    # Divisor vertical entre columna izquierda (SGA) y columna derecha (Frases H & P)
    draw.line([(col_left_w, y_curr), (col_left_w, y_curr + middle_section_h)], fill="black", width=LINE_THICKNESS)
    
    # --- COLUMNA IZQUIERDA: PICTOGRAMAS SGA ---
    draw.rectangle([0, y_curr, col_left_w, y_curr + 28], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    draw.text((40, y_curr + 5), "PICTOGRAMAS SGA", fill="black", font=font_body_bold)
    
    if selected_sga:
        sx = 15
        sy = y_curr + 38
        icon_size = 65 if len(selected_sga) <= 2 else 55
        for idx, sga_file in enumerate(selected_sga):
            sga_path = os.path.join(SGA_DIR, sga_file)
            if os.path.exists(sga_path):
                try:
                    s_img = Image.open(sga_path).convert("RGBA")
                    s_img = s_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                    img.paste(s_img, (sx, sy), s_img)
                    sx += icon_size + 12
                    if sx + icon_size > col_left_w:
                        sx = 15
                        sy += icon_size + 10
                except Exception:
                    pass

    # --- COLUMNA DERECHA: FRASES H (SUPERIOR) & FRASES P (INFERIOR) ---
    # Calcular división horizontal proporcional en la columna derecha
    h_block_height = int(middle_section_h * (h_box_h / right_col_total_h))
    
    # 1. Bloque Frases H
    draw.rectangle([col_left_w, y_curr, WIDTH - 1, y_curr + 28], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    draw.text((col_left_w + 200, y_curr + 5), "INDICACIONES DE PELIGRO (FRASES H)", fill="black", font=font_body_bold)
    
    hy = y_curr + 36
    for line in h_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_body)
        lw = line_bbox[2] - line_bbox[0]
        lx = col_left_w + (col_right_w - lw) // 2
        draw.text((lx, hy), line, fill="black", font=font_body)
        hy += font_body.size + 4
        
    # Línea divisoria entre Frases H y Frases P
    p_start_y = y_curr + h_block_height
    draw.line([(col_left_w, p_start_y), (WIDTH, p_start_y)], fill="black", width=LINE_THICKNESS)
    
    # 2. Bloque Frases P
    draw.rectangle([col_left_w, p_start_y, WIDTH - 1, p_start_y + 28], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    draw.text((col_left_w + 200, p_start_y + 5), "CONSEJOS DE PRUDENCIA (FRASES P)", fill="black", font=font_body_bold)
    
    py = p_start_y + 36
    for line in p_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_body)
        lw = line_bbox[2] - line_bbox[0]
        lx = col_left_w + (col_right_w - lw) // 2
        draw.text((lx, py), line, fill="black", font=font_body)
        py += font_body.size + 4
        
    y_curr += middle_section_h
    
    # ==========================================================================
    # FILA 5: UN | EPP | PROVEEDOR
    # ==========================================================================
    w_col1 = 250
    w_col2 = 430
    w_col3 = WIDTH - w_col1 - w_col2
    
    draw.line([(w_col1, y_curr), (w_col1, y_curr + row5_h)], fill="black", width=LINE_THICKNESS)
    draw.line([(w_col1 + w_col2, y_curr), (w_col1 + w_col2, y_curr + row5_h)], fill="black", width=LINE_THICKNESS)
    
    # 5.1 UN Transport
    draw.rectangle([0, y_curr, w_col1, y_curr + 26], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    draw.text((15, y_curr + 5), "PICTOGRAMAS NACIONES UNIDAS", fill="black", font=load_font(12, is_bold=True))
    
    if selected_un_file:
        un_path = os.path.join(UN_DIR, selected_un_file)
        if os.path.exists(un_path):
            try:
                un_img = Image.open(un_path).convert("RGBA")
                un_img.thumbnail((70, 70), Image.Resampling.LANCZOS)
                img.paste(un_img, (w_col1 // 2 - un_img.width // 2, y_curr + 32), un_img)
            except Exception:
                pass
    draw.text((20, y_curr + row5_h - 25), f"Identificación UN: {un_code}", fill="black", font=font_body_bold)
    
    # 5.2 EPP
    draw.rectangle([w_col1, y_curr, w_col1 + w_col2, y_curr + 26], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    draw.text((w_col1 + 40, y_curr + 5), "EPP (ELEMENTOS PROTECCIÓN PERSONAL A USAR)", fill="black", font=load_font(12, is_bold=True))
    
    if selected_epp:
        ex = w_col1 + 20
        ey = y_curr + 38
        epp_icon_size = 50
        for epp_file in selected_epp:
            epp_path = os.path.join(EPP_DIR, epp_file)
            if os.path.exists(epp_path):
                try:
                    e_img = Image.open(epp_path).convert("RGBA")
                    # Crear fondo circular azul
                    circle_bg = Image.new("RGBA", (epp_icon_size, epp_icon_size), (0, 0, 0, 0))
                    c_draw = ImageDraw.Draw(circle_bg)
                    c_draw.ellipse([0, 0, epp_icon_size - 1, epp_icon_size - 1], fill="#0055A5")
                    
                    e_img.thumbnail((epp_icon_size - 10, epp_icon_size - 10), Image.Resampling.LANCZOS)
                    circle_bg.paste(e_img, ((epp_icon_size - e_img.width) // 2, (epp_icon_size - e_img.height) // 2), e_img)
                    
                    img.paste(circle_bg, (ex, ey), circle_bg)
                    ex += epp_icon_size + 15
                except Exception:
                    pass

    # 5.3 Proveedor
    draw.rectangle([w_col1 + w_col2, y_curr, WIDTH - 1, y_curr + 26], fill="#F3F4F6", outline="black", width=LINE_THICKNESS)
    draw.text((w_col1 + w_col2 + 40, y_curr + 5), "INFORMACIÓN DEL PROVEEDOR", fill="black", font=load_font(12, is_bold=True))
    
    p_y = y_curr + 35
    for line in provider_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_provider)
        lw = line_bbox[2] - line_bbox[0]
        lx = w_col1 + w_col2 + (w_col3 - lw) // 2
        draw.text((lx, p_y), line, fill="#111827", font=font_provider)
        p_y += font_provider.size + 4

    return img

# ==============================================================================
# VISTA PRINCIPAL Y EXPORTACIÓN DE IMAGEN EN STREAMLIT
# ==============================================================================
st.title("🏷️ Generador de Etiquetas SGA - Colmena Seguros")
st.markdown("Genera automáticamente etiquetas de seguridad química en alta resolución basadas en la norma NTC 4435 / SGA Colmena.")

# Generar etiqueta en memoria
generated_label_img = generate_chemical_label()

# Convertir PIL Image a PNG Bytes
buf = BytesIO()
generated_label_img.save(buf, format="PNG")
png_bytes = buf.getvalue()

# Mostrar Vista Previa
col_center, _ = st.columns([1, 0.01])
with col_center:
    st.image(generated_label_img, use_container_width=True, caption="Vista Previa de Etiqueta Generada Dinámicamente")

st.divider()

# Botón de Descarga
clean_filename = f"Etiqueta_SGA_Colmena_{(product_name or 'producto').replace(' ', '_')}.png"
st.download_button(
    label="📥 Descargar Etiqueta en formato PNG",
    data=png_bytes,
    file_name=clean_filename,
    mime="image/png",
    type="primary",
    use_container_width=True
)
