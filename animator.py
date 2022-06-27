def wysAnimate(frameCount, animationName, mp4path):

    levelHeight = (frameCount+4)*60
    levelWidth = 1920
    if frameCount > 60:
        raise Exception("Frame limit exceeded. Due to limitations of the level editor you can only have 60 frames or less.")
    f = open(animationName + ".lvl", "w")
    f.write("1.5\n\n") #Game versiom
    print("Writing boilerplate code")
    f.write("LEVEL DIMENSIONS:\n" + str(levelWidth) + "\n" + str(levelHeight) + "\n\n") #Dimensions

    tooldata = """TOOL DATA:
    14 
    player
    0 
    1 
    1 
    6 
    xsc
    1 
    xoff
    7 
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
    2 
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
    90 
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
    1 
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
    0 
    coru
    0 
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
    1 
    xoff
    0 
    yoff
    0 
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
    0"""
    #Who knew that wys level editor would have more boilerplate code then Java?

    quickslots = """QUICK SLOTS:
    player
    wall
    fantenna
    rantenna
    wire_tool
    door
    antenna
    battery
    property_picker_tool
    delete_tool""" #again... boilerplate

    players = """player
    2 
    39 
    32 
    0 
    1 
    1 
    0 
    39 
    152 
    0 
    1 
    1 
    0 """

    wall = """wall
    1 
    60 
    0 
    0 
    1 
    1 
    0 """

    battery= """battery
    1 
    210 
    179 
    0 
    1 
    1 
    1 """
    othera = """trigg_ai
    0 
    trigg_ai
    0 
    property_picker_tool
    0 
    wire_tool
    0 
    delete_tool
    0 """

    otherb = """wall_gl
    0 
    spike
    0 
    spike_thn
    0 """

    f.write(tooldata + "\n\n")
    f.write(quickslots + "\n\n")

    print("Done writing boilerplate code")
    print("Building frames and the display")
    f.write("PLACED OBJECTS:\n14\n"+players+"\n") 
    f.write(wall+"\n")
    f.write(otherb+"\n")
    f.write("door\n"+str(frameCount+9*16)+"\n")
    for x in range(frameCount):
        f.write("0\n")
        f.write(str(300+x*60)+"\n")
        f.write("90\n")
        f.write("1\n")
        f.write("1\n")
        f.write("0\n")
    for x in range(16):
        for y in range(9):
            f.write(str(4*60+x*60)+"\n")
            f.write(str(y*60)+"\n")
            f.write("0\n")
            f.write("1\n")
            f.write("1\n")
            f.write("0\n")
    f.write("antenna\n0\n")
    f.write("rantenna\n"+str(frameCount)+"\n") 
    for x in range(frameCount):
        f.write(str(x)+"\n")
        f.write("119\n")
        f.write("0\n")
        f.write("1\n")
        f.write("1\n")
        f.write("1\n")
        f.write("coru\n")
        f.write("1\n")
    f.write("fantenna\n"+str(frameCount*2)+"\n")
    for x in range(frameCount):
        f.write("208\n")
        f.write(str(269+x*60)+"\n")
        f.write("0\n")
        f.write("1\n")
        f.write("1\n")
        f.write("1\n")
        f.write("coru\n")
        f.write("0\n")
    for x in range(frameCount):
        f.write("88\n")
        f.write(str(299+x*60)+"\n")
        f.write("0\n")
        f.write("1\n")
        f.write("1\n")
        f.write("1\n")
        f.write("coru\n")
        f.write("0\n")
    f.write(battery+"\n")
    f.write(othera+"\n\n")

    print("Building frames and the display")

    wires = []
    print("Wiring the frame skeleton.")
    #f.write("WIRES:\n"+str(frameCount*3)+"\n")
    wires.append("battery\n0\ndoor\n0\n")
    for x in range(frameCount-1):
        wires.append("door\n"+str(x)+"\n"+"door\n"+str(x+1)+"\n")
    for x in range(frameCount):
        wires.append("door\n"+str(x)+"\n"+"fantenna\n"+str(x+frameCount)+"\n")
    for x in range(frameCount):
        wires.append("fantenna\n"+str(x+frameCount)+"\n"+"fantenna\n"+str(x)+"\n")
    print("Done!")
    import cv2
    import numpy as np

    cap = cv2.VideoCapture(mp4path)

    frames = []
    count = 0
    connections = 0
    print("Processing video.")
    while (cap.isOpened() and count < frameCount):
        ret, frame = cap.read()
        try:
            frame = cv2.resize(frame, (16, 9), fx = 0, fy = 0, interpolation = cv2.INTER_NEAREST)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            for x in range(16):
                for y in range(9):
                    if gray[y,x] > 127:
                        connections += 1
                        wires.append("fantenna\n"+str(count)+"\n"+"door\n"+str(frameCount + y + 9*x)+"\n")
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            count += 1
            print("frame #"+str(count))
        except:
            count += 1
            continue
            
    print("Video processing done!")
    # release the video capture object
    cap.release()
    # Closes all the windows currently opened.
    cv2.destroyAllWindows()

    wires.insert(0, "WIRES:\n"+str(frameCount*3+connections)+"\n")

    f.writelines(wires)



    f.close()

    print("Your file is done!")

#Settings
_frameCount = 60
_animationName="shrek"
_mp4path="s.mp4"

#wysAnimate(_frameCount, _animationName, _mp4path)