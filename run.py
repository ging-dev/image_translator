import cv2
import io
import gradio as gr
from app import ocr
from app.constants import FONT_PATH
from numpy.typing import NDArray
from deep_translator import GoogleTranslator
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image
from wand.font import Font
from PIL import Image as PILImage


def handle_image(image: NDArray):
    result = ocr(image)
    ret, encoded_image = cv2.imencode(".png", image)

    if not ret:
        raise Exception("Unknown error.")

    with Image(blob=encoded_image) as img:
        texts: list[str] = []
        rects: list[tuple[int, int, int, int]] = []
        with Drawing() as draw:
            draw.fill_color = Color("white")
            for shape, text in result:
                x, y, xmax, ymax = map(int, shape.bounds)
                w = xmax - x
                h = ymax - y
                draw.rectangle(x, y, xmax, ymax)
                rects.append((x, y, w, h))
                texts.append(text)
            draw.draw(img)
        font = Font(FONT_PATH)
        translator = GoogleTranslator(source="auto", target="vi")
        texts = translator.translate_batch(texts)
        for (x, y, w, h), text in zip(rects, texts):
            img.caption(text, x, y, w, h, font=font, gravity="center")

        return PILImage.open(io.BytesIO(img.make_blob("png")))


with gr.Blocks() as demo:
    with gr.Column():
        image = gr.Image()
        output = gr.Image()
        image.upload(handle_image, inputs=image, outputs=output)

if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0')
