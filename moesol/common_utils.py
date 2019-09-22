import re

# Splits a file into sections, given a start/end line pattern.
# Any content found between end/start patterns is discarded.
def find_sections(content, start_pattern, end_pattern):
    """
    Splits a file into sections, given a start/end line pattern.
    Any content found between end/start patterns is discarded.
    Any un-terminated section is discarded.

    :param content: The string to process
    :param file out_file: The file to write to (effectively a copy of in_file)
    :param str start_pattern: A regex expression to match the first line of the section
    :param str end_pattern: A regex expression to match the last line of the section
    """
    inside_section = False
    last_line_of_section = False
    sections = []
    for line in content.splitlines():
        # Identify if inside section to replace
        if re.match(start_pattern, line):
            section = []
            inside_section = True
        elif re.match(end_pattern, line):
            section.append(line)
            sections.append('\n'.join(section))
            sectinon = []
            inside_section = False
        if inside_section:
            section.append(line)
    return sections

