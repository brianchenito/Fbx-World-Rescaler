
try:
	import tkinter as tk #ui, io
	import tkinter.filedialog

	import fbx          #drives main functionality
	from fbx import *   
	import FbxCommon
						
	#from memory_profiler import profile  #debug only

	import os
	import sys      

except ImportError:
	print("Missing modules, you're probably missing the Python version of Autodesk FBX SDK. Make sure it's installed right. ")
	sys.exit(0) # Just google the module or something, theres install instructions there too. 
				# If it helps, this script is for python 3.3, and uses FBX SDK 2015.1.

BODY= ("Segoe UI light",9)
HEADER= ("Segoe UI light",14)
TITLE= ("Segoe UI Light",18)

class MainWindow(tk.Frame):
	print("mainwindow")
	
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.LocatedFBX="Empty (no file loaded)"
		self.saveLocation="Empty (no save location specified)"
		self.scalar=float(100.00)
		self.status= tk.StringVar()
		self.status.set("Status: Waiting for input")

		(self.lSdkManager,self.lScene)= FbxCommon.InitializeSdkObjects()

		self.label0 = tk.Label(self, text= "Fbx World Units Rescaler",font=HEADER,)
		self.label0.grid(row=0,column=0,padx=10, pady=4,sticky="nsew", columnspan=2)

		self.button0= tk.Button(self, text=self.LocatedFBX,font=BODY, command=lambda:(self.loadFbx()))
		self.button0.grid(row=1,column=1,padx=10, pady=4,sticky="nsew")
	
		self.label1=tk.Label(self, text="Load .fbx", font=BODY)
		self.label1.grid(row=1,column=0,padx=10,pady=4,sticky="nsew")

		self.entry0=tk.Entry(self, font=BODY, justify="center")
		self.entry0.insert(0, self.scalar)
		self.entry0.grid(row=2,column=1, padx=10,pady=4,sticky="nsew")
		self.entry0.bind("<Return>",self.setScaleVal) 

		self.label2= tk.Label(self, text= ("Resize To: {0} %".format( self.scalar)),font=BODY,wraplength=170 )
		self.label2.grid(row=2,column=0, padx=10,pady=4,sticky="nsew")

		self.label3= tk.Label(self, text= ("Save To:"),font=BODY)
		self.label3.grid(row=3,column=0, padx=10,pady=4,sticky="nsew")

		self.button1= tk.Button(self, text=self.saveLocation,font=BODY, command=lambda:(self.saveLoc()),)
		self.button1.grid(row=3,column=1,padx=10, pady=4,sticky="nsew")

		self.button2= tk.Button(self, text="Resize",font=HEADER, command=lambda:(self.build()))
		self.button2.grid(row=4,column=1,padx=10, pady=4,sticky="nsew")

		self.label4= tk.Label(self, textvariable= self.status,font=BODY,wraplength=170 )
		self.label4.grid(row=4,column=0, padx=10,pady=4,sticky="nsew")

    
	def setScaleVal(self,event ):
		print ("setVal")
		val= self.entry0.get()
		print (val)
		try: 
			val=float(val)
			self.scalar=float(val)
		except ValueError:
			self.entry0.delete(0,tk.END)
			print("non float error, ignoring")
			self.entry0.insert(0, self.scalar)
		self.label2.config(text= ("Resize To:  {0}%") .format(round(self.scalar,4)))
		self.entry0.selection_range(0,tk.END)
		self.checkStatus()
	
	def loadFbx(self):
		print ("LoadFBX")
		self.LocatedFBX="Empty (no file loaded)"
		self.LocatedFBX= tk.filedialog.askopenfilename(
			initialdir=os.path.expanduser("~\Documents"), filetypes=[("Fbx files","*.fbx"),('All','*')])
		print (self.LocatedFBX)
		if len(self.LocatedFBX)>50:
			self.button0.config(text= "...%s" % self.LocatedFBX[-47:])
		else:
			self.button0.config(text= self.LocatedFBX)
		if not self.LocatedFBX:
			self.LocatedFBX="Empty (no file loaded)"
			self.button0.config(text= self.LocatedFBX)		
			return
	
		self.checkStatus()

	
	def saveLoc(self):
		print("saveLoc")
		self.saveLocation= tk.filedialog.asksaveasfilename(
			initialdir=os.path.expanduser("~\Documents"), filetypes=[("Fbx files","*.fbx"),('All','*')])
		print (self.saveLocation)
		if len(self.saveLocation)>50:
			self.button1.config(text= "...%s" % self.saveLocation[-47:])
		else:
			self.button1.config(text= self.saveLocation)
		if not self.saveLocation:
			self.saveLocation="Empty (no save location specified)"
			self.button1.config(text= self.saveLocation)
		self.checkStatus()


	def build(self):
		print("build")
		if (self.checkStatus()):
			self.status.set("Building...")
			if(FbxCommon.LoadScene(self.lSdkManager,self.lScene,self.LocatedFBX)):
				unitType=self.lScene.GetGlobalSettings().GetSystemUnit().GetScaleFactor()
				self.newScale= FbxSystemUnit(unitType,self.scalar/100)
				self.newScale.ConversionOptions.mConvertRrsNodes =False # preserves resizing on elements
				self.newScale.ConvertScene(self.lScene)
				print (self.lScene.GetGlobalSettings().GetSystemUnit().GetScaleFactor())
				FbxCommon.SaveScene(self.lSdkManager, self.lScene,self.saveLocation)
				self.status.set("Build Complete!")
			else:
				self.status.set("Failure to build Scene.")


	def checkStatus(self):
		if (self.LocatedFBX!="Empty (no file loaded)"):
			if (self.saveLocation!="Empty (no save location specified)"):
				if (self.scalar !=0):
					self.status.set("Status: Ready to build")
					if (self.scalar> 99999 or self.scalar< -99999 ):
						self.status.set("Warning! : This is going to be kinda big.") #but it should still execute
					if (self.scalar==100):
						self.status.set("Note : Resizing to 100%"" will do nothing")
					return 1
				else:
					self.status.set("Not ready: Scale cannot be 0")
					return 0
			else:
				self.status.set("Not ready: No save location specified")
				return 0
		else:	
			self.status.set("Not ready: No file loaded")
			return 0

if __name__ == "__main__":
	print ("main ")
	root = tk.Tk()

	MainWindow(root).pack(side="top", fill="both", expand=True)
	root.mainloop()
	print("endmain")
