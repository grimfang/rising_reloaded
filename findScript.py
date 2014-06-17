import os

def scanfolder():
	theFolder = os.path.dirname(os.path.realpath(__file__))
	filesToScan = []
	for path, dirs, files in os.walk(theFolder):
		for f in files:
			if f.endswith('.py'):
				fileLoc = os.path.join(path, f)
				filesToScan.append(fileLoc)

	readLines(filesToScan)

def readLines(_filesList):
	textFile = open("Todo-comments.txt", "w")
	space = "\n"
	

	lineDict = {}
	lineFile = {}

	for _file in _filesList:
		lineCount = 0
		for line in open(_file):
			lineCount += 1
			li = line.strip()
			if li.startswith("#@"):
				splitLine = line.rstrip()

				fileDir = _file.split('/')
				fileName = fileDir[-1:]
				lineDict[lineCount] = splitLine
				lineFile[lineCount] = fileName
				
	

	for i in lineDict.keys():
		print i, lineDict[i]
		print lineFile[i]
		newStr = " " + str(str(i) + lineDict[i])
		fileNameStr = "File: " + str(lineFile[i])
		textFile.write(fileNameStr)
		textFile.write(newStr)
		textFile.write('\n')





scanfolder()