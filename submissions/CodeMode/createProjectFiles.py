from datetime import datetime
import os
def createProjectFiles():
    projectTitle = input("What is the title of your project: ")
    os.mkdir(projectTitle)
    os.chdir(projectTitle)
    os.system("git init")
    name = input("What is your full name for the license (exit to not add a license): ")
    year = datetime.now().year
    if name.lower() != "exit":
        with open("LICENSE", "w") as file:
            file.write(f"""MIT License

Copyright (c) {year} {name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
    with open("README.md", "w") as file:
        file.write(f"# {projectTitle}")
    print("What type of project are you working on?")
    print("1. Web Project")
    print("2. Python project")
    print("3. Other")
    while True:
        projectType = input("Choose an option (exit to not add project files): ").lower()
        if projectType == "1":
            with open("index.html", "w") as file:
                file.write("""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title></title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <script src="script.js"></script>
    </body>
</html>
    """)
            open("styles.css", "w").close()
            open("script.js", "w").close()
            break
        elif projectType == "2":
            with open("main.py", "w") as file:
                file.write("""def main():
    pass

if __name__ == "__main__":
    main()
""")
            break
        elif projectType == "3":
            open("project-file", "w").close()
            break
        elif projectType == "exit":
            break
        else:
            print("Invalid input.")
    os.system("git add .")
    os.system("git commit -m 'Added starter files'")
    os.system("open -a 'Visual Studio Code' .")

if __name__ == "__main__":
    createProjectFiles()
