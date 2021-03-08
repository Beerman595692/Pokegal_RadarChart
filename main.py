from PIL import Image, ImageDraw
from PIL import ImageFont
import requests
from chartmaker import radchar
import csv
import os

def make_chart(name:str,image_url:str,data:dict):
    #creates background image 
    main_img=Image.new("RGBA",(1080,1080),"lightgrey")
    draw = ImageDraw.Draw(main_img)

    draw.rectangle(((30, 30), (1050, 650)), outline="black",width=3, fill="white")

    #gets image of character from url
    dis_image=Image.open(requests.get(image_url, stream=True).raw)
    dis_image.putalpha(255)
    dis_image.thumbnail((1014, 614),Image.ANTIALIAS)

    #creates rader chart image from chartmaker.py
    radarchart=radchar(data,(1050//2,1080-660),"black")

    #sets where to place image of character
    dis_coords=((1080//2)-(dis_image.width//2),(683//2)-(dis_image.height//2))

    #puts image together
    main_img.paste(dis_image, dis_coords, mask=dis_image)
    main_img.paste(radarchart, (1050//4,660), mask=radarchart)

    #saves image
    main_img.save(f"charts/{name}.png", "PNG", quality=70)


#Emptys Charts Folder
folder = 'charts/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


#Runs thourgh CSV file
with open("pokegirls.csv","r") as csvfile:
    #row_count = csvfile.read()
    reader = csv.DictReader(csvfile)
    rl=list(reader)
    print(rl)
    for row_num,row in enumerate(rl):
        #crates table to be printed out on the screen
        table=f"{'╔':═<10}{'╤':═<10}╗\n"
        table+=f"\n{'╟':─<10}{'┼':─<10}╢\n".join([f"║{key[:9].title():<9}│{str(value)[:9].title():<9}║" for key,value in row.items()])
        table+=f"\n{'╚':═<10}{'╧':═<10}╝"
        table+=f'''
{f"{int(100*((row_num+1)/len(rl)))}% done":^21}
{f"{row_num+1}/{len(rl)} lines":^21}
{"█"*int(21*((row_num+1)/len(rl))):▒<21}'''
        os.system("clear")
        print(table)

        #makes image
        data={key:value for key,value in row.items() if not key in ["name","image"]}
        make_chart(str(row_num)+"_"+row["name"].title(),row["image"],data)
    