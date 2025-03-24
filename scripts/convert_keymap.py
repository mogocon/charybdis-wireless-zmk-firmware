import re
import os
import sys
import argparse

def main():
    #####################################################################
    # Define variables & write output keymap file
    #####################################################################
    
    # Create the parser
    parser = argparse.ArgumentParser(description="A script that converts ZMK keymap files from QWERTY <|> Colemak DH")
    # Define flags and parameters
    parser.add_argument(
        '-c', '--convert', 
        type=str, 
        choices=['q2c', 'c2q'], 
        default='q2c',
        help="Specify the conversion: 'q2c' will convert QWERTY to Colemak DH, 'c2q' will convert Colemak DH to QWERTY (default: 'q2c')"
    )
    parser.add_argument(
        '--in-path',
        type=str,
        required=True,
        help="Path to the input keymap file. This is the path where the output will be stored as well"
    )
    # Parse the arguments
    args = parser.parse_args()
    # Set the variable for the chosen option
    conversion_type = args.convert
    full_path = args.in_path
    
    # Check argument values and convert keymap
    if conversion_type not in ['q2c','c2q']:
        print("Error: Invalid conversion type selected.")
        sys.exit(1)

    path, in_file = os.path.split(full_path)
    out_file = 'qwerty.keymap' if conversion_type == 'c2q' else 'colemak_dh.keymap'
    out_full_path = os.path.join(path, out_file)

    print("#####################################################################")
    print(f"Selected conversion type: {conversion_type}")
    print(f"path:........{path}")
    print(f"input_file:..{in_file}")
    print(f"out_file:....{out_file}")
    print("#####################################################################")

    #####################################################################
    # Define conversions
    #####################################################################
    
    if conversion_type == 'q2c':
        initial_keymap = {
            # Top row (numbers and symbols are not included in this example)
            'Q': 'Q', 'W': 'W', 'E': 'F', 'R': 'P', 'T': 'B', 'Y': 'J', 'U': 'L', 'I': 'U', 'O': 'Y', 'P': 'APOS',
            # Home row
            'A': 'A', 'S': 'R', 'D': 'S', 'F': 'T', 'G': 'G', 'H': 'M', 'J': 'N', 'K': 'E', 'L': 'I', 'SEMICOLON': 'O',
            # Bottom row
            'Z': 'Z', 'X': 'X', 'C': 'C', 'V': 'D', 'B': 'V', 'N': 'K', 'M': 'H', 'COMMA': 'COMMA', 'PERIOD': 'PERIOD', 'SLASH': 'SLASH',
            # For 4th row keys which are usually symbols - keep them the same
            'GRAVE': 'GRAVE', 'MINUS': 'MINUS', 'EQUAL': 'EQUAL', 'LEFT_BRACKET': 'LEFT_BRACKET', 'RIGHT_BRACKET': 'RIGHT_BRACKET', 
            'BACKSLASH': 'BACKSLASH', 'SINGLE_QUOTE': 'SINGLE_QUOTE', 'APOSTROPHE': 'APOSTROPHE',
        }
    else:
        initial_keymap = {
            # Top row (numbers and symbols are not included in this example)
            'Q': 'Q', 'W': 'W', 'F': 'E', 'P': 'R', 'B': 'T', 'J': 'Y', 'L': 'U', 'U': 'I', 'Y': 'O', 'APOS': 'P',
            # Home row
            'A': 'A', 'R': 'S', 'S': 'D', 'T': 'F', 'G': 'G', 'M': 'H', 'N': 'J', 'E': 'K', 'I': 'L', 'O': 'SEMICOLON',
            # Bottom row
            'Z': 'Z', 'X': 'X', 'C': 'C', 'D': 'V', 'V': 'B', 'K': 'N', 'H': 'M', 'COMMA': 'COMMA', 'PERIOD': 'PERIOD', 'SLASH': 'SLASH',
            # For 4th row keys which are usually symbols - keep them the same
            'GRAVE': 'GRAVE', 'MINUS': 'MINUS', 'EQUAL': 'EQUAL', 'LEFT_BRACKET': 'LEFT_BRACKET', 'RIGHT_BRACKET': 'RIGHT_BRACKET', 
            'BACKSLASH': 'BACKSLASH', 'SINGLE_QUOTE': 'SINGLE_QUOTE', 'APOSTROPHE': 'APOSTROPHE',
        }
    
    #####################################################################
    # Read and store input keymap 
    #####################################################################

    # Read the content of the keymap_contents
    with open(full_path, 'r') as keymap_file:
        keymap_contents = keymap_file.read()
    
    #####################################################################
    # Functions
    #####################################################################

    def convert_keymap(keymap_contents):   
        # Define regex pattern to find the 'Base' keymap section
        base_keymap_pattern = re.compile(r'(BASE\s*\{\s*bindings\s*=\s*<\s*)(.*?)(\s*>;)', re.DOTALL)     
        # Apply regex substitution to convert keymap
        new_keymap_contents = base_keymap_pattern.sub(replace_keymap, keymap_contents)
        return new_keymap_contents
    
    # Find and replace the 'BASE' keymap layer
    def replace_keymap(match):
        before_keymap = match.group(1)
        old_keymap = match.group(2)
        after_keymap = match.group(3)
        
        print(f">> Found BASE keymap \n{old_keymap}")

        # Split the old keymap by lines
        lines = old_keymap.strip().split('\n')

        # Process each line
        new_lines = []
        print(">> Converting letter keys")
        for line in lines:
            # Enhanced pattern to capture complex ZMK bindings
            pattern = r'(&[^\s]+\s+[A-Z_]+\s+)?([A-Z_]+)'
            
            # Replace keys in the line based on the mapping
            def replace_key(match):
                behavior = match.group(1) or ""
                key = match.group(2)
                
                if key in initial_keymap:
                    print(f"{key}:{initial_keymap[key]}")
                    return f"{behavior}{initial_keymap[key]}"
                return match.group(0)
            
            # Apply the replacement
            new_line = re.sub(pattern, replace_key, line)
            new_lines.append(new_line)

        # Join new lines to form the new keymap keymap_contents
        new_keymap = '\n'.join(new_lines)
        print(f"\n>> Generated {out_file} \n{format_columns(new_keymap)}")
        return before_keymap + format_columns(new_keymap) + after_keymap
    
    def format_columns(text):    
        # Split the input text into lines
        lines = text.strip().split('\n')
        
        # Format each line to maintain alignment using original spaces
        formatted_lines = []
        for line in lines:
            # Preserve the original formatting but ensure consistent spacing
            # between key bindings
            formatted_line = re.sub(r'\s{2,}', '  ', line)
            formatted_lines.append(formatted_line)
        
        # Join all formatted lines
        formatted_text = '\n'.join(formatted_lines)
        return formatted_text

    converted_map = convert_keymap(keymap_contents)

    # Write the new keymap_contents to the output file
    with open(out_full_path, 'w') as file:
        file.write(converted_map)
    
    print("#####################################################################")
    print(f"Updated keymap written to {out_full_path}")
    print("#####################################################################")
if __name__ == "__main__":
    main()