# Fbx-World-Rescaler
A utility that resizes scenes in FBX files without damaging skeletal animations.  Useful in correcting end of workflow scale issues- You 
finished your animation, but accidentally converted it from, say, inches to centimeters a few weeks ago. This allows you to keep your 
baked animations, or to resize a rigged mesh, without the weirdness that happens from directly scaling elements in scene. 

#FBX SDK for Python 2015.1 
download here: http://images.autodesk.com/adsk/files/fbx20151_fbxpythonsdk_win.exe

# FBX SDK for Python setup: 
-Taken from Autodesk Web site-

To install Python FBX:
Follow the instructions of Installing FBX SDK for your development platform (see Installing and Configuring).
Let’s call the directory where you installed FBX SDK <yourFBXSDKpath>.
Determine the directory name (<Pythonxxxxxx>) of the version of Python FBX that you wish to install (see Platforms supported).
Copy the contents of <yourFBXSDKpath>\lib\<Pythonxxxxxx>\ to yourPythonPath\Lib\site-packages\.
Optional: Copy the sample programs for Python FBX to a suitable location. The sample programs are in <yourFBXSDKpath>\examples\Python\.
Optional: Copy the documentation for FBX SDK to a suitable location. The documentation is in <yourFBXSDKpath>\doc.
Optional: Delete <yourFBXSDKpath> and its contents. If you have copied all the directories mentioned above, you do not need the rest of the distribution for FBX SDK.
