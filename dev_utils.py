#!/usr/bin/env python3

import sys
import secrets
import datetime


OPTIONS = {
    "random_hex": {
        "help_text": "Generate random hex string of given length: <key><space><length(default=32)>",
        "keys": ["rand", "random", "randomhex"],
    },
    "random_urlsafe": {
        "help_text": "Generate random url safe string of given length: <key><space><length(default=32)>",
        "keys": ["randu", "randomurlsafe", "randomu"],
    },
    "dotenv_template": {
        "help_text": "Generate env.template from .env: <key>",
        "keys": ["env", "dotenv"],
    }
}


def pp(i, b=0, l=64, e=1):
  """
  i: item to print 
  b: 0 = no border
     1 = top border
     2 = bottom border
     3 = top and bottom border
  l: length of border
  e: 1 = new line at the end
     0 = no new line at the end
  """
  if (b in [1, 3]): print("-" * l)
  print(i, end=("" if e == 0 else "\n"))
  if (b in [2, 3]): print("-" * l, end=("" if e == 0 else "\n"))


def help():
  pp("\nHelp:")
  for s_name, s_desc in OPTIONS.items():
    pp(s_desc["help_text"], 1)
    pp("keys: ", e=0)
    pp(s_desc["keys"], 0)
  pp("", b=1)


if "__main__" == __name__:
  # pp("Params:",1)
  # pp(sys.argv,2)

  if len(sys.argv) < 2:
    pp("No argument passed.")
    help()
    sys.exit()

  if sys.argv[1] in ["h", "help"]:
    help()
    sys.exit()

  if sys.argv[1] in OPTIONS["random_hex"]["keys"]:
    length = 32
    if len(sys.argv) > 2: length = int(sys.argv[2])
    pp(secrets.token_hex(length), 3)
    sys.exit()

  if sys.argv[1] in OPTIONS["random_urlsafe"]["keys"]:
    length = 32
    try:
      if len(sys.argv) > 2: length = int(sys.argv[2])
      pp(secrets.token_urlsafe(length), 3)
    except Exception as e:
      pp(type(e).__name__)
    finally:
      sys.exit()

  if sys.argv[1] in OPTIONS["dotenv_template"]["keys"]:
    env_file = None
    env_template_file = None
    env_template_file_content = []
    try:
      env_file = open('./.env', "r", encoding="utf-8")

      for line in env_file:
        cur_line = line.split("=")[0].strip()
        if cur_line == "": continue
        if not cur_line.startswith("#"):
          env_template_file_content.append(cur_line + "=" + "\n")
        else:
          env_template_file_content.append(cur_line + "\n")

      if len(env_template_file_content) > 0:
        env_template_file = open('./env.template', "w", encoding="utf-8")
        env_template_file.writelines(env_template_file_content)
        pp(f"env.template generated with {len(env_template_file_content)} lines", 1)
      env_file.close()
      env_template_file.close()
    except FileNotFoundError:
      pp(".env file not found", b=3)
    finally:
      if env_file and env_file.closed:
        pp('.env File closed.', b=1)
      else:
        env_file.close()
      if env_template_file and env_template_file.closed:
        pp('env.template File closed.', b=2)
      else:
        env_template_file.close()
      sys.exit()

  # --------------------------
  pp("Switch/Key/Parameter not recognized.", 3)
  sys.exit()