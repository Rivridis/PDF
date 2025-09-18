import pytesseract
from PIL import Image, ImageDraw, ImageFont
import fitz

pages = fitz.open("comp.pdf")
image = pages[0]

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pix = image.get_pixmap(dpi=300)
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

positions = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
print(positions)

box = None

for i in positions['text']:
    ind = positions['text'].index(i)
    if "name" in i.lower() or "company" in i.lower():
        print(i)
        left, top, width, height = (positions['left'][ind],
                                    positions['top'][ind],
                                    positions['width'][ind],
                                    positions['height'][ind])
        print(left, top, width, height)
        box = (left, top, width, height)
        if box:
            pdf_x = box[0] + box[2] + 15
            pdf_y = box[1] - 5

            # write on image
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 40)
            draw.text((pdf_x, pdf_y), "Rivridis", fill="black", font=font)



img.save("edited_page.png")
edited_img = Image.open("edited_page.png")
edited_img.convert("RGB").save("filled_form.pdf", "PDF", resolution=300.0)

print(pdf_x, pdf_y)
