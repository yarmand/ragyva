import os
import re



def extract_tags_from_filename(path):
  """ Extract part of the filename within '.' as tag"""
  """ example:"""
  """    filename: 1-Projects.Reliability.summer2024.md"""
  """    tags: ['1-Projects','Reliability','summer2024']"""
  filename = os.path.basename(path)
  name, ext = os.path.splitext(filename)
  if ext == '.md':
    tags = name.split('.')
  else:
    tags = filename.split('.')
  tags = [tag for tag in tags if tag and tag != 'md']
  return tags

def extract_tags_from_text(text):
  """ Extract tags from the text. Tags are any piece of text starting with `#`"""
  tags = re.findall(r'#([\w-]+)', text)
  return tags

def extract_tags_from_headers(path):
  """ Extract tags from markdown file headers"""
  """ Headers are located at the beginning of the file, between lines as ---"""
  """ example:"""
  """ ---"""
  """ abstract: some description"""
  """ tags: #foo #bar"""
  """ ---"""
  tags = []
  with open(path, 'r') as file:
    lines = file.readlines()
    in_header = False
    for line in lines:
      if line.strip() == '---':
        if in_header:
          break
        else:
          in_header = True
      elif in_header:
        match = re.search(r'tags:\s*(.*)', line)
        if match:
          tags += extract_tags_from_text(match.group(1))
  return tags
