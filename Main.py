# gui imports
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from pylatex import Document, Section, Subsection, Subsubsection, Command, Itemize
from pylatex.utils import italic, NoEscape

import os
import ast

"""UI Classes"""

class Main(QMainWindow):
	def __init__(self, stack, windowStack):
		super(Main, self).__init__()
		loadUi("GUI.ui", self)
		
		self.stack = stack
		self.windowStack = windowStack

		self.LocalUiSetup()

		self.manual_ui = ManualUIMethods()

		self.open_plans = set()
		self.active_path = None

	def LocalUiSetup(self):
		self.ButtonConnect()
		self.ActionConnect()

	"""Connect Methods"""
	def ButtonConnect(self):
		pass
	def ActionConnect(self):
		self.actionCreate_New_Plan.triggered.connect(self.create_plan_window)
		self.actionOpen_Plan.triggered.connect(self.open_plan)
		self.actionEdit_Plan.triggered.connect(self.edit_plan_window)
		self.actionExport_Plan.triggered.connect(self.export_plan)

	"""Window Generators"""
	def create_plan_window(self):
		create_plan_window = CreatePlan(self)
		create_plan_window.show()
	def edit_plan_window(self):
		edit_plan_window = EditPlan(self.active_path, self)
		edit_plan_window.show()

	def open_plan(self):
		# Adding a Plan object made using the information given by the users .dp file to the open_plans set
		file_path, _ = QFileDialog.getOpenFileName(self, "Open Plan", "C:\\", "Developer Plan (*.dp)", )
		opened_plan = Plan(file_path)

		if file_path:
			self.open_plans.add(file_path)

		if len(self.open_plans) == 1:
			self.menuActive_Plan.removeAction(self.actionNo_Open_Plans)

		# Adds the action of setting this new plan as the active plan
		# Also making sure that if two plans have the same name they are indexed
		if file_path:
			names = [i.text() for i in self.menuActive_Plan.actions()]
			if opened_plan.name in names:
				self.menuActive_Plan.addAction(f"{opened_plan.name} ({names.count(opened_plan.name)})")
			else:
				self.menuActive_Plan.addAction(opened_plan.name, lambda: self.set_active_plan(file_path))
	def set_active_plan(self, path):
		plan = Plan(path)
		self.actionEdit_Plan.setEnabled(True)
		self.actionExport_Plan.setEnabled(True)
		self.label_Active_Plan.setText(": Active Plan :\n{}".format(plan.name))
		self.active_path = path
	def export_plan(self):
		# Adding a Plan object made using the information given by the users .dp file to the open_plans set
		file_path, _ = QFileDialog.getSaveFileName(self, "Export Plan", "C:\\")

		plan = Plan(self.active_path)
		plan.export(file_path)

class EditPlan(QMainWindow):
	def __init__(self, path, parent=None):
		super(EditPlan, self).__init__(parent)
		loadUi("EditPlan.ui", self)

		self.manual_ui = ManualUIMethods()

		self.path = path
		self.plan = Plan(path)

		self.LocalUiSetup()

	def LocalUiSetup(self):
		self.ButtonConnect()
		self.ActionConnect()

		self.lineEditEditEnter_Name.setText(self.plan.name)

	def ButtonConnect(self):
		self.pushButtonEditApply.clicked.connect(self.set_program_name)
		self.pushButtonEditClient_Request.clicked.connect(self.client_request_window)
		self.pushButtonEditProgram_Description.clicked.connect(self.program_description_window)
		self.pushButtonEditProgram_Aim.clicked.connect(self.program_aim_window)
		self.pushButtonEditOutstanding_Ideas.clicked.connect(self.outstanding_ideas_window)
		self.pushButtonEditDeveloper_Planning.clicked.connect(self.developer_planning_window)
	
	def ActionConnect(self):
		self.actionEditSave.triggered.connect(self.save_plan)
		self.actionEditSave_Plan_As.triggered.connect(self.save_plan_as)

	def set_program_name(self):
		self.plan.name = self.lineEditEditEnter_Name.text()

	def save_plan(self):
		# Getting the save destination
		save_path = self.plan.save_path
		print(save_path)
		# Checking whether there is an existing save destination
		if save_path == None:
			self.save_plan_as()
		else:
			self.plan.save(save_path)

	def save_plan_as(self):
		# Saving the plan to the destination
		save_path, _ = QFileDialog.getSaveFileName(self, "Save Plan", self.path, "Developer Plan (*.dp)")
		self.plan.save(save_path)

	def client_request_window(self):
		# Opening a window for the client to enter their request
		client_request = ClientRequest(self.plan, self)
		client_request.show()

	def program_description_window(self):
		# Opening a window for the user to enter the program description
		program_description = ProgramDescription(self.plan, self)
		program_description.show()

	def program_aim_window(self):
		# Opening a window for the user to enter the program aim
		program_aim = ProgramAim(self.plan, self)
		program_aim.show()

	def outstanding_ideas_window(self):
		# Opening a window for the user to enter their outstanding ideas
		outstanding_ideas = OutstandingIdeas(self.plan, self)
		outstanding_ideas.show()

	def developer_planning_window(self):
		# Opening a window for the user to start developing the code
		developer_planning = DeveloperPlanning(self.plan, self)
		developer_planning.show()

class CreatePlan(QMainWindow):
	def __init__(self, parent=None):
		super(CreatePlan, self).__init__(parent)
		loadUi("CreatePlan.ui", self)

		# self.stack = stack
		# self.windowStack = windowStack

		self.manual_ui = ManualUIMethods()

		self.new_plan = Plan()

		self.LocalUiSetup()


	def LocalUiSetup(self):
		self.ButtonConnect()
		# self.ActionConnect()

	"""Connect Methods"""
	def ButtonConnect(self):
		self.pushButtonCreateApply.clicked.connect(self.set_program_name)
		self.pushButtonCreateClient_Request.clicked.connect(self.client_request_window)
		self.pushButtonCreateProgram_Description.clicked.connect(self.program_description_window)
		self.pushButtonCreateProgram_Aim.clicked.connect(self.program_aim_window)
		self.pushButtonCreateOutstanding_Ideas.clicked.connect(self.outstanding_ideas_window)
		self.pushButtonCreateDeveloper_Planning.clicked.connect(self.developer_planning_window)
		self.pushButtonCreateSave_Plan.clicked.connect(self.save_plan)

	def set_program_name(self):
		self.new_plan.name = self.lineEditCreateEnter_Name.text()

	def save_plan(self):
		# Saving the plan to the destination
		save_path, _ = QFileDialog.getSaveFileName(self, "Save Plan", "C:\\", "Developer Plan (*.dp)")
		self.new_plan.save(save_path)

	def client_request_window(self):
		# Opening a window for the client to enter their request
		client_request = ClientRequest(self.new_plan, self)
		client_request.show()

	def program_description_window(self):
		# Opening a window for the user to enter the program description
		program_description = ProgramDescription(self.new_plan, self)
		program_description.show()

	def program_aim_window(self):
		# Opening a window for the user to enter the program aim
		program_aim = ProgramAim(self.new_plan, self)
		program_aim.show()

	def outstanding_ideas_window(self):
		# Opening a window for the user to enter their outstanding ideas
		outstanding_ideas = OutstandingIdeas(self.new_plan, self)
		outstanding_ideas.show()

	def developer_planning_window(self):
		# Opening a window for the user to start developing the code
		developer_planning = DeveloperPlanning(self.new_plan, self)
		developer_planning.show()

