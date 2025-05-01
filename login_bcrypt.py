import bcrypt

# Hash the password before storing it
password = "securepassword"
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

print("Hashed password:", hashed_password)

# Verify the password during login
input_password = "securepassword"  # Replace this with the user input
if bcrypt.checkpw(input_password.encode(), hashed_password):
    print("Password is correct!")
else:
    print("Password is incorrect!")
