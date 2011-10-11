#$Id: interface.py,v 1.1 2004/03/18 05:44:21 mandava Exp $
#This is a program which combines  menubar, text area and file browser  
#into a single interface.
#

from Tkinter import *
from tkFileDialog import askopenfilename
from sets import Set
import tkFileDialog, csv, random, re
class mywidgets:
	def __init__(self,root):
	
		#self.svariables = {
			#'#$1':'skip hire',
			#'#$2':'waste removal',
			#'#$3':'skip',					
		#}
		self.svariables = {}
		
		self.tentries = {}
		self.root = root
		self.frame=Frame(root)
		self.makeMenuBar(self.frame)
		self.replaceButton = None
		self.copyButton= None
		self.txtfr(self.frame)
		self.txtfrRaw(self.frame)
		self.filename = "spinning.csv"
		self.openDefault()
		
		self.frame.pack()
		return
		
	
	def setSvariables(self):
		print "setting svariables"
		text = self.text.get(1.0, END)
		m = re.findall(r'\#\${1}([a-z]+[0-9]*|[0-9]+[a-z]*)', text)
		for token in m:
			if not token  in self.svariables:
				self.svariables[token]  = ''
				print "adding %s " % token
			
		
		
		
	
	def replacements(self,frame):
		repFrame = Frame(frame,relief = RAISED,borderwidth = 1)
		if self.replaceButton is None:
			self.replaceButton = Button(repFrame, text="Replace", command=self.replace)
			self.replaceButton.pack(side = TOP)
			
		if self.copyButton is None:
			self.copyButton = Button(repFrame, text="Copy To Clipboard", command=self.copy)
			self.copyButton.pack(side = BOTTOM)
		
		gridFrame = Frame(repFrame)
		
		self.setSvariables()
		
		count = 0
		for k,v in self.svariables.iteritems():
			if not k in self.tentries:
				Label(gridFrame, text=k).grid(row=count)
				self.tentries[k] = Entry(gridFrame)
				self.tentries[k].insert(0,v)
				self.tentries[k].grid(row=count, column=1)
				count += 1
			
		gridFrame.pack(side = RIGHT)
		repFrame.pack(side = LEFT)
		
	def copy(self, event=None):
		text = self.text.get(1.0, END)	
		#self.root.withdraw()
		self.root.clipboard_clear()
		self.root.clipboard_append(text)
		
	def replace(self):
		for r in self.tentries:
			text = self.text.get(1.0, END)	
			self.text.delete(1.0, END)
			self.text.insert(END,text.replace("#$"+r,self.tentries[r].get()))
		
	def openDefault(self):
		print "Opening Default"
		#file = open('spinning.csv', 'rw')	
		self.text.delete(1.0, END)
		self.textraw.delete(1.0, END)
		file = csv.reader(open(self.filename, 'rb'), delimiter=',', quotechar='"')
		if file != None:
			count = 0
			data = []
			for row in file:
				count += 1
				data.append(row)
			
			rowx = random.choice(data)
			print "There are %d rows.   Choosing at random row" % (count)
			
			self.textraw.insert(END,"Article Spinning  From File Row \n\n"  )
			xcount = 0
			for x in rowx:
				xcount += 1
				self.textraw.insert(END,"%s " % x )
				if xcount >= 3:
					self.textraw.insert(END,"\n\n")
					xcount = 0
				
				
			
			pcount = 0
			for sentence in self.spinArticle(rowx):
				pcount += 1
				self.text.insert(END,"%s " % sentence )
				if pcount >= 3:
					self.text.insert(END,"\n\n")
					pcount = 0
					
			self.replacements(self.frame)
			
			
			
	
	def spinArticle(self,data):
		print "Spinning Article Now"
		
		article = []
		scount = 0
		for sentence in data:
			scount += 1
			print scount
			article.append(self.spinSentence(sentence))
			
		return article
			
	def spinSentence(self,SpinSentence):
		sentence = ''
		if SpinSentence[0] == '{':
			print "removing brace {"
			sentence = SpinSentence[1:]
		else:
			sentence = SpinSentence
		if SpinSentence[-1] == '}':
			sentence = sentence[:-1]
			print "removing brace }"
			
		#print SpinSentence	
		#print sentence
		
		def wordReplace( match ):
			choices = match.group().split("|")
			print choices
			return " %s " % random.choice(choices).translate(None, '{}') 
		p = re.compile(r'\{([a-zA-Z0-9_\.-\|\s#$]+)\}')
		spunSentence = p.sub(wordReplace, sentence)
		return spunSentence.replace('  ',' ') 
		
	
	
	#defines the text area
	def txtfr(self,frame):
		textfr = Frame(frame)
		self.text = Text(textfr,height = 30,width = 150,background='white')
		scroll = Scrollbar(textfr)
		self.text.configure(yscrollcommand = scroll.set)
		self.text.pack(side = RIGHT)
		scroll.pack(side = RIGHT,fill = Y)
		textfr.pack(side = TOP)
		return
	#defines the text area
	def txtfrRaw(self,frame):
		textfrRaw = Frame(frame)
		self.textraw = Text(textfrRaw,height = 30,width = 150,background='grey')
		scrollr = Scrollbar(textfrRaw)
		self.textraw.configure(yscrollcommand = scrollr.set)
		self.textraw.pack(side = RIGHT)
		scrollr.pack(side = RIGHT,fill = Y)
		textfrRaw.pack(side = TOP)
		return
	#defines menubar
	def makeMenuBar(self,frame):
		menubar = Frame(frame,relief = RAISED,borderwidth = 1)
		menubar.pack()
		mb_file = Menubutton(menubar,text = 'file')
		mb_file.pack(side = LEFT)
		mb_file.menu = Menu(mb_file)
		mb_file.menu.add_command(label = 'spin',command = self.openDefault)
		mb_file.menu.add_command(label = 'open',command = self.file_open)
		#mb_edit = Menubutton(menubar,text = 'edit')
		#mb_edit.pack(side = LEFT)
		#mb_edit.menu = Menu(mb_edit)
		#mb_edit.menu.add_command(label = 'copy')
		#mb_help = Menubutton(menubar,text = 'help')
		#mb_help.pack(padx = 25,side = RIGHT)
		mb_file['menu'] = mb_file.menu
 		#mb_edit['menu'] = mb_edit.menu
		return
	#defines file_open which is called when file option openis choosen
	#displays the files giving the user choice to choose  file
	def file_open(self):
		filename =askopenfilename(filetypes=[("allfiles","*"),("csv files","*.csv")])
		if filename != None:
			self.filename = filename
			self.openDefault()
		else:
			self.filename = "spinning.csv"
			
        


def main():
	root = Tk()
	k = mywidgets(root)
	root.title('SEO Article Spinner v0.1')
	root.mainloop()
main()
