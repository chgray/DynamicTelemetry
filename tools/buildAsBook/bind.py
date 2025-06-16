#!/usr/bin/env python3

import os
import shutil
import datetime
import uuid
from pathlib import Path

def ensure_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def remove_if_exists(path):
    """Remove file if it exists."""
    if os.path.exists(path):
        os.remove(path)

def create_title_file(bound_docs_path):
    """Create title.txt with metadata."""
    title_path = os.path.join(bound_docs_path, 'title.txt')
    remove_if_exists(title_path)

    current_date = datetime.datetime.now()
    with open(title_path, 'w') as f:
        f.write('---\n')
        f.write(f'title: Dynamic Telemetry {current_date}\n')
        f.write('author: Chris Gray at.al\n')
        f.write(f'date: {current_date}\n')
        f.write('---\n')

def copy_doc_files(source_dir, dest_dir):
    """Copy all documentation files to bound_docs."""
    print("\nCopying all doc files into /data/docs/bound_docs, for processing\n")
    for item in os.listdir(source_dir):
        source = os.path.join(source_dir, item)
        destination = os.path.join(dest_dir, item)

        if os.path.isdir(source):
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    print("Copy Complete")

def process_markdown_files(docs_dir, bound_docs_dir, mkdocs_content):
    """Process markdown files based on navigation markers."""
    in_nav = False
    bind_files = []

    for line in mkdocs_content:
        line = line.strip()

        if line == "#<START_BINDING>":
            print("Found NAV")
            in_nav = True
            continue
        elif line == "#<END_BINDING>":
            print("End NAV")
            in_nav = False
            continue

        if not in_nav:
            continue

        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue

        # Calculate indentation level
        separator_index = line.find('-')
        if separator_index > 4:
            tab_level = (separator_index - 4) // 4 if separator_index % 4 == 0 else 0
            os.environ['CDOCS_TAB'] = str(tab_level)
        os.environ['CDOCS_FILTER'] = '1'

        if not line.endswith('.md'):
            # Generate new section
            title = line.replace('-', '').replace(':', '').strip()
            file_id = str(uuid.uuid4())
            print(f"Generating : [{line}]")
            print(f" ==> {title} ==> {file_id}")

            source_file = os.path.join(bound_docs_dir, f"{file_id}.generated.md")
            dest_leaf = f"{file_id}.generated.converted.md"

            with open(source_file, 'w') as f:
                f.write("\\newpage\n")
                f.write(f"# {title}\n")
        else:
            # Process existing markdown file
            file_path = line.split(':')[1].strip()
            file_path = os.path.join(docs_dir, file_path)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File doesn't exist: {file_path}")

            source_file = file_path
            dest_leaf = os.path.basename(file_path)

        # Convert using pandoc
        dest_file = os.path.join(bound_docs_dir, dest_leaf)
        cmd = f'pandoc -i "{source_file}" -o "{dest_file}" --filter CDocsMarkdownCommentRender'
        print(f"Converting {source_file} ==> {dest_leaf}")
        print(f"    {cmd}")

        if os.system(cmd) != 0:
            raise RuntimeError(f"Pandoc conversion failed for {source_file}")

        if not os.path.exists(dest_file):
            raise RuntimeError(f"Output file not created: {dest_file}")

        bind_files.append(dest_leaf)

    # Write bind.files
    with open(os.path.join(bound_docs_dir, 'bind.files'), 'w') as f:
        f.write('\n'.join(bind_files))

def main():
    print("Binding Docs.............")

    # Set error handling to stop on errors
    os.environ['PYTHONUNBUFFERED'] = '1'

    # Change to docs directory
    os.chdir('/data/docs/docs')

    # Set up DB directory
    db_dir = os.path.abspath(os.path.join('..', 'orig_media'))
    os.environ['CDOCS_DB'] = db_dir

    # Read mkdocs.yml
    with open('../../mkdocs.yml', 'r') as f:
        mkdocs_content = f.readlines()

    # Set up bound_docs directory
    bound_docs_dir = '/data/docs/bound_docs'
    ensure_directory(bound_docs_dir)

    # Remove existing files
    remove_if_exists(os.path.join(bound_docs_dir, 'bind.files'))

    # Create title file
    create_title_file(bound_docs_dir)

    # Copy documentation files
    copy_doc_files('.', bound_docs_dir)

    try:
        os.chdir('/data/docs')
        process_markdown_files('/data/docs', bound_docs_dir, mkdocs_content)
    finally:
        os.chdir('/data/docs')

if __name__ == '__main__':
    main()
