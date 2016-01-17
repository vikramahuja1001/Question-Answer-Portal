# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    
    return dict(form=auth())


def download():
	return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

import datetime
import re
#the admin username is vikram.ahuja@students.iiit.ac.in 
#and the password is 1234
#the password of every other user is 1234



def index():

#	user=User(me)

	return locals()



def index3():
	response.flash='Are you sure you are the admin?	Because I Do not Think You Are The ONE.'
	return locals()


@auth.requires_login()
def addadmin():
	form=SQLFORM(db.admins)
        

	if form.process().accepted:
		response.flash= 'Form Accepted'
		redirect(URL('index2'))
	elif form.errors:
		response.flash='Form has errors'
	else:
		response.flash='Please Fill the Form'
	return dict(form=form)




@auth.requires_login()
def index1():
	user=User(me)
	print user.id
	print db.admins.name
	a=db(db.admins.name==user.id).select()
	if len(a)!=0:
		redirect(URL('index2'))
	else:
		redirect(URL('index3'))

			
	return locals()



@auth.requires_login()
def index2():
	grid = SQLFORM.grid(db.post)
	return locals()



@auth.requires_login()
def alladmin():
	 result=db(db.post.id>0).select(db.post.title,db.post.posted_on,db.post.posted_by,db.post.classification,db.post.id,orderby=~db.post.posted_on)
	 return dict(result=result)




@auth.requires_login()
def adminquestion():
	this_page = db.post(request.args(0)) or redirect(URL('index'))
	db.post.id.default = this_page.id
	db.answer.answer_id.default=this_page.id
	form = crud.create(db.answer) if auth.user else "Login to Answer to this Question"

	pageposts = db(db.post.id==this_page.id).select(db.post.title,db.post.body,db.post.id,db.post.posted_by)
	pageanswer = db(db.answer.answer_id==this_page.id).select(db.answer.posted_by,db.answer.posted_on,db.answer.answer)



	#   LIKES    

	post = db.post(request.args(0)) or redirect(URL('index'))
	db.liked.post_id.default = post.id
	crud.messages.submit_button = 'Like me'

	form1 = crud.create(db.liked,message='You like this question',next=URL(args=post.id)) if auth.user else "Login to Like this Question"
	likes = db(db.liked.post_id==post.id).select()



	#   DISLIKES    

	post1 = db.post(request.args(0)) or redirect(URL('index'))
	db.disliked.post_id.default = post1.id
	crud.messages.submit_button = 'Dislike me'
	form2 = crud.create(db.disliked,message='You dislike this question',next=URL(args=post1.id)) if auth.user else "Login to Dislike this Question"
	dislikes = db(db.disliked.post_id==post1.id).select()


	return dict(project=this_page, posts=pageposts,answer=pageanswer,form=form,form1=form1,likes=likes,form2=form2,dislikes=dislikes)
		





def all():

	
	result=db(db.post.id>0).select(db.post.title,db.post.posted_on,db.post.posted_by,db.post.classification,db.post.id,orderby=~db.post.posted_on)

	return dict(result=result)




@auth.requires_login()
def mywall():
	user = User(me)
	result=db(db.post.posted_by==user.id).select(db.post.title,db.post.posted_on,db.post.posted_by,db.post.classification,db.post.id,orderby=~db.post.posted_on)
	return dict(result=result)




@auth.requires_login()
def mywall1():
	user = User(me)
	result=db((db.answer.answer_id==db.post.id)&(db.answer.posted_by==user.id)).select(db.post.title,db.post.id,db.post.classification,db.post.posted_on,db.post.posted_by,orderby=db.answer.id)
	
	#result1=db((db.answer.answer_id==db.post.id)&(db.answer.posted_by==user.id)).select(db.answer.posted_on)
	return dict(result=result)



