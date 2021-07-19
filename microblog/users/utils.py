from microblog import mail
from flask_mail import Message
from PIL import Image
import secrets
import os
from flask import url_for, current_app


def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, picture_extension = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + picture_extension
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics/' + picture_file_name)

    # resize the image
    image_output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(image_output_size)
    i.save(picture_path)
    return picture_file_name


def send_reset_email(user):
    token = user.generate_reset_token()
    msg = Message('Password Reset Request',
                  sender='kchemutai2@gmail.com', recipients=[user.email])
    msg.body = f'''
    To reset your password, visit the following link {url_for('users_bp.reset_password', token=token, _external=True)}
    If you did not make this request, then ignore this mail and nothing will happen.
    '''
    mail.send(msg)
