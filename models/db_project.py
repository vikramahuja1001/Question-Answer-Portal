#the admin username is vikram.ahuja@students.iiit.ac.in 
#and the password is 1234
#the password of every other user is 1234
from gluon.tools import prettydate

db.define_table('classify',
		db.Field('topic','string',label='Name'))

db.define_table('admins',
		db.Field('name',db.auth_user,requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name')))

db.define_table('expert',
		db.Field('name',db.auth_user,requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name')))


db.define_table('post',
		db.Field('title','string',requires=IS_NOT_EMPTY(),label='Title'),
		db.Field('body','text',label='Question',represent=lambda text, row:PRE(text)),
		db.Field('classification',db.classify,requires=IS_IN_DB(db,'classify.id','classify.topic')),
		db.Field('posted_on','datetime',default=request.now,writable=False,readable=False),
		db.Field('posted_by',db.auth_user,writable=False,readable=False,default=auth.user_id,requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name','auth_user.last_name')),
		db.Field('counter','integer',default=0,readable=False,writable=False),
		db.Field('liked','integer',default=0,readable=False,writable=False),	
		db.Field('disliked','integer',default=0,readable=False,writable=False))


db.define_table('answer',
		db.Field('answer_id','reference post'),
		db.Field('answer','text' ,required=True,notnull=True,represent=lambda text, row:PRE(18)),
		db.Field('yoursource','string',label='Source'),
		db.Field('link','string'),
		db.Field('posted_on', 'datetime', default=request.now),
		db.Field('posted_by', db.auth_user, default=auth.user_id,requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name','auth_user.second_name')))


db.define_table('privatemessage',

		db.Field('posted_to',db.auth_user,requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name','auth_user.second_name')),
		db.Field('title','string'),
		db.Field('messages','text'),
		db.Field('posted_by', db.auth_user,readable=False,writable=False, default=auth.user_id,requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name'    ,'auth_user.second_name')),
		db.Field('posted_on','datetime',readable=False,writable=False,default=request.now))












#this is for portal feed back to improve technically
db.define_table('feedback',
		db.Field('userid',db.auth_user,readable=False,writable=False),
		db.Field('posted_on','datetime',readable=False,writable=False,default=request.now),
		db.Field('feedback','text',requires = [IS_NOT_EMPTY()]))
#This table is for requesting any songs from users to all and admin
db.define_table('requests',
		db.Field('userid',db.auth_user,readable=False,writable=False),
		db.Field('posted_on','datetime',readable=False,writable=False,default=request.now),
		db.Field('request','text',requires = [IS_NOT_EMPTY()]))
# this table is to report is any songs is against to rules to admin to del them from users
db.define_table('reportabuse',
		db.Field('userid',db.auth_user),
		db.Field('postid',db.post))
#this table is for user to upload his profile pic

db.define_table('image',
		db.Field('title', unique=True),
                db.Field('uploaded_by', db.auth_user,default=auth.user_id),
                db.Field('uploaded_on','datetime', default=request.now),
		db.Field('files', 'upload',requires=IS_IMAGE()),
	        format = '%(title)s')

	

db.define_table('liked',
		db.Field('post_id',db.post),
		db.Field('posted_by', db.auth_user, default=auth.user_id,requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name','auth_user.second_name')))


db.define_table('delpost',
		db.Field('post_id', db.post))


db.define_table('disliked',
		db.Field('post_id',db.post),
		db.Field('posted_by', db.auth_user, default=auth.user_id,requires=IS_NOT_IN_DB(db,'db.liked.posted_by')))




db.define_table('favorite',
		db.Field('post_id',db.post,unique=True),
		db.Field('posted_by', db.auth_user, default=auth.user_id,requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name','auth_user.second_name')))



db.favorite.post_id.writable = db.favorite.post_id.readable = False
db.favorite.posted_by.writable = db.favorite.posted_by.readable = False

db.post.id.writable = db.post.id.readable = False


db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.image.uploaded_by.writable = db.image.uploaded_by.readable = False
db.image.uploaded_on.writable = db.image.uploaded_on.readable = False
#db.image.image_id.writable = db.image.image_id.readable = False

db.liked.post_id.requires = IS_IN_DB(db, db.post.id)
db.liked.post_id.writable = db.liked.post_id.readable = False
db.liked.posted_by.writable = db.liked.posted_by.readable=False


db.disliked.post_id.requires = IS_IN_DB(db, db.post.id)
db.disliked.post_id.writable = db.disliked.post_id.readable = False
db.disliked.posted_by.writable = db.disliked.posted_by.readable=False




db.delpost.post_id.writable = db.delpost.post_id.readable = False

db.answer.answer.requires = IS_NOT_EMPTY()
db.answer.answer_id.readable = db.answer.answer_id.writable = False
db.answer.posted_by.readable = db.answer.posted_by.writable = False
db.answer.posted_on.readable = db.answer.posted_on.writable = False



User = db.auth_user
me = auth.user_id
