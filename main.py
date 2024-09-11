# You will need to install the moviepy, skimage and PIL libraries (os is built in):
import moviepy.editor as mpy 
from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageOps
import os
import os.path
from skimage.filters import gaussian


## If running in IDE, set currentdir to be the directory to the folder your file is in:
currentdir = "projects/python/mels_auto_editor/"

## Sources:
# To add media to edit, you need a sources folder next to this file. The sources folder should look as follows:
#
#   sources v
#       <clip number> v             < The number of the clip
#           assets v
#               background.png      < The thumbnail background
#               figure.png          < The figure in the thumbnail
#           clips v
#               audio.mp3           < The music for the video
#               clip.mp4            < The video clip (Can be several hours - the program automatically shrinks it into a timelapse)

screenSize = screenW, screenH = 610, 1080 # The video dimensions

LENGTH = 25 # The length of the video in seconds (The videos were origionally a minute, but the creator's community voted that they should be 25s instead)

def renderVideo(videoData,currentdir):
    
    number = videoData[0]
    end_length = videoData[1]
    startPoint = videoData[2]


    print("Creating video {}".format(number))

    print("\nLocating clips...")

    clips = []

    # Walk through the clips folder and convert each file to an mpy video file
    for root, directories, files in os.walk(currentdir + "sources/{}/clips".format(number)):
        for item in files:
            if item.endswith(".mp4"):
                clips.append(mpy.VideoFileClip(os.path.join(root, item)))
                print("Added clip {}".format(item))

    # Turn all clips into a fixed clip
    wholeClip = mpy.concatenate_videoclips(clips)
    print("Done")

    print("\nCreating subclips...")

    print("Total clip length is {} seconds".format(wholeClip.duration))

    # Create a clip of the last 3 seconds of the whole clip
    finishingClip = wholeClip.subclip(t_start=(float(wholeClip.duration) - end_length))
    print("Finishing Clip Length is {}".format(finishingClip.duration))
    print("Created finishing clip")

    # Create a clip without the last 3 seconds and speed it up to just under LENGTH seconds
    mainClip = wholeClip.subclip(0,wholeClip.duration-end_length)
    mainClip = mainClip.fx( mpy.vfx.speedx, (float(mainClip.duration) / (LENGTH - end_length - 0.1)))
    print("Created main clip")

    # Take the first 3 seconds of the mainClip and make it into a blurred clip called beginningClip
    def blur(image):
        return gaussian(image.astype(float), sigma=5)
    beginningClip = mainClip.subclip(0,2).fl_image(blur)
    print("Created beginning clip\nDone")

    print("\nApplying effects...")

    # Adds the fade to black effect for the main clip
    mainClip.fadeout(2)

    # Adds the fade in for the main clip
    mainClip.crossfadein(2.0)

    print("Done")

    # Create Text

    print("\nGenerating Text Image...")
    textImage = Image.new('RGBA', (610, 1080), color = (0, 0, 0, 0))
    
    fnt = ImageFont.truetype('/Users/george\ 1/Library/Fonts/Bubblegum.ttf', 105)
    d = ImageDraw.Draw(textImage)
    d.text((5,250), "IMakeSkins", fill=(255,255,255), font=fnt)

    fnt = ImageFont.truetype('/Users/george\ 1/Library/Fonts/Bubblegum.ttf', (550 if len(str(number)) == 1 else (355 if len(str(number)) == 2 else (265 if len(str(number)) == 3 else (210 if len(str(number)) == 4 else 175 )))))
    d = ImageDraw.Draw(textImage)
    d.text((0,400), "#{}".format(number), fill=(255,255,255), font=fnt)
    textImage.save('textImageTEMP.png')
    print("Done")

    textClip = mpy.ImageClip('textImageTEMP.png').set_duration(2).crossfadeout(1.0)

    os.remove('textImageTEMP.png')

    print("\nCompiling clip...")


    # Build audio
    print("\nTrimming audio...")

    try:
        audioClip = mpy.AudioFileClip(currentdir + "sources/{}/clips/audio.mp3".format(number)).subclip(startPoint, startPoint + LENGTH - 0.1)
    except:
        print("\n\n!!!  Audio start length invalid, please start again\n\n")



    # Render Clip

    finalClip = mpy.CompositeVideoClip([mainClip,beginningClip,textClip.resize((610/1.68,1080/1.68)),finishingClip.set_start(LENGTH - end_length - 0.1)])

    finalClip = finalClip.set_audio(audioClip)

    finishDir = os.path.join(currentdir + "outputs/videos")
    if not os.path.exists(finishDir):
        os.makedirs(finishDir)

    finalClip.resize(width=610,height=1080)

    print("\nVideo Data:\nVideo Length: {}\n".format(finalClip.duration))

    finalClip.write_videofile(finishDir + "/IMakeSkins{}.mp4".format(number))
    print("VIDEO RENDERING COMPLETE")



