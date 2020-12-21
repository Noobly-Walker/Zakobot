from datetime import datetime

num = [0]
def breakpoint(comment=""):
    print("Point ", num[0], ": ", datetime.now().time(), "\t\tComment: ",comment)
    num[0] = num[0] + 1
