#!/usr/bin/env python

from flask import Flask, flash, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from webforms import (
    UserForm, DeleteUserForm, FacilityForm, DeleteFacilityForm, RoleForm, DeleteRoleForm,
    BlockForm, DeleteBlockForm, DuplicateBlockForm,
    MembersForm, AssignMembersForm, AddCollaboratorForm, DeleteCollaboratorForm,
    EventForm, DeleteEventForm,
    AttendeesForm,
    LocationsForm,
)
from models import users, facilities, blocks, events, memberships, collaborators, roles
from flask_migrate import Migrate
#from flask_talisman import Talisman
import msal
import app_config
from datetime import datetime, timedelta


app = Flask(__name__)
ckeditor = CKEditor(app)

app.config.from_object(app_config)

# db.init_app(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buildingblocks.db'
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

migrate = Migrate(app, db)

Session(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    initials = db.Column(db.String(3), nullable=False, unique=True)
    emp_typ = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_admin = db.Column(db.Boolean(), nullable=False)
    
    membership = db.relationship('Membership', backref='user')

    def __repr__(self):
         return '<Name %r>' % self.first_name


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    view_block = db.Column(db.Boolean(), nullable=False)
    update_block = db.Column(db.Boolean(), nullable=False)
    delete_block = db.Column(db.Boolean(), nullable=False)
    duplicate_block = db.Column(db.Boolean(), nullable=False)
    export_block = db.Column(db.Boolean(), nullable=False)
    select_members = db.Column(db.Boolean(), nullable=False)
    assign_members = db.Column(db.Boolean(), nullable=False)
    view_events = db.Column(db.Boolean(), nullable=False)
    add_events = db.Column(db.Boolean(), nullable=False)
    update_events = db.Column(db.Boolean(), nullable=False)
    delete_events = db.Column(db.Boolean(), nullable=False)
    select_attendees = db.Column(db.Boolean(), nullable=False)
    select_locations = db.Column(db.Boolean(), nullable=False)
    delete_events_limited = db.Column(db.Boolean(), nullable=False)
    update_events_limited = db.Column(db.Boolean(), nullable=False)
    select_attendees_limited = db.Column(db.Boolean(), nullable=False)
    select_locations_limited = db.Column(db.Boolean(), nullable=False)

    membership = db.relationship('Membership', backref='role')


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(50), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    additional_info = db.Column(db.String(3), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    location = db.relationship('Location', backref='facility')


class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    season = db.Column(db.String(6), nullable=False)
    additional_info = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    membership = db.relationship('Membership', backref='block')
    collaborator = db.relationship('Collaborator', backref='block')
    event = db.relationship('Event', backref='block')


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class Collaborator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    initials = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    notes = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
    start_datetime = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    format = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text)
    attendance_required = db.Column(db.Boolean(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    attendee = db.relationship('Attendee', backref='event')
    guest = db.relationship('Guest', backref='event')
    location = db.relationship('Location', backref='event')


class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    collaborator_id = db.Column(db.Integer, db.ForeignKey('collaborator.id'))

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))


# SAVING FOR LATER
# from flask import Response
# from flask import Flask, make_response  
# construct your app
# @app.route("/get-file")
# def get_file():
#     content = bytes(str(users), 'utf-8')
#     return Response(content, 
#             mimetype='application/json',
#             headers={'Content-Disposition':'attachment;filename=export.json'})
# @app.route('/csv/')  
# def download_csv():  
#     csv = 'foo,bar,baz\nhai,bai,crai\n'  
#     response = make_response(csv)
#     cd = 'attachment; filename=mycsv.csv'
#     response.headers['Content-Disposition'] = cd 
#     response.mimetype='text/csv'
#     return response


# user = Users.query.filter_by(email=form.email.data).first()
#     if user is None:
#         user = Users(name=form.name.data, email=form.email.data)
#         db.session.add(user)
#         db.session.commit()
#     name = form.name.data
#     form.name.data = ''
#     form.email.data = ''


@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    #Fetch user.id of users where (session.get("user").get("preferred_username") == user.email)
    return redirect(url_for("user", user_id=session.get("user").get("oid")))

@app.route("/admin")
def admin():
    if not session.get("user"):
        return redirect(url_for("login"))
    #check user email with users in user database
    #if user.is_admin == true, then allow access
    user_form = UserForm()
    delete_user_form = DeleteUserForm()
    facility_form = FacilityForm()
    delete_facility_form = DeleteFacilityForm()
    role_form = RoleForm()
    delete_role_form_ = DeleteRoleForm()
    return render_template("admin.html", user=session["user"], users=users, facilities=facilities, roles=roles)

# BLOCK MEMBERSHIPS: Landing page which displays all blocks available to the logged in user
## Links on this page: all blocks available to the logged in user
### Forms on this page: add block
#### Future forms: import block
@app.route("/user/<user_id>")
def user(user_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    #if the email address of the user with the user_id provided
    #if it doesn't match the session email add
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    #Fetch All memberships where (membership.user_id == user.id), return block_list
    #Fetch All blocks where (block.id == block_list.block_id), 
    #Display blocks
    #Else if user.is_admin = true then display everything
    memberships = memberships

    block_form = BlockForm()
    block_form.title.data = None
    block_form.year.data = None
    block_form.season.data = None
    block_form.additional_info.data = None
    block_form.submit_block.label.text = "Create"
    block_action_url = f'/user/{user_id}/block/add'
    return render_template("user.html", user=session["user"], blocks=blocks, 
        block_form=block_form, block_action_url=block_action_url)


# BLOCK DETAILS (BLOCK ID): Displays details on a single block
## Links on this page: breadcrumbs, all events that have been added to the block
### Forms on this page: update/delete/duplicate/share block, update members, add events
#### Future forms: import events
@app.route("/user/<user_id>/block/<block_id>")
def block(user_id, block_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    
    #Fetch block in blocks where (block.block_id == url.block_id)
    block = blocks[int(block_id)]
    members = block["members"]
    events = block["events"]

    #Fetch role_id where (permissions.block_id == blocks.block_id) and (session.user_id == permissions>user_id)
    #If (permissions.role_id == role.role_id) where (role.title == 'admin') then [all tools]
    #Else If (permissions.role_id == roles.role_id) where (role.title == 'owner') then
    #Else If (permissions.role_id == roles.role_id) where (role.title == 'manager') then
    #Else If (permissions.role_id == roles.role_id) where (role.title == 'editor') then
    #Else If (permissions.role_id == roles.role_id) where (role.title == 'viewer') then [disable everything but view]
    #Fetch All members where member>block_id is equal to url>block_id
    #Display if permissions allow
    #Fetch events where events>block_id is equal to url_block_id
    #convert stored data to human readable data
    for event in events:
        event["date"] = event["start_datetime"].strftime("%m/%d/%Y")
        event["day"] = event["start_datetime"].strftime("%A")
        event["start_time"] = event["start_datetime"].strftime("%I:%M%p")
        event["end_time"] = (event["start_datetime"] + timedelta(minutes = event["duration"])).strftime("%I:%M%p")
        #Display if permissions allow
    
    #load forms if permissions allow
    block_form = BlockForm()
    block_form.title.data = block["title"]
    block_form.season.data = block["season"]
    block_form.year.data = block["year"]
    block_form.additional_info.data = block["additional_info"]
    block_form.submit_block.label.text = "Update"
    block_action_url = f"/user/{user_id}/block/update/{block_id}"
    
    delete_block_form = DeleteBlockForm()
    delete_block_form.delete_block_id.data = block["id"]

    duplicate_block_form = DuplicateBlockForm()
    duplicate_block_form.duplicate_block_id.data = block["id"]
    
    members_form = MembersForm()
    member_options = [(n["id"],f"{n['last_name']}, {n['first_name']} ({n['email']})") for n in users]
    member_defaults = [n["id"] for n in members]
    members_form.members.choices = member_options
    members_form.members.default = member_defaults
    members_form.process()

    assign_members_form = AssignMembersForm()

    add_collaborator_form = AddCollaboratorForm()
    delete_collaborator_form = DeleteCollaboratorForm()
    
    event_form = EventForm()
    event_form.submit_event.label.text = "Create"
    event_action_url = f"/user/{user_id}/block/{block_id}/event/add"
    
    return render_template('block.html', users=users, user=session["user"],
        block=block, block_action_url=block_action_url, block_form=block_form, delete_block_form=delete_block_form, 
        duplicate_block_form=duplicate_block_form, members_form=members_form, assign_members_form=assign_members_form,
        collaborators=collaborators, add_collaborator_form=add_collaborator_form, delete_collaborator_form=delete_collaborator_form,
        event_form=event_form, event_action_url=event_action_url
    )


#BLOCK EVENT (EVENT ID): Displays details on a single event within a block
## Links on this page: breadcrumbs
### Forms on this page: update/delete event, update attendees, add/delete location
@app.route("/user/<user_id>/block/<block_id>/event/<event_id>")
def event(user_id, block_id, event_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    
    block = blocks[int(block_id)]
    members = block["members"]
    events = block["events"]

    event = events[int(event_id)]
    attendees = event["attendees"]
    locations = event["locations"]
    
    #convert stored data to human readable data
    event["date"] = event["start_datetime"].strftime("%m/%d/%Y")
    event["day"] = event["start_datetime"].strftime("%A")
    event["start_time"] = event["start_datetime"].strftime("%I:%M%p")
    event["end_time"] = (event["start_datetime"] + timedelta(minutes = event["duration"])).strftime("%I:%M%p")
    #Fetch event where events>event_id = url>event_id and events>event_id>block_id is =
    #Fetch block where blocks>block_id is equal to url>block_id
    #Fetch role_id where permissions>block_id is equal to blocks>block_id and session>user_id is equal to permissions>user_id
    #If permissions>role_id is equal to role>role_id where role>title is equal to 'admin' then [all tools]
    #Else If permissions>role_id is equal to role>role_id where role>title is equal to 'owner' then
    #Else If permissions>role_id is equal to role>role_id where role>title is equal to 'manager' then
    #Else If permissions>role_id is equal to role>role_id where role>title is equal to 'editor' then
    #Else If permissions>role_id is equal to role>role_id where role>title is equal to 'viewer' then [disable everything]
    #Fetch attendees where attendees>event_id is equal to url>event_id
    #load forms as necessary based on permissions
    #populate form appropriate data (see datetime fields) from stored data
    event_form = EventForm()
    event_form.date.data = event["start_datetime"]
    event_form.start_time.data = event["start_datetime"]
    event_form.end_time.data = (event["start_datetime"] + timedelta(minutes = event["duration"]))
    event_form.format.data = event["format"]
    event_form.topic.data = event["topic"]
    event_form.notes.data = event["notes"]
    event_form.attendance.data = event["attendance"]
    event_form.submit_event.label.text = "Update"
    event_action_url = f"/user/{user_id}/block/{block_id}/event/update/{event_id}"

    delete_event_form = DeleteEventForm()
    delete_event_form.event_id.data = event["id"]
    
    attendees_form = AttendeesForm()
    attendee_options = [(n["id"],f"{n['last_name']}, {n['first_name']} ({n['email']})") for n in members]
    attendee_defaults = [n["id"] for n in attendees]
    attendees_form.attendees.choices = attendee_options
    attendees_form.attendees.default = attendee_defaults
    attendees_form.process()

    locations_form = LocationsForm()
    locations_options = [(n["id"],f"Building: {n['building']} > Room: {n['room']}") for n in facilities]
    locations_defaults = [n["id"] for n in locations]
    locations_form.locations.choices = locations_options
    locations_form.locations.default = locations_defaults
    locations_form.process()

    return render_template('event.html', user=session["user"], block=block, event=event, 
        event_form=event_form, event_action_url=event_action_url, delete_event_form=delete_event_form,
        attendees_form=attendees_form, locations_form=locations_form)





#######  ######  ######  #     #  ######
#        #    #  #    #  ##   ##  #
#######  #    #  ######  # # # #  ######
#        #    #  #  #    #  #  #       #
#        ######  #   #   #     #  ######

#########################
# BLOCKS FORMS HANDLING #
#########################
@app.route("/user/<user_id>/block/add", methods=["POST"])
def add_block(user_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    block_form = BlockForm(request.form)
    if block_form.validate_on_submit():
        #collect data from form
        title = block_form.title.data
        season = block_form.season.data
        year = block_form.year.data
        additional_info = block_form.additional_info.data
        #add to database
        blocks.append({
            'id': '1',
            'title': title,
            'year': year,
            'season': season,
            'additional_info':additional_info,
            'date_added':datetime.now(),
            'date_modified':datetime.now(),
            'created_by':session.get("user").get("name"),
            'modified_by':session.get("user").get("name"),
            'events': []
        })
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> A new block was added sucessfully!", 'success')
        return redirect(url_for("user", user_id=user_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {block_form.errors}", 'danger')
    return redirect(url_for("user", user_id=user_id), code=303)

@app.route("/user/<user_id>/block/update/<block_id>", methods=["POST"])
def update_block(user_id, block_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    block_form = BlockForm(request.form)
    if block_form.validate_on_submit():
        #collect data from form
        title = block_form.title.data
        season = block_form.season.data
        year = block_form.year.data
        additional_info = block_form.additional_info.data
        #update database
        blocks[int(block_id)] = {
            'id': int(block_id),
            'title': title,
            'year': year,
            'season': season,
            'additional_info':additional_info,
            'date_added':'July 8, 2022 at 10:15am',
            'date_modified':'July 8, 2022 at 10:15am',
            'created_by':'Bailey, Cameron',
            'modified_by':'Bailey, Cameron',
        }
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Block was updated sucessfully!", 'success')
        return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {block_form.errors}", 'danger')
    return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)

@app.route("/user/<user_id>/block/delete/<block_id>", methods=["POST"])
def delete_block(user_id, block_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    delete_block_form = DeleteBlockForm(request.form)
    if delete_block_form.validate_on_submit():
        block_id = delete_block_form.delete_block_id.data
        #remove block from database
        blocks.pop(
            int(block_id)
        )
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Block was deleted sucessfully!", 'success')
        return redirect(url_for("user", user_id=user_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {delete_block_form.errors}", 'danger')
    return redirect(url_for("user", user_id=user_id), code=303)

@app.route("/user/<user_id>/block/duplicate/<block_id>", methods=["POST"])
def duplicate_block(user_id, block_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    duplicate_block_form = DuplicateBlockForm(request.form)
    if duplicate_block_form.validate_on_submit():
        # block_id = duplicate_block_form.duplicate_block_id.data
        #make a copy of the block and all events
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Block was duplicated sucessfully!", 'success')
        return redirect(url_for("user", user_id=user_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {duplicate_block_form.errors}", 'danger')
    return redirect(url_for("user", user_id=user_id), code=303)


##########################
# MEMBERS FORMS HANDLING #
##########################
@app.route("/user/<user_id>/block/<block_id>/members/update", methods=["POST"])
def add_member(user_id, block_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    block = blocks[int(block_id)]
    members = block["members"]

    members_form = MembersForm(request.form)
    member_options = [(n["id"],f"<{n['last_name']}, {n['first_name']}> {n['email']}") for n in users]
    # member_defaults = [(n["id"],f"<{n['last_name']}, {n['first_name']}> {n['email']}") for n in members]
    members_form.members.choices = member_options

    if members_form.validate_on_submit():
        members_update = []
        for m in members_form.members.data:
            members_update.append({
                "id":users[int(m)],
                "first_name": users[int(m)]["first_name"],
                "last_name": users[int(m)]["last_name"],
                "email": users[int(m)]["email"],
                "initials": users[int(m)]["initials"],
                "type": users[int(m)]["type"]
            })
        block["members"] = members_update
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Block members list was updated sucessfully!", 'success')
        return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {members_form.errors} ", 'danger')
    return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)

@app.route("/user/<user_id>/block/<block_id>/member/<member_id>/role/update", methods=["POST"])
def assign_member(user_id, block_id, member_id):
    print(member_id)
    flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Block members list was updated sucessfully!", 'success')
    return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)


########################
# GUEST FORMS HANDLING #
########################
@app.route("/user/<user_id>/block/<block_id>/guest/add", methods=["POST"])
def add_guest(user_id, block_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index")) 
    add_collaborator_form = AddCollaboratorForm(request.form)
    if add_collaborator_form.validate_on_submit():
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> A new guest was added sucessfully!", 'success')
        return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {add_collaborator_form.errors} ", 'danger')
    return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)

@app.route("/user/<user_id>/block/<block_id>/guest/delete/<guest_id>", methods=["POST"])
def delete_guest(user_id, block_id, guest_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    print(guest_id) 
    delete_collaborator_form = DeleteCollaboratorForm(request.form)
    if delete_collaborator_form.validate_on_submit():
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> A new guest was added sucessfully!", 'success')
        return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {delete_collaborator_form.errors} ", 'danger')
    return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)


#########################
# EVENTS FORMS HANDLING #
#########################
@app.route("/user/<user_id>/block/<block_id>/event/add", methods=["POST"])
def add_event(user_id, block_id):    
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    
    event_form = EventForm(request.form)
    if event_form.validate_on_submit():
        #collect values from form and convert to storable data
        event_start_datetime = datetime.strptime(f"{event_form.date.data} {event_form.start_time.data}", "%Y-%m-%d %H:%M:%S")  
        event_end_datetime = datetime.strptime(f"{event_form.date.data} {event_form.end_time.data}", "%Y-%m-%d %H:%M:%S") 
        event_duration = (event_end_datetime - event_start_datetime).seconds / 60
        event_format = event_form.format.data
        event_topic = event_form.topic.data
        event_notes = event_form.notes.data
        event_attendance = event_form.attendance.data
        #add to database
        block = blocks[int(block_id)]
        block["events"].append({ 
            "id":1,
            "start_datetime": event_start_datetime,
            "duration": event_duration,
            "format":event_format,
            "topic":event_topic,
            "notes":event_notes,
            "attendance":event_attendance,
            "attendees": [],
            "locations":[]
        })
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Event was added sucessfully!", 'success')
        return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {event_form.errors} ", 'danger')
    return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)

@app.route("/user/<user_id>/block/<block_id>/event/update/<event_id>", methods=["POST"])
def update_event(user_id, block_id, event_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    event_form = EventForm(request.form)
    if event_form.validate_on_submit():
        #collect values from form and convert to storable data
        event_start_datetime = datetime.strptime(f"{event_form.date.data} {event_form.start_time.data}", "%Y-%m-%d %H:%M:%S")  
        event_end_datetime = datetime.strptime(f"{event_form.date.data} {event_form.end_time.data}", "%Y-%m-%d %H:%M:%S") 
        event_duration = (event_end_datetime - event_start_datetime).seconds / 60
        event_format = event_form.format.data
        event_topic = event_form.topic.data
        event_notes = event_form.notes.data
        event_attendance = event_form.attendance.data
        #update event in database
        block = blocks[int(block_id)]
        block["events"][int(event_id)] = { 
            "id":event_id,
            "start_datetime": event_start_datetime,
            "duration": event_duration,
            "format":event_format,
            "topic":event_topic,
            "notes":event_notes,
            "attendance":event_attendance,
            "attendees": [],
            "locations":[]
        }
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Event was updated sucessfully!", 'success')
        return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {event_form.errors} ", 'danger')
    return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)

@app.route("/user/<user_id>/block/<block_id>/event/delete/<event_id>", methods=["POST"])
def delete_event(user_id, block_id, event_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Event was deleted sucessfully!", 'success')
    return redirect(url_for("block", user_id=user_id, block_id=block_id), code=303)


############################
# ATTENDEES FORMS HANDLING #
############################
@app.route("/user/<user_id>/block/<block_id>/event/<event_id>/attendees/update", methods=["POST"])
def update_attendees(user_id, block_id, event_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    
    block = blocks[int(block_id)]
    members = block["members"]

    attendees_form = AttendeesForm(request.form)
    attendee_options = [(n["id"],f"<{n['last_name']}, {n['first_name']}> {n['email']}") for n in members]
    attendees_form.attendees.choices = attendee_options

    if attendees_form.validate_on_submit():
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Attendees list was updated sucessfully!", 'success')
        return redirect(url_for("event", user_id=user_id, block_id=block_id, event_id=event_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {attendees_form.errors} ", 'danger')
    return redirect(url_for("event", user_id=user_id, block_id=block_id, event_id=event_id), code=303)


############################
# LOCATIONS FORMS HANDLING #
############################
@app.route("/user/<user_id>/block/<block_id>/event/<event_id>/locations/update", methods=["POST"])
def update_locations(user_id, block_id, event_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    if user_id != session.get("user").get("oid"):
        return redirect(url_for("index"))
    
    block = blocks[int(block_id)]
    members = block["members"]

    locations_form = LocationsForm(request.form)
    location_options = [(n["id"],f"<{n['last_name']}, {n['first_name']}> {n['email']}") for n in members]
    locations_form.locations.choices = location_options

    if locations_form.validate_on_submit():
        flash("<strong><i class='fa-solid fa-circle-check'></i></strong> Attendees list was updated sucessfully!", 'success')
        return redirect(url_for("event", user_id=user_id, block_id=block_id, event_id=event_id), code=303)
    flash(f"<strong><i class='fa-solid fa-circle-exclamation'></i></strong> {locations_form.errors} ", 'danger')
    return redirect(url_for("event", user_id=user_id, block_id=block_id, event_id=event_id), code=303)

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

# @app.route("/graphcall")
# def graphcall():
#     token = _get_token_from_cache(app_config.SCOPE)
#     if not token:
#         return redirect(url_for("login"))
#     graph_data = requests.get(  # Use token to call downstream service
#         app_config.ENDPOINT,
#         headers={'Authorization': 'Bearer ' + token['access_token']},
#         ).json()
#     return render_template('display.html', result=graph_data)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        cache = _load_cache()
        print(cache)
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        print(result)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    print(cca)
    accounts = cca.get_accounts()
    print(accounts)
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

# Wrap Flask app with Talisman
#Talisman(app, content_security_policy=None)

if __name__ == "__main__":
    app.run(debug=True)
