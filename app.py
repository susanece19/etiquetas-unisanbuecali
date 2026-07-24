import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = "assets"
SGA_DIR = os.path.join(BASE_DIR, "sga")
EPP_DIR = os.path.join(BASE_DIR, "epp")
UN_DIR = os.path.join(BASE_DIR, "un")
LOGO_PATH = os.path.join(BASE_DIR, "logo_colmena.png")

# --- FUNCIONES DE APOYO ---
def get_font(size, bold=False):
    """Carga una fuente. Intenta buscar una negrita si se solicita."""
    try:
        # En Streamlit Cloud (Linux), estas son rutas comunes de fuentes
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def draw_wrapped_text(draw, text, x, y, max_width, font, fill="black"):
    """Dibuja texto con ajuste de línea automático."""
    # Estimar caracteres por línea según el ancho
    avg_char_width = font.getlength('x')
    chars_per_line = int(max_width / avg_char_width)
    lines = textwrap.wrap(text, width=chars_per_line)
    
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill)
        current_y += font.size + 5
    return current_y

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Generador de Etiquetas Pro", layout="wide")
st.title("🛡️ Generador de Etiquetas de Seguridad Química")

with st.sidebar:
    st.header("1. Información del Producto")
    nombre = st.text_input("Nombre del Producto", "VARSOL").upper()
    comp = st.text_area("Composición", "Mezcla compleja de hidrocarburos...")
    palabra = st.selectbox("Palabra de Advertencia", ["ATENCIÓN", "PELIGRO"])
    
    st.header("2. Peligros y Prudencia")
    frases_h = st.text_area("Indicaciones de Peligro (Frases H)", "H226 Líquidos y vapores inflamables...")
    frases_p = st.text_area("Consejos de Prudencia (Frases P)", "P102 Mantener fuera del alcance de los niños...")
    
    st.header("3. Pictogramas")
    sga_sel = st.multiselect("Pictogramas SGA (GHS)", os.listdir(SGA_DIR) if os.path.exists(SGA_DIR) else [])
    un_sel = st.multiselect("Pictogramas UN (Transporte)", os.listdir(UN_DIR) if os.path.exists(UN_DIR) else [])
    un_id = st.text_input("Identificación UN (Número)", "1268")
    
    epp_sel = st.multiselect("EPP Recomendados", os.listdir(EPP_DIR) if os.path.exists(EPP_DIR) else [])
    
    st.header("4. Proveedor")
    prov = st.text_area("Datos del Proveedor", "CONSTELACIÓN INDUSTRIAL S.A.S\nBogotá, Colombia")

# --- GENERACIÓN DE IMAGEN ---
if st.button("GENERAR ETIQUETA PROFESIONAL"):
    # 1. Definir fuentes
    font_product = get_font(80, bold=True)
    font_title = get_font(30, bold=True)
    font_body = get_font(24)
    font_small = get_font(18)

    # 2. Lienzo (Ancho fijo 1500px, alto dinámico)
    # Calculamos una altura base amplia, luego podrías recortarla
    w, h = 1500, 1600
    img = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(img)
    
    # 3. Dibujar Estructura (Líneas gruesas)
    draw.rectangle([20, 20, w-20, h-20], outline="black", width=6)
    
    # --- FILA 1: LOGO | NOMBRE | COMPOSICIÓN ---
    draw.line([(20, 250), (w-20, 250)], fill="black", width=4) # Línea horizontal
    draw.line([(350, 20), (350, 250)], fill="black", width=4)  # Divisor logo
    draw.line([(1050, 20), (1050, 250)], fill="black", width=4) # Divisor comp
    
    # Logo
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo.thumbnail((300, 200))
        img.paste(logo, (40, 40), logo)
    
    # Nombre Producto
    draw.text((380, 80), nombre, font=font_product, fill="black")
    
    # Composición
    draw.text((1065, 35), "Composición:", font=get_font(22, True), fill="black")
    draw_wrapped_text(draw, comp, 1065, 75, 400, font_small)

    # --- FILA 2: PALABRA DE ADVERTENCIA ---
    draw.line([(20, 330), (w-20, 330)], fill="black", width=4)
    draw.line([(450, 250), (450, 330)], fill="black", width=4)
    
    draw.text((40, 270), "Palabra de Advertencia", font=font_title, fill="black")
    color_adv = "red" if "PELIGRO" in palabra else "black"
    draw.text((750, 265), palabra, font=get_font(50, True), fill=color_adv)

    # --- CUERPO CENTRAL: PICTOGRAMAS (IZQ) | FRASES H (DER) ---
    draw.line([(20, 1000), (w-20, 1000)], fill="black", width=4) # Cierre sección media
    draw.line([(450, 330), (450, 1000)], fill="black", width=4) # Divisor vertical
    
    # Títulos Secciones
    draw.text((40, 345), "Pictogramas SGA / UN", font=font_title, fill="black")
    draw.text((470, 345), "Indicaciones de peligro (Frases H)", font=font_title, fill="black")
    
    # Pegar Pictogramas SGA (Grandes)
    y_pics = 420
    x_pics = 50
    for i, p in enumerate(sga_sel):
        p_img = Image.open(os.path.join(SGA_DIR, p)).convert("RGBA")
        p_img = p_img.resize((220, 220)) # Tamaño aumentado
        img.paste(p_img, (x_pics, y_pics), p_img)
        x_pics += 190
        if x_pics > 300: # Salto de línea si hay más de 2
            x_pics = 50
            y_pics += 200

    # Pegar Pictogramas UN (Abajo de los SGA)
    y_un = y_pics + 220
    draw.text((40, y_un), "Transporte UN:", font=get_font(24, True), fill="black")
    y_un += 40
    x_un = 60
    for p in un_sel:
        p_img = Image.open(os.path.join(UN_DIR, p)).convert("RGBA")
        p_img = p_img.resize((160, 160))
        img.paste(p_img, (x_un, y_un), p_img)
        x_un += 180
    
    draw.text((60, y_un + 180), f"ID UN: {un_id}", font=font_title, fill="black")

    # Frases H (Derecha)
    draw_wrapped_text(draw, frases_h, 470, 420, 1000, font_body)

    # --- SECCIÓN FRASES P (ANCHO TOTAL) ---
    draw.line([(20, 1300), (w-20, 1300)], fill="black", width=4)
    draw.text((40, 1020), "Consejos de prudencia (Frases P)", font=font_title, fill="black")
    draw_wrapped_text(draw, frases_p, 40, 1080, 1400, font_body)

    # --- FILA FINAL: EPP | PROVEEDOR ---
    draw.line([(850, 1300), (850, 1580)], fill="black", width=4)
    draw.text((40, 1320), "EPP (Protección Personal a usar):", font=font_title, fill="black")
    
    x_epp = 40
    for p in epp_sel:
        p_img = Image.open(os.path.join(EPP_DIR, p)).convert("RGBA")
        p_img = p_img.resize((120, 120))
        img.paste(p_img, (x_epp, 1380), p_img)
        x_epp += 140
        
    draw.text((870, 1320), "Información del Proveedor:", font=font_title, fill="black")
    draw_wrapped_text(draw, prov, 870, 1380, 600, font_body)

    # Mostrar y Descargar
    st.image(img, caption="Previsualización de Etiqueta")
    
    img.save("etiqueta_pro.png")
    with open("etiqueta_pro.png", "rb") as f:
        st.download_button("Descargar Etiqueta en Alta Resolución", f, "etiqueta.png", "image/png")
