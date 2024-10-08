# By Abdul https://github.com/AbdulGoodLooks

import time
import sys
import re

def text_script(line:str) -> str:
    """
    Wraps text portion in speech marks and adds a new line character
    Returns a string in the format.
    `"Text goes here\\n"`
    """
    text = line.strip()

    # Fix bug with empty strings.
    if text == "":
        text = ""
    # Check if the line already has speech marks wrapping the string.
    elif text[0] == '"':
        # Check if the line has speech marks used as text, and replace them with opening and closing unicode speech marks.
        text = text.strip()
        text = speech_marks_handling(text)
        text =  "\"" + text + "\"" + "\n"
    else:
        # Check if the line has speech marks used as text, and replace them with opening and closing unicode speech marks.
        if '"' in text:
            text = text.strip()
            text = speech_marks_handling(text)
        # Wrap in speechmarks and add a new line character
            text =  "\"" + text + "\"" + "\n"
        else:
            text = text.strip()
            text =  "\"" + text + "\"" + "\n"
    return text

def defined_character_script(line:str, character:str, character_tag:str) -> str:
    """
    Returns a string in the format
    `character "text"`
    """
    split_line = line.split()
    # Process speaker.
    split_line.pop(0)
    speaker = character_tag

    # Process text.
    text = text_script(split_line)

    # Concatenate and format the speaker and the text.
    line = speaker + " " + text
    return line

def undefined_character_script(line:str) -> str:
    """
    Returns a string in the format
    `"Character" "Text"`
    """
    # Find out who the speaker is.
    split_line = line.split(":")
    speaker, spoken_line = split_line[0], split_line[1]

    # Process speaker.
    speaker = "\"" + speaker + "\""

    # Process text.

    # Attempt to fix bug with colons in text
    speaker_length = len(split_line[0].split(" "))
    if speaker_length >= 4:
        # This is narration - the colon stays.
        return text_script(line)
    else:
        spoken_line = text_script(spoken_line)
        return speaker + " " + spoken_line

def asterisks_to_italics(line:str) -> str:
    # Convert asterisks into RenPy style text tags
    asterisk_count = 0
    output_line = ''
    escape_next_char = False
    for char in line:
        if char == "\\":
            escape_next_char = True
        
        elif char == "*":
            if escape_next_char == False:
                asterisk_count += 1
                if asterisk_count % 2 == 0:
                    output_line += "{/i}"
                else:
                    output_line += "{i}"
            else:
                escape_next_char = False
                output_line += char
        else:
            output_line += char
    
    return output_line



def markdown_to_renpy(line:str) -> str:
    # Replace characters their unicode equivalents
    line = line.replace("'", "’")
    line = line.replace("--", "–")
    
    # Transform italic text into the correct format.
    line = asterisks_to_italics(line)

    return line

def speech_marks_handling(line:str) -> str:
    text = ""
    open_quote = True  # Track whether to insert an opening or closing quote
    
    for character in line:
        if character == '"':
            if open_quote:
                text += '“' # “
            else:
                text += '”' # ”
            open_quote = not open_quote  # Toggle between opening and closing
        else:
            text += character
    return text




try:
    file_path = sys.argv[1]
except IndexError:
    print("No file dropped. Drag and drop a text file onto the program to convert.")
    input("Press Enter to close the program.")
    sys.exit(0)

output_filename = file_path.split("/")[-1]
output_filename = output_filename.replace(".txt", ".rpy")
with open(file_path,'r', encoding='utf-8-sig') as file:
    file = file.read()
file = file.split("\n")
start_time = time.time()


all_characters = {}
# Get the characters from the characters.rpy file.
try:
    with open("characters.rpy", 'r') as character_file:
        characters_file = character_file.read()
except:
    try:
        with open("characters.rpy", 'r') as character_file:
            characters_file = character_file.read()
    except:
        print("No characters.rpy file found. No problem, we'll just put every speaker as a string.")
        characters_file = ""

characters_file = characters_file.split("\n")



# Parse the characters file
all_characters = {}
for line in characters_file:
    line = line.replace(" ", "")
    if line.strip().startswith('define'):
        if 'Character("' in line:
            # Grab the variable name of the character
            line = line.replace("define", "")
            index = line.find('=')
            character_variable = line[:index]

            # Grab the full name of the character
            character_full_name = line[index + 12:]
            index = character_full_name.find('"')
            character_full_name = character_full_name[:index]

            all_characters[character_variable] = character_full_name







# Process the input file and write to the output text file.
with open(output_filename, "w", encoding = "utf-8-sig") as output_file:
    for line in file:
        line_processed = False

        # If the line is blank, just insert a blank line to maintain the paragraph spacing.
        if line == '':
            output_file.write('\n')

        # Comments are marked with %%, so convert them into Python comments.
        elif line.strip().startswith('%%'):
            line = '# ' + line + '\n'
            output_file.write(line)

        # Lines beginning with a '#' are labels
        elif line[0] == "#":
            line = line.removeprefix("#")
            line = line.removeprefix("#")
            line = line.removeprefix(" ")
            line = line.removesuffix("\n")
            line = line.replace(" ", "_")
            line = line.replace(".", "")
            line = " " + line
            line = line.lower()
            line = "label" + line.removeprefix("#").removesuffix("\n") + ":"
        
        # This keyword is used to create a choice menu
        elif '**(Choice)**' in line:
            line = "    menu:\n"
        
        # For choices, anything matching the pattern `**number` is a choice 
        elif bool(re.match(r'^\*\*\d+', line)): # I'm not even going to begin to pretend to know what black magic this is. 
            line = '        "' + line + '":\n'

        elif '---' in line:
            line = "    scene clear\n"

        else:
            # Convert all markdown syntax into RenPy
            line = markdown_to_renpy(line)

            # Check if the speaker is a defined character.
            for character in all_characters:
                if character in line:
                    line = defined_character_script(line, character, all_characters[character])
                    line_processed = True

            if line_processed == False:
                # Check if the speaker is an undefined character
                if ":" in line:
                    line = undefined_character_script(line)
                # Check if the line is an empty line
                elif line == "":
                    pass
                # The speaker is the narrator.
                else:
                    line = line.strip(" ")
                    line = speech_marks_handling(line)
                    line = "\"" + line + "\"" + "\n"
            
            # Indent lines to 4 spaces
            line = "    " + line
        
        # Write line to file.
        output_file.write(line)

end_time = time.time()
time_elapsed = end_time - start_time

print(f"Conversion complete. Saved as {output_filename}")
print(f"Completed in {time_elapsed} s.")
input("Press Enter to close the program.")