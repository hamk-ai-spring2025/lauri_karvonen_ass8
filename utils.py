def load_env_variables():
    from dotenv import load_dotenv
    import os

    load_dotenv()

def handle_exception(e):
    print(f"An error occurred: {e}")

def is_exit_command(command):
    return command.lower() in ["exit", "quit"]