import re

def find_sections(content, start_pattern, end_pattern):
    """
    Splits a file into sections, given a start/end line pattern.
    Any content found between end/start patterns is discarded.
    Any un-terminated section is discarded.

    :param str content: The string to process
    :param re start_pattern: A compiled regex pattern to match the first line of a section
    :param re end_pattern: A compiled regex pattern to match the last line of a section
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


def simple_pattern_to_regex(simple_pattern):
    """
    Convers a "simple pattern" (where "*" represents a multi-char wildcard)
    into a standard regex pattern.

    :param str simple_pattern: The simple pattern to convert
    """

    # Split on simple wildcards
    constant_segements = simple_pattern.split('*')
    # Regex escape each segment
    constant_segements = map(lambda segment:re.escape(segment), constant_segements)
    # Join segments with regex wildcards
    return re.compile('.*'.join(constant_segements))
