# HECS: An Intelligent Refactoring Plugin

## Plugin Overview

![1720263309164](C:\Users\rain_n\AppData\Roaming\Typora\typora-user-images\1720263309164.png)

The HECS Intelligent Refactoring Plugin is an extension for performing intelligent code refactoring in Visual Studio Code. It provides a set of prediction and refactoring tools to help developers improve code quality and readability. Our prototype implementation adopts a two-layer C/S architecture: the client layer for interaction with users and the server layer for refactoring opportunity detection. It is worth noting that in the server layer, we have deployed a large model for automated verification of the legitimacy of refactoring candidates.

## Installation

1. Download the .vsix file from our package.
2. Open Visual Studio Code (VS Code).
3. Go to the Extensions view (Ctrl+Shift+X).
4. Click the menu button (three dots) at the top right of the Extensions view.
5. Select "Install from VSIX."
6. Navigate to and open .vsix extension file using the file browser.

## Usage

A demo video of HECS is available: [HECS-A Hypergraph Learning based System for Detecting Extract Class Refactoring Opportunities (youtube.com)](https://www.youtube.com/watch?v=-Jtss1eKo5U)

1. Open your test project.
2. Open the Java file that you want to refactor in the editor.
3. Click the HECS icon in the bottom-right corner to open the plugin interface.
4. In the plugin interface, select the file and the refactoring operation:
   - Choose the Java source file to refactor.
   - Predict: Click to predict code refactoring.
   - Preview: View a preview of the code refactoring.
   - Refactor: Execute the code refactoring.
5. Follow the prompts to complete the refactoring.

## Plugin Entry Point

You can find the HECS icon in the bottom-right corner of VS Code. Click it to open the plugin interface.

## The Client Layer

![1720099505989](C:\Users\rain_n\AppData\Roaming\Typora\typora-user-images\1720099505989.png)

The client layer serves as a Visual Studio Code (VSCode) extension, which accepts user inputs and communicates with the server layer. Once installing this extension, users can access the client layer with a launch button shown in Fig.1 and Fig.2. The client layer has two different views: detection view and refactoring view, which are illustrated as follows: 1) The Detection View. Fig.1 presents a snapshot of the detection view. First, users should click the file selection button to select a source file for detection. Next, when the user clicks the `detection` button (Button 1) to require detection results, the client layer will send an HTTPS request to the server layer and receive the data package simultaneously. The detection results will further be summarized with a table (Extraction Summary Table), where each row presents names, types, and code line ranges of the field or method to be extracted. The detection results will also be highlighted and displayed with the red colour in the window of the source file. The functionality of the `preview`  button (Button 2) and `refactoring` button (Button 3) will be illustrated in the refactoring view. 2) The Refactoring View. 

![1720099563105](C:\Users\rain_n\AppData\Roaming\Typora\typora-user-images\1720099563105.png)

Fig.2 presents a snapshot of the detection view. When the user clicks the `preview` button (Button 2) in Fig.1, a new window will be created to demonstrate fine-grained code differences between the target class and extracted class, where differences with the green colour represent the extracted added code and differences with the red colour represent the extracted deleted code. We employ a state-of-the-art tool: diff2html, to support the visualization of code differences in an HTML format. The refactoring view assists users in examining each refactoring operation. Users can further click the `refactoring` button (Button 3) in Fig.1 to automatically and accurately execute detected extract class refactoring opportunities. 