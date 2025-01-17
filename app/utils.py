from .constants import MODEL_PATH
from rapidocr_onnxruntime import RapidOCR
from numpy.typing import NDArray
from os import PathLike
from shapely import Polygon
from shapely.geometry import box, MultiPolygon
from shapely.ops import unary_union
from typing import cast

_rapid_ocr = RapidOCR(rec_model_path=MODEL_PATH)


def ocr(image: NDArray | PathLike, esp: float = 0.5) -> list[tuple[Polygon, str]]:
    result, _ = _rapid_ocr(image)
    result.sort(key=lambda x: x[0][0][1])
    texts: list[str] = []
    shapes: list[Polygon] = []
    for points, text, _ in result:
        x, y, xmax, ymax = Polygon(points).bounds
        ymax += (ymax - y) * esp
        shapes.append(box(x, y, xmax, ymax))
        texts.append(text)
    merged_shapes = cast(MultiPolygon, unary_union(shapes)).geoms
    merged_texts = [""] * len(merged_shapes)
    visited = [False] * len(texts)
    for i, shape in enumerate(merged_shapes):
        for j, text in enumerate(texts):
            if not visited[j]:
                if shapes[j].intersects(shape):
                    merged_texts[i] += f" {text}"
                    visited[j] = True
    return list(zip(merged_shapes, merged_texts))
