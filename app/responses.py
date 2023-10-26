import random


def handle_response(message) -> str:
    processed_message = message.lower()
    if processed_message == "hello":
        return "Hello, how are you?"

    if processed_message == "roll":
        return str(random.randint(1, 6))

    if processed_message == "help":
        return "`I can roll a dice for you. Just type 'roll'.`"

    return "Sorry, I don't understand you."
