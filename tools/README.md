# Tools

- `validate_course.py`: validates every JSON file in the repo,
  the fixture cross references (tasks against documents and
  facts), and the capstone gates file. Run from anywhere:
  `python3 tools/validate_course.py`.
- `check_links.py`: checks that relative links in Markdown files
  resolve on disk. External URLs are not fetched.
