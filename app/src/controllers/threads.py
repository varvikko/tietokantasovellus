import re
from datetime import datetime
from flask import session

from controllers import users
from db import db
from middleware.error import (
    InvalidDataError,
    NotFoundError,
    AccessDeniedError
)

def create_thread(content, board, author, image_id=None):
    if not content:
        raise InvalidDataError('Thread must have content.')

    if users.is_banned(author):
        ban_details = users.get_ban_details(author)
        raise AccessDeniedError(f'You are banned. Reason: {ban_details["reason"]}. Ban will end on {ban_details["ends_at"]}')

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
        raise InvalidDataError('Post must have content.')

    if users.is_banned(author):
        raise AccessDeniedError('You are banned')

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
        WHERE thread IS NULL
            AND board = :board
            AND id NOT IN (
                SELECT id
                FROM hides
                WHERE thread = T.id
                    AND user_id = :uid
            )
        ORDER BY COALESCE(most_recent, created_at) DESC
        LIMIT :count OFFSET :offset
    ''', { 'count': count, 'offset': offset, 'board': path, 'uid': session['uid'] })

    thread_ids = list(map(lambda i: i[0], result.fetchall()))
    return construct_threads(thread_ids, 5)

def get_most_popular_threads(n):
    result = db.session.execute('''
        SELECT T.id, T.body, B.name, B.path
        FROM posts AS T
        LEFT JOIN (
            SELECT thread, COUNT(*) AS post_count
            FROM posts
            WHERE thread IS NOT NULL AND created_at > NOW() - INTERVAL '1 DAY'
            GROUP BY thread
        ) AS P
        ON T.id = P.thread
        LEFT JOIN boards AS B
        ON T.board = B.path
        WHERE T.thread IS NULL AND P.post_count IS NOT NULL
        ORDER BY P.post_count DESC
        LIMIT :thread_count
    ''', { 'thread_count': n })

    return list(
        map(
            lambda t: {
                'id': t[0],
                'body': t[1],
                'board_name': t[2],
                'board_path': t[3]
            }, result.fetchall()
        )
    )

def get_most_recent_threads(n):
    result = db.session.execute('''
        SELECT T.id, T.body, B.name, B.path
        FROM posts AS T
        LEFT JOIN boards AS B
        ON T.board = B.path
        WHERE thread IS NULL
        ORDER BY created_at DESC
        LIMIT :thread_count
    ''', { 'thread_count': n })

    return list(
        map(
            lambda t: {
                'id': t[0],
                'body': t[1],
                'board_name': t[2],
                'board_path': t[3]
            }, result.fetchall()
        )
    )

def get_thread(thread_id):
    return construct_thread(thread_id)

def construct_thread(thread_id, limit=None):
    result = db.session.execute(f'''
        SELECT
            posts.id,
            body, image,
            created_at,
            edited,
            filename,
            users.name,
            COUNT(*) OVER() AS post_count,
            users.id
        FROM posts
        LEFT JOIN images
        ON posts.image = images.id
        LEFT JOIN users
        ON posts.author = users.id
        WHERE thread = :id OR posts.id = :id
        ORDER BY created_at ASC
        {f'LIMIT {limit}' if limit else ''}
    ''', { 'id': thread_id })

    threads = result.fetchall()

    if len(threads) == 0:
        raise NotFoundError(f'No thread with id {thread_id} was not found.')

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
                'post_count': t[7] - 1,
                'user_id': t[8]
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

def hide_thread(thread_id):
    db.session.execute('''
        INSERT INTO hides (user_id, thread)
        VALUES (:user_id, :thread_id) ON CONFLICT DO NOTHING
    ''', { 'user_id': session['uid'], 'thread_id': thread_id})
    db.session.commit()
