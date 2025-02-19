import pyotp



key = pyotp.random_base32()
totp = pyotp.TOTP(key, interval=180)
# print(totp.now()) # => '492039'
print((totp.now()))


totp.verify('541627') # => True
totp = pyotp.TOTP(key, interval=180)
totp = pyotp.TOTP(key, interval=180)
input_2fa  = input("Enter your OTP: ")

print(totp.verify(input_2fa))
