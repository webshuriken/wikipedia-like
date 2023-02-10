from os.path import exists
from os import linesep
import re


# @description check for header in string
# @params file_line {string} the string to check
# @returns {tuple} of two values {bool, string}
def get_header(file_line):
  header = re.match(r'#{1,6}\s', file_line)
  if header:
    header_level = header.end() - 1
    html_header = f'<h{header_level}>{file_line[header.end():]}</h{header_level}>'
    return (True, html_header)
  else:
    return (False, 'Header not found')

# @description check for list items
# @params all_file_lines {list}
# @returns {tuple} of three values {bool, string, updatedFileLines}
def get_lists(all_file_lines):
  # list of dictionaries, each has the list level and match end location
  list_levels = [{"level": 0, "end": 0, "tabs": -2}]
  current_level = 0
  # will store the list as a combination of html tags and text items
  html_list = []
  # to start a list, the first item must start at 0 spaces or 2 spaces from margin
  match = re.match(r'(^[\s\t]{,4})[\*\+-] ', all_file_lines[0])

  # go further, when rule 2 of unordered lists is matched
  if match and valid_list_marker(match, list_levels, current_level, 'start'):
    html_list.append('<ul>')
    list_levels[0]["end"] = match.end()
    # lets see if they are using tabs or spaces
    list_with_tabs = match.group().count('\t') == 1 if True else False
    list_levels[0]["tabs"] = list_with_tabs if match.group().count('\t') else -2
    # loop will find all items including the nested ones
    while current_level >= 0:
      # at this point we guaranty a valid list item, so lets append to 'html_list'
      html_list.append(f'<li>{all_file_lines[0][match.end():]}')
      # remove the first file line as its a list item
      all_file_lines.pop(0)
      # while there list is not empty, lets check for another list item
      if len(all_file_lines) > 0:
        match = re.match(r'[\s\t]*[\*\+-] ', all_file_lines[0])
      else:
        match = False

      # is current item match same as current list level
      if match and valid_list_marker(match, list_levels, current_level, 'current'):
        html_list[len(html_list) - 1] += '</li>'
      # is current item match a nested list
      elif match and valid_list_marker(match, list_levels, current_level, 'nested'):
        html_list.append('<ul>')
        current_level += 1
        # add a new level to the list
        list_levels.append({"level": current_level, "end": match.end(), "tabs": list_with_tabs if match.group().count("\t") else -2})
      # is current item match a level before the current active list level
      elif match and valid_list_marker(match, list_levels, current_level, 'previous'):
        # appending here is to guarante the closure of currently nested list
        html_list[len(html_list) - 1] += '</li>'
        html_list.append('</ul>')
        # if a list has a single item, the extra closure is not needed
        if current_level > 0:
          html_list.append('</li>')
        current_level -= 1
        # close all open lists until we arrive at a valid list level that matches
        i = current_level
        while i >= 0:
          # level found so lets exit loop
          if match.end() == list_levels[i]["end"]:
            i = -1
          else:
            html_list.append('</ul>')
            html_list.append('</li>')
            current_level -= 1
            i -= 1
      else:
        # as there are not more matches, close all nested lists and list items
        i = current_level
        while i >= 0:
          html_list.append('</li>')
          html_list.append('</ul>')
          i -= 1
        current_level = -1

  # prepares the tuple to be returned
  list_found = (False, 'No list here', all_file_lines)
  if len(html_list) >= 1:
    # filter the text for each item in the list
    for i in range(len(html_list)):
      html_list[i] = text_filter(html_list[i])
    list_found = (True, html_list, all_file_lines)

  return list_found

# @description check the list marker was used properly
# @params match {re_class} to check matched text
# @params list_level {dictionary} so we know what level we are in during the list creation
# @params list_type {string} start | current | previous | nested
# @returns {boolean} True if the marker is valid and Flase if it is not


