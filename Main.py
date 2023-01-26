from functools import reduce
import xml.etree.ElementTree as ET
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory

TAGS_WITH_DATA:list[str] = ["sub-flow", "flow"]

def printxml(s:str):
    # whil
    print(s)

def get_xml_files_in_directory_as_list_of_files(directory:str) -> list[Path]:
    return list(Path(directory).rglob("*.[xX][mM][lL]"))

def print_info_from_root(path:Path, root:ET.Element):
     for element in root.iter():
        if "flow" in element.tag:
            printxml(f"{element.tag} in {path}")
            for attrib in element.items():
                    printxml(f"\t\t{attrib}")
            for child in element.findall("*"):
                printxml(f"\t{child.tag}")
                for attrib in child.items():
                    printxml(f"\t\t{attrib}")
            
            # print (ET.tostring(element, encoding='unicode'))

def get_root_from_path(xml_file:Path) -> ET.Element:
    tree:ET.ElementTree = ET.parse(xml_file)

    root:ET.Element = tree.getroot()

    return root


def main():
    path:str = askdirectory(title='Select Folder') 

    files:list[Path] = get_xml_files_in_directory_as_list_of_files(path)
       
    roots:map[ET.ElementTree] = map(lambda path : (path, get_root_from_path(path)), files)

    for path, root in roots:
        print_info_from_root(path, root)


"""
service
listener
flow
subflow
interceptor
"""

if __name__ == "__main__":
    main()