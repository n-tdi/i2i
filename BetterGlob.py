import glob
import os
import subprocess
SEP = os.sep
def megaglob(name):
    m = 0
    while m > -1:
        path = "*/"*m
        path = path+name
        if not glob.glob(path) == []:
            m =-1
            return(glob.glob(path)[0].replace(r'\\'[1], SEP))
        else:
            m+=1

def megaglobos(name4):
    for r,d,f in os.walk(f"c:{SEP}"):
        for files in f:
            if files == name4:
                return(os.path.join(r,files).replace(r'\\'[1], SEP))
def getdirect(name, extrapath = f"c:{SEP}"):
    for r,d,f in os.walk(extrapath):
        for files in f:
            if files == name:
                return(os.path.join(r,files).replace(r'\\'[1], SEP).replace(name, ""))
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
