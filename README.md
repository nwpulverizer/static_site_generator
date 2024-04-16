# A simple static site generator

This is a static site generator that will take in Markdown documents in the content folder, and output them
to the public folder. It will also copy your static folder into public which may contain images and styling. This is a learning project and not suitable for production use.

# Usage

To generate your site and also spin up a local version of it run:

```bash
main.sh path/to/static_site/
```

Your static site directory should contain a `/static` folder and a `/content` folder.

To generate your site run starting a local server run:

```bash
src/main.py path/to/static_site/
```

# Learning implemented in this project

## Object oriented programming

I definitely applied object oriented principles, specifically to the HTMLNode class. Breaking out a generic HTML node into subclasses of parent and leaf worked out great while also avoiding too many levels of abstraction.

## Functional programming

I tried to do some of my string formatting in a functional manner. I also used recursion to copy the contents of the static and content directories. While not strictly functional, it seems to be taught alongside it.

# My favorite parts of the project

## Enums

I used python's enums to give great type hints to my code. If I am not mistaken, they don't enforce anything in python, but at the very least I think enums were a clean way to set up my different text node types - bold, italic, normal text, code etc. as well as my HTML node types.

## Switch statements

I liked using the switch statements in python. I first started using these when I learned bash years ago and it did not make sense why it was useful. Last year, I messed around a bit with Rust and it clicked for me.
