import sys
from time import sleep
import xml.etree.ElementTree as ET
from pathlib import Path
from tkinter.filedialog import askdirectory
from colours import Colours

TAB:str = f"{Colours.HEADER}----{Colours.ENDC}"
VERT_LINE:str = f"{Colours.HEADER}|{Colours.ENDC}"
VERT_LINE_WITH_SPACE = VERT_LINE+'\t'

DEPTH:int = 5

def remove_url_in_curly_bracers(s:str):
    url:int = s.find("{http://")

    if url == -1:
        return s

    end_url:int = s.find("}", url)

    return remove_url_in_curly_bracers(s[0:url] + s[end_url+1::])

def printxml(s:str):
    print(remove_url_in_curly_bracers(s))

def get_root_from_path(xml_file:Path) -> ET.Element:
    tree:ET.ElementTree = ET.parse(xml_file)

    root:ET.Element = tree.getroot()

    return root

def get_xml_files_in_directory_as_list_of_files(directory:str) -> list[Path]:
    return list(Path(directory).rglob("*.[xX][mM][lL]"))

def print_children(element:ET.Element, current_depth:int=1):
    for child in element.findall("*"):
        print(VERT_LINE_WITH_SPACE*(current_depth))
        printxml(f"{VERT_LINE_WITH_SPACE*(current_depth-1) + VERT_LINE + TAB} {Colours.BOLD}{child.tag}{Colours.ENDC}")

        for attrib in child.items():
            printxml(f"{VERT_LINE_WITH_SPACE*(current_depth)}{VERT_LINE + TAB} {Colours.OKCYAN}{attrib[0]} : {Colours.OKGREEN}{attrib[1]}{Colours.ENDC}")

        if current_depth != DEPTH:
            print_children(child, current_depth+1)

def print_summary_of_element(path:Path, element:ET.Element):
    print()

    printxml(f"{Colours.BOLD}{element.tag}{Colours.ENDC}\nin {Colours.UNDERLINE}{Colours.OKBLUE}{path}{Colours.ENDC}")

    for attrib in element.items():
            printxml(f"{VERT_LINE + TAB} {Colours.OKCYAN}{attrib[0]} : {Colours.OKGREEN}{attrib[1]}{Colours.ENDC}")

    print_children(element)

def has_tag(tag_desired:str, element:ET.Element):
    return tag_desired.lower() in remove_url_in_curly_bracers(element.tag).lower()

def print_related_tags(roots:map, main_directory:str, looking_for:str):
    print(f"{Colours.BOLD}{looking_for} in {Colours.UNDERLINE}{Colours.OKBLUE}{main_directory}{Colours.ENDC}")

    for file, root in roots:
        for element in root.iter():
            if has_tag(looking_for, element):
                print_summary_of_element(file, element)

def main():
    path:str = askdirectory(title='Select Folder') 

    files:list[Path] = get_xml_files_in_directory_as_list_of_files(path)
       
    roots:map = map(lambda path : (path, get_root_from_path(path)), files)

    if len(sys.argv) > 2:
        global DEPTH
        DEPTH = int(sys.argv[2])
        print_related_tags(roots, path, sys.argv[1])
    elif len(sys.argv) > 1:
        print(f"{Colours.WARNING}HINT: Add a number as a second argument to explore to a certain depth for each matching element.{Colours.ENDC}")
        sleep(2)
        print_related_tags(roots, path, sys.argv[1])
        
    else:
        print(f"{Colours.WARNING}HINT: Add a string as a first argument to make a custom match for elements.{Colours.ENDC}")
        print(f"{Colours.WARNING}HINT: Add a number as a second argument to explore to a certain depth for each matching element.{Colours.ENDC}")
        sleep(2)
        print_related_tags(roots, path, "flow")



    


"""
service
listener
flow
subflow
interceptor
"""

if __name__ == "__main__":
    main()