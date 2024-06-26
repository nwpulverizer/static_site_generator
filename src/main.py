import os
import shutil
import argparse
from pathlib import Path
from generatepage import generate_pages_recursive


def copy_dir_r(src: Path, dest: Path):
    paths = [x for x in src.iterdir() if x.is_dir()]
    files = [x for x in src.iterdir() if not x.is_dir()]
    for file in files:
        shutil.copy(file, dest)
        print(f"copied {file}")
    if len(paths) == 0:
        return
    for path in paths:
        print(f"moving to {dest / path.parts[-1]}")
        os.mkdir(dest / path.parts[-1])
        copy_dir_r(path, dest / path.parts[-1])


def main():
    parser = argparse.ArgumentParser(
        prog="Static site generator",
        description="Generate static site from content",
        epilog="Not meant for prod. This is a learning project.",
    )
    parser.add_argument(
        "ssg_path",
        help="The path to your static site. Expects the folder to contain static/ and content/",
    )
    args = parser.parse_args()
    ssg_path = Path(args.ssg_path)
    static_path = ssg_path / "static/"
    public_path = ssg_path / "public/"
    if public_path.exists():
        shutil.rmtree(public_path)
        print("removing old public")
    os.mkdir(ssg_path / "public/")
    copy_dir_r(static_path, public_path)
    content_path = ssg_path / "content/"
    public_index = public_path / "index.html"
    print(f"before generate_pages_recursive, {content_path}, {ssg_path} ,{public_path}")
    generate_pages_recursive(content_path, ssg_path / "template.html", public_path)


if __name__ == "__main__":
    main()