@auth.requires_login()
def mypage():

	user=User(me)
	result=db(db.auth_user.id==user.id).select()
	result1=db((db.auth_user.id==user.id)&(db.image.uploaded_by==user.id)).select(db.image.files,orderby=~db.image.uploaded_on)

	return dict(result=result,result1=result1)


@auth.requires_login()
def insertimage():
	form=SQLFORM(db.image)
	#Check if uploaded file is either JPEG or PNG:
	
	if form.process().accepted:
		response.flash= 'Form Accepted'
		redirect(URL('mypage'))

	elif form.errors:
		response.flash='Form has errors'
	else:
		response.flash='Please Fill the Form'
	return dict(form=form)


def find2():

	result=db(db.post.id>0).select()
	return dict(result=result)





def question():
	user=User(me)	         
	form3=''
	form5=''
	this_page = db.post(request.args(0)) or redirect(URL('index'))
	db.ratings.postid.default=this_page.id
	db.answerratings.postid.default=this_page.id

	db.post.id.default = this_page.id
	db(db.post.id == this_page.id).update(
		counter = db.post.counter + 1)
	
	pageanswer = db(db.answer.answer_id==this_page.id).select(db.answer.posted_by,db.answer.posted_on,db.answer.answer,db.answer.id)

	for j in pageanswer:
		db.answerratings.answerid.default=j.id
		

	if auth.user:	
		db.answerratings.userids.default=auth.user.id
		form5 = SQLFORM(db.answerratings)
		if form5.accepts(request.vars, session):
			session.flash = 'Thanks for rating this question'
			redirect(URL('question',args=request.args))
			


	
	db.answer.answer_id.default=this_page.id
	form4 = crud.create(db.answer) if auth.user else "Login to Answer to this Question"
	if auth.user:
		db.ratings.userids.default=auth.user.id
		form3 = SQLFORM(db.ratings)
		if form3.accepts(request.vars, session):
			session.flash = 'Thanks for rating this question'
			
			redirect(URL('question',args=request.args))

	pageposts = db(db.post.id==this_page.id).select(db.post.title,db.post.body,db.post.id,db.post.posted_by,db.post.counter)	   
	pageanswer = db(db.answer.answer_id==this_page.id).select(db.answer.posted_by,db.answer.posted_on,db.answer.answer,db.answer.id)
	

		
	 #   LIKES    
	    
	post = db.post(request.args(0)) or redirect(URL('index'))
	db.liked.post_id.default = post.id	
	crud.messages.submit_button = 'Like me'
	
	form1 = crud.create(db.liked,message='You like this question',next=URL(args=post.id)) if auth.user else "Login to Like this Question"
	likes = db(db.liked.post_id==post.id).select()




   	#   DISLIKES    

        post1 = db.post(request.args(0)) or redirect(URL('index'))
	db.disliked.post_id.default = post1.id
	crud.messages.submit_button = 'Dislike me'
	form2 = crud.create(db.disliked,message='You dislike this question',next=URL(args=post1.id)) if auth.user else "Login to Dislike this Question"
	dislikes = db(db.disliked.post_id==post1.id).select()

	


	return dict(form4=form4,form5=form5,form3=form3,project=this_page, posts=pageposts,answer=pageanswer,form1=form1,likes=likes,form2=form2,dislikes=dislikes)





def answerquestion():
	user=User(me)
	this_page=db.post(request.args(0))
	db.post.id.default = this_page.id
	db.answer.answer_id.default=this_page.id
	form=''
	if auth.user:
		form = crud.create(db.answer)
		db.answer.posted_by==user.id
	else:
		form=crud.create(db.answer)
		db.answer.posted_by=="Anon"
	return dict(form=form)


@auth.requires_login()
def myquestion():

	  this_page1 = db.post(request.args(0)) or redirect(URL('index'))
	  db.post.id.default = this_page1.id

	  db.answer.answer_id.default=this_page1.id

	  pageposts = db(db.post.id==this_page1.id).select(db.post.title,db.post.body,db.post.id)
	  pageanswer = db(db.answer.answer_id==this_page1.id).select()
	  return dict(project=this_page1, posts=pageposts,answer=pageanswer)




