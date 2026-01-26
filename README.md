# Magnetic Field Simulator
introduction video
    [한국어] https://youtu.be/XghdGBYB3hE (English Subtitle is ready)
This simulates intensity and dirction of magnetic field of each location via Finite Element Method.
You must install CUDA for your hardware before executing this program.
You may use it for educational/research purposes without asking me!

CUDA version 13.1, CUpy 13.6.0, numpy 2.4.0 was used.
Since I haven't tested it in a virtual environment for users without a graphics card or with CPU built-in graphic card, I can't guarantee proper program execution without NVIDIA grapyic card.
"run.bat" file will automatically construct virtual python environment for you and intall necessary requirements. You can check the requirements.txt for module names and versions.

==========How to run this program==========
1. Run the "run.bat" file.
2. Access the local server page using your default web browser. (If the page doesn't appear, enter 127.0.0.1:5000 in the URL.) The initial screen is "simulation settings". Please be careful not to enter blank or non-numeric values in each numeric input box. 
    2-1. In Step 0, user can define the simulation space size and specify the Mesh Dense variable, which specifies the density of the simulated points. For example, if Mesh Dense is 10, the width/length/height are divided into 10 points with equal distances between neighboring points (including vertices).
    2-2. In Step 1, user enters electric current informations that determine the current shape (type), intensity (in Ampheres), and detailed current location(3D vectors). Here, Vector Dense is a variable that determines the number of vectors to represent corresponding current. Higher Vector Dense values ​​linearly increase the time complexity. Once you've entered the desired current configuration values, click the Request button to register them in the request list.
    2-3. You can cancel any current data items registered in the request list by clicking the X button to the right of each item. Once you've requested all the desired current data, you can start the simulation by clicking the "Start Simulation" button at the bottom. At this point, app.py starts GPU computation using CuPy.
3. Clicking the "Start Simulation" button causes app.py to start computation using the external graphics card. Once the calculation is complete, numerous vectors representing the magnetic field will be displayed simultaneously. Click the "Download this data as .csv file" button to download it as a .csv file, or the "Go back to simulation settings" button to start a new simulation. If too many vectors overlap and are not visible at this stage, the Mesh Dense variable set in step 0 is too high.
4. To turn off, please press "Simulation turn off" button. It will turn of your python file correctly, while the web browser based GUI sometimes does not close by itself. You may close it manually. But be careful, closing GUI without pressing "Simulation turn off" button might leave background process of my python code alive.

==========!Any help is welcome!==========
My main occupation is not a software developer. This program was developed out of academic curiosity while studying magnetic fields, and any help or feedback is welcome.
The following are the issues I currently have unresolved:
1. Instead of visualizing the magnetic field vectors at each point, visualize the magnetic field lines by connecting them with lines.
2. How to package this into a single .exe file (pyinstaller and pywebviewer, which I tried, failed to recognize the CUDA DLL file and resulted in errors.)
3. How to reduce vector overlap by specifying the region that Three.js visualizes.
4. Make this into an online server so that children and students can access the site and use it even on low-spec hardware.(Server provides GPU computation)
5. Simulation settings page can turn of by itself, but magnetic field visualization page does not, even I used the same function, window.close().