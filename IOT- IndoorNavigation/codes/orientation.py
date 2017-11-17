orientation=1
for i in finpath:
	if orientation=1:
		if i=='down':
            robfinpath.append("down")
            orientation=1
        elif i=='left':
            robfinpath.append("left")
            robfinpath.append("up")
            orientation=4
        elif i=='right':
            robfinpath.append("left")
            robfinpath.append("up")
            orientation=2
        elif i=='up':
            robfinpath.append("up")
            orientation=1

	if orientation=2:
		if i=='down':
            robfinpath.append("right")
            robfinpath.append("up")
            orientation=3
        elif i=='left':
            robfinpath.append("down")
            orientation=2
        elif i=='right':
            robfinpath.append("up")
            orientation=2
        elif i=='up':
            robfinpath.append("left")
            robfinpath.append("up")
            orientation=3

    if orientation=3:
		if i=='down':
            robfinpath.append("up")
            orientation=3
        elif i=='left':
            robfinpath.append("right")
            robfinpath.append("up")
            orientation=4
        elif i=='right':
           robfinpath.append("left")
           robfinpath.append("up")
           orientation=2
        elif i=='up':
            robfinpath.append("down")
            orientation=3

    if orientation=4:
		if i=='down':
            robfinpath.append("left")
            robfinpath.append("up")
            orientation=3
        elif i=='left':
            robfinpath.append("up")
            orientation=4
        elif i=='right':
            robfinpath.append("down")
            orientation=4
        elif i=='up':
            robfinpath.append("right")
            robfinpath.append("up")
            orientation=1