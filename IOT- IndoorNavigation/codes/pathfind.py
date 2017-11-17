import Queue


def intheblock(x,y,lx,ly):
    if x>0 and x<lx and y>0 and y<ly:
        return True
    else:
        return False

array=[]
with open("maze2.txt",'r') as f:
    for line in f:
        array.append(line)
#for a in array:
    #print a
endx=0
endy=0
startx=0
starty=0
lx=len(array[0])
ly=len(array)
#print lx,ly
parent=[]
visited=[]
for a in xrange(ly):
    parent.append([])
    visited.append([])
    for b in xrange(lx-1):
        if array[a][b]=='E':
            endy=a
            endx=b
        if array[a][b]=='S':
            starty=a
            startx=b
        parent[a].append((0,0))
        visited[a].append(0)


#print starty,startx
#print endy,endx


q=Queue.Queue()
q.put((starty,startx))
visited[starty][startx]=1
parent[starty][startx]=(-1,-1)
bol=True

while not q.empty():
    tup=q.get()
    x=tup[1]
    y=tup[0]
    #print tup,parent[y][x]
    if x==endx and y==endy:
        print "path found"
        bol=False
        break
    else:

        # check the above block array[y-1][x]
        if (intheblock(x,y,lx,ly) and (not array[y-1][x]=="+") and (not visited[y-1][x]==1)):
            q.put((y-1,x))
            visited[y-1][x]=1
            parent[y-1][x]=((y,x))
        # check the below block array[y+1][x]
        if (intheblock(x,y,lx,ly) and (not array[y+1][x]=="+") and (not visited[y+1][x]==1)):
            q.put((y+1,x))
            visited[y+1][x]=1
            parent[y+1][x]=((y,x))
        # check the right block array[y][x+1]
        if (intheblock(x,y,lx,ly) and (not array[y][x+1]=="+") and (not visited[y][x+1]==1)):
            q.put((y,x+1))
            visited[y][x+1]=1
            parent[y][x+1]=((y,x))
        # check the left block array[y][x-1]
        if (intheblock(x,y,lx,ly) and (not array[y][x-1]=="+") and (not visited[y][x-1]==1)):
            q.put((y,x-1))
            visited[y][x-1]=1
            parent[y][x-1]=((y,x))

if not bol:

    tempx=endx
    tempy=endy
    c=0
    path=[]
    while (True):
        t=parent[tempy][tempx]
        #print t
        path.append(t)
        tempy=t[0]
        tempx=t[1]
        c+=1
        if (tempx==startx and tempy==starty):
            break

    path = path[::-1]
    path.append((endy,endx))

    l=len(path)
    finpath=[]
    print "shortest path"
    print "-------------"
    for i in range(1,l):
        cury=path[i][0]
        curx=path[i][1]
        if cury-starty==1:
            finpath.append("down")
        elif cury-starty==-1:
            finpath.append("up")
        elif curx-startx==1:
            finpath.append("right")
        else:
            finpath.append("left")

        starty=cury
        startx=curx
    robfinpath=[]
    ori=1
    for i in finpath:
        if ori==1:
            if i=="up":
                robfinpath.append('f')
                ori=1
            elif i=='down':
                robfinpath.append('b')
                ori=1
            elif i=='right':
                robfinpath.append('r')
                robfinpath.append('f')
                ori=2
            elif i=='left':
                robfinpath.append('l')
                robfinpath.append('f')
                ori=4

        elif ori==2:
            if i=="up":
                robfinpath.append('l')
                robfinpath.append('f')
                ori=1
            elif i=='down':
                robfinpath.append('r')
                robfinpath.append('f')
                ori=3
            elif i=='right':
                robfinpath.append('f')
                ori=2
            elif i=='left':
                robfinpath.append('b')
                ori=2


        elif ori==3:
            if i=="up":
                robfinpath.append('b')
                ori=3
            elif i=='down':
                robfinpath.append('f')
                ori=3
            elif i=='right':
                robfinpath.append('l')
                robfinpath.append('f')
                ori=2
            elif i=='left':
                robfinpath.append('r')
                robfinpath.append('f')
                ori=4

        elif ori==4:
            if i=="up":
                robfinpath.append('r')
                robfinpath.append('f')
                ori=1
            elif i=='down':
                robfinpath.append('l')
                robfinpath.append('f')
                ori=3
            elif i=='right':
                robfinpath.append('b')
                ori=4
            elif i=='left':
                robfinpath.append('f')
                ori=4
    instruction = "".join(robfinpath)

if bol:
    print "no path found"


'''
SOCKET
'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#host = "192.168.0.102"                          
print "Enter PORT"
port = input()

# connection to hostname on the port.
s.connect(("10.42.0.112", port))  
print s.recv(1024)                             
                                    
s.send(instruction)
for i in instruction:
    print s.recv(1024)

s.close()