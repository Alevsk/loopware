# loopware
PoC of a ransomware that encrypts your files using AES and unlocks them only after you have seen a 10 hours loop youtube video.

## Usage

```
$ python3 loopware.py --help

( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)

loopWare v0.0.1 (https://github.com/Alevsk/loopware)

Usage: loopware.py -f secret.txt | --file secret.txt | --folder allmysecrets

Options:
  -h/--help             show this help message and exit
  -p/--password=PASS..  set password file for AES decryption
  -f/--file=FILE        encrypt/decrypt this file
  -F/--folder=FOLDER    encrypt/decrypt all files in this folder
  --encrypt             encrypt file(s)
  --decrypt             decrypt file(s)
  --recursive           encrypt/decrypt files in folder recursively

Examples:
python3 loopware.py -f secret.txt --encrypt
python3 loopware.py -f secret.txt -p key.secret --decrypt
python3 loopware.py -F my_secret_folder/ --encrypt --recursive
python3 loopware.py -F my_secret_folder/ -p key.secret --decrypt --recursive
python3 loopware.py --help

```

## For educational purpose only

Malware research is one of the most exciting field in the information security industry, the purpose of this project is to try to understand how some of the most sophisticate ransomwares (such as locky) works, what are their weaknesses and how can we stop them.

What a better way to learn than to design and implement one piece of malware from scratch.