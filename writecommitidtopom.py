from os import listdir
from os.path import isfile, join, isdir

def findlinenumber():
    mypath = "pom_xmls"
    foldernames = [f for f in listdir(mypath) if isdir(mypath+'/'+f)]
    print(foldernames)
    allfolders = [mypath+'/'+f for f in listdir(mypath) if isdir(mypath+'/'+f)]
    print(allfolders)
    i = 0
    for folder in allfolders:
        linenumber = -1
        allfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        print(allfiles)
        if 'pom.xml' in allfiles:
            pom = open(folder+'/'+'pom.xml', 'r')
            parentendtagmet = 0
            for line in pom:
                linenumber += 1
                if "</parent>" in line:
                    parentendtagmet = 1
                    continue
                if parentendtagmet == 0:
                    continue
                elif parentendtagmet == 1:
                    if "<groupId>" in line:
                        start = line.find(">")
                        end = line.find("</g")
                        groupid = line[start+1:end]
                        print(line[start+1:end])
                        #pom.close()
                        writenewpomxml(linenumber, foldernames[i], folder, groupid)
                        parentendtagmet = 0
                        break
        i += 1
        print(folder+'/'+'pom.xml')

def writenewpomxml(linenumber, foldername, folderpath, groupid):
    with open(folderpath+'/'+'pom.xml', 'r') as file:
        lines = file.readlines()
    # now we have an array of lines. If we want to edit the line 17...

    if len(lines) > int(linenumber):
        lines[linenumber] = "  <groupId>" + groupid + "_" + foldername + "</groupId>" + "\n"

    with open(folderpath+'/'+'pom.xml', 'w') as file:
        file.writelines(lines)

    print("Completed writing to folder: " + folderpath )

if __name__ == "__main__":
    findlinenumber()
