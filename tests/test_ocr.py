from app import ocr
from pathlib import Path

def test_detection():
    result = ocr(str(Path(__file__).parent / 'demo.jpg'))
    assert len(result) == 11
