import Image

CELL_WIDTH = 15
CELL_HEIGHT = 15

THRESHOLD = 7

lCol = (255,0,0,255)
rCol = (0,255,0,255)
fCol = (0,0,255,255)
yellow = (255,255,0,255)
lila = (255,0,255,255)
colors = [lCol,rCol,fCol,yellow, lila]
def same_col(a,b):
    acc = 0
    for x,y in zip(a,b):
        acc+=(x-y)*(x-y)

    if acc < THRESHOLD:
        return True
    return False



def get_fields(path, offset):
    img = Image.open(path)
    WIDTH, HEIGHT = img.size


    x = CELL_WIDTH


    trackers = []
    while x < WIDTH:
        y = CELL_HEIGHT
        while y < HEIGHT:
            if img.getpixel((x,y)) in colors:
                trackers.append((x,y))
                #img.putpixel((x-1,y-1),(0,255,0))
            y+=CELL_HEIGHT
        x+=CELL_WIDTH
    print(path)
    print("TRACKERS CREATED. COUNT: %d" % len(trackers))
    edges = set()
    div_class = {lCol:"left",rCol:"right",fCol:"center",yellow:'date', lila:'date'}



    for tracker in trackers:
        x, y = tracker
        left , top = tracker
        right, bottom = tracker
        marker = img.getpixel((x,y))
        #print('Marker: ',marker,x,y);
        #left
        while same_col(img.getpixel((left, y)), marker):
            left-=1
        col = img.getpixel((left, y))
        while same_col(img.getpixel((left, y)), col):
            left-=1
        #right
        while same_col(img.getpixel((right, y)) , marker):
            right+=1
     
        while same_col(img.getpixel((right, y)), col):
            right+=1
        #top
        while same_col(img.getpixel((x, top)), marker):
            top-=1

        while same_col(img.getpixel((x, top)), col):
            top-=1
        #bottom
        while same_col(img.getpixel((x, bottom)), marker):
            bottom+=1

        while same_col(img.getpixel((x, bottom)), col):
            bottom+=1            
        edges.add((top+offset[1],left+offset[0], right-left, bottom-top, div_class[marker]))

    
    edges = list(edges)
    edges.sort()
    return edges
