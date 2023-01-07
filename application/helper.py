import uuid
from PIL import Image
import os

def get_disk_space():
    stream = os.popen('quota -gsl | grep /')
    output = stream.read()
    items = [item for item in output.split(" ") if item!=""]
    used_space = int(items[1][:-1])
    total_space = int(items[2][:-1])
    return (used_space, total_space)

def get_unique_id():
  return uuid.uuid1().hex

def save_logo_thumbnail(source_path, dest_path):
  image = Image.open(source_path)
  image.thumbnail((300, 300), Image.LANCZOS)
  image.save(dest_path, "png")

def save_user_avatar_thumbnail(source_path, dest_path):
  image = Image.open(source_path)
  image.thumbnail((200, 300), Image.LANCZOS)
  image.save(dest_path, "png")


def save_case_avatar_thumbnail(source_path, dest_path):
  image = Image.open(source_path)
  image.thumbnail((800, 600), Image.LANCZOS)
  image.save(dest_path, "png")


def save_conversation_photo_thumbnail(source_path, dest_path):
  image = Image.open(source_path)
  image.thumbnail((800, 600), Image.LANCZOS)
  image.save(dest_path, "png")