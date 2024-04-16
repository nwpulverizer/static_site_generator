import os
import re
from pathlib import Path

from block_to_html import markdown_to_htmlnodes


def extract_title(markdown: str) -> str:
    restring = r"#\s.+\n"
    title = re.search(restring, markdown)
    if title is None:
        raise SyntaxError("All md files need a level 1 heading.")
    return title.group(0)


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"generating path from: {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        content = f.read()
    title = extract_title(content)
    with open(template_path) as f:
        template = f.read()
    filled = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", markdown_to_htmlnodes(content).to_html()
    )
    renamed = dest_path.with_suffix(".html")
    with open(renamed, "w") as f:
        f.write(filled)
    
def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path):
    directories = [x for x in dir_path_content.iterdir() if x.is_dir()]
    files = [x for x in dir_path_content.iterdir() if not x.is_dir()]
    print(files)
    for file in files:
        if file.suffix == ".md":
            print(dest_dir_path / file)
            generate_page(file, template_path, dest_dir_path / file.name)
        else:
            print(f"File {file} is not md. Not generating page.")
    for dir in directories:
        dest_dir_path = dest_dir_path / dir.parts[-1]
        # if dir exists, remove it
        if dest_dir_path.exists():
            print("destination dir exists, removing")
            os.rmdir(dest_dir_path)
        os.makedirs(dest_dir_path)
        print(f"recursive call to {dir} with dest_dir_path = {dest_dir_path}")
        generate_pages_recursive(dir, template_path, dest_dir_path)


    

