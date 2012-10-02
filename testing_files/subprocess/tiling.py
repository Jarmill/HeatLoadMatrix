import math
import sys
import copy

"""
    Tiling.py

    Purpose:    Given a beam of dimensions W and H, and N threads runnable at once
                on the computer, divide the beam into smaller rectangles for processing,
                such that all of the cores on the computer are operating in parallel for as
                long as possible, in order to reduce the elapsed time of processing the entire W by H beam.

    Author:     Wayne Miller

    Changed:    September 1st, 2012

    Structure:  Given a rectangle of dimensions W and H, and a number of threads runnable at once
                on the computer N, create a list of rectangles that:
                 1) Covers W by H, does not omit any points
                 2) Does not duplicate coverage of any points
                 3) Uses all cores for as much time as possible

    Usage:      rectList = Tiling(EntireWidth, EntireHeight, TargetN)
                 
                rectList is a list of Rect objects.
                EntireWidth and EntireHeight describe the width and height of the beam
                TargetN is the number of threads that the computer can run at once

                rd = RectDispatcher(rectList, TargetN)  # Pass list from Tiling call

                while rd.hasMoreRects()                 # Run this when capacity available on machine
                    rectsToDispatch = rd.nextListOfRects()
                    for R in rectsToDispatch:
                        # Start next job

"""


"""
    Rect - a class that describes a rectangle's position and size. Also has a single character identifier.
"""

class Rect():
    def __init__(self, X, Y, Width, Height, LetterID = " "):
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height
        self.LetterID = LetterID

    def __str__(self):
        return self.LetterID + " Rect(" + str(self.X) + "," + str(self.Y) + "," + str(self.Width)  \
                 + "," + str(self.Height) + ") sz=" + str(self.Width * self.Height)  

    def Size(self):
        return self.Width * self.Height

"""
    SetRectLetters - a function that orders the rectangle by row and column,
                     and labels them from left to right, up to down
"""

def SetRectLetters(rectList):

    RectLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    lenRectLetters = len(RectLetters)

    rectList.sort(key = lambda a: (a.Y * 1000) + a.X)    # For labeling
    
    for I in range(0, len(rectList), 1):
        rectList[I].LetterID = RectLetters[I % lenRectLetters]

    return rectList

"""
    RectDispatcher - a class that stores a list of rectangles and the target number of threads
                     that can run at once. Method nextListOfRects is called to return a list
                     of rects to run at that time. First call returns rectangles for the
                     target number of threads, and subsequent calls return a single item list
                     with the next rectangle to run.
                     The initial list of rectangles may return all rectangles, including those
                     beyond the target number of threads. This is done when the number of rectangles
                     beyond that target number is a small fraction of the target number, so the
                     operating system can overlap processing. Other code in this file optimizes
                     the number of rectangles to be an even multiple of the target number of threads,
                     so this situation will rarely occur.
"""

class RectDispatcher():
    def __init__(self, rectList, TargetN, DispatchAllFactor = 1.33):
        self.rectList = copy.deepcopy(rectList)
        self.rectList.sort(key = lambda a: -(a.Width * a.Height * 100000) + (a.Y * 1000) + a.X)    # largest first
        self.TargetN = TargetN
        self.NextI = 0
        self.DispatchAllFactor=DispatchAllFactor

    def nextListOfRects(self):
        if self.NextI == 0:     # Single rectangle in list, return it alone
            self.NextI = self.TargetN-1
            if self.TargetN == 1:
                self.NextI = len(self.rectList) + 2
                return [self.rectList[0]]
            elif len(self.rectList) <= (self.DispatchAllFactor * self.TargetN):  # return all, let it contend at the cpu
                self.NextI = len(self.rectList) + 2
                return self.rectList
            else:               # Return first TargetN items, too many to contend
                self.NextI = self.TargetN 
                return self.rectList[0:self.TargetN]

        if self.NextI <= len(self.rectList) + 1:
            self.NextI = self.NextI + 1
            return [self.rectList[self.NextI-1]]

        return []

    def hasMoreRects(self):
        return self.NextI < len(self.rectList)
    
