# -*- coding: utf-8 -*-

import datetime
import itertools
import functools

from bottle import (Bottle, request, redirect, response,
                    static_file, redirect, template, error)

from sqlalchemy.orm import subqueryload
from sqlalchemy import extract


from models import Tag, Post
from convert import Convert
from utils import jinja_view, key_verified, session_context

from sblog.settings import DEBUG, STATIC_ROOT, STATIC_URL

from view_func import edit_post, store_new_post

from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append('../views/')

app = Bottle()


format_time = lambda t, f: datetime.datetime.strftime(t, f)
get_year = functools.partial(format_time, f='%Y')
get_month = functools.partial(format_time, f='%B')


def group_posts(items):
    """group items with year and month"""
    
    def _year(items):
        return itertools.groupby(items, lambda a: get_year(a.create_at))
    
    def _month(items):
        return itertools.groupby(items, lambda a: get_month(a.create_at))
    
    groupby_year = _year(items)
    groupby_year_month = ((year, _month(items)) for year, items in groupby_year)
    return groupby_year_month
    
@app.get('/')
@app.get('/blog')
@app.get('/blog/latest')
@jinja_view('index.html')
def index():
    with session_context() as session:
        posts = session.query(Post).order_by(Post.create_at.desc()).limit(5)
    return {'posts': posts, 'index': True}
    

@app.get('/blog/archive')
@jinja_view('archive.html')
def archive():
    with session_context() as session:
        posts = session.query(Post).order_by(Post.create_at.desc())
        
    posts = group_posts(posts)
    return {'posts': posts}

@app.get('/blog/archive/<year:re:[0-9]{4}>')
@jinja_view('archive.html')
def archive_year(year):
    year = int(year)
    with session_context() as session:
        posts = session.query(Post).filter(
            extract('year', Post.create_at) == year).order_by(
                Post.create_at.desc())
    posts = group_posts(posts)
    return {'posts': posts}
    
@app.get('/blog/tag/<tag>')
@jinja_view('archive.html')
def filter_by_tag(tag):
    with session_context() as session:
        posts = session.query(Post).filter(Post.tags.any(Tag.name==tag)
                                        ).order_by(Post.create_at.desc())
    
    posts = group_posts(posts)
    return {'posts': posts}
    

@app.get('/blog/<year:re:[0-9]{4}>')
@jinja_view('index.html')
def index_year(year):
    year = int(year)
    with session_context() as session:
        posts = session.query(Post).options(
            subqueryload(Post.tags)).filter(
                extract('year', Post.create_at) == year).order_by(
                    Post.create_at.desc()).limit(20)
    return {'posts': posts, 'index': True, 'is_by_year': year}
        

@app.get('/blog/<year:re:[0-9]{4}>/<month:re:[0-9]{1,2}>/<day:re:[0-9]{1,2}>/<slug>')
@jinja_view('post.html')
def detail(year, month, day, slug):
    year = int(year)
    month = int(month)
    day = int(day)
    with session_context() as session:
        post = session.query(Post).options(
            subqueryload(Post.tags)).filter(Post.slug == slug).filter(
                extract('year', Post.create_at) == year,
                extract('month', Post.create_at) == month,
                extract('day', Post.create_at) == day)
        try:
            if post.count() < 1:
                redirect('/blog')
        except:
            print "error occurred"
            redirect('/blog')
        post = post.first()
        post.view_count += 1
        # get related posts
        # dont forget to filter self
        tag_ids = [_t.id for _t in post.tags]
        related_posts = session.query(Post).filter(
            Post.tags.any(Tag.id.in_(tag_ids))
        ).filter(
            Post.id != post.id
        ).order_by(Post.view_count.desc())

        session.commit()
    return {'post': post, 'title': post.title, 'related_posts': related_posts}



    
@app.post('/blog/edit')
@jinja_view('markdown_edit_preview.html')
def edit():
    
    key = request.forms.get('key')
    if not key_verified(key):
        return {"example": "Security key NOT matched!", "title": '', 'tags': '', 'code': ''}
    post_id = request.forms.get("blog_id")
    try:
        post_id_int = int(post_id)
    except ValueError as err:
        example = str(err)
    

    with session_context() as session:
        p = session.query(Post).filter(Post.id == post_id_int)
        if p.count > 0:
            p = p.one()
            title = p.title
            example = p.markdown
            tags_list = [t.name for t in p.tags]
            tags = ','.join(tags_list)
            code = p.code
        else:
            example = 'No blog found!'
            title = ''
            tags = ''
            code = ''

    return {"example": example, "title": title, "tags": tags, "code": code}



@app.get('/blog/editcheck/<blog_id:int>')
def editcheck(blog_id):
    blog_id = int(blog_id)
    return template("editcheck", blog_id = blog_id)

@app.get("/blog/add")
@jinja_view("markdown_edit_preview.html")
def markdown_edit_preview():
    return {"example": '', "title": "", "tags": ""}

@app.post('/blog/post')
def new_post():
    key = request.forms.get('key')
    
    if not key_verified(key):
        return '<h2>Security Key NOT matched!</h2>'
    
    title = request.forms.get('title').strip()
    if not title:
        return "<h2>Error: title is empty!</h2>"

    tags_str = request.forms.get('tags').strip().strip(",")
    if not tags_str:
        return "<h2>Error: tag is empty!</h2>"
    tags = [t.strip() for t in tags_str.split(',')]
    
    md = request.forms.get('markdown')
    if not md:
        return "<h2>Error: no contents!</h2>"

    code = request.forms.get('code')
    html = Convert("md").convert(md)
    try:
        with session_context() as session:
            if not code:
                p = store_new_post(session, title, html, md, tags)
            else:
                p = edit_post(session, code, title, html, md, tags)
    except Exception as err:
        p = None
        msg = str(err)
    return template('jump2article', p = p, msg = '' if p else msg)


@app.get('/blog/tagcloud')
def tagcloud():
    return template('tagcloud')
    
@app.get('/blog/about')
@jinja_view('about.html')
def about():
    return {'title': 'about'}


@error(404)
def error404(error):
    return 'Nothing here, sorry'


@app.get(STATIC_URL + '<filepath:path>')
def static(filepath):
    return static_file(filepath, root = STATIC_ROOT)


