from db import db

def get_post(post_id):
    result = db.session.execute('''
        SELECT posts.id, posts.body, posts.thread
        FROM posts
        WHERE posts.id = :id
    ''', { 'id': post_id })
    
    post = result.fetchone()

    return {
        'id': post[0],
        'content': post[1],
        'thread': post[2] or post[0]
    }
