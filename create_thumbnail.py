import PIL
from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageOps

number = 15
currentdir = "projects/python/mels_auto_editor/"


# Thumbnail


left = True if number % 2 == 0 else False


canvas = Image.new('RGBA', (1920, 1080), color = (0, 0, 0, 0))

playerCanvas = Image.new('RGBA', (1920, 1080), color = (0, 0, 0, 0))

background = Image.open(currentdir + "sources/{}/assets/background.png".format(number))
figure = Image.open(currentdir + "sources/{}/assets/figure.png".format(number))

if not left:
    figure = ImageOps.mirror(figure)

figureWhite = Image.composite(Image.new('RGBA', figure.size, color = (255, 255, 255, 255)), Image.new('RGBA', (1920, 1080), color = (0, 0, 0, 0)), figure)

figureWhiteBlurred = figureWhite.filter(ImageFilter.GaussianBlur(radius = 10))

canvas.paste(background.resize((1920, 1080)).filter(ImageFilter.GaussianBlur(radius = 5)))
playerCanvas.paste(figureWhiteBlurred.resize((3000,1500)),(-100 if left else 1050 ,20),figureWhiteBlurred.resize((3000,1500)))
playerCanvas.paste(figure.resize((840,1104)),(30 if left else 1000 ,20),figure.resize((840,1104)))



fnt = ImageFont.truetype('/Users/george\ 1/Library/Fonts/Bubblegum.ttf', (963 if len(str(number)) == 1 else (621 if len(str(number)) == 2 else (464 if len(str(number)) == 3 else (368 if len(str(number)) == 4 else 306 )))))
d = ImageDraw.Draw(canvas)
d.text((775 if left else 100 ,375), "#{}".format(number), fill=(0,0,0), font=fnt)

fnt = ImageFont.truetype('/Users/george\ 1/Library/Fonts/Bubblegum.ttf', 184)
d = ImageDraw.Draw(canvas)
d.text((775 if left else 100 ,225), "IMakeSkins", fill=(0,0,0), font=fnt)




fnt = ImageFont.truetype('/Users/george\ 1/Library/Fonts/Bubblegum.ttf', (963 if len(str(number)) == 1 else (621 if len(str(number)) == 2 else (464 if len(str(number)) == 3 else (368 if len(str(number)) == 4 else 306 )))))
d = ImageDraw.Draw(canvas)
d.text((800 if left else 125 ,400), "#{}".format(number), fill=(255,255,255), font=fnt)

fnt = ImageFont.truetype('/Users/george\ 1/Library/Fonts/Bubblegum.ttf', 184)
d = ImageDraw.Draw(canvas)
d.text((800 if left else 125 ,250), "IMakeSkins", fill=(255,255,255), font=fnt)


canvas.paste(playerCanvas,(0,0),playerCanvas)
canvas.save("outputs/thumbnail.png")