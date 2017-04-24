'''
Created on Apr 2, 2017

@author: Steven Proctor
'''

path=""
jpath=""
text=""
newfile=False
def select(filePath="default"):
    lpath=filePath+".json"
    newFile=False
    try:
        ltext = open(lpath).read()
    except Exception:
        newFile=True
        ltext="{\n\n}"
    return [lpath,ltext,newFile]
def commit(path,text):
    open(path,"w").write(text)
def key(text,akey = "default",val="null"):
    text=text[:2]+"\t"+akey+":"+"\""+val+"\","+"\n"+text[2:]
    return text
def lst(text,args):
    line = "\t"+args[0]+":"+"["
    for s in args[1:len(args)-1]:
        line+="\""+s+"\", "
    line+="\""+args[len(args)-1]+"\""+"],\n"
    text=text[:2]+line+text[2:]
    return text
t=select(raw_input("Select or create a file: "))
path=t[0]
text=t[1]
newfile=t[2]
while(True):
    try:
        temp = raw_input("<"+jpath)
        c=temp.split(" ")[0]
        args=temp.split(" ")[1:]
    
    
        if c=="select":
            commit(path,text)
            t=select(args[0])
            path=t[0]
            text=t[1]
            newfile=t[2]
        if c=="def":
            text=key(text,args[0],args[1])
            if newfile:
                text=text[:-4]+"\n}"
                newfile=False
        if c=="quit":
            commit(path,text)
            break
        if c=="list":
            text=lst(text,args)
            if newfile:
                text=text[:-4]+"\n}"
                newfile=False
        if c=="help":
            print "select <fileName> switches to or creates a .json file (do not type \".json\" in fileName or you'll get thing.json.json\n def <key> <value> - adds a simple entry to the json\n list <key> <val1> <val2> ... - adds a list to json\n quit- quits"
        commit(path,text)
    except:
        print "Error"