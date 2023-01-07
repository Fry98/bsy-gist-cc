from github import Github, InputFileContent
from threading import Thread
from dotenv import load_dotenv
from time import sleep, time
from os import getenv, path
from math import floor

CHSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

load_dotenv()
g = Github(getenv('GITHUB_TOKEN'))
me = g.get_user()

if path.exists('gid.bot'):
  with open('gid.bot', 'r') as f:
    gist = g.get_gist(f.read())
else:
  gist = me.create_gist(False, {
    'heartbeat.md': InputFileContent(f'sup\n<!-- {floor(time())} -->'),
    'comm.md': InputFileContent(f'hi\n<!-- res temp -->')
  }, 'bsy-cc')

  with open('gid.bot', 'w') as f:
    f.write(gist.id)

def heartbeat():
  while True:
    gist.edit(files={
      'heartbeat.md': InputFileContent(f'sup\n<!-- {floor(time())} -->')
    })
    sleep(5)

Thread(target=heartbeat, daemon=True).start()

while True:
  pass
