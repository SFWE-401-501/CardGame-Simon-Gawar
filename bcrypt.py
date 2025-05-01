import bcrypt

# Hash the password before storing it
hashed_password = bcrypt.hashpw("securepassword".encode(), bcrypt.gensalt())

# Verify the password during login
if bcrypt.checkpw(input_password.encode(), hashed_password):
    print("Password matches!")
else:
    print("Invalid password!")
