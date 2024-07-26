## Prerequisites

To run this program, ensure you have the following Python libraries installed:
- `selenium`
- `beautifulsoup4`
- `pandas`
- `FPDF`
- `fdpf2`
- `tk`
- `requests`

### ProfileScraper.exe
ProfileScaper.exe is the built file of the program
Run it if IDEs are not available

### Installation

To install the required libraries, run the following command:

```sh
pip install selenium beautifulsoup4 pandas FPDF tk requests fpdf2
```

Verification
To verify the installation of the libraries, use the following command:

```sh
pip show selenium beautifulsoup4 pandas FPDF tk requests fpdf2
```

GUI User Guide

Running the Program
To start the program, execute the Main.py file:

```sh
python Main.py
```

Available Commands
Type /help within the program to see a list of possible commands.

build exe
pyinstaller --name=ProfileScraper --onefile --windowed --add-binary "C:\Users\keanl\Documents\GitHub\nssecu2_hacktool\edgedriver_win64\msedgedriver.exe;." Main.py

For password masking purposes 
Press control+m

Procedures

```sh
/loginUser [username]
/loginPass [password] (use ctrl+m for masking)
/targetUsername [username]
/scrape
/generateReport
```

### Errors

```sh
UserWarning: You have both PyFPDF & fpdf2 installed. Both packages cannot be installed at the same time as they share the same module namespace. To only keep fpdf2, run: pip uninstall --yes pypdf && pip install --upgrade fpdf2
```

- uninstall and reinstall FPDFm, pip install --upgrade FPDF