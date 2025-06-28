import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="DTR Image Generator", layout="centered")
st.title("🔐 DTR Image Generator")

# Load template
try:
    template = Image.open("template.png")
except Exception:
    st.error("❌ Template image not found. Make sure 'template.png' is in the same directory.")
    st.stop()

# Load main font (Roboto Mono Bold)
def load_font(size):
    try:
        return ImageFont.truetype("RobotoMono-Bold.ttf", size)
    except OSError:
        st.warning("⚠️ Roboto Mono font not found. Using default font instead.")
        return ImageFont.load_default()

# Load Manrope ExtraBold for Token Symbol
def load_token_font(size):
    try:
        return ImageFont.truetype("Manrope-ExtraBold.ttf", size)
    except OSError:
        st.warning("⚠️ Manrope ExtraBold font not found. Using default font instead.")
        return ImageFont.load_default()

# Font sizes
base_font_size = 60
percent_font_size = base_font_size * 2
token_symbol_font_size = int(base_font_size * 2)

# User input
with st.form("input_form"):
    col1, col2 = st.columns(2)
    entry_price = col1.text_input("Entry Price", "0.00")
    mark_price = col2.text_input("Mark Price", "0.00")
    ath = col1.text_input("ATH", "0.00")
    token_symbol = col2.text_input("Token Symbol", "")
    submitted = st.form_submit_button("Generate Image")

# Calculate percentage change
try:
    entry = float(entry_price)
    mark = float(mark_price)
    if entry != 0:
        percent_change_value = ((mark - entry) / entry) * 100
        percent_change = f"{percent_change_value:+.2f}%"
    else:
        percent_change = "+0.00%"
except:
    percent_change = "+0.00%"

# Positioning
img_height = template.height
percent_y = int(img_height * 0.75)  # 25% from bottom

positions = {
    "Entry Price": (450, 505),
    "Mark Price": (450, 685),
    "ATH": (225, 870),
    "%": (180, percent_y),
    "Token Symbol": (725, 935)  # Adjust as needed
}

max_width = 1000

# Draw text function for main font (Roboto Mono)
def draw_text(draw, position, text, max_width, font_size, color="white"):
    font = load_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    while text_width > max_width and font_size > 10:
        font_size -= 2
        font = load_font(font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]

    draw.text(position, text, font=font, fill=color)

# Generate image
if submitted:
    img = template.copy()
    draw = ImageDraw.Draw(img)

    # Draw token symbol in Manrope ExtraBold
    token_font = load_token_font(token_symbol_font_size)
    bbox = draw.textbbox((0, 0), token_symbol, font=token_font)
    draw.text(positions["Token Symbol"], token_symbol, font=token_font, fill="white")

    # Draw data with dollar signs
    draw_text(draw, positions["Entry Price"], f"${entry_price}", max_width, base_font_size, color="white")
    draw_text(draw, positions["Mark Price"], f"${mark_price}", max_width, base_font_size, color="white")
    draw_text(draw, positions["ATH"], f"${ath}", max_width, base_font_size, color="white")

    # Draw percentage in your signature green/blue
    draw_text(draw, positions["%"], percent_change, max_width, percent_font_size, color="#12ee0e")

    # Show image
    st.image(img, caption="Generated Image", use_container_width=True)

    # Download button
    output_path = "output.png"
    img.save(output_path)
    with open(output_path, "rb") as file:
        st.download_button(
            label="📥 Download Image",
            data=file,
            file_name="DTR_image.png",
            mime="image/png"
        )
