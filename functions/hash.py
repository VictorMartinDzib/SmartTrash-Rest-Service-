from bcrypt import hashpw, checkpw, gensalt

def encryptPassword(password):
      return hashpw(password.encode(), gensalt())


def validatePassword(password, hashAndSalt):
      return checkpw(password.encode(), hashAndSalt)


'''
#Testing functions

password = input("password: ")

print(res:=encryptPassword(password))
password = "hs"
print(val:=validatePassword(password, res))
 '''


from secrets import token_hex

print(token_hex(16))