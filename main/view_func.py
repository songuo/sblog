import os
import base64

from sqlalchemy.orm import subqueryload

from models import Tag, Post
from utils import session_context



def edit_post(session, code, title, content, md, tags):
    if not isinstance(tags, (list, tuple)):
        tags = [tags]

    new_tags = tags

    post_obj = session.query(Post).options(
        subqueryload(Post.tags)).filter(Post.code == code)
    if post_obj.count() >= 1:
        post_obj = post_obj.first()
    old_tags = [t.name for t in post_obj.tags]
    new_tags, old_tags = set(new_tags), set(old_tags)
    
    removed_tags = old_tags - new_tags
    added_tags = new_tags - old_tags
    
    def _get_tag_obj(name):
        obj = session.query(Tag).filter(Tag.name == name)
        if obj.count() == 0:
            return None
        return obj.one()
    
    for t in removed_tags:
        t_obj = _get_tag_obj(t)
        post_obj.tags.remove( t_obj )
        # if this tag's count == 1, then delete this tag
        if t_obj.posts_count < 2:
            session.delete(t_obj)
        
    for t in added_tags:
        t_obj = _get_tag_obj(t)
        if t_obj is None:
            # new tag
            t_obj = Tag(t)
        else:
            # increase exists tag's posts_count
            t_obj.posts_count += 1
        post_obj.tags.append( t_obj )

    post_obj.title = title
    post_obj.content = content
    post_obj.markdown = md
    session.commit()
    return post_obj
    

def store_new_post(session, title, content, md, tags):
    p = Post(title, content, md)
    
    if not isinstance(tags, (list, tuple)):
        tags = [tags]
        
    def _get_tag_obj(tag):
        t = session.query(Tag).filter(Tag.name == tag)
        if t.count() > 0:
            # this tag already exists, increase `posts_count`
            t = t.one()
            t.posts_count += 1
        else:
            # new tag
            t = Tag(tag)
            
        return t
    
    tags = filter(lambda t: '#' not in t, tags)
    p.tags = [_get_tag_obj(t) for t in tags]
    code = base64.b64encode(os.urandom(64))
    p.code = code    
    session.add(p)
    session.commit()
    return p


