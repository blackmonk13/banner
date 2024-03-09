# Banner

## Table of Contents

- [About](#about)
- [Installation](#installation)
  - [Regular Users](#regular-users)
  - [Setting up a Random Banner on Terminal Startup](#terminal-startup)
- [Usage](#usage)
- [Contributing](#contributing)

## About <a name = "about"></a>

Banner is a command-line application designed to manage and display beautiful ASCII art and rich-text banners for your terminal. Inspired by the eye-catching banners and ASCII art found in various CLI applications, this tool allows you to easily add, delete, edit, show, and export your collection of banners.

## Installation <a name = "installation"></a>

### Regular Users <a name="regular-users"></a>

For regular users, install Banner using `pip` directly from GitHub:

```bash
pip install git+https://github.com/blackmonk13/banner.git
```

This command will install Banner and its dependencies, allowing you to run the `banner` command directly from your terminal without any hassle.

#### Setting up a Random Banner on Terminal Startup <a name="terminal-startup"></a>

To set up a random banner to display every time you open a new terminal on Unix-based systems (such as Linux or macOS), follow these steps:

1. Open your preferred text editor.
2. Create a new file named `.bashrc` in your home directory if it doesn't already exist. If you're using macOS with the default zsh shell, create or edit the `.zshrc` file instead.
3. Add the following line at the end of the file:

   ```bash
   banner show random
   ```

4. Save the file and close the text editor.
5. To apply the changes, run the following command in your terminal:

   ```bash
   source ~/.bashrc
   ```

   Or, if you're using macOS with the default zsh shell:

   ```bash
   source ~/.zshrc
   ```

Now, every time you open a new terminal window or tab, a random banner will be displayed. Enjoy!

For developers or those who want to contribute to the project, follow the instructions in the [Contributing](#contributing) section.

## Usage <a name = "usage"></a>

To use Banner, run the following command:

```bash
banner [command] [options]
```

Here are some examples of available commands:

- Add a new banner:

  ```bash
  banner add "Hello, World!"
  ```

  You can also add banners from files or URLs:

  ```bash
  banner add /path/to/banner.txt
  banner add http://example.com/banner.txt
  ```

  To generate ASCII art from the input text, use the `--ascii` flag:

  ```bash
  banner add "Hello, World!" --ascii
  ```

  You can choose a specific font for ASCII art using the `--font` option:

  ```bash
  banner add "Hello, World!" --ascii --font "standard"
  ```

  To print the generated ASCII text to the console instead of adding it as a banner, use the `--dry-run` flag:

  ```bash
  banner add "Hello, World!" --ascii --dry-run
  ```

- Delete a banner:

  ```bash
  banner delete 1
  ```

- Edit a banner:

  ```bash
  banner edit 1
  ```

- Reset the markup of a banner:

  ```bash
  banner reset 1
  ```

- Show a banner:

  ```bash
  banner show 1
  ```

  To show a random banner:

  ```bash
  banner show random
  ```

  To print the content of the banner rather than the markup, use the `--content-only` flag:

  ```bash
  banner show 1 --content-only
  ```

- Export banners to a file or multiple files:

  ```bash
  banner export --single-file output.txt
  ```

  This will export all banners to a single file named `output.txt`. You can also specify a separator between banners:

  ```bash
  banner export --single-file --separator "\n===\n" output.txt
  ```

  To export banners to multiple files, use the `--base-name` and `--extension` options:

  ```bash
  banner export --base-name "my_banner" --extension "md"
  ```

  This will create files with names like `my_banner_1.md`, `my_banner_2.md`, etc.

For more information on available commands and options, run:

```bash
banner --help
```

With Banner, you can easily manage and enjoy your collection of ASCII art and rich-text banners, making your terminal experience more enjoyable and creative.

## Contributing <a name="contributing"></a>

We welcome contributions from the community! If you'd like to contribute to Banner, please follow these steps:

1. Fork the repository and create a new branch for your changes.
4. Commit your changes and push them to your fork.
5. Open a pull request against the main branch of the original repository.

Please make sure that your contributions adhere to the project's coding style and guidelines.

Before submitting a pull request, please make sure that:

1. Your changes do not introduce any new bugs or regressions.
4. Your code is well-documented and easy to understand.

We appreciate your help in making Banner even better!