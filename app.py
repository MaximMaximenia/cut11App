import streamlit as st
import cv2
import tempfile
import os

st.title("🎬 Обрезка видео до формата 1:1")

uploaded_file = st.file_uploader("Загрузите видео", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
        tmp_input.write(uploaded_file.read())
        tmp_input_path = tmp_input.name

    # Читаем видео
    cap = cv2.VideoCapture(tmp_input_path)
    
    # Получаем информацию о видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    st.write(f"Оригинальное разрешение: {width}x{height}")

    # Определяем координаты для обрезки
    if width > height:
        x_center = width // 2
        crop_width = height
        x1 = x_center - crop_width // 2
        x2 = x1 + crop_width
        y1, y2 = 0, height
    else:
        y_center = height // 2
        crop_height = width
        y1 = y_center - crop_height // 2
        y2 = y1 + crop_height
        x1, x2 = 0, width

    # Проверка значений crop_width и crop_height
    if crop_width <= 0 or crop_height <= 0:
        st.error("Ошибка: Некорректные размеры для обрезки.")
    else:
        st.write(f"Размер обрезанного видео: {crop_width}x{crop_height}")

        # Создаем выходной файл
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        output_path = output_file.name
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # Проверка на корректность размера
        if crop_width <= 0 or crop_height <= 0:
            st.error("Ошибка: некорректный размер выходного видео.")
        else:
            out = cv2.VideoWriter(output_path, fourcc, fps, (crop_width, crop_height))

            # Читаем и обрабатываем каждый кадр
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cropped_frame = frame[y1:y2, x1:x2]
                out.write(cropped_frame)

            cap.release()
            out.release()

            st.write("📼 Обрезка завершена. Сохраняем результат...")

            # Показываем видео
            st.video(output_path)

            # Кнопка для скачивания
            with open(output_path, "rb") as f:
                st.download_button("⬇️ Скачать обрезанное видео", data=f, file_name="cropped_video.mp4")

            os.remove(tmp_input_path)
            os.remove(output_path)
