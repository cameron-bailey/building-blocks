from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


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


# class Posts(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	title = db.Column(db.String(255))
# 	content = db.Column(db.Text)
# 	#author = db.Column(db.String(255))
# 	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
# 	slug = db.Column(db.String(255))
# 	# Foreign Key To Link Users (refer to primary key of the user)
# 	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# memberships = db.Table('memberships',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
# )

# class User(): 
#     def __init__(self,id,first_name,last_name,initials,emp_type,email,is_admin):
#         self.id = id
#         self.first_name = first_name
#         self.last_name = last_name
#         self.initials = initials
#         self.emp_type = emp_type
#         self.email = email
#         self.is_admin = is_admin

# class Facilities(db.Model):
#     pass

# class Facility:
#     facilities =[]
#     def __init__(self,id,building,room,additional_info):
#         self.id = id
#         self.building = building
#         self.room = room
#         self.additional_info = additional_info

# class Role:
#     roles = []
#     def __init__(self,id,title,view_block,update_block,delete_block,duplicate_block,
#         export_block,select_members,assign_members,view_events,add_events,update_events,
#         delete_events,select_attendees,delete_created_events,update_created_events,
#         select_created_events_attendees,select_locations):
#         self.id = id
#         self.title = title
#         self.view_block = view_block
#         self.update_block = update_block
#         self.delete_block = delete_block
#         self.duplicate_block = duplicate_block
#         self.export_block = export_block
#         self.select_members = select_members
#         self.assign_members = assign_members
#         self.view_events = view_events
#         self.add_events = add_events
#         self.update_events = update_events
#         self.delete_events = delete_events
#         self.select_attendees = select_attendees
#         self.delete_created_events = delete_created_events
#         self.update_created_events = update_created_events
#         self.select_created_events_attendees = select_created_events_attendees
#         self.select_locations = select_locations

# class Block:
#     blocks = []
#     def __init__(self,id,title,year,season,additional_info,date_created,created_by,date_modified,modified_by):
#         self.id = id
#         self.title = title
#         self.year = year
#         self.season = season
#         self.additional_info = additional_info
#         self.date_created = date_created
#         self.created_by = created_by
#         self.date_modified = date_modified
#         self.modified_by = modified_by

# class Member:
#     memberships = []
#     def __init__(self,id,user,block,role):
#         pass

# class Event:
#     events = []
#     def __init__(self,id,block_id,start_datetime,timedelta,format,topic,notes,attendence_required,date_added,date_modified,created_by,modified_by):
#         pass

# class Attendee:
#     attendees = []
#     def __init__(self,id,event_id,user_id,date_added,created_by):
#         pass

# class Location:
#     Locations = []
#     def __init__(self,id,event_id,facilities_id,date_added,added_by,**kwargs):
#         pass















# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50), nullable=False)
#     semester = db.Column(db.Integer, default=0)
#     notes = db.Column(db.String(), default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id


# # Create a Blog Post model
# class Posts(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	title = db.Column(db.String(255))
# 	content = db.Column(db.Text)
# 	#author = db.Column(db.String(255))
# 	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
# 	slug = db.Column(db.String(255))
# 	# Foreign Key To Link Users (refer to primary key of the user)
# 	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# ##Create Model
# # class Users(db.Model, UserMixin):
# class Users(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(20), nullable=False, unique=True)
# 	name = db.Column(db.String(200), nullable=False)
# 	email = db.Column(db.String(120), nullable=False, unique=True)
# 	favorite_color = db.Column(db.String(120))
# 	about_author = db.Column(db.Text(), nullable=True)
# 	date_added = db.Column(db.DateTime, default=datetime.utcnow)
# 	profile_pic = db.Column(db.String(), nullable=True)
# 	# Do some password stuff!
# 	password_hash = db.Column(db.String(128))
# 	# User Can Have Many Posts
# 	posts = db.relationship('Posts', backref='poster')

# 	@property
# 	def password(self):
# 		raise AttributeError('password is not a readable attribute!')

# 	# @password.setter
# 	# def password(self, password):
# 	# 	self.password_hash = generate_password_hash(password)

# 	# def verify_password(self, password):
# 	# 	return check_password_hash(self.password_hash, password)

# 	# Create A String
# 	def __repr__(self):
# 		return '<Name %r>' % self.name







# user_channel = db.Table('user_channel',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'))
# )

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     following = db.relationship('Channel', secondary=user_channel, backref='followers')

#     def __repr__(self):
#         return f'<User: {self.name}>'

# class Channel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))

#     def __repr__(self):
#         return f'<Channel: {self.name}>'




# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     addresses = db.relationship('Address', backref='person', lazy=True)

# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
#         nullable=False)

# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
# )

# class Page(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tags = db.relationship('Tag', secondary=tags, lazy='subquery',
#         backref=db.backref('pages', lazy=True))

# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)










users = [
    {
        "id":"0",
        "first_name": "Cameron",
        "last_name": "Bailey",
        "email": "cameron.bailey@som.umaryland.edu",
        "initials": "CB",
        "type": "Staff",
        'date_created':datetime.strptime("10/25/1987 08:00AM", "%m/%d/%Y %I:%M%p"),
        'created_by': "Bailey, Cameron",
        'date_modified':datetime.strptime("09/11/1980 10:00AM", "%m/%d/%Y %I:%M%p"),
        'modified_by': "Bailey, Cameron",
        "is_admin":True
    },
    {   "id":"1",
        "first_name": "Angel",
        "last_name": "Chavez",
        "email": "agchavez@som.umaryland.edu",
        "initials": "AC",
        "type": "Staff",
        'date_created':datetime.strptime("10/25/1987 08:00AM", "%m/%d/%Y %I:%M%p"),
        'created_by': "Bailey, Cameron",
        'date_modified':datetime.strptime("09/11/1980 10:00AM", "%m/%d/%Y %I:%M%p"),
        'modified_by': "Bailey, Cameron",
        "is_admin":True
    },
    {
        "id":"2",
        "first_name": "Nicole",
        "last_name": "Willhide",
        "email": "nwillhide@som.umaryland.edu",
        "initials": "NW",
        "type": "Staff",
        'date_created':datetime.strptime("10/25/1987 08:00AM", "%m/%d/%Y %I:%M%p"),
        'created_by': "Bailey, Cameron",
        'date_modified':datetime.strptime("09/11/1980 10:00AM", "%m/%d/%Y %I:%M%p"),
        'modified_by': "Bailey, Cameron",
        "is_admin":False
    },
    {
        "id":"3",
        "first_name": "Linda",
        "last_name": "Horn",
        "email": "lhorn@som.umaryland.edu",
        "initials": "LH",
        "type": "Core Faculty",
        'date_created':datetime.strptime("10/25/1987 08:00AM", "%m/%d/%Y %I:%M%p"),
        'created_by': "Bailey, Cameron",
        'date_modified':datetime.strptime("09/11/1980 10:00AM", "%m/%d/%Y %I:%M%p"),
        'modified_by': "Bailey, Cameron",
        "is_admin":False
    }
]



roles = [
    {
        "id":"0",
        "title":"Creator",
        "view_block":True,
        "update_block":True,
        "delete_block":True,
        "duplicate_block":True,
        "export_block":True,
        "select_members":True,
        "assign_members":True,
        "view_events":True,
        "add_events":True,
        "update_events":True,
        "delete_events":True,
        "select_attendees":True,
        "select_locations":True,
        "delete_events_limited":True,
        "update_events_limited":True,
        "select_attendees_limited":True,
        "select_locations_limited":True,
    },
    {
        "id":"1",
        "title":"Owner",
        "view_block":True,
        "update_block":True,
        "delete_block":False,
        "duplicate_block":True,
        "export_block":True,
        "select_members":True,
        "assign_members":True,
        "view_events":True,
        "add_events":True,
        "update_events":True,
        "delete_events":True,
        "select_attendees":True,
        "select_locations":True,
        "delete_events_limited":True,
        "update_events_limited":True,
        "select_attendees_limited":True,
        "select_locations_limited":True,
    },
    {
        "id":"2",
        "title":"Manager",
        "view_block":True,
        "update_block":True,
        "delete_block":False,
        "duplicate_block":True,
        "export_block":True,
        "select_members":False,
        "assign_members":False,
        "view_events":True,
        "add_events":True,
        "update_events":True,
        "delete_events":True,
        "select_attendees":True,
        "select_locations":True,
        "delete_events_limited":True,
        "update_events_limited":True,
        "select_attendees_limited":True,
        "select_locations_limited":True,
    },
        {
        "id":"3",
        "title":"Organizer",
        "view_block":True,
        "update_block":False,
        "delete_block":False,
        "duplicate_block":True,
        "export_block":False,
        "select_members":False,
        "assign_members":False,
        "view_events":True,
        "add_events":True,
        "update_events":False,
        "delete_events":False,
        "select_attendees":True,
        "select_locations":True,
        "delete_events_limited":True,
        "update_events_limited":True,
        "select_attendees_limited":True,
        "select_locations_limited":True,
    },
    {
        "id":"4",
        "title":"Participant",
        "view_block":True,
        "update_block":False,
        "delete_block":False,
        "duplicate_block":False,
        "export_block":False,
        "select_members":False,
        "assign_members":False,
        "view_events":True,
        "add_events":False,
        "update_events":False,
        "delete_events":False,
        "select_attendees":False,
        "select_locations":False,
        "delete_events_limited":False,
        "update_events_limited":False,
        "select_attendees_limited":False,
        "select_locations_limited":False,
    }
]