@auth.requires_login()
def myanswer():
           this_page1 = db.post(request.args(0)) or redirect(URL('index'))
	   db.post.id.default = this_page1.id
           db.answer.answer_id.default=this_page1.id
           pageposts = db(db.post.id==this_page1.id).select(db.post.title,db.post.body,db.post.id)
           pageanswer = db(db.answer.answer_id==this_page1.id).select()
           return dict(project=this_page1, posts=pageposts,answer=pageanswer)




@auth.requires_login()
def ask():
	response.flash="Write the question"
	form=SQLFORM(db.post)

	if form.process().accepted:
		response.flash= 'Question Accepted'
		redirect(URL('all'))
	elif form.errors:
		response.flash='Form has errors'
	else:
		response.flash='Write the question'
	
	return dict(form=form)
	





def find1():
	si=request.post_vars['si']
	s=db(db.post.title.like('%'+si+'%')).select()
	
	return dict(s=s)
	




def find3():
	si=request.post_vars['si']
	if len(si)==0:
		redirect(URL('index'))
	if si==' ':
		redirect(URL('index'))
	
	if si=='  ':
		redirect(URL('index'))
	s=db(db.post.title.like('%'+si+'%')).select(db.post.title,db.post.classification,db.post.posted_by,db.post.id,db.post.posted_on,orderby=~db.post.posted_on)
	s2=db(db.post.classification.like('%'+si+'%')).select()
	return dict(s=s,s2=s2)



@auth.requires_login()
def edit():
	
	this_page = db.post(request.args(0,cast=int)) or redirect(URL('index'))
	form = SQLFORM(db.post, this_page).process(
			next = URL('myquestion',args=request.args))
	return dict(form=form)





@auth.requires_login()
def editadmin():
	this_page = db.post(request.args(0,cast=int)) or redirect(URL('index'))
	form = SQLFORM(db.post, this_page).process(
   			next = URL('adminquestion',args=request.args))
	return dict(form=form)



@auth.requires_login()
def deleteadmin():
	this_page1 = db.post(request.args(0))
	db.post.id.default = this_page1.id

	db.answer.answer_id.default=this_page1.id

	pageposts = db(db.post.id==this_page1.id).delete()
	pageanswer = db(db.answer.answer_id==this_page1.id).delete()
	redirect(URL('alladmin'))
	return dict(project=this_page1, posts=pageposts,answer=pageanswer)





@auth.requires_login()
def delete():

	this_page1 = db.post(request.args(0)) 
        db.post.id.default = this_page1.id

	db.answer.answer_id.default=this_page1.id

	pageposts = db(db.post.id==this_page1.id).delete()
	pageanswer = db(db.answer.answer_id==this_page1.id).delete()
	redirect(URL('mywall'))
	return dict(project=this_page1, posts=pageposts,answer=pageanswer)





@auth.requires_login()
def addfavorite():
	 user = User(me)
	 this_page1 = db.post(request.args(0))
	 
	 s=db((db.favorite.post_id==this_page1.id)&(db.favorite.posted_by==user.id)).select(db.favorite.post_id)
	 print 's=',s
	 if len(s)==0:
 	 	db.favorite.insert(posted_by=user.id,post_id=this_page1.id)
 	 	session.flash='Added to your Favorites List'
	 else:
		session.flash='Already in your Favorites List'
	 redirect(URL('all'))
	 return locals() 
 



@auth.requires_login()
def printfavoriteall():
	user = User(me)
	result=db((db.favorite.posted_by==user.id)&(db.favorite.post_id==db.post.id)).select(db.post.title,db.post.posted_on,db.post.posted_by,db.post.classification,db.post.id,orderby=~db.favorite.post_id)
	return dict(result=result)






