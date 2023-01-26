import xml.etree.ElementTree as ET
from pathlib import Path
from tkinter.filedialog import askdirectory
from Colours import Colours

TAGS_WITH_DATA:list[str] = ["sub-flow", "flow"]

TAB:str = f"{Colours.HEADER}----{Colours.ENDC}"
VERT_LINE:str = f"{Colours.HEADER}|{Colours.ENDC}"

def printxml(s:str):
    url:int = s.find("{http://www.mulesoft.org/schema/mule")

    if url == -1:
        print(s)
        return

    end_url:int = s.find("}", url)
    print(s[0:url] + s[end_url+1::])

def get_xml_files_in_directory_as_list_of_files(directory:str) -> list[Path]:
    return list(Path(directory).rglob("*.[xX][mM][lL]"))

def print_flow_info_from_root(path:Path, root:ET.Element):
     for element in root.iter():

        if "flow" in element.tag:
            print()

            printxml(f"{Colours.BOLD}{element.tag}{Colours.ENDC}\nin {Colours.UNDERLINE}{Colours.OKBLUE}{path}{Colours.ENDC}")

            for attrib in element.items():
                    printxml(f"{VERT_LINE + TAB} {Colours.OKCYAN}{attrib[0]} : {Colours.OKGREEN}{attrib[1]}{Colours.ENDC}")

            for child in element.findall("*"):
                print(VERT_LINE)
                printxml(f"{VERT_LINE + TAB} {Colours.BOLD}{child.tag}{Colours.ENDC}")
                for attrib in child.items():
                    printxml(f"{VERT_LINE}\t{VERT_LINE + TAB} {Colours.OKCYAN}{attrib[0]} : {Colours.OKGREEN}{attrib[1]}{Colours.ENDC}")

def get_root_from_path(xml_file:Path) -> ET.Element:
    tree:ET.ElementTree = ET.parse(xml_file)

    root:ET.Element = tree.getroot()

    return root

def print_flow_info_from_roots(roots:map, main_directory:str):
    print(f"{Colours.BOLD}Flows in {Colours.UNDERLINE}{Colours.OKBLUE}{main_directory}{Colours.ENDC}")
    for file, root in roots:
        print_flow_info_from_root(file, root)

def main():
    path:str = askdirectory(title='Select Folder') 

    files:list[Path] = get_xml_files_in_directory_as_list_of_files(path)
       
    roots:map = map(lambda path : (path, get_root_from_path(path)), files)

    print_flow_info_from_roots(roots, path)


    


"""
service
listener
flow
subflow
interceptor
"""

if __name__ == "__main__":
    main()