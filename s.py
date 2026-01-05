from PIL import Image, ImageDraw, ImageFont

FONT_FILE = r"C:\Windows\Fonts\Mangal.ttf"  # exact path to Marathi font
img = Image.new("RGB", (800, 400), "black")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FONT_FILE, 50)
draw.text((50, 150), "चला निरोप आलाय स्वामीनंचा", font=font, fill="white")
img.show()
