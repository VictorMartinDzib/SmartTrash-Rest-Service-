from bcrypt import hashpw, checkpw, gensalt

def encryptPassword(password):
      return hashpw(password.encode('utf-8'), gensalt())


def validatePassword(password, hashAndSalt):
      return checkpw(password.encode('utf-8'), hashAndSalt)



#Testing functions
'''
password = input("password: ")

print(res:=encryptPassword(password))
password = "hs"
print(val:=validatePassword(password, res))
'''