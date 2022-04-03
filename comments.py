from random import sample

#Holds the assessment and all associated expectations
class lastUsedComment:
    def __init__(self, start, lvl4, lvl3, lvl2, lvl1, lvl0, link, demo, review):
        self.start = start
        self.lvl4 = lvl4
        self.lvl3 = lvl3
        self.lvl2 = lvl2
        self.lvl1 = lvl1
        self.lvl0 = lvl0
        self.link = link
        self.demo = demo
        self.review = review
    
    def updateLevel4(self,lvl4):
        self.lvl4 = lvl4
    def updateLevel3(self,lvl3):
        self.lvl3 = lvl3
    def updateLevel2(self,lvl2):
        self.lvl2 = lvl2
    def updateLevel1(self,lvl1):
        self.lvl1 = lvl1
    def updateLevel0(self,lvl0):
        self.lvl0 = lvl0


    def update(self, start, link, demo, review):
        self.start = start
        self.link = link
        self.demo = demo
        self.review = review

#Make initial blank comment
lastComment = lastUsedComment('','','','','','','','','')

def trim(listOfSection, lastUsed):
    if lastUsed in listOfSection:
        listOfSection.remove(lastUsed)
        return listOfSection

    return listOfSection

#Constructs the comment based on the mark of the highest mark.
def makeComment(starters,modifiers,links,demonstrators,reviewStatments,assignment,str,wkn):
    global lastComment
    #trim ALL the lists
    commentParts = [starters,links,demonstrators,reviewStatments]
    lastCommentParts = [lastComment.start,lastComment.link,lastComment.demo,lastComment.review]
    for i in range(len(commentParts)):
        if len(commentParts[i])>1:
            commentParts[i] = trim(commentParts[i],lastCommentParts[i])

    start = sample(commentParts[0],1)[0]
    link = sample(commentParts[1],1)[0]
    demo = sample(commentParts[2],1)[0]
    review = sample(commentParts[3],1)[0]

    for i in range(len(commentParts)):
        if lastCommentParts[i] != '' and not lastCommentParts[i] in commentParts[i]:
            commentParts[i].append(lastCommentParts[i])
    #trim modifiers
    modLvl = [lastComment.lvl4,lastComment.lvl3,lastComment.lvl2,lastComment.lvl1,lastComment.lvl0]
    for i in range(len(modifiers)):
        if len(modifiers[i])>2:
            modifiers[i] = trim(modifiers[i],modLvl[i])

    if assignment[1] >= 80:
        mod = sample(modifiers[0][1:],1)[0]
        if lastComment.lvl4 != '' and not lastComment.lvl4 in modifiers[0][1:]:
            modifiers[0].append(lastComment.lvl4)
        lastComment.lvl4 = mod
    elif assignment[1] >= 70:
        mod = sample(modifiers[1][1:],1)[0]
        if lastComment.lvl3 != '' and not lastComment.lvl3 in modifiers[1][1:]:
            modifiers[1].append(lastComment.lvl3)
        lastComment.lvl3 = mod
    elif assignment[1] >= 60:
        mod = sample(modifiers[2][1:],1)[0]
        if lastComment.lvl2 != '' and not lastComment.lvl2 in modifiers[2][1:]:
            modifiers[2].append(lastComment.lvl2)
        lastComment.lvl2 = mod
    elif assignment[1] >= 50:
        mod = sample(modifiers[3][1:],1)[0]
        if lastComment.lvl1 != '' and not lastComment.lvl1 in modifiers[3][1:]:
            modifiers[3].append(lastComment.lvl1)
        lastComment.lvl1 = mod
    else:
        mod = sample(modifiers[4][1:],1)[0]
        if lastComment.lvl0 != '' and not lastComment.lvl0 in modifiers[4][1:]:
            modifiers[4].append(lastComment.lvl0)
        lastComment.lvl0 = mod

    text = f"{start} {mod} {link} {str} {demo} {assignment[0]}. {review} {wkn}."
    lastComment.update(start,link,demo,review)
    return text

