
#configure
pathOfLevel = "C:\\Users\\fille\\AppData\\Local\\Will_You_Snail\\MyFirstLevel.lvl" #path of the .lvl file you want to write the animation to
pathOfVideo = ".\\Bad Apple.mp4" #path of the video you want to turn into a wys level
activationThreshold = 127 #the brightness threshold if a pixel is above this it will be white otherwise it will be black
screenResoution = [16, 9] #the amount of door pixels in the door screen
pixelsPerPixel = [60, 60] #the amount of real pixels per door pixel a normal 1x1 wys door is 60x60 real pixels
speedMultiplier = 3 #the playback speed of the video you can use this to gain performance
frameOffset = 14 #the amount of frames to skip THIS IS IN WYS FRAMES MEANING THAT IF THE PLAYBACK SPEED ISN'T 1 IT WILL SKIP frameOffset*speedMultiplier ACTUAL FRAMES


from level import Level
import cv2

def addObject(level, objType, data):
    objects = level.localData["PLACED OBJECTS"][objType]
    objects.update({objType + str(objects["QUANTITY"]) : data})
    objects["QUANTITY"] += 1

def addWire(level, obj1, obj2):
    wires = level.localData["WIRES"]
    wires["QUANTITY"] += 1
    wires["WIRES"].append([obj1, obj2])



aLevel = Level(pathOfLevel)
aLevel.writeRawLevel("""1.5

LEVEL DIMENSIONS:
1920 
1080 

TOOL DATA:
14 
player
0 
1 
1 
6 
xsc
0 
xoff
0 
yoff
0 
ltyp
0 
ldrk
0 
lmsc
1 
wall
0 
1 
1 
1 
blsi
3 
wall_gl
0 
1 
1 
1 
blsi
3 
spike
0 
1 
1 
3 
rot
0 
xoff
0 
yoff
0 
spike_thn
0 
1 
1 
3 
rot
0 
xoff
0 
yoff
0 
door
0 
1 
1 
3 
rot
0 
xoff
0 
yoff
0 
antenna
0 
1 
1 
4 
ysc
1 
coru
0 
xoff
0 
yoff
0 
rantenna
0 
1 
1 
4 
ysc
1 
coru
1 
xoff
0 
yoff
0 
fantenna
0 
1 
1 
4 
ysc
1 
coru
0 
xoff
-10 
yoff
-30 
battery
0 
1 
1 
4 
ysc
0 
coru
0 
xoff
0 
yoff
0 
trigg_ai
0 
1 
1 
15 
onoff
1 
ahea
50 
fsp
0.4 
wsp
0.4 
csp
0.4 
asp
0 
fiw
0 
lsr
0 
drp
0 
jmp
0.3 
rjmp
0.15 
stp
0.15 
st
0.5 
tur
0.1 
inview
1 
property_picker_tool
0 
1 
1 
1 
hlp
0 
wire_tool
0 
1 
1 
1 
hlp
0 
delete_tool
0 
1 
1 
0 

QUICK SLOTS:
player
wall
wall_gl
rantenna
fantenna
door
wire_tool
battery
property_picker_tool
delete_tool

PLACED OBJECTS:
14 
player
2 
31 
32 
0 
1 
1 
0 
31 
92 
0 
1 
1 
0 
wall
0 
wall_gl
1 
-40 
0 
0 
1 
1 
0 
spike
0 
spike_thn
0 
door
0 
antenna
0 
rantenna
0
fantenna
0 
battery
1 
150 
119 
0 
1 
1 
1 
coru
0 
trigg_ai
0 
property_picker_tool
0 
wire_tool
0 
delete_tool
0 

WIRES:
0 
""".split('\n'))
aLevel.localData = aLevel.getLevel()

capture = cv2.VideoCapture(pathOfVideo)
for x in range(screenResoution[0]):
    for y in range(screenResoution[1]):
        addObject(aLevel, 'door', [180 + x*pixelsPerPixel[0], y*pixelsPerPixel[1], 0, pixelsPerPixel[0]/60, pixelsPerPixel[1]/60, 0, {}])

doorIndexOffset = screenResoution[0]*screenResoution[1]
wysFrameCount = 0
while capture.isOpened():
    (ret, frame) = capture.read()
    if capture.get(1)%speedMultiplier == 0 and capture.get(1) > frameOffset*speedMultiplier:
        grayFrame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), screenResoution,
                               interpolation=cv2.INTER_NEAREST)

        (thresh, blackAndWhiteFrame) = cv2.threshold(grayFrame, activationThreshold, 255, cv2.THRESH_BINARY)

        addObject(aLevel, 'door', [0, 180 + 60 * wysFrameCount, 90, 1, 1, 0, {}])
        addObject(aLevel, 'fantenna', [78, 179 + 60 * wysFrameCount, 0, 1, 1, 1, {'coru': 0}])
        addObject(aLevel, 'fantenna', [148, 149 + 60 * wysFrameCount, 0, 1, 1, 1, {'coru': 0}])
        addObject(aLevel, 'rantenna', [30, 59, 0, 1, 1, 1, {'coru': 1}])
        if wysFrameCount == 0:
            addWire(aLevel, "door" + str(doorIndexOffset), "battery0")
        else:
            addWire(aLevel, "door" + str(doorIndexOffset + wysFrameCount), "door" + str(doorIndexOffset + wysFrameCount - 1))
        addWire(aLevel, "door" + str(doorIndexOffset + wysFrameCount), "fantenna" + str(2 * wysFrameCount))
        addWire(aLevel, "fantenna" + str(2 * wysFrameCount), "fantenna" + str(2 * wysFrameCount + 1))

        for y in range(blackAndWhiteFrame.shape[0]):
            for x in range(blackAndWhiteFrame.shape[1]):
                if blackAndWhiteFrame[y][x] > 0:
                    addWire(aLevel, "fantenna" + str(2 * wysFrameCount + 1), "door" + str(x * screenResoution[1] + y))

        wysFrameCount += 1
        cv2.imshow('video bw', cv2.resize(blackAndWhiteFrame, [screenResoution[0] * pixelsPerPixel[0],
                                                               screenResoution[1] * pixelsPerPixel[1]],
                                          interpolation=cv2.INTER_NEAREST))
        cv2.imshow('video original', frame)


 
    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()

aLevel.localData["LEVEL DIMENSIONS"] = [1920, (wysFrameCount + 2) * 60]
aLevel.writeLevel(aLevel.localData)

print(wysFrameCount)
