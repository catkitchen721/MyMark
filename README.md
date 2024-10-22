# MyMark: Markdown Previewer with Custom Syntax

MyMark is a powerful Markdown previewer that supports custom syntax extensions. It allows users to create and use their own syntax rules, making Markdown documents more versatile and expressive.

## Features

- Real-time Markdown preview
- Support for custom syntax extensions
- User-friendly graphical interface
- File drag-and-drop functionality
- Built-in examples of useful custom syntax

## Installation

1. Ensure you have Python 3.7 or higher installed.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/mymark.git
   ```
3. Navigate to the project directory:
   ```
   cd mymark
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the following command to start MyMark:
```
python main.py
```

## Custom Syntax

You can create your own custom syntax by adding Python files to the `mod` directory. Click the `Custom Syntax Tutorial` button in the application for detailed instructions.

## Built-in Custom Syntax Examples

MyMark comes with several built-in custom syntax examples:

- Calculator: `==2+2==`
- Countdown: `!!2023-12-31!!`
- Caesar Cipher: `+*3|Hello+*` (shift by 3)
- Random Color: `$$`
- Random Number: `#100#` (random number between 0 and 100)
- Red Text: `@@Red Text@@`
- Quick Exit: `\q`
- Line Break: `\n`

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Building Standalone Executable

To create a standalone executable that doesn't require Python installation:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Run PyInstaller:
   ```
   pyinstaller --onefile --windowed --add-data "mod;mod" main.py
   ```
3. Find the generated .exe file in the `dist` folder.

## Troubleshooting

If you encounter any issues or have questions, please open an issue on GitHub.
