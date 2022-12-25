import uuid
from PIL import Image


def get_unique_id():
  return uuid.uuid1().hex


def save_user_avatar_thumbnail(source_path, dest_path):
  image = Image.open(source_path)
  image.thumbnail((200, 300), Image.LANCZOS)
  image.save(dest_path, "png")


def save_case_avatar_thumbnail(source_path, dest_path):
  image = Image.open(source_path)
  image.thumbnail((800, 600), Image.LANCZOS)
  image.save(dest_path, "png")