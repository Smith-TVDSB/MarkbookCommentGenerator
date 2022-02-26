from random import sample

#Holds the assessment and all associated expectations


#Constructs the comment based on the mark of the highest mark.

def makeComment(starters,modifiers,links,demonstrators,reviewStatments,assignment,str,wkn):
    start = sample(starters,1)[0]
    link = sample(links,1)[0]
    demo = sample(demonstrators,1)[0]
    review = sample(reviewStatments,1)[0]
    if assignment[1] >= 80:
        mod = sample(modifiers[0][1:],1)[0]
    elif assignment[1] >= 70:
        mod = sample(modifiers[1][1:],1)[0]
    elif assignment[1] >= 60:
        mod = sample(modifiers[2][1:],1)[0]
    elif assignment[1] >= 50:
        mod = sample(modifiers[3][1:],1)[0]
    else:
        mod = sample(modifiers[4][1:],1)[0]

    text = f"{start} {mod} {link} {str} {demo} {assignment[0]}. {review} {wkn}."
    return text

