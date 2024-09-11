import moviepy.editor as mpy 
from PIL import Image, ImageDraw, ImageFont

number = int(input("number:  "))

textImage = Image.new('RGBA', (610, 1080), color = (0, 0, 0, 0))
 
fnt = ImageFont.truetype('/Users/george\ 1/Library/Fonts/Bubblegum.ttf', 105)
d = ImageDraw.Draw(textImage)
d.text((5,250), "IMakeSkins", fill=(255,255,255), font=fnt)

fnt = ImageFont.truetype('/Users/george\ 1/Library/Fonts/Bubblegum.ttf', (550 if len(str(number)) == 1 else (355 if len(str(number)) == 2 else (265 if len(str(number)) == 3 else (210 if len(str(number)) == 4 else 175 )))))
d = ImageDraw.Draw(textImage)
d.text((0,400), "#{}".format(number), fill=(255,255,255), font=fnt)


textImage.save('textImage.png')
print("Done")