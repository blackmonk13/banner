# Banner

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Banner is a command-line application designed to manage and display beautiful ASCII art and rich-text banners for your terminal. Inspired by the eye-catching banners and ASCII art found in various CLI applications, this tool allows you to easily add, delete, update, search, and export your collection of banners. With the help of the [Prisma ORM](https://www.prisma.io/) for database interactions, the [Prisma Python Client](https://github.com/RobertCraigie/prisma-client-py), and the [Rich library](https://github.com/Textualize/rich) for enhanced console output, Banner brings creativity and fun to your terminal experience.

## Getting Started <a name = "getting_started"></a>

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

You need to have Python 3.7 or later installed on your machine. You can download it from the [official Python website](https://www.python.org/downloads/).

### One-liner Installation and Setup

To install Banner and set it up for shell integration, run the following command:

```bash
curl -sSL https://raw.githubusercontent.com/blackmonk13/banner/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh
```

### Installing

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/blackmonk13/banner.git
   ```

2. Change to the project directory:

   ```bash
   cd banner
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

5. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```
### Setting up Random Banner on Terminal Startup

To display a random banner every time a new terminal is started, follow these steps:

1. Create a shell script named `random_banner.sh` in the project directory with the following content:

   ```bash
   #!/bin/bash
   
   # Activate the virtual environment
   source venv/bin/activate
   
   # Run the banner.py script with the random command
   python banner.py random
   
   # Deactivate the virtual environment
   deactivate
   ```

2. Make the script executable:

   ```bash
   chmod +x random_banner.sh
   ```

3. Open the shell's startup file (e.g., `.bashrc` for Bash or `.zshrc` for Zsh) in a text editor:

   ```bash
   nano ~/.bashrc
   ```
   or
   ```bash
   nano ~/.zshrc
   ```

4. Add the following line at the end of the file to run the `random_banner.sh` script every time a new terminal is started:

   ```bash
   ~/path/to/banner/random_banner.sh
   ```

5. Save and close the file.

6. Reload the shell's configuration:

   ```bash
   source ~/.bashrc
   ```
   or
   ```bash
   source ~/.zshrc
   ```

Now, every time a new terminal is started, the `random_banner.sh` script will run, activating the virtual environment, displaying a random banner, and then deactivating the virtual environment.

## Usage <a name = "usage"></a>

To use Banner, run the following command:

```bash
python banner.py [command] [options]
```

Here are some examples of available commands:

- Add a new banner:

  ```bash
  python banner.py add "Hello, World!"
  ```

- List all banners:

  ```bash
  python banner.py list --page 1 --page_size 10
  ```

- Display a random banner:

  ```bash
  python banner.py random
  ```

- Update a banner:

  ```bash
  python banner.py update 1 --editor nano
  ```

- Search for banners containing a keyword:

  ```bash
  python banner.py search keyword
  ```

- Import a banner from a file:

  ```bash
  python banner.py add /path/to/banner.txt
  ```

- Import a banner from a URL:

  ```bash
  python banner.py add http://example.com/banner.txt
  ```

- Export banners to a single file:

  ```bash
  python banner.py export --single-file --separator "\n===\n" output.txt
  ```

- Export banners to multiple files:

  ```bash
  python banner.py export --base-name "my_banner" --extension "md"
  ```

- Reset the markup of a banner:

  ```bash
  python banner.py reset 1
  ```

For more information on available commands and options, run:

```bash
python banner.py --help
```

With Banner, you can easily manage and enjoy your collection of ASCII  art and rich-text banners, making your terminal experience more  enjoyable and creative.
