from argparse import Action
import email
from flask_wtf import FlaskForm
from wtforms import (
	StringField, SelectField, DateField, SubmitField, PasswordField, BooleanField, 
	ValidationError, TextAreaField, HiddenField, FileField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import widgets, SelectMultipleField
from wtforms_components import TimeField, DateRange
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from datetime import datetime, date, time

class MultiCheckboxField(SelectMultipleField):
	widget = widgets.TableWidget()
	option_widget = widgets.CheckboxInput()

###################################
#ADMIN USERS (Add/Update, Delete) #
###################################
class UserForm(FlaskForm):
	pass
class DeleteUserForm(FlaskForm):
	pass

########################################
#ADMIN FACILITIES (Add/Update, Delete) #
########################################
class FacilityForm(FlaskForm):
	pass
class DeleteFacilityForm(FlaskForm):
	pass

###################################
#ADMIN ROLES (Add/Update, Delete) #
###################################
class RoleForm(FlaskForm):
	pass
class DeleteRoleForm(FlaskForm):
	pass

#################################################
#BLOCKS (Add/Update, Delete, Duplicate, Share) #
#################################################
class BlockForm(FlaskForm):
	title = StringField("Title:", validators=[DataRequired(),Length(min=5, max=50)])
	season = SelectField("Season:", choices=[('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall')], validators=[DataRequired()])
	year = SelectField(u"Year:", choices=[(n, n) for n in range(date.today().year, date.today().year+5)], validators=[DataRequired()])
	additional_info = CKEditorField("Additional Information:", validators=[])
	submit_block = SubmitField(label=None)
class DeleteBlockForm(FlaskForm):
	delete_block_id = HiddenField("block_id", validators=[DataRequired()])
	delete_block = SubmitField("Yes, Delete!")
class DuplicateBlockForm(FlaskForm):
	duplicate_block_id = HiddenField("block_id", validators=[DataRequired()])
	duplicate_block = SubmitField("Yes, Make a Copy!")

###############################
#MEMBERS (Add/Delete, Update) #
###############################
class MembersForm(FlaskForm):
	members = MultiCheckboxField(label=None)
	submit_members = SubmitField("Save")
class AssignMembersForm(FlaskForm):
	member_id = HiddenField("block_id", validators=[DataRequired()])
	new_role = SelectField("Season:", choices=[('Owner','Owner'),('Manager','Manager'),('Organizer','Organizer'),('Participant','Participant')], validators=[DataRequired()])
	submit_role = SubmitField("Save")

#######################
#COLLABORATORS (Add, Delete) #
#######################
class AddCollaboratorForm(FlaskForm):
	first_name = StringField("First Name", validators=[DataRequired(),Length(min=1, max=50)])
	last_name = StringField("Last Name", validators=[DataRequired(),Length(min=1, max=50)])
	email = StringField("Email", validators=[DataRequired(),Email()])
	initials = StringField("Initials", validators=[DataRequired(),Length(min=2, max=6)])
	notes = TextAreaField("Notes")
	submit = SubmitField("Add")
class DeleteCollaboratorForm(FlaskForm):
	collaborator_id = HiddenField("id", validators=[DataRequired()])
	submit_delete_collaborator = SubmitField("Yes, Delete!")

#############################
#EVENTS (Add/Update, Delete) #
#############################
class EventForm(FlaskForm):
	date = DateField("Date:", validators=[DataRequired()])
	start_time = TimeField("Start-Time:", validators=[DataRequired()])
	end_time = TimeField("End-Time:", validators=[DataRequired()])
	format = SelectField("Format:", choices=[('Lab', 'Lab'), ('Lecture', 'Lecture'), ('Assignment', 'Assignment'), ('Testing', 'Assessment/Exam/Quiz')], validators=[DataRequired()])
	topic = StringField("Topic:", validators=[DataRequired(), Length(min=3, max=100)])
	notes = TextAreaField("Notes")
	attendance = BooleanField("Attendence")
	submit_event = SubmitField(label=None)
	def validate_end_time(self, filed):
		t1 = datetime.strptime(f"1983-03-25 {filed.data}", "%Y-%m-%d %H:%M:%S")
		t2 = datetime.strptime(f"1983-03-25 {self.start_time.data}", "%Y-%m-%d %H:%M:%S")
		if (t1 < t2):
			raise ValidationError("End-Time must be later than Start-Time.")
		return True
class DeleteEventForm(FlaskForm):
	event_id = HiddenField("id", validators=[DataRequired()])
	delete_event = SubmitField("Yes, Delete!")

#####################
#ATTENDEES (Update) #
#####################
class AttendeesForm(FlaskForm):
	attendees = MultiCheckboxField(label=None)
	submit_attendees = SubmitField("Save")

#####################
#Locations (Update) #
#####################
class LocationsForm(FlaskForm):
	locations = MultiCheckboxField(label=None)
	submit_locations = SubmitField("Save")

## WTForms Fields
# BooleanField
# DateField
# DateTimeField
# DecimalField
# FileField
# HiddenField
# MultipleField
# FieldList
# FloatField
# FormField
# IntegerField
# PasswordField
# RadioField
# SelectField
# SelectMultipleField
# SubmitField
# StringField
# TextAreaField

## Validators
# DataRequired
# Email
# EqualTo
# InputRequired
# IPAddress
# Length
# MacAddress
# NumberRange
# Optional
# Regexp
# URL
# UUID
# AnyOf
# NoneOf