facilities = [
    {
    "id":"0",
    "building": "AHRB",
    "room": "146",
    "additional_info": ""
    },
    {
    "id":"1",
    "building": "AHRB",
    "room": "152",
    "additional_info": ""
    },
    {
    "id":"2",
    "building": "AHRB",
    "room": "202",
    "additional_info": ""
    },
    {
    "id":"3",
    "building": "AHRB",
    "room": "204",
    "additional_info": ""
    },
    {
    "id":"4",
    "building": "AHRB",
    "room": "211",
    "additional_info": ""
    },
    {
    "id":"5",
    "building": "AHRB",
    "room": "219",
    "additional_info": ""
    },
    {
    "id":"6",
    "building": "AHRB",
    "room": "248",
    "additional_info": ""
    },
    {
    "id":"7",
    "building": "AHRB",
    "room": "252",
    "additional_info": ""
    }
]



blocks = [
    {
        'id': '0',
        'title':'Fall 2022 Basic Sciences I',
        'year':'2022',
        'season': 'Fall',
        'add_info':'alkjsdffkljlkj jjjjes',
        'date_created':datetime.strptime("10/25/1987 08:00AM", "%m/%d/%Y %I:%M%p"),
        'created_by':users[0],
        'date_modified':datetime.strptime("09/11/1980 10:00AM", "%m/%d/%Y %I:%M%p"),
        'modified_by':users[0],
    }	
]

memberships = [
    {
        "id":"0",
        "user_id":"0",
        "block_id":"0",
        "role_id":"2",
    },
    {
        "id":"0",
        "user_id":"1",
        "block_id":"0",
        "role_id":"2",
    },
]

collaborators = [
    {
        "id":"0",
        "block_id":"0",
        "first_name":"Steph",
        "last_name":"Curry",
        "email":"stephcurry@gmail.com",
        "initials":"SC30",
        "notes":"best shooter EVAR."
    }
]

events = [
    { 
        "id":"0",
        "block_id":"0",
        "start_datetime":datetime.strptime("03/25/1983 08:00AM", "%m/%d/%Y %I:%M%p"),
        "duration":90,
        "format":"Assignment",
        "topic":"Topics Topics Topics!",
        "notes":"here are some notes",
        "attendance":True,
        'date_created':datetime.strptime("10/25/1987 08:00AM", "%m/%d/%Y %I:%M%p"),
        'create_by':"0",
        'date_modified':datetime.strptime("09/11/1980 10:00AM", "%m/%d/%Y %I:%M%p"),
        'modified_by':"0",
    }
]

attendees = [
    {
    "users_id":"0"
    }
]

locations = [
    {
        "id":"0",
        "event_id":"0",
        "facility_id":"2"
    },
    {
        "id":"0",
        "event_id":"0",
        "facility_id":"3"
    }
]










# blocks = [
#     {
#         'id': '0',
#         'title':'Fall 2022 Basic Sciences I',
#         'year':'2022',
#         'season': 'Fall',
#         'additional_info':'alkjsdffkljlkj jjjjes',
#         'date_created':datetime.strptime("10/25/1987 08:00AM", "%m/%d/%Y %I:%M%p"),
#         'date_modified':datetime.strptime("09/11/1980 10:00AM", "%m/%d/%Y %I:%M%p"),
#         'created_by':'Bailey, Cameron',
#         'modified_by':'Bailey, Cameron',
#         'members':[
#                 users[0],
#                 users[1]
#             ],
#         'events': [
#             { 
#                 "id":"0",
#                 "block_id":"0",
#                 "start_datetime":datetime.strptime("03/25/1983 08:00AM", "%m/%d/%Y %I:%M%p"),
#                 "duration":90,
#                 "format":"Assignment",
#                 "topic":"Topics Topics Topics!",
#                 "notes":"here are some notes",
#                 "attendance":True,
#                 "attendees": [
#                         users[0]
#                     ],
#                 "locations":[
#                         facilities[2],
#                         facilities[3]
#                     ],
#                 'date_created':datetime.strptime("10/25/1987 08:00AM", "%m/%d/%Y %I:%M%p"),
#                 'created_by':users[0],
#                 'date_modified':datetime.strptime("09/11/1980 10:00AM", "%m/%d/%Y %I:%M%p"),
#                 'modified_by':users[0]
#             }
#         ]
#     }	
# ]
