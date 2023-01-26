# XML SCANNER

A Python app that searches for xml files in a directory and matches any tags with a given term, then prints the results to the terminal or as an html file.

## Requirements

    Python 3.x
    xml.etree.ElementTree
    pathlib
    tkinter.filedialog

## Usage

###     Run the script in the command line: 
        python explore.py [term] [depth] [options]
###     Argument Explanation
    term: a string to match against xml element tags
    depth: an integer to specify how many levels deep to search for matching elements. Inputting 0 will make it go infinitely deep. (optional)
    options: a list of commands to modify the output (optional)

## Arguments

    Add a string as the first argument to make a custom match for elements.
    Add a number as the second argument to explore to a certain depth for each matching element.

## Options

    --tabs-only or -to: Replaces the default printout to use tabs instead of dashes.
    --as-html or -ah: Outputs an html table instead of printout.
    --help: Prints a list of commands

## Example

    (.venv) python explore.py tagname 2 -ah

This will search for xml files in the current directory, match any elements with the tag 'tagname' and its children up to 2 levels deep, and output the results as an html table.

## Note

Make sure to activate your virtual environment before running the script (.venv in this example)