"""
    CombineRects - a function that takes a sorted list of rectangles and combines them to eventually end up with
                   the targeted number of rectangles, while attempting to make each rectangle approximately
                   maxPointCountPerRect points per rectangle.
"""

def CombineRects(rl, TargetN, maxPointCountPerRect):   # This is destructive to the input list, do not use rl after calling
    returnList = []

    if len(rl) <= TargetN:
        return rl

    #rl = copy.deepcopy(rectList)  # This is very slow, so if we assume that we are changing the input list parameter, we can skip this
    
    reduceBy = len(rl) - TargetN

    for i in range(0, len(rl), 1):
    
        if i >= len(rl)-1:
            if i == len(rl) - 1:
                returnList.append(rl[i])
            break;
        
        if reduceBy <= 0:
            returnList.extend(rl[i:len(rl)]) # copy the remainder
            break;
                              
        R1 = rl[i]
        R2 = rl[i+1]
        
        if R1.X != R2.X and R1.Y != R2.Y:  # Not same row or column
            returnList.append(R1) #copy it out
                              
        elif (R1.X == R2.X + R1.Width or R1.X == R2.X - R1.Width or R2.X == R1.X + R2.Width or R2.X == R1.X - R2.Width)  \
                and R1.Height == R2.Height \
                and R1.Y == R2.Y and (R1.Width + R2.Width) * R1.Height <= maxPointCountPerRect:
            returnList.append(Rect(min(R1.X, R2.X), R1.Y, R1.Width + R2.Width, R1.Height))
            del rl[i+1] # Don't see this again
            reduceBy = reduceBy - 1

        elif (R1.Y == R2.Y + R1.Height or R1.Y == R2.Y - R1.Height or R2.Y == R1.Y + R2.Height or R2.Y == R1.Y - R2.Height) \
                and R1.Width == R2.Width \
                and R1.X == R2.X and (R1.Height + R2.Height) * R1.Width <= maxPointCountPerRect:
            returnList.append(Rect(R1.X, min(R1.Y, R2.Y), R1.Width, R1.Height + R2.Height))
            del rl[i+1] # Don't see this again
            reduceBy = reduceBy - 1

        else:
            returnList.append(R1) #copy it out

    return returnList

"""
    CombineRectsOnRows - a function to sort the rectangle list by row, column, and combine adjacent rectangles
"""

def CombineRectsOnRows(rectList, TargetN, maxPointCountPerRect):
    rectList.sort(key = lambda a: (a.Y * 1000) + a.X)    # Now combine on Y
    rectList = CombineRects(rectList, TargetN, maxPointCountPerRect)
    return rectList

"""
    CombineRectsOnRowsUntilStable - a function to repeatedly call CombineRectsOnRows until the number of rectangles
                                    do not increase anymore. Used to maximize the size of the rectables along the rows.
"""

def CombineRectsOnRowsUntilStable(rectList, TargetN, maxPointCountPerRect):
    lenRectList = 0
    while len(rectList) > TargetN and lenRectList != len(rectList):
        lenRectList = len(rectList)  # save length to compare for later
        rectList = CombineRectsOnRows(rectList, TargetN, maxPointCountPerRect)

    return rectList

"""
    CombineRectsOnColumns - a function to sort the rectangle list by column, row, and combine adjacent rectangles.
"""

def CombineRectsOnColumns(rectList, TargetN, maxPointCountPerRect):
    rectList.sort(key = lambda a: (a.X * 1000) + a.Y)    # Now combine on X
    rectList = CombineRects(rectList, TargetN, maxPointCountPerRect)
    return rectList

"""
    CombineRectsOnColumnsUntilStable - a function to repeatedly call CombineRectsOnColumns until the number of rectangles
                                       do not increase anymore. Used to maximize the size of the rectables along the columns.
"""            

def CombineRectsOnColumnsUntilStable(rectList, TargetN, maxPointCountPerRect):
    lenRectList = 0
    while len(rectList) > TargetN and lenRectList != len(rectList):
        lenRectList = len(rectList)  # save length to compare for later
        rectList = CombineRectsOnColumns(rectList, TargetN, maxPointCountPerRect)

    return rectList

