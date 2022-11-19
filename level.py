from re import findall

class Level:
    def __init__(self, path):
        self.path = path
        self.localData = self.getLevel()
    
    def getRawLevel(self) -> list:
        """Get the level's data in a plain list"""

        with open(self.path,"r") as file:
            raw = []
            for i in file:
                i = i.rstrip() # get rid of \n and extra whitespace, later we'll have to add \n back in to save our changes
                raw.append(i)
        return raw
    
    def getLevel(self) -> dict:
        """Get the level's data in a dictionary"""

        raw = self.getRawLevel()

        # get tool data
        toolData = {"QUANTITY" : int(raw[7])}
        tools = ["player","wall","wall_gl","spike","spike_thn","door","antenna","rantenna","fantenna",
        "battery","trigg_ai","property_picker_tool","wire_tool","delete_tool"]
        for i in range(len(tools)): # for every tool
            toolInfo = []
            extraAttr = {}
            start = raw.index(tools[i])+1
            try:
                end = raw.index(tools[i+1])
            except:
                end = raw.index("",start)
            for j in range(start,start+4): # get the first 4 values
                toolInfo.append(int(raw[j]))
            for j in range(start+4,end,2): # get the extra attributes, compiled into a dict
                extraAttr[raw[j]] = float(raw[j+1])
            toolInfo.append(extraAttr)
            toolData[tools[i]] = toolInfo

        # get quick slots
        slotIndex = raw.index("QUICK SLOTS:")+1
        slots = []
        while raw[slotIndex] != "":
            slots.append(raw[slotIndex]) 
            slotIndex += 1
        
        # get objects
        objStart = raw.index("PLACED OBJECTS:")
        activeObjData = {"QUANTITY" : raw[objStart+1]}
        for i in tools: # for every type

            # NOTE: object format is like this:
            # "OBJECT NAME", "QUANTITY", "object0value0", "object0value1" ... "object0value-1", "object1value0" ...

            position = raw.index(i,objStart) # find where the object type's name is
            objQuantity = int(raw[position+1]) # how many objects
            objDict = {"QUANTITY" : objQuantity}
            valueStart = position + 2
            defaultValues = 6
            for j in range(objQuantity): # for every object
                values = []
                extraAttr = {}
                for k in range(defaultValues): # every object has at least 6 values so we grab those first
                    values.append(float(raw[valueStart+k]))
                attrQuantity = values[-1] # get the last value, which will be the attr quantity
                for k in range(0,int(attrQuantity)*2,2): # get the extra attributes, compiled into a dict
                    extraAttr[raw[valueStart+defaultValues+k]] = float(raw[valueStart+defaultValues+k+1])
                values.append(extraAttr)
                objDict[i+str(j)] = values
                valueStart += len(values)-1 + 2*len(extraAttr)
            activeObjData[i] = objDict

        # get wires
        wireStart = raw.index("WIRES:")
        wireQuantity = int(raw[wireStart+1])
        wires = {"QUANTITY" : wireQuantity}
        wireData = wireStart+2
        wireObj = []
        for i in range(wireQuantity): # for every wire
            currentWire = [raw[wireData+i*4]+raw[wireData+i*4+1],raw[wireData+i*4+2]+raw[wireData+i*4+3]]
            wireObj.append(currentWire)
        wires["WIRES"] = wireObj
        
        # combine all data into one dict
        levelDict = {
            "VERSION" : float(raw[0]),
            "LEVEL DIMENSIONS" : [int(raw[3]),int(raw[4])],
            "TOOL DATA" : toolData,
            "QUICK SLOTS" : slots,
            "PLACED OBJECTS" : activeObjData,
            "WIRES" : wires
            }
        
        return levelDict
    
    # get wires
    def writeRawLevel(self, data) -> None:
        """Write to the level with a plain list"""
        localData = data.copy() # for some reason when we modify data it modifies the global variable as well, so we gotta make a local copy
        for i in range(len(localData)):
            localData[i] += "\n"
        with open(self.path, "w") as file:
            file.writelines(localData)
    
    def writeLevel(self, data) -> None:
        """Write to the level with a dictionary"""

        # NOTE: right now we arent dealing with the types or the small formatting (ex: \n), we'll handle that at the end

        # establish starting data 
        writeList = [data["VERSION"],"","LEVEL DIMENSIONS:",data["LEVEL DIMENSIONS"][0],data["LEVEL DIMENSIONS"][1],"","TOOL DATA:",data["TOOL DATA"]["QUANTITY"]]

        # get tool data
        tools = ["player","wall","wall_gl","spike","spike_thn","door","antenna","rantenna","fantenna",
        "battery","trigg_ai","property_picker_tool","wire_tool","delete_tool"]
        for i in tools:
            writeList.append(i)
            currentData = data["TOOL DATA"][i]
            for j in range(4): # get starting 4 values
                writeList.append(currentData[j])
            attrDict = currentData[4]
            keys = list(attrDict.keys())
            values = list(attrDict.values())
            for j in range(currentData[3]): # for every extra attr
                writeList.append(keys[j])
                writeList.append(values[j])
        
        # get quick slot data
        writeList.append("")
        writeList.append("QUICK SLOTS:")
        for i in data["QUICK SLOTS"]:
            writeList.append(i)

        # get placed objects
        writeList.append("")
        writeList.append("PLACED OBJECTS:")
        currentData = data["PLACED OBJECTS"]
        typeQuantity = currentData["QUANTITY"]
        writeList.append(typeQuantity)
        for i in tools: # for every object type
            objectData = currentData[i]
            writeList.append(i)
            writeList.append(objectData["QUANTITY"])
            for j in range(len(objectData)-1): # for every object
                currentObject = objectData[i+str(j)]
                for k in range(6): # get first 6 values
                    writeList.append(currentObject[k])
                attrDict = currentObject[6]
                keys = list(attrDict.keys())
                values = list(attrDict.values())
                for k in range(int(currentObject[5])): # get extra attr
                    writeList.append(keys[k])
                    writeList.append(values[k])

        # get wires 
        writeList.append("")
        writeList.append("WIRES:")
        currentData = data["WIRES"]
        wireQuantity = currentData["QUANTITY"]
        writeList.append(wireQuantity)
        wires = currentData["WIRES"]
        for i in range(wireQuantity): # for every wire
            for j in range(2): # for every object
                type = "".join(findall(r'[a-z]+', wires[i][j])) # i dont know how to use regex
                number = "".join(findall(r'\d+',wires[i][j]))
                writeList.append(type)
                writeList.append(number)

        # final(ish) formatting fixes
        for i in range(len(writeList)):
            current = writeList[i]
            if isinstance(current, float):
                if current.is_integer():
                    current = str(int(current))
                else:
                    current = str(current)
            elif isinstance(current, int):
                current = str(current)
            writeList[i] = current
        
        self.writeRawLevel(writeList)
