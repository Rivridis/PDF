from logging import root
import tkinter as tk
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import fitz

Field = ""
Value = ""

def save_file():
    global Field, Value
    Field = entry_field.get()
    Value = entry_value.get()
    root.after(100, root.destroy)

root = tk.Tk()
root.title("PDF Form")
root.geometry("400x250")


label_field = tk.Label(root, text="Field To Fill:")
label_field.pack(pady=5)


entry_field = tk.Entry(root, width=40)
entry_field.pack(pady=5)

label_value = tk.Label(root, text="Value:")
label_value.pack(pady=5)

entry_value = tk.Entry(root, width=40)
entry_value.pack(pady=5)

btn_enter = tk.Button(root, text="Enter", command=save_file)
btn_enter.pack(pady=10)

root.mainloop()

pages = fitz.open("form.pdf")
image = pages[0]

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pix = image.get_pixmap(dpi=300)
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

positions = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
print(positions)

box = None

for i in positions['text']:
    ind = positions['text'].index(i)
    if str(Field).lower() in i.lower():
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
            draw.text((pdf_x, pdf_y), str(Value), fill="black", font=font)



img.save("edited_page.png")
edited_img = Image.open("edited_page.png")
edited_img.convert("RGB").save("filled_form.pdf", "PDF", resolution=300.0)

print(pdf_x, pdf_y)
