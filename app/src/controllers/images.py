import secrets

from db import db

def add_image(image):
    if not image:
        return

    content_type = image.content_type

    if not content_type.startswith('image/'):
        raise Exception('invalid type')

    filename = secrets.token_hex(16)
    data = image.read()

    result = db.session.execute('''
        INSERT INTO images (filename, data, content_type)
        VALUES (:filename, :data, :content_type)
        RETURNING id
    ''', { 'filename': filename, 'data': data, 'content_type': content_type })
    db.session.commit()

    image_id = result.fetchone()[0]

    return image_id

def get_image(filename):
    result = db.session.execute('''
        SELECT data, content_type
        FROM images
        WHERE filename = :filename
    ''', { 'filename': filename })

    image_obj = result.fetchone()

    return {
        'data': image_obj[0],
        'content_type': image_obj[1]
    }