"""
    CombineRectsOnColumnsAndRowsUntilStable - a function to repeatedly call CombineRectsOnColumns and CombineRectsOnRows
                                              until the number of rectangles do not increase anymore. Used to shape
                                              rectangles to be longer on the columns than the rows, based on parameter
                                              timesToRunColPerRow
"""  

def CombineRectsOnColumnsAndRowsUntilStable(rectList, TargetN, maxPointCountPerRect, timesToRunColPerRow = 1):
    lenRectList = 0
    while len(rectList) > TargetN and lenRectList != len(rectList):
        lenRectList = len(rectList)  # save length to compare for later
        for i in range(0,timesToRunColPerRow, 1): 
            rectList = CombineRectsOnColumns(rectList, TargetN, maxPointCountPerRect)
        rectList = CombineRectsOnRows(rectList, TargetN, maxPointCountPerRect)

    return rectList

"""
    CombineRectsOnRowsAndColumnsUntilStable - a function to repeatedly call CombineRectsOnColumns and CombineRectsOnRows
                                              until the number of rectangles do not increase anymore. Used to shape
                                              rectangles to be longer on the rows than the columns, based on parameter
                                              timesToRunColPerRow
""" 

def CombineRectsOnRowsAndColumnsUntilStable(rectList, TargetN, maxPointCountPerRect, timesToRunRowPerCol = 1):
    lenRectList = 0
    while len(rectList) > TargetN and lenRectList != len(rectList):
        lenRectList = len(rectList)  # save length to compare for later
        for i in range(0,timesToRunRowPerCol, 1): 
            rectList = CombineRectsOnRows(rectList, TargetN, maxPointCountPerRect)
        rectList = CombineRectsOnColumns(rectList, TargetN, maxPointCountPerRect)

    return rectList
 
"""
    SplitLargestRectsToFillOutTargetN - After creating the target set of rectangles, this function is used to split the largest
                                        rectangles into smaller ones, in order to make the number of rectangles evenly divisable
                                        by the target number of threads. By also optimizing the target size of those new rectangles,
                                        the resultant set of rectangles will optimially oocupy all of the threads for the most time,
                                        minimizing the number of threads that are idle.
"""

def SplitLargestRectsToFillOutTargetN(rectList, TargetN):
    overageCount = len(rectList) - TargetN
    if overageCount <= 0:
        return rectList

    # Sort list by size, largest first
    rectList.sort(key = lambda a: (a.Width * a.Height * 100000) + (a.Y * 1000) + a.X)    # smallest first

    newRectList = rectList[:TargetN]  # We keep the smallest rectangles

    listToSplit = rectList[TargetN:]  # We process this list

    listToSplit.sort(key = lambda a: -(a.Width * a.Height * 100000) + (a.Y * 1000) + a.X)    # largest first
    
    numRectToCreate = TargetN - len(listToSplit)

    totalPointsInList = 0
    for R in listToSplit:
        totalPointsInList = totalPointsInList + (R.Width * R.Height)

    avgSizeForNewRect = int(totalPointsInList / (numRectToCreate+1))

    if avgSizeForNewRect == 0:
        avgSizeForNewRect = 1

    # any rectangles <= the average size gets copied as is

    listToSplit2 = []
    for R in listToSplit:
        if R.Width * R.Height <= avgSizeForNewRect:
            newRectList.append(R) #keep
        else:
            listToSplit2.append(R) #save to split

    for R in listToSplit2: #Recursion!
        newRectList.extend(Tiling(R.Width,R.Height, (R.Width * R.Height / avgSizeForNewRect), R.X, R.Y, DoSplit=0))

    return newRectList

"""
    Tiling - main function, given the width, length, and target number of threads, return a list of
             rectangles that cover the width and length, and that optimize the usage of all available threads.
             Also used in recursion to split larger rectangles into smaller ones, using parameters XBase, YBase, and DoSplit=0.
"""

