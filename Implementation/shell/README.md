# HECS: An Intelligent Extract Class Refactoring Tool

## Overview

Welcome to the README guide for the HECS shell tool. This guide will walk you through the process of using the tool for individual refactoring predictions.

## Using the Out-of-the-Box Tool

Our package includes a pre-built command-line executable that you can use out of the box to perform refactoring predictions. This tool is designed for ease of use and allows you to test individual class for refactoring. Here's a step-by-step example:

1.**Download the Tool**: Download our HECS executable program:  ` HECS.exe`.

2.**Execute Refactoring Prediction**: Run the executable program in the command line, open  `cmd ` and execute the following commands::

```bash
C:\Users\rain_n\Desktop\HECS\Implementation\shell>HECS.exe "D:\HECS\Implementation\shell\sample\IDDatatypeValidator.java"
    id                  filename                   class_name-entity_name  ...  entity-start  entity-end     tag
0    0  IDDatatypeValidator.java           IDDatatypeValidator-fNullValue  ...            80          80   field
1    1  IDDatatypeValidator.java     IDDatatypeValidator-fMessageProvider  ...            81          81   field
2    2  IDDatatypeValidator.java           IDDatatypeValidator-fTableOfId  ...            82          82   field
3    3  IDDatatypeValidator.java              IDDatatypeValidator-fLocale  ...            83          83   field
4    4  IDDatatypeValidator.java       IDDatatypeValidator-fFacetsDefined  ...            86          86   field
5    5  IDDatatypeValidator.java              IDDatatypeValidator-fLength  ...            87          87   field
6    6  IDDatatypeValidator.java         IDDatatypeValidator-fEnumeration  ...            88          88   field
7    7  IDDatatypeValidator.java          IDDatatypeValidator-IDREF_STORE  ...            90          90   field
8    8  IDDatatypeValidator.java             IDDatatypeValidator-ID_CLEAR  ...            91          91   field
9    9  IDDatatypeValidator.java  IDDatatypeValidator-IDDatatypeValidator  ...            95          97  method
10  10  IDDatatypeValidator.java             IDDatatypeValidator-validate  ...           114         165  method
11  11  IDDatatypeValidator.java                IDDatatypeValidator-clone  ...           171         173  method
12  12  IDDatatypeValidator.java                IDDatatypeValidator-addId  ...           177         197  method
13  13  IDDatatypeValidator.java            IDDatatypeValidator-setLocale  ...           203         205  method
14  14  IDDatatypeValidator.java       IDDatatypeValidator-getErrorString  ...           208         214  method

[15 rows x 8 columns]
----------------------------------------------------------------------------
Start To Load Pretrain Model ... ...
Finish Loading Pretrain Model ! !
----------------------------------------------------------------------------
Subprocess finished successfully
Subprocess completed, continuing main program execution.
----------------------------------------------------------------------------
The following code entities are recommended to be extracted into a new class:
    id                  filename              class_name-entity_name  class-start  class-end  entity-start  entity-end     tag
3    3  IDDatatypeValidator.java         IDDatatypeValidator-fLocale           77        215            83          83   field
4    4  IDDatatypeValidator.java  IDDatatypeValidator-fFacetsDefined           77        215            86          86   field
5    5  IDDatatypeValidator.java         IDDatatypeValidator-fLength           77        215            87          87   field
13  13  IDDatatypeValidator.java       IDDatatypeValidator-setLocale           77        215           203         205  method
```

Replace `D:\HECS\Implementation\shell\sample\IDDatatypeValidator.java` with the desired class path.

**Note:** If no Java source file to be detected is specified, the program will terminate with an error:

```bash
C:\Users\rain_n\Desktop\HECS\Implementation\shell>HECS.exe
usage: HECS.exe [-h] file_path
HECS.exe: error: the following arguments are required: file_path
```

3.**batch processing**: Our executable program supports batch processing of Python scripts. You can detect many source files at once and save the results to disk. To do this, follow these steps:

```python
import os
import subprocess

def batch_detect(input_folder, output_folder):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith('.java'):  # Check if the file is a Java source file
            file_path = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            
            # Run the HECS.exe command
            command = ["HECS.exe", file_path]
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                # Save the result to the output file
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error processing file {file_path}: {e}")
                with open(output_file, 'w') as f:
                    f.write(f"Error processing file {file_path}: {e}\n")
                    f.write(e.stdout)
                    f.write(e.stderr)

if __name__ == "__main__":
    input_folder = "/path/to/source/files"  # Replace with your source files directory
    output_folder = "/path/to/save/results"  # Replace with your results directory
    batch_detect(input_folder, output_folder)
```

1. **Prepare Directories**:

   - Place all your Java source files in the directory specified by `input_folder`.
   - Ensure the directory specified by `output_folder` exists or will be created by the script.

2. **Running the Script**:

   - Save the above script to a file, for example `batch_detect.py`.

   - Open the command line ( `cmd `).

   - Navigate to the directory where `batch_detect.py` is saved.

   - Run the script using the command:

     ```bash
     python batch_detect.py
     ```

Make sure to replace `/path/to/source/files` and `/path/to/save/results` with the actual paths to your directories. This script will process each `.java` file in the input folder, run the `HECS.exe` command on it, and save the output to a `.txt` file in the output folder.

