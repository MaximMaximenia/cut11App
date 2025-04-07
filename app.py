import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os

st.title("🎬 Обрезка видео до формата 1:1")

uploaded_file = st.file_uploader("Загрузите видео", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
        tmp_input.write(uploaded_file.read())
        tmp_input_path = tmp_input.name

    clip = VideoFileClip(tmp_input_path)

    width, height = clip.size
    st.write(f"Оригинальное разрешение: {width}x{height}")

    if width > height:
        x_center = width // 2
        crop_width = height
        x1 = x_center - crop_width // 2
        x2 = x1 + crop_width
        cropped = clip.crop(x1=x1, y1=0, x2=x2, y2=height)
    else:
        y_center = height // 2
        crop_height = width
        y1 = y_center - crop_height // 2
        y2 = y1 + crop_height
        cropped = clip.crop(x1=0, y1=y1, x2=width, y2=y2)

    st.write("📼 Обрезка завершена. Сохраняем результат...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_output:
        cropped.write_videofile(tmp_output.name, codec="libx264", audio_codec="aac")
        st.video(tmp_output.name)
        with open(tmp_output.name, "rb") as f:
            st.download_button("⬇️ Скачать обрезанное видео", data=f, file_name="cropped_video.mp4")

    os.remove(tmp_input_path)