def Tiling(EntireWidth, EntireHeight, TargetN, XBase=1, YBase=1, DoSplit=1):  # main routine
    rectList = []
    
    for x in range(0, EntireWidth, 1):
        for y in range(0, EntireHeight, 1):
            rectList.append(Rect(XBase+x, YBase+y, 1, 1))

    maxPointCountPerRect = int(round(EntireWidth * EntireHeight / TargetN))
    if maxPointCountPerRect < 1:
        maxPointCountPerRect = 1

    lenRectList = 0

    if EntireWidth % TargetN == 0:
        rectList = CombineRectsOnColumnsUntilStable(rectList, TargetN, maxPointCountPerRect)
        rectList = CombineRectsOnRowsUntilStable(rectList, TargetN, maxPointCountPerRect)
    elif EntireHeight % TargetN == 0:
        rectList = CombineRectsOnRowsUntilStable(rectList, TargetN, maxPointCountPerRect)
        rectList = CombineRectsOnColumnsUntilStable(rectList, TargetN, maxPointCountPerRect)
    elif EntireHeight > EntireWidth:
        timesToRunColPerRow = int(math.sqrt(EntireHeight / EntireWidth))
        if timesToRunColPerRow == 0:
           timesToRunColPerRow = 1 
        rectList = CombineRectsOnColumnsAndRowsUntilStable(rectList, TargetN, maxPointCountPerRect, timesToRunColPerRow)
    else:
        timesToRunRowPerCol = int(math.sqrt(EntireWidth / EntireHeight))
        if timesToRunRowPerCol == 0:
           timesToRunRowPerCol = 1 
        rectList = CombineRectsOnRowsAndColumnsUntilStable(rectList, TargetN, maxPointCountPerRect, timesToRunRowPerCol)

    if DoSplit == 1:
        rectList = SplitLargestRectsToFillOutTargetN(rectList, TargetN)
     
    return SetRectLetters(rectList)

#
#
# Testing and Debugging code below
#
#

def DisplayGrid(rectList, EntireWidth, EntireHeight, TargetN, PrintOnlyOnError = 0):

    strTilingText = "Tiling(" + str(EntireWidth) + "," + str(EntireHeight) + "," + str(TargetN) + ")"
    if PrintOnlyOnError == 0:
        print("************************")
        print (strTilingText)

    if len(rectList) == 0:
        print ("Error + " + strTilingText + "  Empty rectangle list passed.")
        return 1
    
    strDisplay = []
    for I in range(0, EntireHeight, 1):
        strDisplay.append(" " * EntireWidth)

    Errcode = 0
    I = -1
    for R in rectList:
        I += 1
        for Yoffset in range(0, R.Height, 1):
            for Xoffset in range(0, R.Width, 1):
                strWork = strDisplay[R.Y - 1 + Yoffset]
                oldLetter = strWork[R.X - 1 + Xoffset]
                if oldLetter != " ":            # Already assigned
                    Errcode = 2
                    print("Error + " + strTilingText + " Rectangle " + str(R) + " being assigned to grid location (" + str(Xoffset) + "," +  str(Yoffset) + ") which was already assigned to rectangle " + oldLetter + ".")

                strLeft = strWork[0:(R.X - 1 + Xoffset)]
                strRight = strWork[(R.X + Xoffset):]
                strNew = strLeft + R.LetterID + strRight
                strDisplay[R.Y - 1 + Yoffset] = strNew
                
##                print ("strWork=" + strWork)
##                print ("oldLetter=" + oldLetter)
##                print ("strLeft=" + strLeft)
##                print ("strRight=" + strRight)
##                print ("strNew=" + strNew)


    # Is the rectangle totally covered?

    for i in range(0, len(strDisplay), 1):
        if strDisplay[i].find(" ") >= 0:
            print("Error + " + strTilingText + " Unallocated areas on the grid (" + str(i) + "," + str(strDisplay[i].find(" ")) + ").")
            Errcode = 3
            break
        
    # Spaces between characters for display

    for i in range(0, len(strDisplay), 1):
        strWork = strDisplay[i]
        strNew = ""
        for c in strWork:
            strNew += c + " "
        strDisplay[i] = strNew

    # Display to console if error or if flag indicates to always display

    if PrintOnlyOnError != 1 or Errcode != 0:
        print(" ")
        for strDisp in strDisplay:
            print(strDisp)

    return Errcode

