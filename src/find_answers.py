import cv2
import configparser
import math
import time

# Import settings
config = configparser.ConfigParser()
config.read('./src/settings.ini')
default = config['DEFAULT']
out_path = default['out_path']
questions = int(default['questions'])
choices = int(default['choices'])
correct = default['correct_answers'].split(", ")
save_im = default['save_im'] == "True"
out_im = default['output_im'] == "True"

def find(cells, bild, image):


    def Sort(sub_li, i):
        sub_li.sort(key = lambda x: x[i])
        return sub_li


    # Skapar en lista som inehåller en lista för varje rad med koordinater
    # inre listan sorteras i x led (1 x 2)
    rows = []
    for y in range(questions):
        row = []
        for i in range(choices):
                row.append(cells[choices * y + i])

        row = Sort(row, 0)
        rows.append(row)


    res = [] #Lista inehållande svar
    coords = []
    count = 0 #Antal svar

    # Går igenom alla rader och kontrollerar om svarskryss ligger nära mitten på en ruta
    img  = cv2.imread(bild)
    for row in rows:
            #print("-----------")
            found = False
            ans = []
            for i in range(choices):
                    # Koordinater för ruta
                    cX, cY = row[i]

                    valueList = []

                    w = 70

                    for c in range(w):
                            r, g, b = img[cY, cX + c]
                            num = int(r) + int(g) + int(b)
                            valueList.append(num)

                            r, g, b = img[cY, cX - c]
                            num = int(r) + int(g) + int(b)
                            valueList.append(num)

                    valueList.sort()

                    a = 0
                    for i in range(10):
                            a += valueList[i]

                    a = a/10

                    ans.append([a, cX, cY])

                    if save_im:
                        cv2.circle(image, (cX, cY), 1, (232, 14, 250), -1)
                    

                    string = f"{cX}, {cY}"


            if not found:
                    #print(ans)
                    ls = [ans[0][0], ans[1][0], ans[2][0]]
                    r = ls.index(min(ls))
                    x = int(ans[r][1])
                    y = int(ans[r][2])
                    coords.append([x, y])
                    if save_im:
                        cv2.circle(image, (x, y), 20, (0,0,255), -1)
                    res.append(r)

    c = 0
    for i in range(len(correct)):
        x, y = coords[i]
        if res[i] == int(correct[i]):
                if out_im:
                    cv2.circle(img, (x, y), 40, (0, 200, 0), -1)
                c += 1
        else:
            if out_im:
                cv2.circle(img, (x, y), 40, (0, 0, 200), -1)

    if save_im:
        cv2.imwrite(f"{ out_path }3answers.jpg", image)

    if out_im:
        cv2.imwrite(f"{ out_path }4correct.jpg", img)

    return {'corr': c}