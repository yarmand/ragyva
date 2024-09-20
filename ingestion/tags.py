import os
import re



# extract part of the filename within '.' as tag
# example:
#    filename: "1-Projects.Reliability.summer2024.md"
#    tags: ["1-Projects","Reliability","summer2024"]
def extract_tags_from_filename(path):
  filename = os.path.basename(path)
  name, ext = os.path.splitext(filename)
  if ext == '.md':
    tags = name.split('.')
  else:
    tags = filename.split('.')
  tags = [tag for tag in tags if tag and tag != 'md']
  return tags

# extract tags from the text. Tags are any piece of text starting with `#`
def extract_tags_from_text(text):
  tags = re.findall(r'#([\w-]+)', text)
  return tags