def renderThumbnail(number,currentdir):
    # Thumbnail

    left = number % 2 == 0

    canvas = Image.new('RGBA', (1920, 1080), color = (0, 0, 0, 0))

    playerCanvas = Image.new('RGBA', (1920, 1080), color = (0, 0, 0, 0))

    background = Image.open(currentdir + "sources/{}/assets/background.png".format(number))
    figure = Image.open(currentdir + "sources/{}/assets/figure.png".format(number))

    if not left:
        figure = ImageOps.mirror(figure)

    figureWhite = Image.composite(Image.new('RGBA', figure.size, color = (255, 255, 255, 255)), Image.new('RGBA', (1920, 1080), color = (0, 0, 0, 0)), figure)

    figureWhiteBlurred = figureWhite.filter(ImageFilter.GaussianBlur(radius = 10))

    canvas.paste(background.resize((1920, 1080)).filter(ImageFilter.GaussianBlur(radius = 5)))
    playerCanvas.paste(figureWhiteBlurred.resize((6000,3000)),(-400 if left else 1000 ,20),figureWhiteBlurred.resize((6000,3000)))
    playerCanvas.paste(figure.resize((1104,1104)),(-234 if left else 1000 ,20),figure.resize((1104,1104)))



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

    finishDir = os.path.join(currentdir + "outputs/thumbnails")
    if not os.path.exists(finishDir):
        os.makedirs(finishDir)

    canvas.save(finishDir + "/IMakeSkins{0}.png".format(number))



# Main Program

print("\n\nWelcome to the Mels Auto Editor!")

selecting = True
while selecting:
    while True:
        rawVideoNumbers = input("\nPlease enter all the VIDEOS you would like to edit (Seperated by commas):  ")
        if rawVideoNumbers != "":
            try:
                rawVideoNumbers = rawVideoNumbers.split(" ")
                videoNumbers = []
                for i in range(len(rawVideoNumbers)):
                    videoNumbers.append(int(rawVideoNumbers[i]))
                break
            except:
                print("Invalid entry")
        else:
            videoNumbers = []
            break



    while True:
        rawThumbnailNumbers = input("\nPlease enter all the THUMBNAILS you would like to create (Seperated by commas):  ")
        if rawThumbnailNumbers != "":
            try:
                rawThumbnailNumbers = rawThumbnailNumbers.split(" ")
                thumbnailNumbers = []
                for i in range(len(rawThumbnailNumbers)):
                    thumbnailNumbers.append(int(rawThumbnailNumbers[i]))
                break
            except:
                print("Invalid entry")
        else:
            thumbnailNumbers = []
            break


    
    if len(videoNumbers) > 0:
        # Get the end clip length
        while True:
            raw_end_lengths = input("\nWhat length should the ending clips be (answer in seconds, with decimals allowed, for each video, in order entered):  ")
            if raw_end_lengths != "":
                try:
                    raw_end_lengths = raw_end_lengths.split(" ")
                    end_lengths = []
                    for i in range(len(raw_end_lengths)):
                        end_lengths.append(float(raw_end_lengths[i]))
                    break
                except:
                    print("Invalid entry")
            else:
                end_lengths = []
                break
        # Get the audio clip begining            
        while True:
            raw_startPoints = input("\nWhere should the audio start (answer in seconds, with decimals allowed, for each video, in order entered):  ")
            if raw_startPoints != "":
                try:
                    raw_startPoints = raw_startPoints.split(" ")
                    startPoints = []
                    for i in range(len(raw_startPoints)):
                        startPoints.append(float(raw_startPoints[i]))
                    break
                except:
                    print("Invalid entry")
            else:
                startPoints = []
                break


    videoData = []

    try:
        for i in range(len(videoNumbers)):
            videoData.append([videoNumbers[i],end_lengths[i],startPoints[i]])
    except:
        print("There was an invalid entry")
        continue

    while True:
        if len(videoNumbers) > 0:
            confirm = input("\nPlease confirm you want to:\nEdit VIDEOS: {}\nEdit THUMBNAILS: {}\nVideo END LENGTHS: {}\nVideo AUDIO START POINT: {}\nVideo DATA: {}\n(Y/N):  ".format(videoNumbers,thumbnailNumbers,end_lengths,startPoints,videoData))
        else:
            confirm = input("\nPlease confirm you want to:\nEdit THUMBNAILS: {}\n(Y/N):  ".format(thumbnailNumbers))
        if confirm.upper() == "Y":
            selecting = False
            break
        elif confirm.upper() == "N":
            break
        else:
            print("Invalid responce\n")

    

if len(videoNumbers) > 0:
    for videoDataSet in videoData:
        renderVideo(videoDataSet,currentdir)
        print("\nDONE {}!\n".format(videoDataSet[0]))
else:
    print("No Videos Selected")

if len(thumbnailNumbers) > 0:
    for number in thumbnailNumbers:
        renderThumbnail(number,currentdir)
        print("\nDONE {}!\n".format(number))
else:
    print("No Thumbnails Selected")



