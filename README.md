# GIST-CC
All communication is using hidden comments inside markdown to transfer data. In most cases, data is being sent directly in the form of an ascii string but in the case of the `scp` command, the binary content of the file is encoded in base64 by the bot and decoded back into binary on the side of controller before being written into a file.

Demo: https://youtu.be/pmssUB6hJvo

## Requirements
This script was written to target `Python 3.10.6` *(but afaik it doesn't use any particularly new features so you're probably fine)*.

Install all dependecies *(probably inside a venv)* by running:
```
pip install -r requirements.txt
```

Before running either of the scripts, you need to set an environment variable `GITHUB_TOKEN` containing your GitHub access token with the `gist` scope selected. Alternatively, you can create a `.env` file inside this project directory and specify the token there in the format:
```
GITHUB_TOKEN=<your_token>
```


## Commands
```
list
```
```
help
```
```
ls <bot_id> <path>
```
```
w <bot_id>
```
```
id <bot_id>
```
```
scp <bot_id> <src_path> <dest_path>
```
```
exec <bot_id> <command>
```
