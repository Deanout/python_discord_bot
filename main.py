from app.cogs.Help import MyHelpCommand
from app.client import Client


def main():
    print("Starting bot...")
    client = Client()
    client.help_command = MyHelpCommand()
    client.run(client.token)


if __name__ == "__main__":
    main()
