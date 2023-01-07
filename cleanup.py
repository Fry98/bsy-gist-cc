from github import Github
from dotenv import load_dotenv
import os

load_dotenv()
g = Github(os.getenv('GITHUB_TOKEN'))
me = g.get_user()

for gist in me.get_gists():
  if gist.description == 'bsy-cc':
    gist.delete()
