from datetime import datetime
from db import db

def create_thread(content, board, author, image_id=None):
    db.session.execute('''
        INSERT INTO posts (board, author, body, image, created_at)
        VALUES (:board, :author, :body, :image, current_timestamp)
    ''', { 'board': board, 'author': author, 'body': content, 'image': image_id })
    db.session.commit()

def reply(thread_id, content, author, image_id=None):
    db.session.execute('''
        INSERT INTO posts (board, thread, author, body, image, created_at)
        VALUES (
            (SELECT board FROM posts WHERE id = :thread),
            :thread, :author, :body, :image, current_timestamp)
        ''', {'thread': thread_id, 'author': author, 'body': content, 'image': image_id})
    db.session.commit()

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
    return construct_threads(thread_ids)

def get_thread(thread_id):
    return construct_thread(thread_id)

def construct_thread(thread_id):
    result = db.session.execute('''
        SELECT posts.id, body, image, created_at, edited, filename
        FROM posts
        LEFT JOIN images
        ON posts.image = images.id
        WHERE thread = :id OR posts.id = :id
        ORDER BY created_at ASC
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
            },
            threads
        )
    )

def construct_threads(thread_ids):
    return list(map(construct_thread, thread_ids))