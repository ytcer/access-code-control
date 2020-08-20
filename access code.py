from Crypto import Random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
#from Crypto.Util.Padding import pad
import hashlib
def generate_access_code():
	acode=raw_input("please sign your access code")
	m=hashlib.sha256()
	m.update(acode)
	acode_hash=m.digest()
	with open("hash_access_code.txt", "wb") as f:
		f.write(acode_hash)
	return acode

def generate_data_key(acode,iv):
	key=acode + "444444444444"
	mode=AES.MODE_CFB
	data_key=Random.new().read(AES.block_size)
	key_encrypted=AES.new(key,mode,iv)
	encrypted_data_key=key_encrypted.encrypt(data_key)
	with open ("Key.pem", "wb") as f:
		f.write(encrypted_data_key)

def get_data_key(acode):
	with open ("Key.pem", "r") as f:
		encrypted_data_key=f.read()

	data=encrypted_data_key
	with open ("IV.pem","r") as f:
		iv=f.read()
	key=acode + "444444444444"
	mode=AES.MODE_CFB
	
	key_decrypted=AES.new(key,mode,iv)
	pt=key_decrypted.decrypt(data)
	return pt
def get_data(data_key):
	with open ("encrypted.text","r") as f:
		data=f.read()
	
	with open ("IV.pem","r") as f:
		iv=f.read()
	
	key=data_key
	mode=AES.MODE_CFB
	
	key_decrypted=AES.new(key,mode,iv)
	pt=key_decrypted.decrypt(data)
	return pt
def generate_iv():
	iv=Random.new().read(AES.block_size)
	with open ("IV.pem", 'wb') as f:
		f.write(iv)
	return iv
def encrypted_iv():
	with open ("IV.pem","r") as f:
		iv=f.read()
	return iv
def encrypted_key():
	with open ("Key.pem","r") as f:
		key=f.read()
	return key		
def encrypted_message(text,iv,key):

	mode=AES.MODE_CFB
	
	iv=encrypted_iv()
	
	cryptos=AES.new(key,mode,iv)
	cipher_text=cryptos.encrypt(text)
	with open ("encrypted.text","wb") as f:
		f.write(cipher_text)
	return cipher_text
#def encrypted_key()
if __name__=='__main__':
	text='0'
	print "input '1' for regenrate AES and access code"
	print "input '2' for encryption"
	print "input '3' for decryption"
	print "input 'exit' for quiting"

	while text!="quit":
		text=raw_input("input 1,2,3")
		
		if text=="1":
			print "generate key and iv"
			iv=generate_iv()
			acode=generate_access_code()
			generate_data_key(acode,iv)
		if text=="3":
			print "decrypted mode"
			acode=raw_input("please input your access code")
			data_key=get_data_key(acode)
			get_data(data_key)
			with open("hash_access_code.txt", "r") as f:
				correct=f.read()
				m=hashlib.sha256()
				m.update(acode)
				acode_hash=m.digest()
			if acode_hash==correct:
				print "access code check ok!"
				data_key=get_data_key(acode)
				pt=get_data(data_key)
				print pt
			else:
				print "input error!"
		if text=='2':
			print "encrypted message"
			acode=raw_input("please input your access code")
			with open("hash_access_code.txt", "r") as f:
				correct=f.read()
			m=hashlib.sha256()
			m.update(acode)
			acode_hash=m.digest()
			if acode_hash==correct:
				print "access code check ok!"
				message=raw_input("please input the message you want to encrypt")
				iv=encrypted_iv()
				data_key=get_data_key(acode)
				en=encrypted_message(message,iv,data_key)
			else:
				print "input error!"
			
	
	
	