class ProgramAim(QDialog):

	def __init__(self, plan, parent=None):
		super(ProgramAim, self).__init__(parent)
		loadUi("ProgramAim.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.LocalUiSetup()

	def LocalUiSetup(self):
		self.ButtonConnect()

		# Enters any previously saved plan aim into the entry box
		if not self.plan.aim == "":
			self.plainTextEditProgram_Aim.setPlainText(self.plan.aim)

	"""Connect Methods"""
	def ButtonConnect(self):
		self.pushButtonSave_Program_Aim.clicked.connect(self.save_program_aim)

	def save_program_aim(self):
		self.plan.aim = self.plainTextEditProgram_Aim.toPlainText()

class ProgramDescription(QDialog):

	def __init__(self, plan, parent=None):
		super(ProgramDescription, self).__init__(parent)
		loadUi("ProgramDescription.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.empty = True

		self.LocalUiSetup()

	def LocalUiSetup(self):

		# Checks whether there are any description elements already in the plan
		# Updates the combo box and text entry accordingly
		if len(self.plan.description) > 0:
			self.empty = False
			self.comboBoxDescription_Elements.clear()
			self.comboBoxDescription_Elements.currentIndexChanged.connect(self.on_desc_element_change)
			self.comboBoxDescription_Elements.addItems(list(self.plan.description.keys()))

		self.ComboBoxConnect()
		self.ButtonConnect()
		

	"""Connect Methods"""
	def ButtonConnect(self):
		self.pushButtonSave_Desc_Element.clicked.connect(self.save_description_element)
		self.pushButtonRemove_Desc_Element.clicked.connect(self.remove_discription_element)
	def ComboBoxConnect(self):
		self.comboBoxDescription_Elements.currentIndexChanged.connect(self.on_desc_element_change)


	def on_desc_element_change(self):
		# Checking whether the plan has any description elements and whether the combobox is empty
		if len(self.plan.description) == 0 and self.empty == False:
			# Removing all description id's and clearing the plain text edit
			self.empty = True
			self.comboBoxDescription_Elements.clear()
			self.plainTextEditDesc_Text.clear()
			self.comboBoxDescription_Elements.addItem("No Description Elements Yet")
		elif len(self.plan.description) > 0 and self.empty == False:
			# Updating the plain text edit based on the id
			new_desc_id = self.comboBoxDescription_Elements.currentText()
			self.plainTextEditDesc_Text.setPlainText(self.plan.description[new_desc_id])

	def remove_discription_element(self):

		# Grapping the description id and text
		desc_id = self.comboBoxDescription_Elements.currentText()

		# Asking user if they want to overwrite the existing description
		remove = QMessageBox.warning(self, "Warning", f"Are you sure you want to remove {desc_id}?", QMessageBox.Yes|QMessageBox.No)
		if remove == QMessageBox.No:
			return

		# Deleting the description and description id
		desc_id_index = self.comboBoxDescription_Elements.findText(desc_id)
		del self.plan.description[desc_id]
		self.comboBoxDescription_Elements.removeItem(desc_id_index)

	def save_description_element(self):

		# Grapping the description id and text
		desc_id = self.lineEditDesc_Element_id.text()
		text = self.plainTextEditDesc_Text.toPlainText()

		# Checking whether the id already exists
		if self.comboBoxDescription_Elements.findText(desc_id) == -1:
			self.comboBoxDescription_Elements.addItem(desc_id)
		else:
			# Asking user if they want to overwrite the existing description
			overwrite = QMessageBox.warning(self, "Warning", "A description with that ID already exists.\nOverwrite?", QMessageBox.Yes|QMessageBox.No)
			if overwrite == QMessageBox.No:
				return
		# Adding/updating the description for the corresponding id
		self.plan.description[desc_id] = text

		# Removing the temporary first combo box item if this is the first element
		if self.empty:
			self.comboBoxDescription_Elements.removeItem(0)
			self.empty = False	

		# Making sure that the combo box shows the id corresponding to the text
		if not self.comboBoxDescription_Elements.currentText() == desc_id:
			desc_id_index = self.comboBoxDescription_Elements.findText(desc_id)
			self.comboBoxDescription_Elements.setCurrentIndex(desc_id_index)

class OutstandingIdeas(QDialog):

	def __init__(self, plan, parent=None):
		super(OutstandingIdeas, self).__init__(parent)
		loadUi("OutstandingIdeas.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.empty = True

		self.LocalUiSetup()

	def LocalUiSetup(self):


		# Adding any previously saved ideas, versions, and corresponding text
		if len(self.plan.outstanding_ideas) > 0:
			self.comboBoxIdea_Index.clear()
			self.comboBoxIdea_Version.clear()

			idea_indexes = list(self.plan.outstanding_ideas.keys())
			idea_versions = list(self.plan.outstanding_ideas[idea_indexes[0]].keys())
			idea_text = self.plan.outstanding_ideas[idea_indexes[0]][idea_versions[0]]
			self.comboBoxIdea_Index.addItems(idea_indexes)
			self.comboBoxIdea_Version.addItems(map(lambda x : str(x), idea_versions))
			self.plainTextEditOutstanding_Idea.setPlainText(idea_text)

			self.empty = False

		self.ButtonConnect()
		self.ComboBoxConnect()

	def ButtonConnect(self):
		self.pushButtonAdd_Idea.clicked.connect(self.add_idea)
		self.pushButtonRemove_Idea.clicked.connect(self.remove_idea)
		self.pushButtonCommit_To_Idea.clicked.connect(self.commit_to_idea)
		self.pushButtonRemove_Latest_Commit.clicked.connect(self.remove_latest_commit)
	def ComboBoxConnect(self):
		self.comboBoxIdea_Index.currentIndexChanged.connect(self.on_idea_index_element_change)
		self.comboBoxIdea_Version.currentIndexChanged.connect(self.on_idea_version_element_change)

	def on_idea_index_element_change(self):
		# Checking whether there are any outstanding ideas and whether the combo box is already empty
		if len(self.plan.outstanding_ideas) == 0 and self.empty == False:
			# Updating the combo box with the default message to show that it is empty
			self.empty = True
			self.comboBoxIdea_Index.clear()
			self.comboBoxIdea_Version.clear()
			self.comboBoxIdea_Index.addItem("No Outstanding Ideas")
			self.comboBoxIdea_Version.addItem("No Outstanding Ideas")
		elif len(self.plan.outstanding_ideas) > 0 and self.empty == False:
			# Adding the versions to the versions combo box based on the outstanding idea
			idea_index = self.comboBoxIdea_Index.currentText()
			versions = map(lambda x : str(x), list(self.plan.outstanding_ideas[idea_index].keys()))
			self.comboBoxIdea_Version.clear()
			self.comboBoxIdea_Version.addItems(versions)
	def on_idea_version_element_change(self):
		# Updating the plain text based on the version
		if self.comboBoxIdea_Version.count() > 0 and self.empty == False:
			idea_index = self.comboBoxIdea_Index.currentText()
			idea_version = int(self.comboBoxIdea_Version.currentText())
			new_plain_text = self.plan.outstanding_ideas[idea_index][idea_version]
			self.plainTextEditOutstanding_Idea.setPlainText(new_plain_text)

	def add_idea(self):
		
		new_item_index = f"[{len(self.plan.outstanding_ideas)}]"

		# Adding the new item index to the plan outstanding ideas and combo box
		self.comboBoxIdea_Index.addItem(new_item_index)
		self.plan.outstanding_ideas[new_item_index] = {0:self.plainTextEditOutstanding_Idea.toPlainText()}

		# Adding the initial version
		self.comboBoxIdea_Version.clear()
		self.comboBoxIdea_Version.addItem("0")

		# Checking whether the combo box was previously empty to remove the default text
		if self.empty:
			self.comboBoxIdea_Index.removeItem(0)
			self.empty = False


	def remove_idea(self):

		# Making sure that there is an item to remove
		if self.empty:
			self.manual_ui.DisplayError("There are no outstanding ideas to remove.")
			return

		to_remove = self.comboBoxIdea_Index.currentText()
		
		# Making sure that the user wants to remove the outstanding idea
		remove = QMessageBox.warning(self, "Warning", f"Are you sure you want to delete outstanding idea {to_remove}?", QMessageBox.Yes|QMessageBox.No)
		if remove == QMessageBox.No:
			return

		# Removing the outstanding idea
		del self.plan.outstanding_ideas[to_remove]
		self.comboBoxIdea_Index.removeItem(self.comboBoxIdea_Index.findText(to_remove))	

		# Checking whether there are any ideas and updating the empty bool accordingly
		if self.comboBoxIdea_Index.count() == 0:
			self.empty = True

	def commit_to_idea(self):
		
		# Preventing the user from commiting a version when there are no ideas
		if self.empty == True:
			self.manual_ui.DisplayError("No outstanding ideas. You must create an idea to commit to it.")
			return

		# Getting all the variables required to commit the idea
		idea_text = self.plainTextEditOutstanding_Idea.toPlainText()
		idea_index = self.comboBoxIdea_Index.currentText()
		idea_version = self.comboBoxIdea_Version.count()

		# Checking whether the user has written an idea
		if idea_text == "":
			self.manual_ui.DisplayError("Please enter an outstanding idea.")
			return

		# Updating the plan and combo box to reflect the new versions
		self.plan.outstanding_ideas[idea_index][idea_version] = idea_text
		self.comboBoxIdea_Version.clear()
		self.comboBoxIdea_Version.addItems(map(lambda x : str(x), list(self.plan.outstanding_ideas[idea_index].keys())))
		self.comboBoxIdea_Version.setCurrentIndex(self.comboBoxIdea_Version.count()-2)

	def remove_latest_commit(self):

		# Preventing the user from removing a version when there are none
		if self.empty == True:
			self.manual_ui.DisplayError("There are no versions to remove.")
			return

		# Getting all the variables required to remove the commit
		idea_index = self.comboBoxIdea_Index.currentText()
		idea_version = self.comboBoxIdea_Version.count() - 1

		# Preventing the user from removing the last and only version
		if self.comboBoxIdea_Version.count() == 1:
			self.manual_ui.DisplayError("You cannot remove the last version.")
			return

		# Clearing the latest commit
		del self.plan.outstanding_ideas[idea_index][idea_version]
		self.plan.outstanding_ideas[idea_index][idea_version-1] = ""
		self.comboBoxIdea_Version.removeItem(self.comboBoxIdea_Version.count()-1)

class DeveloperPlanning(QDialog):

	def __init__(self, plan, parent=None):
		super(DeveloperPlanning, self).__init__(parent)
		loadUi("DeveloperPlanning.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.LocalUiSetup()

	def LocalUiSetup(self):
		self.ButtonConnect()

	def ButtonConnect(self):
		self.pushButton_Packages_Globals.clicked.connect(self.packages_globals_window)
		self.pushButton_Classes.clicked.connect(self.classes_window)
		self.pushButton_Methods.clicked.connect(self.methods_window)
		self.pushButton_Functions.clicked.connect(self.functions_window)

	def packages_globals_window(self):
		packages_globals = PackagesGlobals(self.plan, self)
		packages_globals.show()

	def classes_window(self):
		classes = Classes(self.plan, self)
		classes.show()

	def methods_window(self):
		methods = Methods(self.plan, self)
		methods.show()

	def functions_window(self):
		functions = Functions(self.plan, self)
		functions.show()

class PackagesGlobals(QDialog):

	def __init__(self, plan, parent=None):
		super(PackagesGlobals, self).__init__(parent)
		loadUi("PackagesGlobals.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.globals_empty = True
		self.packages_empty = True

		self.LocalUiSetup()

	def LocalUiSetup(self):
		
		# Updating the globals and packages combo boxes if there are already some saved
		if len(self.plan.globals) > 0:
			self.comboBox_Globals.clear()
			for var_type,var_name in self.plan.globals:
				self.comboBox_Globals.addItem(f"{var_name} :: {var_type}")
		if len(self.plan.packages) > 0:
			self.comboBox_Packages.clear()
			for package_name, package_from in self.plan.packages:
				self.comboBox_Packages.addItem(f"{package_name} << {package_from}")

		self.ButtonConnect()

	def ButtonConnect(self):
		self.pushButtonAdd_Global.clicked.connect(self.add_global)
		self.pushButtonAdd_Package.clicked.connect(self.add_package)
		self.pushButton_Remove_Global.clicked.connect(self.remove_global)
		self.pushButton_Remove_Package.clicked.connect(self.remove_package)

	def add_global(self):
		
		# Making sure the minimum necessary information has been provided
		if self.lineEditGlobal_Type.text() == "":
			self.manual_ui.DisplayError("Please enter a data type.")
			return
		if self.lineEditGlobal_Name.text() == "":
			self.manual_ui.DisplayError("Please enter a variable name.")
			return

		# Adding the new global variable to the plan
		self.plan.globals.append((self.lineEditGlobal_Type.text(), self.lineEditGlobal_Name.text()))

		# Updating the combo box to show all global variables
		self.comboBox_Globals.clear()
		for var_type,var_name in self.plan.globals:
			self.comboBox_Globals.addItem(f"{var_name} :: {var_type}")

	def remove_global(self):
		
		# Checking whether there are any globals to remove
		if len(self.plan.globals) == 0:
			self.manual_ui.DisplayError("There are no global variables to remove.")
			return

		# Asking the user whether they are sure they want the remove the global variable
		choice = QMessageBox.warning(self, "Warning", f"Are you sure you want to delete {self.comboBox_Globals.currentText()}?", QMessageBox.Yes|QMessageBox.No)
		if choice == QMessageBox.No:
			return

		# Removing the global variable from the plan
		to_remove = tuple(self.comboBox_Globals.currentText().split(" :: "))
		self.plan.globals.remove(to_remove)
		# Updating the combo box to show all global variables
		self.comboBox_Globals.clear()
		# Checking whether there are any global variables left
		if len(self.plan.globals) == 0:
			self.comboBox_Globals.addItem("No Global Variables")
		else:
			for var_type,var_name in self.plan.globals:
				self.comboBox_Globals.addItem(f"{var_name} :: {var_type}")


	def add_package(self):
		
		# Making sure the minimum necessary information has been provided
		if self.lineEdit_Import.text() == "":
			self.manual_ui.DisplayError("Please enter a package name.")
			return

		# Adding the new package to the plan
		self.plan.packages.append((self.lineEdit_Import.text(), self.lineEdit_From.text()))

		# Updating the combo box to show all packages
		self.comboBox_Packages.clear()
		for package_name, package_from in self.plan.packages:
			self.comboBox_Packages.addItem(f"{package_name} << {package_from}")

	def remove_package(self):
		
		# Checking whether there are any packages to remove
		if len(self.plan.packages) == 0:
			self.manual_ui.DisplayError("There are no packages to remove.")
			return

		# Asking the user whether they are sure they want the remove the package
		choice = QMessageBox.warning(self, "Warning", f"Are you sure you want to delete {self.comboBox_Packages.currentText()}?", QMessageBox.Yes|QMessageBox.No)
		if choice == QMessageBox.No:
			return

		# Removing the package from the plan
		to_remove = tuple(self.comboBox_Packages.currentText().split(" << "))
		self.plan.packages.remove(to_remove)
		# Updating the combo box to show all global variables
		self.comboBox_Packages.clear()
		# Checking whether there are any packages left
		if len(self.plan.packages) == 0:
			self.comboBox_Packages.addItem("No Packages")
		else:
			for package_name, package_from in self.plan.packages:
				self.comboBox_Packages.addItem(f"{package_name} << {package_from}")

# Stored format (Name, Description, Inherits, Parameters, Attributes, Methods)
class Classes(QDialog):

	def __init__(self, plan, parent=None):
		super(Classes, self).__init__(parent)
		loadUi("Classes.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.classes = []

		self.empty = True

		# Ensures that the data loss warning message only shows when needed
		self.cool = True

		self.LocalUiSetup()

	def LocalUiSetup(self):

		# Checking whether there were any pre-existing classes
		if len(self.plan.classes) > 0:
			self.empty = False
			self.comboBox_Classes.clear()
			self.comboBox_Classes.addItems([i[0] for i in self.plan.classes])
			for i in self.plan.classes:
				new_class = Class(i[0],i[1],i[2],i[3],i[4],i[5])
				self.classes.append(new_class)

		self.ButtonConnect()
		self.ComboBoxConnect()

	def ButtonConnect(self):
		self.pushButton_Add_Class.clicked.connect(self.add_class)
		self.pushButton_Remove_Class.clicked.connect(self.remove_class)
	def ComboBoxConnect(self):
		self.comboBox_Classes.currentIndexChanged.connect(self.on_class_change) 

	def remove_class(self):

		if self.empty == True:
			self.manual_ui.DisplayError("No classes to remove.")
			return

		# Making sure the user wants to remove the class
		choice = QMessageBox.warning(self, "Warning", f"Are you sure you want to remove class {self.comboBox_Classes.currentText()}?", QMessageBox.Yes|QMessageBox.No)
		if choice == QMessageBox.No:
			return

		# Getting the class to remove
		to_remove = self.comboBox_Classes.currentIndex()

		# Removing the class from memory
		self.classes.pop(to_remove)
		self.plan.classes.pop(to_remove)

		# Removing the class from the combo box
		self.cool = False
		self.comboBox_Classes.removeItem(to_remove)

		# Adding a combo box item to tell the user that there are no classes
		if len(self.classes) == 0:
			self.comboBox_Classes.addItem("No Classes Yet")
			self.empty = True

		self.manual_ui.DisplayMessageBox("Class successfully removed.", "Success", QMessageBox.Information, QMessageBox.Close)

	def on_class_change(self):

		# Checking whether the combo box is empty
		if self.comboBox_Classes.count() == 0 or self.empty == True or len(self.classes) == 0:
			return

		# Making sure that no unsaved changes are lost
		if self.cool == True and len(self.classes) == self.comboBox_Classes.count() and not (self.plainTextEdit_Class_Description.toPlainText() == "" or self.lineEdit_Class_Inherits.text() == "" or self.lineEdit_Class_Parameters.text() == "" or self.lineEdit_Class_Attributes.text() == "" or self.lineEdit_Class_Methods.text() == ""):
			choice = QMessageBox.warning(self, "Warning", f"If you switch classes now any unsaved information will be lost.", QMessageBox.Ok|QMessageBox.Abort)
			if choice == QMessageBox.Abort:
				return

		self.cool = True

		# Updating all the input fields to show the relavent information from the chosen class
		at = self.comboBox_Classes.currentIndex()
		clss = self.classes[at]

		# Updating the input boxes contents
		self.lineEdit_Class_Name.setText(clss.name)
		self.plainTextEdit_Class_Description.setPlainText(clss.description)
		self.lineEdit_Class_Inherits.setText(clss.inherits)
		self.lineEdit_Class_Parameters.setText(clss.parameters)
		self.lineEdit_Class_Attributes.setText(clss.attributes)
		self.lineEdit_Class_Methods.setText(clss.methods)


	def add_class(self):
		update = False
		# Checking whether a valid class name has been entered
		if self.lineEdit_Class_Name.text() == "":
			self.manual_ui.DisplayError("Please give the class a name.")
			return
		if self.lineEdit_Class_Name.text().rstrip() in [i[0] for i in self.plan.classes]:
			choice = QMessageBox.warning(self, "Warning","A class with that name already exists. Update the existing class?", QMessageBox.Yes|QMessageBox.No)
			if choice == QMessageBox.No:
				return
			else:
				update = True

		# Creating a new class and adding it to the local and plan lists
		name = self.lineEdit_Class_Name.text().rstrip()
		description = self.plainTextEdit_Class_Description.toPlainText()
		inherits = self.lineEdit_Class_Inherits.text()
		parameters = self.lineEdit_Class_Parameters.text()
		attributes = self.lineEdit_Class_Attributes.text()
		methods = self.lineEdit_Class_Methods.text()

		if update:

			# Updating the information of the class
			for i in self.classes:
				if i.name == name:
					i.description = description
					i.inherits = inherits
					i.parameters = parameters
					i.attributes = attributes
					i.methods = methods
					break
			self.manual_ui.DisplayMessageBox("Class successfully updated.", "Success", QMessageBox.Information)
		else:
			# Creating and adding a new class
			new_class = Class(name, description, inherits, parameters, attributes, methods)

			# Adding the new class to the plan and classes list
			self.classes.append(new_class)
			self.plan.classes.append(new_class.get_info())


			# Updating the combo box
			self.comboBox_Classes.clear()
			for i in self.classes:
				self.comboBox_Classes.addItem(i.name)
			self.cool = False
			self.comboBox_Classes.setCurrentText(new_class.name)
			self.empty = False

			self.manual_ui.DisplayMessageBox("Class successfully added.", "Success", QMessageBox.Information)

# Stored format (Name, Description, Parent Class, Decorators, Parameters, Local Variables, Pseudo Code)
class Methods(QDialog):

	def __init__(self, plan, parent=None):
		super(Methods, self).__init__(parent)
		loadUi("Methods.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.methods = []

		self.empty = True

		# Ensures that the data loss warning message only shows when needed
		self.cool = True

		self.LocalUiSetup()

	def LocalUiSetup(self):

		# Checking whether there were any pre-existing methods
		if len(self.plan.methods) > 0:
			self.empty = False
			self.comboBox_Methods.clear()
			self.comboBox_Methods.addItems([i[0] for i in self.plan.methods])
			for i in self.plan.methods:
				new_method = Method(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
				self.methods.append(new_method)

		self.ButtonConnect()
		self.ComboBoxConnect()

	def ButtonConnect(self):
		self.pushButton_Add_Method.clicked.connect(self.add_method)
		self.pushButton_Remove_Method.clicked.connect(self.remove_method)
	def ComboBoxConnect(self):
		self.comboBox_Methods.currentIndexChanged.connect(self.on_method_change) 

	def remove_method(self):

		if self.empty == True:
			self.manual_ui.DisplayError("No methods to remove.")
			return

		# Making sure the user wants to remove the method
		choice = QMessageBox.warning(self, "Warning", f"Are you sure you want to remove method {self.comboBox_Methods.currentText()}?", QMessageBox.Yes|QMessageBox.No)
		if choice == QMessageBox.No:
			return

		# Getting the method to remove
		to_remove = self.comboBox_Methods.currentIndex()

		# Removing the method from memory
		self.methods.pop(to_remove)
		self.plan.methods.pop(to_remove)

		# Removing the method from the combo box
		self.cool = False
		self.comboBox_Methods.removeItem(to_remove)

		# Adding a combo box item to tell the user that there are no methods
		if len(self.methods) == 0:
			self.comboBox_Methods.addItem("No Methods Yet")
			self.empty = True

		self.manual_ui.DisplayMessageBox("Method successfully removed.", "Success", QMessageBox.Information, QMessageBox.Close)

	def on_method_change(self):

		# Checking whether the combo box is empty
		if self.comboBox_Methods.count() == 0 or self.empty == True or len(self.methods) == 0:
			return

		# Making sure that no unsaved changes are lost
		if self.cool == True and len(self.methods) == self.comboBox_Methods.count() and not (self.plainTextEdit_Method_Description.toPlainText() == "" or self.lineEdit_Method_Parent.text() == "" or self.lineEdit_Method_Decorators.text() == "" or self.lineEdit_Method_Parameters.text() == "" or self.lineEdit_Method_Locals.text() == "" or self.plainTextEdit_Method_PseudoCode.toPlainText() == ""):
			choice = QMessageBox.warning(self, "Warning", f"If you switch methods now any unsaved information will be lost.", QMessageBox.Ok|QMessageBox.Abort)
			if choice == QMessageBox.Abort:
				return

		self.cool = True

		# Updating all the input fields to show the relavent information from the chosen method
		at = self.comboBox_Methods.currentIndex()
		mthd = self.methods[at]

		# Updating the input boxes contents
		self.lineEdit_Method_Name.setText(mthd.name)
		self.plainTextEdit_Method_Description.setPlainText(mthd.description)
		self.lineEdit_Method_Parent.setText(mthd.parent)
		self.lineEdit_Method_Decorators.setText(mthd.decorators)
		self.lineEdit_Method_Parameters.setText(mthd.parameters)
		self.lineEdit_Method_Locals.setText(mthd.local_vars)
		self.plainTextEdit_Method_PseudoCode.setPlainText(mthd.pseudo)


	def add_method(self):
		update = False
		# Checking whether a valid method name has been entered
		if self.lineEdit_Method_Name.text() == "":
			self.manual_ui.DisplayError("Please give the method a name.")
			return
		if self.lineEdit_Method_Name.text().rstrip() in [i[0] for i in self.plan.methods]:
			choice = QMessageBox.warning(self, "Warning","A method with that name already exists. Update the existing method?", QMessageBox.Yes|QMessageBox.No)
			if choice == QMessageBox.No:
				return
			else:
				update = True

		# Creating a new method and adding it to the local and plan lists
		name = self.lineEdit_Method_Name.text().rstrip()
		description = self.plainTextEdit_Method_Description.toPlainText()
		parent = self.lineEdit_Method_Parent.text()
		decorators = self.lineEdit_Method_Decorators.text()
		parameters = self.lineEdit_Method_Parameters.text()
		local_vars = self.lineEdit_Method_Locals.text()
		pseudo = self.plainTextEdit_Method_PseudoCode.toPlainText()

		if update:

			# Updating the information of the method
			for i in self.methods:
				if i.name == name:
					i.description = description
					i.parent = parent
					i.decorators = decorators
					i.parameters = parameters
					i.local_vars = local_vars
					i.pseudo = pseudo
					break
			self.manual_ui.DisplayMessageBox("Method successfully updated.", "Success", QMessageBox.Information)
		else:
			# Creating and adding a new method
			new_method = Method(name, description, parent, decorators, parameters, local_vars, pseudo)

			# Adding the new method to the plan and methods list
			self.methods.append(new_method)
			self.plan.methods.append(new_method.get_info())

			# Updating the combo box
			self.comboBox_Methods.clear()
			for i in self.methods:
				self.comboBox_Methods.addItem(i.name)
			self.cool = False
			self.comboBox_Methods.setCurrentText(new_method.name)
			self.empty = False

			self.manual_ui.DisplayMessageBox("Method successfully added.", "Success", QMessageBox.Information)

# Stored format (Name, Description, Decorators, Parameters, Local Variables, Pseudo Code)
class Functions(QDialog):

	def __init__(self, plan, parent=None):
		super(Functions, self).__init__(parent)
		loadUi("Functions.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.functions = []

		self.empty = True

		# Ensures that the data loss warning message only shows when needed
		self.cool = True

		self.LocalUiSetup()

	def LocalUiSetup(self):

		# Checking whether there were any pre-existing functions
		if len(self.plan.functions) > 0:
			self.empty = False
			self.comboBox_Functions.clear()
			self.comboBox_Functions.addItems([i[0] for i in self.plan.functions])
			for i in self.plan.functions:
				new_function = Function(i[0],i[1],i[2],i[3],i[4],i[5])
				self.functions.append(new_function)

		self.ButtonConnect()
		self.ComboBoxConnect()

	def ButtonConnect(self):
		self.pushButton_Add_Function.clicked.connect(self.add_function)
		self.pushButton_Remove_Function.clicked.connect(self.remove_function)
	def ComboBoxConnect(self):
		self.comboBox_Functions.currentIndexChanged.connect(self.on_function_change) 

	def remove_function(self):

		if self.empty == True:
			self.manual_ui.DisplayError("No functions to remove.")
			return

		# Making sure the user wants to remove the function
		choice = QMessageBox.warning(self, "Warning", f"Are you sure you want to remove function {self.comboBox_Functions.currentText()}?", QMessageBox.Yes|QMessageBox.No)
		if choice == QMessageBox.No:
			return

		# Getting the function to remove
		to_remove = self.comboBox_Functions.currentIndex()

		# Removing the function from memory
		self.functions.pop(to_remove)
		self.plan.functions.pop(to_remove)

		# Removing the function from the combo box
		self.cool = False
		self.comboBox_Functions.removeItem(to_remove)

		# Adding a combo box item to tell the user that there are no functions
		if len(self.functions) == 0:
			self.comboBox_Functions.addItem("No Functions Yet")
			self.empty = True

		self.manual_ui.DisplayMessageBox("Function successfully removed.", "Success", QMessageBox.Information, QMessageBox.Close)

	def on_function_change(self):

		# Checking whether the combo box is empty
		if self.comboBox_Functions.count() == 0 or self.empty == True or len(self.functions) == 0:
			return

		# Making sure that no unsaved changes are lost
		if self.cool == True and len(self.functions) == self.comboBox_Functions.count() and not (self.plainTextEdit_Function_Description.toPlainText() == "" or self.lineEdit_Function_Parent.text() == "" or self.lineEdit_Function_Decorators.text() == "" or self.lineEdit_Function_Parameters.text() == "" or self.lineEdit_Function_Locals.text() == "" or self.plainTextEdit_Function_PseudoCode.toPlainText() == ""):
			choice = QMessageBox.warning(self, "Warning", f"If you switch functions now any unsaved information will be lost.", QMessageBox.Ok|QMessageBox.Abort)
			if choice == QMessageBox.Abort:
				return

		self.cool = True

		# Updating all the input fields to show the relavent information from the chosen function
		at = self.comboBox_Functions.currentIndex()
		func = self.functions[at]

		# Updating the input boxes contents
		self.lineEdit_Function_Name.setText(func.name)
		self.plainTextEdit_Function_Description.setPlainText(func.description)
		self.lineEdit_Function_Decorators.setText(func.decorators)
		self.lineEdit_Function_Parameters.setText(func.parameters)
		self.lineEdit_Function_Locals.setText(func.local_vars)
		self.plainTextEdit_Function_PseudoCode.setPlainText(func.pseudo)

	def add_function(self):
		update = False
		# Checking whether a valid function name has been entered
		if self.lineEdit_Function_Name.text() == "":
			self.manual_ui.DisplayError("Please give the function a name.")
			return
		if self.lineEdit_Function_Name.text().rstrip() in [i[0] for i in self.plan.functions]:
			choice = QMessageBox.warning(self, "Warning","A function with that name already exists. Update the existing function?", QMessageBox.Yes|QMessageBox.No)
			if choice == QMessageBox.No:
				return
			else:
				update = True

		# Creating a new function and adding it to the local and plan lists
		name = self.lineEdit_Function_Name.text().rstrip()
		description = self.plainTextEdit_Function_Description.toPlainText()
		decorators = self.lineEdit_Function_Decorators.text()
		parameters = self.lineEdit_Function_Parameters.text()
		local_vars = self.lineEdit_Function_Locals.text()
		pseudo = self.plainTextEdit_Function_PseudoCode.toPlainText()

		if update:

			# Updating the information of the function
			for i in self.functions:
				if i.name == name:
					i.description = description
					i.parent = parent
					i.decorators = decorators
					i.parameters = parameters
					i.local_vars = local_vars
					i.pseudo = pseudo
					break
			self.manual_ui.DisplayMessageBox("Function successfully updated.", "Success", QMessageBox.Information)
		else:
			# Creating and adding a new function
			new_function = Function(name, description, decorators, parameters, local_vars, pseudo)

			# Adding the new function to the plan and functions list
			self.functions.append(new_function)
			self.plan.functions.append(new_function.get_info())

			# Updating the combo box
			self.comboBox_Functions.clear()
			for i in self.functions:
				self.comboBox_Functions.addItem(i.name)
			self.cool = False
			self.comboBox_Functions.setCurrentText(new_function.name)
			self.empty = False

			self.manual_ui.DisplayMessageBox("Function successfully added.", "Success", QMessageBox.Information)


"""Main Functionality Classes"""

class Plan:

	def __init__(self, path=None):
		self.name = ""
		self.description = dict()
		self.outstanding_ideas = dict()
		self.aim = ""
		self.packages = []
		self.classes = []
		self.methods = []
		self.functions = []
		self.globals = []

		# Stored Fromat [Description, [(Feature_id, Feature)]]
		self.client_request = ["", []]

		self.saved_path = None

		if path:
			self.load(path)

	def load(self, path):

		# Checking whether the user has selected a path
		if path == "":
			return

		# Opening the destination file
		with open(path, "r") as r:

			# Resetting all of the variables

			self.name = ""
			self.description = dict()
			self.outstanding_ideas = dict()
			self.aim = ""
			self.packages = []
			self.classes = []
			self.methods = []
			self.functions = []
			self.globals = []

			# Formatting the file contents

			contents = r.read().split("<>")

			try:
				name = contents[0]
				desc_string = contents[1]
				ideas_string = contents[2]
				aim = contents[3]
				packages_string = contents[4]
				classes_string = contents[5]
				methods_string = contents[6]
				functions_string = contents[7]
				globals_string = contents[8]
				client_request_string = contents[9]
			except Exception as e:
				mui = ManualUIMethods()
				mui.DisplayError(str(e))
				return

			self.name = name

			if not desc_string == "":
				descriptions = desc_string.split("->")
				for desc in descriptions:
					desc = desc.split(">>")

					desc_id = desc[0]
					desc = desc[1]

					self.description[desc_id] = desc

			if not ideas_string == "":
				ideas = ideas_string.split("->")
				for idea in ideas:
					idea = idea.split(">>")

					idea_id = idea[0]
					versions = ast.literal_eval(idea[1])

					self.outstanding_ideas[idea_id] = versions

			self.aim = aim

			if packages_string == "":
				self.packages = []
			else:
				self.packages  = packages_string.split("|")
			if classes_string == "":
				self.classes = []
			else:
				for clss in classes_string.split("|"):
					self.classes.append(list(ast.literal_eval(clss)))
			if methods_string == "":
				self.methods = []
			else:
				for method in methods_string.split("|"):
					self.methods.append(list(ast.literal_eval(method)))
			if functions_string == "":
				self.functions = []
			else:
				for function in functions_string.split("|"):
					self.functions.append(list(ast.literal_eval(function)))
			if globals_string == "":
				self.globals = []
			else:
				for glbl in globals_string.split("|"):
					self.globals.append(list(ast.literal_eval(glbl)))
			if client_request_string == "":
				self.client_request = []
			else:
				client_request_string = client_request_string.split("|")
				self.client_request = [client_request_string[0],[]]

				for feature in client_request_string[1:]:
					self.client_request[1].append(ast.literal_eval(feature))

			self.save_path = path

	def save(self, path):

		# Checking whether the user has selected a path
		if path == "":
			return
		
		# Opening the destination file
		with open(path, "w") as w:

			# Formatting the file contents
			
			desc_string = ""
			ideas_string = ""
			packages_string = ""
			classes_string = ""
			methods_string = ""
			functions_string = ""
			globals_string = ""
			client_request_string = ""

			to_write = []

			to_write.append(self.name)

			for desc_id, desc in list(self.description.items()):
				desc_string += f"{desc_id}>>{desc}->"
			desc_string = desc_string[:-2]
			to_write.append(desc_string)
			
			for idea_id, idea in list(self.outstanding_ideas.items()):
				ideas_string += f"{idea_id}>>{idea}->"
			ideas_string = ideas_string[:-2]
			to_write.append(ideas_string)

			to_write.append(self.aim)

			for pkg in self.packages:
				packages_string += pkg + "|"
			packages_string = packages_string[:-1]

			for clss in self.classes:
				classes_string += str(clss) + "|"
			classes_string = classes_string[:-1]

			for mtd in self.methods:
				methods_string += str(mtd) + "|"
			methods_string = methods_string[:-1]

			for fnc in self.functions:
				functions_string += str(fnc) + "|"
			functions_string = functions_string[:-1]

			for glb in self.globals:
				globals_string += str(glb) + "|"
			globals_string = globals_string[:-1]

			if self.client_request[0] == "" and self.client_request[1] == []:
				client_request_string = ""
			else:
				client_request_string = self.client_request[0]
				for feature in self.client_request[1]:
					client_request_string += "|" + str(feature)

			to_write.append(packages_string)
			to_write.append(classes_string)
			to_write.append(methods_string)
			to_write.append(functions_string)
			to_write.append(globals_string)
			to_write.append(client_request_string)

			to_write = "<>".join(to_write)

			w.write(to_write)

		self.save_path = path

	def export(self, path):

		# Checking whether the user has selected a path
		if path == "":
			return

		# Formatting the file contents

		doc = Document()
		doc.preamble.append(Command('title', self.name))
		doc.append(NoEscape(r'\maketitle'))

		with doc.create(Section("Client Request")):
			if self.client_request == []:
				with doc.create(Itemize()) as itemize:
					itemize.add_item("This plan has no client request")
					itemize.append(Command("ldots"))
			with doc.create(Subsection("Description")):
				with doc.create(Itemize()) as itemize:
						itemize.add_item(self.client_request[0])
						itemize.append(Command("ldots"))
			with doc.create(Subsection("Features")):
				for feature in self.client_request[1:]:
					feature_id,feature_desc = feature
					with doc.create(Subsubsection(feature_id)):
						with doc.create(Itemize()) as itemize:
							itemize.add_item(feature_desc)
							itemize.append(Command("ldots"))
		with doc.create(Section("Program Description")):
			if self.description == "":
				with doc.create(Itemize()) as itemize:
					itemize.add_item("This plan has no description")
					itemize.append(Command("ldots"))
			for desc_id, desc in list(self.description.items()):
				with doc.create(Subsection(desc_id)):
					with doc.create(Itemize()) as itemize:
						itemize.add_item(desc)
						itemize.append(Command("ldots"))

		with doc.create(Section("Outstanding Ideas")):
			if len(self.outstanding_ideas) == 0:
				with doc.create(Itemize()) as itemize:
					itemize.add_item("This plan has no outstanding ideas")
					itemize.append(Command("ldots"))
			for idea_id, versions in list(self.outstanding_ideas.items()):
				with doc.create(Subsection("Idea " + idea_id)):
					for i in range(len(versions.items())):
						version_id, version = list(versions.items())[i]
						with doc.create(Subsubsection("Version " + str(version_id))):
							with doc.create(Itemize()) as itemize:
								itemize.add_item(version)
								itemize.append(Command("ldots"))
		
		with doc.create(Section("Program Aim")):
			with doc.create(Itemize()) as itemize:
				if self.aim == "":
					itemize.add_item("This plan has no aim")
				else:
					itemize.add_item(self.aim)
				itemize.append(Command("ldots"))

		with doc.create(Section("Packages Required")):
			with doc.create(Itemize()) as itemize:
				if len(self.packages) == 0:
					itemize.add_item("This program imports no packages")
				for package in self.packages:
					itemize.add_item(package)
				itemize.append(Command("ldots"))

		with doc.create(Section("Global Variables")):
			with doc.create(Itemize()) as itemize:
				if len(self.globals) == 0:
					itemize.add_item("This program has no global variables")
				for glbl in self.globals:
					itemize.add_item(glbl)
				itemize.append(Command("ldots"))

		with doc.create(Section("Classes")):
			if len(self.classes) == 0:
				with doc.create(Itemize()) as itemize:
					doc.append("This program has no classes")
					itemize.append(Command("ldots"))
			for clss in self.classes:
				name = clss[0]
				description = clss[1]
				inherits = clss[2]
				parameters = clss[3]
				attributes = clss[4]
				methods = clss[5]

				with doc.create(Subsection(f"Class {name}")):
					with doc.create(Subsubsection("Description")):
						with doc.create(Itemize()) as itemize:
							doc.append(description)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Inherits")):
						with doc.create(Itemize()) as itemize:
							doc.append(inherits)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Parameters")):
						with doc.create(Itemize()) as itemize:
							doc.append(parameters)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Attributes")):
						with doc.create(Itemize()) as itemize:
							doc.append(attributes)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Methods")):
						with doc.create(Itemize()) as itemize:
							doc.append(methods)
							itemize.append(Command("ldots"))

		with doc.create(Section("Methods")):
			if len(self.methods) == 0:
				with doc.create(Itemize()) as itemize:
					doc.append("This program has no methods")
					itemize.append(Command("ldots"))
			for method in self.methods:

				name = method[0]
				description = method[1]
				parent_class = method[2]
				decorators = method[3]
				parameters = method[4]
				local_variables = method[5]
				pseudo_code = method[6]

				with doc.create(Subsection(f"Method {name}")):
					with doc.create(Subsubsection("Description")):
						with doc.create(Itemize()) as itemize:
							doc.append(description)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Parent Class")):
						with doc.create(Itemize()) as itemize:
							doc.append(parent_class)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Decorators")):
						with doc.create(Itemize()) as itemize:
							doc.append(decorators)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Parameters")):
						with doc.create(Itemize()) as itemize:
							doc.append(parameters)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Local Variables")):
						with doc.create(Itemize()) as itemize:
							doc.append(methods)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Pseudo Code")):
						with doc.create(Itemize()) as itemize:
							doc.append(pseudo_code)
							itemize.append(Command("ldots"))

		# Stored format (Name, Description, Decorators, Parameters, Local Variables, Pseudo Code)
		with doc.create(Section("Functions")):
			if len(self.functions) == 0:
				with doc.create(Itemize()) as itemize:
					doc.append("This program has no functions")
					itemize.append(Command("ldots"))
			for function in self.functions:

				name = function[0]
				description = function[1]
				decorators = function[2]
				parameters = function[3]
				local_variables = function[4]
				pseudo_code = function[5]

				with doc.create(Subsection(f"Function {name}")):
					with doc.create(Subsubsection("Description")):
						with doc.create(Itemize()) as itemize:
							doc.append(description)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Decorators")):
						with doc.create(Itemize()) as itemize:
							doc.append(decorators)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Parameters")):
						with doc.create(Itemize()) as itemize:
							doc.append(parameters)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Local Variables")):
						with doc.create(Itemize()) as itemize:
							doc.append(methods)
							itemize.append(Command("ldots"))
					with doc.create(Subsubsection("Pseudo Code")):
						with doc.create(Itemize()) as itemize:
							doc.append(pseudo_code)
							itemize.append(Command("ldots"))

		try:
			doc.generate_pdf(path, compiler='pdfLaTeX')
		except Exception as e:
			print(str(e))

class Connection:

	def __init__(self):
		pass

class ToDo:

	def __init__(self):
		pass

class ClientRequest(QDialog):

	def __init__(self, plan, parent=None):
		super(ClientRequest, self).__init__(parent)
		loadUi("ClientRequest.ui", self)

		self.manual_ui = ManualUIMethods()

		self.plan = plan

		self.empty = True
		self.cool = True
		self.warn = True

		self.plainTextEditProgram_Description.setPlainText(self.plan.client_request[0])
		for feature_id, feature_desc in self.plan.client_request[1]:
			self.add_feature(feature_id, feature_desc)

		self.LocalUiSetup()

	def LocalUiSetup(self):
		self.ButtonConnect()
		self.ComboBoxConnect()

	def ButtonConnect(self):
		self.pushButtonSet_Description.clicked.connect(self.set_description)
		self.pushButtonAdd_Feature.clicked.connect(self.add_feature)
		self.pushButtonRemove_Feature.clicked.connect(self.remove_feature)

	def ComboBoxConnect(self):
		self.comboBoxFeatures.currentIndexChanged.connect(self.on_feature_change)

	def on_feature_change(self):
		
		if self.empty == True or self.cool == True:
			return

		if self.warn == True:
			# Making sure the user knows that the feature description and ID fields will change
			choice = QMessageBox.warning(self, "Warning", "When changing the feature any unsaved changes will be lost. Continue?", QMessageBox.Yes|QMessageBox.No)
			if choice == QMessageBox.No:
				return

		new_feature_id = self.comboBoxFeatures.currentText()

		# Getting the feature description based on the ID
		for feature_id, feature_desc in self.plan.client_request[1]:
			if feature_id == new_feature_id:
				new_feature_desc = feature_desc
				break
			new_feature_desc = ""

		# Updating the entry fields with the new feature ID and description
		self.lineEditFeature_ID.setText(new_feature_id)
		self.plainTextEditFeature_Description.setPlainText(new_feature_desc)

	def set_description(self):
		
		# Setting the plans description to the text in the entry box
		if self.plan.client_request == []:
			self.plan.client_request = [self.plainTextEditProgram_Description.toPlainText(), []]
		else:
			self.plan.client_request[0] = self.plainTextEditProgram_Description.toPlainText()

	def add_feature(self, feature_id=False, feature_desc=False):


		# Defining the feature components
		if feature_id == False:
			feature_id = self.lineEditFeature_ID.text()
		if feature_desc == False:
			feature_desc = self.plainTextEditFeature_Description.toPlainText()


		# Checking whether the feature has a description and 
		if feature_id == "":
			self.manual_ui.DisplayError("Please give the feature an ID.")
			return
		if feature_desc == "":
			self.manual_ui.DisplayError("Please give the feature a description.")
			return
		if feature_id in [f_id for f_id, _ in self.plan.client_request[1]]:
			self.manual_ui.DisplayError("A feature with that name already exists.")
			return

		self.empty = False

		# Updating the client_request list in the plan and the feature combobox
		self.plan.client_request[1].append((feature_id, feature_desc))
		self.cool = True
		self.comboBoxFeatures.clear()
		self.comboBoxFeatures.addItems([f_id for f_id, _ in self.plan.client_request[1]])
		self.comboBoxFeatures.setCurrentIndex(self.comboBoxFeatures.count()-1)
		self.cool = False


	def remove_feature(self):
		
		# Checking whether there are any features to remove
		if self.empty == True:
			self.manual_ui.DisplayError("No features to remove.")
			return

		feature_index = self.comboBoxFeatures.currentIndex()

		# Removing the feature from the plan and combobox
		self.warn = False
		self.comboBoxFeatures.removeItem(feature_index)
		self.plan.client_request[1].pop(feature_index)
		self.warn = True

		# Making sure the program knows that there are no features
		if self.comboBoxFeatures.count() == 0:
			self.empty = True
			self.comboBoxFeatures.addItem("No Features Yet")


class Class:

	def __init__(self, name, description, inherits, parameters, attributes, methods):
		self.name = name
		self.description = description
		self.inherits = inherits
		self.parameters = parameters
		self.attributes = attributes
		self.methods = methods

	def get_info(self):
		return (self.name, self.description, self.inherits, self.parameters, self.attributes, self.methods)

class Method:
	
	def __init__(self, name, description, parent, decorators, parameters, local_vars, pseudo):
		self.name = name
		self.description = description
		self.parent = parent
		self.decorators = decorators
		self.parameters = parameters
		self.local_vars = local_vars
		self.pseudo = pseudo

	def get_info(self):
		return (self.name, self.description, self.parent, self.decorators, self.parameters, self.local_vars, self.pseudo)

class Function:

	def __init__(self, name, description, decorators, parameters, local_vars, pseudo):
		self.name = name
		self.description = description
		self.decorators = decorators
		self.parameters = parameters
		self.local_vars = local_vars
		self.pseudo = pseudo

	def get_info(self):
		return (self.name, self.description, self.decorators, self.parameters, self.local_vars, self.pseudo)


"""Other"""

class ManualUIMethods(QMainWindow):

	def __init__(self):
		pass

	def DisplayMessageBox(self, message, title, icon=QMessageBox.NoIcon, button=QMessageBox.Ok):
		msg = QMessageBox()
		msg.setText(message)
		msg.setWindowTitle(title)
		msg.setIcon(icon)
		msg.setDefaultButton(button)
		msg.exec_()
	def DisplayError(self, message):
		self.DisplayMessageBox(message, "Error", QMessageBox.Critical, QMessageBox.Close)
	def ClearLayout(self, currentLayout):
		if currentLayout is not None:
			while currentLayout.count():
				item = currentLayout.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.ClearLayout(item.layout())
	def ComboBox(self, items=None, font=None, connection=None):
		comboBox = QComboBox()
		if not font == None:
			comboBox.setFont(font)
		if not items == None:
			comboBox.addItems(items)
		if not connection == None:
			comboBox.currentIndexChanged.connect(connection)
		return comboBox
	def SpinBox(self, font=None, minimum=None, maximum=None):
		spinBox = QSpinBox()
		if not font == None:
			spinBox.setFont(font)
		if not minimum == None:
			spinBox.setMinimum(minimum)
		if not maximum == None:
			spinBox.setMaximum(maximum)
		return spinBox
	def LineEdit(self, placeHolderText=None, font=None):
		lineEdit = QLineEdit()
		if not placeHolderText == None:
			lineEdit.setPlaceholderText(placeHolderText)
		if not font == None:
			lineEdit.setFont(font)
		return lineEdit
	def PushButton(self, connection=None, text=None, font=None):
		pushButton = QPushButton()
		if not connection == None:
			pushButton.clicked.connect(connection)
		if not text == None:
			pushButton.setText(text)
		if not font == None:
			pushButton.setFont(font)
		return pushButton
	def Layout(self, lType, widgets):
		layoutTypes = [QHBoxLayout, QVBoxLayout, QGridLayout]
		layout = lType
		for i in widgets:
			if type(i) is tuple:
				if i[0] == "s":
					layout.addStretch(i[1])
			elif i == "s":
				layout.addStretch()
			elif i.isWidgetType():
				layout.addWidget(i)
			elif type(i) in layoutTypes:
				layout.addLayout(i)
		return layout

def window():

	windowStack = ("main")

	app = QApplication(sys.argv)
	stack = QStackedWidget()

	main = Main(stack, windowStack)

	stack.addWidget(main)
	stack.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	window()