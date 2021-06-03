import re
from datetime import datetime
from db import db

def create_thread(content, board, author, image_id=None):
    if not content:
        raise Exception('Content is required')

    result = db.session.execute('''
        INSERT INTO posts (board, author, body, image, created_at)
        VALUES (:board, :author, :body, :image, current_timestamp)
        RETURNING id
    ''', { 'board': board, 'author': author, 'body': content, 'image': image_id })
    db.session.commit()

    post_id = result.fetchone()[0]
    reply_ids = extract_replies(content)
    insert_replies(post_id, reply_ids)

def reply(thread_id, content, author, image_id=None):
    if not content:
        raise Exception('Content is required')

    result = db.session.execute('''
        INSERT INTO posts (board, thread, author, body, image, created_at)
        VALUES (
            (SELECT board FROM posts WHERE id = :thread),
            :thread, :author, :body, :image, current_timestamp)
        RETURNING id
        ''', {'thread': thread_id, 'author': author, 'body': content, 'image': image_id})
    db.session.commit()

    post_id = result.fetchone()[0]
    reply_ids = extract_replies(content)
    insert_replies(post_id, reply_ids)

def insert_replies(from_id, reply_ids):
    if len(reply_ids) == 0:
        return

    exprs = []
    rid = { 'from_id': from_id }
    for i in range(len(reply_ids)):
        exprs.append(f'(:from_id, :to_id_{i})')
        rid[f'to_id_{i}'] = reply_ids[i]

    query = f'''
        INSERT INTO replies (from_post, to_post) VALUES
        {','.join(exprs)}
    '''

    print(query, flush=True)

    db.session.execute(query, rid)
    db.session.commit()

def extract_replies(content):
    return list(set(re.findall(r'>>(\d+)', content)))

def get_threads_from_board(path, offset, count):
    result = db.session.execute('''
        SELECT T.id
        FROM posts AS T
        LEFT JOIN (
            SELECT
                thread AS thread_id,
                MAX(created_at) AS most_recent
            FROM posts
            WHERE thread IS NOT NULL
            GROUP BY thread
        ) AS P
        ON T.id = P.thread_id
        WHERE thread IS NULL AND board = :board
        ORDER BY COALESCE(most_recent, created_at) DESC
        LIMIT :count OFFSET :offset
    ''', { 'count': count, 'offset': offset, 'board': path })

    thread_ids = list(map(lambda i: i[0], result.fetchall()))
    return construct_threads(thread_ids, 5)

def get_thread(thread_id):
    return construct_thread(thread_id)

def construct_thread(thread_id, limit=None):
    result = db.session.execute(f'''
        SELECT posts.id, body, image, created_at, edited, filename, users.name, COUNT(*) OVER() AS post_count
        FROM posts
        LEFT JOIN images
        ON posts.image = images.id
        LEFT JOIN users
        on posts.author = users.id
        WHERE thread = :id OR posts.id = :id
        ORDER BY created_at ASC
        {f'LIMIT {limit}' if limit else ''}
    ''', { 'id': thread_id })

    threads = result.fetchall()
    return list(
        map(
            lambda t: {
                'id': t[0],
                'body': t[1],
                'image': t[2],
                'created_at': t[3].strftime('%d/%m/%Y %H:%M:%S'),
                'edited': t[4],
                'filename': t[5],
                'author': t[6],
                'replies': get_post_replies(t[0]),
                'post_count': t[7] - 1
            },
            threads
        )
    )

def get_post_replies(post_id):
    result = db.session.execute('''
        SELECT replies.from_post
        FROM posts, replies
        WHERE posts.id = :post_id AND posts.id = replies.to_post
    ''', { 'post_id': post_id })

    return list(
        map(
            lambda r: r[0],
            result.fetchall()
        )
    )

def construct_threads(thread_ids, limit):
    return list(map(lambda tid: construct_thread(tid, limit), thread_ids))