@auth.requires_login()
def feedback():
	form=SQLFORM(db.feedback)
	form.vars.userid=auth.user_id
	if form.accepts(request.vars, session):
		session.flash = 'Feedback Submited'
		redirect(URL(r=request,f="index"))
	return(dict(form=form))




@auth.requires_login()
def reportabuse():
	form=SQLFORM(db.reportabuse)
	form.vars.userid=auth.user_id
	if form.accepts(request.vars, session):
		session.flash = 'Submited'
		redirect(URL(r=request,f="index"))
	return(dict(form=form))



def one():
	return dict()

def echo():
	return "jQuery('#target').html(%s);" % repr(request.vars.name)







def month_input():
	return dict()




def month_selector():

	if not request.vars.month: return ''
	t=[]
	t=db(db.classify.id>0).select(db.classify.title)
	print len(t)	
	months=['CSO','Maths','Science']
	for i in len(t):
		months.append('aa')
	print months


	month_start = request.vars.month.capitalize()
	selected = [m for m in months if m.startswith(month_start)]
	return DIV(*[DIV(k,
		_onclick="jQuery('#month').val('%s')" % k,
		_onmouseover="this.style.backgroundColor='yellow'",
		_onmouseout="this.style.backgroundColor='white'"
		) for k in selected])



@auth.requires_login()
def showfriends():
	user=User(me)
	this_page = db.auth_user(request.args(0)) or redirect(URL('index'))
	db.auth_user.id.default = this_page.id
#	db.answer.answer_id.default=this_page1.id
	if user.id==this_page.id:
		redirect(URL('mypage'))
	else:
		userpage = db(db.auth_user.id==this_page.id).select()
		userpost=db(db.post.posted_by==this_page.id).select()
		userimage=db(db.image.uploaded_by==this_page.id).select(db.image.files,orderby=~db.image.uploaded_on)
#	pageanswer = db(db.answer.answer_id==this_page1.id).select()
	return dict(project=this_page, userpage=userpage,userpost=userpost,userimage=userimage)


def showtopic():
	user=User(me)
	this_page=db.classify(request.args(0))
	db.classify.id.default=this_page.id
	users=db((db.classify.id==this_page.id)&(db.post.classification==this_page.id)).select(db.post.title,db.post.posted_on,db.post.posted_by,db.post.id,orderby=~db.post.posted_on)
#	if user.id==db.admins.id:
#	deleteoption=db((db.classify.id==this_page.id)&db(db.post.classification)).delete()
	return dict(users=users,project=this_page)

@auth.requires_login()
def showtopicadmin():
	user=User(me)
	this_page=db.classify(request.args(0))
	db.classify.id.default=this_page.id
	users=db((db.classify.id==this_page.id)&(db.post.classification==this_page.id)).select(db.post.title,db.post.posted_on,db.post.posted_by,db.post.id,orderby=~db.post.posted_on)
	return dict(users=users,project=this_page)



def topicquestion():
	topic=db(db.classify.id>0).select()
	return dict(topic=topic)

def about():
	return locals()



@auth.requires_login()
def deletequestion():
	this_page1 = db.post(request.args(0))
	db.post.id.default = this_page1.id
	db.answer.answer_id.default=this_page1.id
	pageposts = db(db.post.id==this_page1.id).delete()
	pageanswer = db(db.answer.answer_id==this_page1.id).delete()
	redirect(URL('topicquestion'))
	return dict(project=this_page1, posts=pageposts,answer=pageanswer)




def unanswered():
	
	qwe=db(db.post.id>0).select(db.post.id,db.post.title,db.post.posted_by,db.post.posted_on,db.post.classification,orderby=~db.post.posted_on)
	
	qwe1=db(db.answer.id>0).select(db.answer.answer_id)	
		
	return dict(qwe=qwe,qwe1=qwe1)








