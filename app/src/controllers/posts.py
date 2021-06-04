from db import db
from middleware.error import NotFoundError

def get_post(post_id):
    result = db.session.execute('''
        SELECT posts.id, posts.body, posts.thread
        FROM posts
        WHERE posts.id = :id
    ''', { 'id': post_id })
    
    post = result.fetchone()
    if not post:
        raise NotFoundError(f'No thread containing a post with id {post_id} was found.')

    return {
        'id': post[0],
        'content': post[1],
        'thread': post[2] or post[0]
    }

def delete(post_id):
    db.session.execute('''
        DELETE FROM posts
        WHERE id = :id
    ''', { 'id': post_id })
    db.session.commit()