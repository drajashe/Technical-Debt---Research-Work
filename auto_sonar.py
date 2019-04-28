import xml.etree.ElementTree as ET
import os,errno
from os import listdir
from os.path import isfile, join, isdir
from xml.dom import minidom


def change_build_xml_properties(file_name,folder):
    pathSonarJar = "./ant_projects_folder/sonarqube-6.7.5.jar"
    folder_name = folder.split("/")[1]
    tree = ET.parse (file_name)

    root = tree.getroot ()
    # adding the sonar xmlns tag into project
    root.attrib["xmlns:sonar"] = "antlib:org.sonar.ant"

    # Add this next:<property name="sonar.host.url" value="http://localhost:9000" />
    root1 = ET.SubElement(root,'property')
    root1.set ('name', "sonar.host.url")
    root1.set ("value", "http://localhost:9000")


    #Define the SonarQube project properties

    root1 = ET.SubElement(root,'property')
    root1.set("name","sonar.projectKey")
    root1.set("value","org.sonarqube:sonarqube-scanner-ant")

    root1 = ET.SubElement(root,'property')
    root1.set("name","sonar.projectName")
    root1.set("value",folder_name)

    root1 = ET.SubElement(root,'property')
    root1.set("name","sonar.projectVersion")
    root1.set("value","1.0")

    root1 = ET.SubElement(root,'property')
    root1.set("name","sonar.sources")
    root1.set("value","src")

    root1 = ET.SubElement(root,'property')
    root1.set("name","sonar.java.binaries")
    root1.set("value","build")

    root1 = ET.SubElement(root,'property')
    root1.set("name","sonar.java.libraries")
    root1.set("value","lib/*.jar")


    # # iv.)Define SonarQube Scanner for Ant Target
    target_path=ET.SubElement(root,"target")
    taskdef=ET.SubElement(target_path,"taskdef")
    sonar=ET.SubElement(target_path,"sonar:sonar")
    taskdef.set ("uri", "antlib:org.sonar.ant")
    taskdef.set ("resource", "org/sonar/ant/antlib.xml")
    taskdef.set ("path", pathSonarJar)

    # write back to buil.xml
    print("Changing build properties for"+" "+"project" + " " + folder_name)

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open("build.xml", "w") as f:

        f.write(xmlstr)



def editAllSonars():
    mypath = "ant_projects_folder"
    foldernames = [f for f in listdir(mypath) if isdir(mypath+'/'+f)]
    #print(foldernames)
    allfolders = [mypath+'/'+f for f in listdir(mypath) if isdir(mypath+'/'+f)]
    #print(allfolders)

    for folder in allfolders:
        allfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        #print(allfolders)
        path=folder+"/build"
        try:
            #print("-successfuly created a folder")
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print ("-creation of the directory failed")
                raise



        if 'build.xml' in allfiles:
            build_xml = open(folder+'/'+'build.xml')
        change_build_xml_properties(build_xml,folder)


if __name__ == "__main__":
    editAllSonars()
