
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="DTR Image Generator", layout="centered")
st.title("🔐 DTR Image Generator")

# Load template
try:
    template = Image.open("template.png")
except Exception as e:
    st.error("❌ Template image not found. Make sure 'template.png' is in the same directory.")
    st.stop()

# Font setup with fallback
def load_font(size):
    try:
        return ImageFont.truetype("RobotoMono-Bold.ttf", size)
    except OSError:
        st.warning("⚠️ Font file not found. Using default font instead.")
        return ImageFont.load_default()

base_font_size = 60
percent_font_size = base_font_size * 2

# Form input
with st.form("input_form"):
    col1, col2 = st.columns(2)
    entry_price = col1.text_input("Entry Price", "0.00")
    mark_price = col2.text_input("Mark Price", "0.00")
    ath = col1.text_input("ATH", "0.00")
    submitted = st.form_submit_button("Generate Image")

# Auto-calculate percent change
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

# Text positions
img_height = template.height
percent_y = int(img_height * 0.80)  # 20% from bottom

positions = {
    "Entry Price": (750, 450),
    "Mark Price": (750, 650),
    "ATH": (750, 850),
    "%": (150, percent_y)  # dynamic bottom placement
}

max_width = 1000

# Draw text function
def draw_text(draw, position, text, max_width, font_size):
    font = load_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    while text_width > max_width and font_size > 10:
        font_size -= 2
        font = load_font(font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]

    draw.text(position, text, font=font, fill="white")

# Generate image
if submitted:
    img = template.copy()
    draw = ImageDraw.Draw(img)

    draw_text(draw, positions["Entry Price"], str(entry_price), max_width, base_font_size)
    draw_text(draw, positions["Mark Price"], str(mark_price), max_width, base_font_size)
    draw_text(draw, positions["ATH"], str(ath), max_width, base_font_size)
    draw_text(draw, positions["%"], str(percent_change), max_width, percent_font_size)

    st.image(img, caption="Generated Image", use_container_width=True)

    output_path = "output.png"
    img.save(output_path)
    with open(output_path, "rb") as file:
        st.download_button(
            label="📥 Download Image",
            data=file,
            file_name="DTR_image.png",
            mime="image/png"
        )
