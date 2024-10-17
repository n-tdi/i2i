import glob
import os
import subprocess
def megaglob(name):
    m = 0
    while m > -1:
        path = "*/"*m
        path = path+name
        if not glob.glob(path) == []:
            m =-1
            return(glob.glob(path)[0].replace(r'\\'[1], '\\'))
        else:
            m+=1

def megaglobos(name4):
    for r,d,f in os.walk("c:\\"):
        for files in f:
            if files == name4:
                return(os.path.join(r,files).replace(r'\\'[1], '\\'))
def getdirect(name, extrapath = "c:\\"):
    for r,d,f in os.walk(extrapath):
        for files in f:
            if files == name:
                return(os.path.join(r,files).replace(r'\\'[1], '\\').replace(name, ""))
    raise FileNotFoundError
def getdirectb(name):
    try:
        return(getdirect(name, os.getcwd()))
    except:
        return(getdirect(name))

def getprocess(process_name):
    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)
    output = subprocess.check_output(cmd, shell=True).decode()
    if process_name.lower() in output.lower():
        return True
    else:
        return False
