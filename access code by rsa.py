from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import sys
import os
def generate_RSA():
	
	random_generator=Random.new().read
	print random_generator
	rsa=RSA.generate(1024, random_generator)
	private_pem=rsa.exportKey()
	public_pem=rsa.publickey().exportKey()
	with open('master-private.pem','wb') as f:
    		f.write(private_pem)
	print private_pem
	with open('master-public.pem','wb') as f:
    		f.write(public_pem)
	print random_generator
	
def collect_id():
    #collect bidder_info
    bidder_id=raw_input('please input your company name:')
    with open(bidder_id+" price info",'wb') as f:
	f.write('empty')
    return bidder_id
def collect_price():
    price=raw_input("please input your price:")
    return price

def encrypted(bidder_id,price):
    #encryption bidder_info
    with open('master-public.pem','r') as f:
    	Key=f.read()
        public_key=RSA.importKey(Key)
        cipher= PKCS1_v1_5.new(public_key)
        cipher_message=base64.b64encode(cipher.encrypt(price.encode(encoding='utf-8')))
	#print "this is encrypted price\n"
        #print cipher_message
    with open(bidder_id+' price info','wb') as f:	
        f.write(cipher_message)
def decrypted():
    #decrption bidder_info
    company=raw_input("please select the company name:")
	
    with open('master-private.pem') as f:
        private_key=f.read()
    with open(company+ ' price info','r') as f:
        encrypted_message=f.read()
	Key=RSA.importKey(private_key)
        decrypted_cipher= PKCS1_v1_5.new(Key)
	print "this is plaintext\n" 
        plaintext_message=decrypted_cipher.decrypt(base64.b64decode(encrypted_message),'ERROR')        
	print plaintext_message
def list_company():
	names=os.listdir('/root')
	for name in names:
		if name.endswith('price info'):
			print name
if __name__=='__main__':
   # generate RSA
	print "input 'generate' for regenrate RSA key"
	print "input 'bidder' for storing price"
	print "input 'admin' for checking price"
	print "input 'exit' for quiting"
	print "input 'list' for listing all the company information"
	while raw_input!='exit':
		command = raw_input()
		print command
		if command=="generate":
			generate_RSA()
		if command=='bidder':
			id=collect_id()
			price=collect_price()
			encrypted(id,price)
		if command=='admin':
			
			decrypted()
		if command=='list':
			list_company()

	  
