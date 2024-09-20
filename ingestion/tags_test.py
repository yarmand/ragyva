#!/usr/bin/env python3

import unittest
from tags import extract_tags_from_filename, extract_tags_from_text

class TestExtractTagsFromFilename(unittest.TestCase):
  def test_extract_tags(self):
    path = "1-Projects.Reliability.summer2024.md"
    expected_tags = ["1-Projects", "Reliability", "summer2024"]
    self.assertEqual(extract_tags_from_filename(path), expected_tags)

  def test_extract_tags_no_extension(self):
    path = "1-Projects.Reliability.summer2024"
    expected_tags = ["1-Projects", "Reliability", "summer2024"]
    self.assertEqual(extract_tags_from_filename(path), expected_tags)

  def test_extract_tags_single_tag(self):
    path = "Projects.md"
    expected_tags = ["Projects"]
    self.assertEqual(extract_tags_from_filename(path), expected_tags)

  def test_extract_tags_empty_string(self):
    path = ""
    expected_tags = []
    self.assertEqual(extract_tags_from_filename(path), expected_tags)

  def test_extract_tags_no_tags(self):
    path = ".md"
    expected_tags = []
    self.assertEqual(extract_tags_from_filename(path), expected_tags)

  def test_extract_tags_from_text(self):
    text = "This is a sample text with #tag1 and #tag2."
    expected_tags = ["tag1", "tag2"]
    self.assertEqual(extract_tags_from_text(text), expected_tags)

  def test_extract_tags_from_text_no_tags(self):
    text = "This is a sample text with no tags."
    expected_tags = []
    self.assertEqual(extract_tags_from_text(text), expected_tags)

  def test_extract_tags_from_text_special_characters(self):
    text = "This is a sample text with #tag1, #tag-2, and #tag_3."
    expected_tags = ["tag1", "tag-2", "tag_3"]
    self.assertEqual(extract_tags_from_text(text), expected_tags)

  def test_extract_tags_from_text_empty_string(self):
    text = ""
    expected_tags = []
    self.assertEqual(extract_tags_from_text(text), expected_tags)

if __name__ == '__main__':
  unittest.main()