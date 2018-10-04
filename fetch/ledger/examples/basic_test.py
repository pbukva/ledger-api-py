import basic

def main():
    """business logic for when running this module as the primary one!"""
    request = basic.SimpleBalanceRequest("localhost", 8000)
    request.run(number_of_identities=10)

if __name__ == '__main__':
    main()
