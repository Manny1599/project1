
import os
import pickle
import re
##making the nodes class
##takes in node id, time to terminate in s, destination, data string, start time, neightbors list
class node:
    def __init__(self, id, time, dest, data, startT, neigh):
        self.id = id
        self.time = time
        self.dest = dest
        self.data = data
        self.startT = startT
        self.neigh = neigh
        self.sNum = 0

nodes = []
liveN = [False for _ in range(10)]


def add(message):
    if not os.path.exists("objects.txt"):
        with open("objects.txt", "wb") as f:
            pickle.dump([], f)
    # Read the existing objects from the file
    with open("objects.txt", "rb") as f:
        existing_objects = pickle.load(f)
    with open("objects.txt", "rb") as f:
        nodes = pickle.load(f)
    for i in nodes:
        liveN[i.id] = True

    ##-------------------------------------------------------------------------
    ## see if the string is sending data or just setting neighbors
    msgstringchar = '"'
    ##tdata if there is data to send
    tdata = False
    if msgstringchar in message:
        ## pulling message out from input
        start_index = message.index('"') + 1
        end_index = message.index('"', start_index)
        substring = message[start_index:end_index]
        print(substring)  # Output: hello world
        t = re.sub('".*?"', '', message)
        print(t)
        #splitting string up removing word node first
        my_list = list(map(int, t.split()[1:]))
        print(my_list)
        tdata = True

    else: ##just setting up neighbors
        my_list = list(map(int, message.split()[1:]))
        print(my_list)
    ##---------------------------------------------------------------------------------------------------



    ##checking to see if the node is live or not if not then make  new node else update info

    if int(my_list[0] in liveN):
        print("in list")
    else:#if not create a new node and add to live list
        print("else")
        ##message to deliver
        if tdata:
            print("in if of else tdata:",tdata)
            id = my_list[0]
            time = my_list[1]
            dest = my_list[2]
            data = substring
            starttime = my_list[3]
            negh = my_list[4:]
            new_object = node(id, time,dest,data,starttime,negh)
        else:#no msg to deliver
            print("in else of else tdata:", tdata)
            id = my_list[0]
            print(id)
            time = my_list[1]
            dest = my_list[2]
            data = ""
            starttime = 0
            negh = my_list[3:]
            new_object = node(id, time, dest, data, starttime, negh)

    #if sending message
    if tdata:
        frame = ""
        ##send to transport
        for i in data:
            frame+= (i)
            if(((len(frame) + 1) % 5) == 0): ##5 bytes
                msg = ['D', id, dest, new_object.sNum, frame]

                new_object.sNum = new_object.sNum + 1
                frame = ""
    ##if padding needed pad and send
    if (len(frame) != 0 ):
        while len(frame) != 5:
            frame+= " "
        print("frame length is : ",len(frame))
        msg = ['D', id, dest, new_object.sNum, frame]
        new_object.sNum = new_object.sNum + 1
        frame = ""



    ##appending new node to file
    existing_objects.append(new_object)
    with open("objects.txt", "wb") as f:
        pickle.dump(existing_objects, f)

    # Access the objects from the file
    with open("objects.txt", "rb") as f:
        nodes = pickle.load(f)

    for i in nodes:
        liveN[i.id] = True



