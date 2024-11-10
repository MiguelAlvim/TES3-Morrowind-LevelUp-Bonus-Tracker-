import platform
import os
import sys
import FreeSimpleGUI as g
from AttributesAndSkills import attributesAndSkills as attributes, skill, attribute

#This Class has all we need to handle a minus or plus event
class buttonEvent:
	"""Represents an custom event to be trigged by the plus and minus buttons of the screen
	"""
	def __init__(self,id:str,skillname:str,attributename:str,modifyValue:int):
		"""
		:param id Screen object ID
		:param skillname Name of the skill that the buttons modifies. Used to determine which field to modify
		:param attributename Name of the attribute that the buttons modifies. Used to determine which field to modify
		:param modifyValue Value to be added to the total of the attribute if the button is pressed
		"""
		self.id:str = id
		self.skillname:str = skillname
		self.attributename:str = attributename
		self.modifyValue:int = modifyValue

	def actionToExecute(self,id:str):
		"""Checks to see if the event ID passed is the one soted on this object.
			Returns None if it's not the correct ID; A tuple with the name of the field, it's attribute and the value to be incremented to it otherwise
		:param id String containing the detected event
		
		"""
		if id == self.id:
			return (f'{self.skillname}',self.attributename,self.modifyValue)
		return None


#List of Event IDs and what to Do with them
eventList:list[buttonEvent] = []
pointsGainedThisLevel:dict[str,int] = {}
modifiersGainedThisLevel:dict[str,int] = {}

#STAR GUI creation
layoutLeft = [[g.Push(),g.Text("Skills Raised on Current Level", font='bold'),g.Push()]]
layoutLeft.append([g.HorizontalSeparator()])
totalPerColumn = 3
elementOnColumnCounter = 0
colunms = []
colunm = []
finalLayout = []
for atrib in attributes:
	modifiersGainedThisLevel[atrib.name] = 0
	if len(atrib.skills)>0:
		colunm.append([g.Text(atrib.name, font='bold', )])
		for ski in atrib.skills:
			colunm.append(
				[
				g.Button(button_text="-", key=f'mb_{ski.name}', enable_events= True),
				g.InputText(size=(3,1),   key=f'vl_{ski.name}', disabled=True, default_text='0', justification='center'),
				g.Button(button_text="+", key=f'pb_{ski.name}', enable_events= True),
				g.Text(ski.name)
				]
			)
			eventList.append(buttonEvent(id=f'mb_{ski.name}',modifyValue=-1,skillname=ski.name, attributename=atrib.name))
			eventList.append(buttonEvent(id=f'pb_{ski.name}',modifyValue=1,skillname=ski.name, attributename=atrib.name))
			pointsGainedThisLevel[ski.name] = 0
		elementOnColumnCounter += 1
	if elementOnColumnCounter >= totalPerColumn or atrib == attributes[-1]:
		elementOnColumnCounter = 0
		colunms.append(colunm)
		colunm = []

for col in colunms:
	finalLayout.append(g.Column(col,vertical_alignment='top'))
layoutLeft.append(finalLayout)

layoutRight = [[g.Push(),g.Text("Expected Bonuses on Next Level Up", font='bold'),g.Push()]]
layoutRight.append([g.HorizontalSeparator()])
for atrib in attributes:
	layoutRight.append([g.Text("+0", key=f"mf_{atrib.name}"),g.Text(atrib.name, font='bold')])

#selecting icon type - On windows must be .ico, on linux must not be icon
icon = os.path.dirname(os.path.realpath(sys.argv[0]))+"\icon.ico"
if platform.system() == "Linux":
	icon = os.path.dirname(os.path.realpath(sys.argv[0]))+"\icon.png"

window = g.Window("TES 3:Morrowind Level Up Bonus Tracker",
	[[g.Column(layoutLeft,vertical_alignment='top'),g.VerticalSeparator(),g.Column(layoutRight,vertical_alignment='top')]],
	icon=os.path.dirname(os.path.realpath(sys.argv[0]))+".\icon.ico"
	)
#END GUI creation

def updateGuiAndSkillValues(windowObjectArray, checkResult):
	"""Receives and array with the objects of the window and the result of the function actionToExecute from a buttonEvent object and update the GUI and internal values if necessary
	"""
	if checkResult != None:
		currentVal = pointsGainedThisLevel[checkResult[0]]
		newVal = currentVal + checkResult[2]
		if newVal >= 0 and newVal <=99:
			#skill counter
			pointsGainedThisLevel[checkResult[0]] = newVal
			windowObjectArray[f'vl_{result[0]}'].update(newVal) 
			#attribute modifier counter
			modifiersGainedThisLevel[checkResult[1]] = modifiersGainedThisLevel[checkResult[1]] + newVal/2 - currentVal/2
			windowObjectArray[f'mf_{result[1]}'].update(f"+{min(round(modifiersGainedThisLevel[checkResult[1]]),5)}") 

#GUI loop and event handling
while True:
	event, values = window.read()
	if event == g.WIN_CLOSED or event == "Cancel":
		break

	#Button Events
	for evnt in eventList:
		result = evnt.actionToExecute(event)
		if result != None:
			updateGuiAndSkillValues(window,result)			

window.close()