def valid_list_marker(match, list_levels, current_level, list_type):
  marker_is_valid = False
  matched_tabs = match.group().count('\t')

  # are we creating the first item of a fresh list
  if list_type == 'start':
    if (matched_tabs == 1 or match.end() == 2 or match.end() == 4 or match.end() == 6):
      marker_is_valid = True
  elif list_type == 'current':
    if (list_levels[current_level]["tabs"] == matched_tabs or match.end() == list_levels[current_level]["end"]):
      # current item is part of the previous list
      marker_is_valid = True
  elif list_type == 'nested':
    if ((list_levels[current_level]["tabs"] + 1) == matched_tabs or (list_levels[current_level]["end"] + 2) == match.end() or (list_levels[current_level]["end"] + 4) == match.end()):
      # current item is to be nested as a list within the previous item
      marker_is_valid = True
  elif list_type == 'previous':
    # lets see if current matched space is equal to another match in previous levels
    matched_spaces = False
    for level in range(len(list_levels) - 1):
      if list_levels[level]["end"] == match.end():
        matched_spaces = True
    # first check if the tabs match otherwise check the matched_spaces
    if (list_levels[0]["tabs"] != -1 and matched_tabs < list_levels[current_level]["tabs"]) or matched_spaces:
      marker_is_valid = True

  # numbers.count('\t')
  return marker_is_valid

# @description check for valid paragraphs creating one with html tags
# @params all_file_lines {list}
# @returns {tuple} of three values {bool, string, updatedFileLines}
def get_paragraphs(all_file_lines):
  # use the middle item, item 1, to create the string in the paragraph
  html_p = ['<p>', '', '</p>']
  # lets keep going until we find an empty line
  while all_file_lines[0].strip() != '':
    # catch any run away list items trying to become paragraphs
    if get_lists([all_file_lines[0]])[0]:
      break

    html_p[1] += f'{all_file_lines[0]} '
    all_file_lines.pop(0)

    # exit loop if there are not more items in the list
    if len(all_file_lines) == 0:
      break

  # remove any trailing spaces and join the array items
  html_p[1] = html_p[1].strip()
  html_p = ''.join(html_p)

  # filter the text for boldness or links
  html_p = text_filter(html_p)

  return (True, html_p, all_file_lines)

# @description filter text to find boldness and/or links
# @params text {string}
# @returns {string} the string with a ny link of bold tags


def text_filter(text):
  html_text = get_boldness(text)
  html_text = get_links(html_text)
  return html_text

# @description replace all matches of boldness with its html tags
# @params text {string}
# @returns {string} the string with html tags


def get_boldness(text):
  match = re.finditer(r'[*_]{2}(\w\s?)+\w[*_]{2}', text)
  html_bold = ''
  match_end = 0
  # regex iterator, lets loop
  for item in match:
    html_bold += text[match_end:item.start()]
    html_bold += f'<b>{text[item.start() + 2:item.end() - 2]}</b>'
    match_end = item.end()

  # finalize the bold update
  if match_end > 0:
    html_bold += text[match_end:len(text)]
  else:
    html_bold = text

  return html_bold

# @description replace all matched links with their html tags
# @params text {string}
# @returns {string} the string with html links


def get_links(text):
  match = re.finditer(r'(\[[^\s]+\])(\([^\s]+\))', text)
  html_link = ''
  match_end = 0
  # use the iterator
  for item in match:
    # extract the link text and url
    link_text = item.group(1)[1:len(item.group(1)) - 1]
    link_url = item.group(2)[1:len(item.group(2)) - 1]
    # put it all together
    html_link += text[match_end:item.start()]
    html_link += f'<a href="{link_url}">{link_text}</a>'
    match_end = item.end()

  # finalize the text creation
  if match_end > 0:
    html_link += text[match_end:len(text)]
  else:
    html_link = text

  return html_link


# @description Parser logic taking care of transforming the markdown file to HTML
# @params file {string} the markdown file we are going to convert
# @returns {html_list} the string with html items
def parse_file(file_name):
  # lets catch any errors
  try:
    # to store the entire HTML created from the markdown file
    html_list = []

    # use built-in method to split line so we dont worry about the OS use of EOF
    md_file_lines = file_name.splitlines()

    while len(md_file_lines) > 0:
      # check for empty item in array
      if md_file_lines[0].strip() == '':
        md_file_lines.pop(0)
        continue

      # lets check for header
      header = get_header(md_file_lines[0])
      if header[0]:
        html_list.append(header[1])
        md_file_lines.pop(0)
        continue

      # lets check for lists
      list = get_lists(md_file_lines)
      if list[0]:
        html_list.extend(list[1])
        md_file_lines = list[2]
        continue

      # at this point we can assume, without certainty, the line is a paragraph
      paragraph = get_paragraphs(md_file_lines)
      if (paragraph[0]):
        html_list.append(paragraph[1])
        md_file_lines = paragraph[2]
        continue

    # return the HTML
    return html_list
  except Exception as err:
    print(err.args)
  except:
    print("There was an issue creating the HTML file")
