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

def print_children_tabs_only(element:ET.Element, current_depth:int=1):
    TABS = '\t'*(current_depth)
    for child in element.findall("*"):
        printxml(f"{TABS}{Colours.BOLD}{child.tag}{Colours.ENDC}")

        for attrib in child.items():
            printxml(f"{TABS}\t{Colours.OKCYAN}{attrib[0]}:\t{Colours.OKGREEN}{attrib[1]}{Colours.ENDC}")

        if current_depth != DEPTH:
            print_children_tabs_only(child, current_depth+1)

def print_summary_of_element_tabs_only(path:Path, element:ET.Element):
    print()

    printxml(f"{Colours.BOLD}{element.tag}{Colours.ENDC}\nin {Colours.UNDERLINE}{Colours.OKBLUE}{path}{Colours.ENDC}")

    for attrib in element.items():
            printxml(f"\t{Colours.OKCYAN}{attrib[0]}:\t{Colours.OKGREEN}{attrib[1]}{Colours.ENDC}")

    print_children_tabs_only(element)

def print_related_tags_tabs_only(roots:map, main_directory:str, looking_for:str):
    print(f"{Colours.BOLD}{looking_for} in {Colours.UNDERLINE}{Colours.OKBLUE}{main_directory}{Colours.ENDC}")

    for file, root in roots:
        for element in root.iter():
            if has_tag(looking_for, element):
                print_summary_of_element_tabs_only(file, element)

def handle_args() -> list[str]:
    COMMANDS:dict[str, tuple[function, str]] = dict()

    def tabs_only():
        global print_related_tags
        print_related_tags = print_related_tags_tabs_only

    def help():
        print(f"{Colours.FAIL}ARGUMENTS:{Colours.ENDC}")
        print(f"{Colours.WARNING}Add a string as a first argument to make a custom match for elements.{Colours.ENDC}")
        print(f"{Colours.WARNING}Add a number as a second argument to explore to a certain depth for each matching element.{Colours.ENDC}")
        print(f"{Colours.FAIL}LIST OF COMMANDS:{Colours.ENDC}")
        for key in COMMANDS.keys():
            print(f"{Colours.WARNING}{key} : {Colours.OKCYAN}{COMMANDS.get(key)[1]}{Colours.ENDC}")
        exit()

    TABS_ONLY = (tabs_only, "Replaces the default printout to use tabs instead of dashes.")
    HELP = (help, "Prints a list of commands")

    COMMANDS = {
        "--tabs-only": TABS_ONLY,
        "-to": TABS_ONLY,
        "--help": HELP
    }

    args:list[str] = list()

    for i in range(len(sys.argv)-1):
        arg = sys.argv[i]
        if arg in COMMANDS.keys():
            COMMANDS.get(arg)[0]()
        else:
            args += arg

    return args


def main():
    args:list[str] = handle_args()

    path:str = askdirectory(title='Select Folder') 

    files:list[Path] = get_xml_files_in_directory_as_list_of_files(path)
       
    roots:map = map(lambda path : (path, get_root_from_path(path)), files)



    if len(args) > 2:
        global DEPTH
        DEPTH = int(args[2])
        print_related_tags(roots, path, args[1])
    elif len(args) > 1:
        print(f"{Colours.WARNING}HINT: Add a number as a second argument to explore to a certain depth for each matching element.{Colours.ENDC}")
        sleep(2)
        print_related_tags(roots, path, args[1])
        
    else:
        print(f"{Colours.WARNING}HINT: Add a string as a first argument to make a custom match for elements.{Colours.ENDC}")
        print(f"{Colours.WARNING}HINT: Add a number as a second argument to explore to a certain depth for each matching element.{Colours.ENDC}")
        sleep(2)
        print_related_tags(roots, path, "flow")


if __name__ == "__main__":
    main()