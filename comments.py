from random import sample

#Holds the assessment and all associated expectations


#Constructs the comment based on the mark of the highest mark.

def makeComment(assignment,str,wkn):
    if assignment[1] >= 80:
        mod = sample(["thorough", "exceptional"],1)[0]
    elif assignment[1] >= 70:
        mod = "considerable"
    elif assignment[1] >= 60:
        mod = "some"
    elif assignment[1] >= 50:
        mod = "limited"
    else:
        mod = "very limited"

    filler = sample(['knowledge of','understanding of','ability in using'],1)[0]

    text = f"$ has demonstrated {mod} {filler} {str} as demonstrated by # {assignment[0]}. $ should review {wkn}."
    return text

