from main import getresponse
while True:
    user=input("You(Q to exit): ").lower()
    if user=="q":
        break
    print("-"*75)
    print(f"Bot: {getresponse(user)}")
    print("-"*75)
