# import AksharaJaana as aj
from AksharaJaana.main import OCREngine
from AksharaJaana.utils import ModelTypes, FileOperationUtils

ocr = OCREngine(modelType=ModelTypes.Tesseract)
# choices are Paddleocr, Easyocr, Tesseract

text = ocr.get_text_from_file("Your file Path") 
print(text) 