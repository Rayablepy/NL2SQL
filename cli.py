import asyncio
from main import getresponse
async def main():
    while True:
        user=input("You(Q to exit): ").lower()
        if user=="q":
            break
        print("-"*75)
        response = await getresponse(user)
        print(f"Bot: {response}")
        print("-"*75)

asyncio.run(main())
