

def RightHandFingerCount(hand, handType):
    
    ## Tip ids of fingers  ##
    tipIds = [4, 8, 12, 16, 20]
    
    if len(hand) > 0:
        fingers = []
        count = 0
        ##  Thumb  ##
        if hand[tipIds[0]][0] < hand[tipIds[0]-1][0]:
            count+=1

        ## For the rest of the fingers  ##
        for id in range(1, 5):
            if hand[tipIds[id]][1] < hand[tipIds[id]-2][1]:
                count+=1
    return count