def DisplayRects(rectList):
    if len(rectList) == 0:
        return
    
    for R in rectList:
        print(str(R))

def TestTiling(EntireWidth, EntireHeight, TargetN, PrintOnlyOnError = 1):

    strTilingText = "Tiling(" + str(EntireWidth) + "," + str(EntireHeight) + "," + str(TargetN) + ")"

    rectList = Tiling(EntireWidth, EntireHeight, TargetN)
    
    Errcode = DisplayGrid(rectList, EntireWidth, EntireHeight, TargetN, PrintOnlyOnError)

    if PrintOnlyOnError != 1 or Errcode != 0:
        print(" ")
        DisplayRects(rectList)

    numOfRects = len(rectList)

    if numOfRects < TargetN and (EntireWidth * EntireHeight) >= TargetN:
        Errcode = 11
        print ("Error " + strTilingText + " len(rectList) < TargetN   TargetN = " + str(TargetN) + "  len(rectList) = " + str(len(rectList)))

    if PrintOnlyOnError != 1:
        print(" ")

        rd = RectDispatcher(rectList, TargetN)

        # Simulate TargetN cpus, find the longest path length of rectangle points
        # Place the next dispatched set of rects onto the shortest CPU

        cpuList = []
        for i in range(0, TargetN, 1):
            cpuList.append(0)

        while rd.hasMoreRects():
            rectsToDispatch = rd.nextListOfRects()
            print("Processing rect list of length " + str(len(rectsToDispatch)))
            DisplayRects(rectsToDispatch)
            for R in rectsToDispatch:
                cpuList.sort()   # lowest number at [0]
                cpuList[0] = cpuList[0] + R.Size()

        strOut = ""
        cpuList.sort()   # lowest number at [0]
        for i in cpuList:
            if strOut != "":
                strOut = strOut + " "
            strOut = strOut + str(i)

        print("Cpu job loading = (" + strOut + ")")

def SelfTestTiling(PrintOnlyOnError = 1):
    for EntireWidth in range(1, 65, 1):
        print("Processing Width=" + str(EntireWidth))
        for EntireHeight in range(1, 65, 1):
            for TargetN in range(1, 65, 1):
                try:
                    TestTiling(EntireWidth, EntireHeight, TargetN, PrintOnlyOnError)
                except Exception:
                    strTilingText = "Tiling(" + str(EntireWidth) + "," + str(EntireHeight) + "," + str(TargetN) + ")"
                    strWork = ""
                    for e in sys.exc_info():
                        strWork = strWork + str(e) + "\n"
                    print("Fault " + strTilingText + "  " + strWork)


##SelfTestTiling(1)

#TestTiling(6,80,13, 0)                     
##TestTiling(1,7,4, 0)                    
##TestTiling(3,7,2, 0)
##TestTiling(9,61,64, 0)  
##TestTiling(7,3,4, 0)
##TestTiling(6, 6, 22, 0)
##TestTiling(7, 11, 13, 0) 
##TestTiling(2, 2, 4, 0)    
##TestTiling(4, 4, 5, 0)   
##TestTiling(6, 6, 4, 0)    
##TestTiling(6, 6, 2, 0)    
##TestTiling(6, 6, 3, 0)    
##TestTiling(3, 6, 3, 0)   
##TestTiling(6, 3, 3, 0)   
##TestTiling(7, 11, 8, 0) 
##TestTiling(7, 11, 2, 0) 
##TestTiling(11, 7, 2, 0)  
##TestTiling(13, 7, 5, 0) 
##TestTiling(11, 7, 3, 0)

                    
##testBadRectList = [Rect(1, 1, 1, 1), Rect(1, 1, 2, 2)]  # overlap
##testBadRectList[0].LetterID = "A"
##testBadRectList[1].LetterID = "B"
##DisplayGrid(testBadRectList, 2, 2, 2)

##testBadRectList2 = [Rect(1, 1, 1, 1)]  # missing coverage
##testBadRectList2[0].LetterID = "A"
##DisplayGrid(testBadRectList2, 2, 2, 2)