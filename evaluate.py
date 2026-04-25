import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def load_prompt():
    with open("prompt.txt", "r") as f:
        return f.read()

def main():
    system_prompt = load_prompt()
    conversation_history = []

    print("\n╔════════════════════════════════════════╗")
    print("║   VERDIKT — Investment Dialogue Agent  ║")
    print("╚════════════════════════════════════════╝\n")
    print("Paste your startup description below.")
    print("When done, press Enter twice.\n")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    description = "\n".join(lines)

    if not description.strip():
        print("No description provided. Exiting.")
        return

    print("\nEvaluating... please wait.\n")
    print("─" * 50)

    conversation_history.append({
        "role": "user",
        "content": f"Please evaluate this startup:\n\n{description}"
    })

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        system=system_prompt,
        messages=conversation_history
    )

    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    print(assistant_message)

    session_log = []
    session_log.append(f"STARTUP:\n{description}\n")
    session_log.append(f"VERDIKT:\n{assistant_message}\n")

    print("\n" + "─" * 50)
    print("DIALOGUE MODE — Type your response below.")
    print("Commands: 'match me' to find VCs, 'save' to export, 'quit' to exit")
    print("─" * 50 + "\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("\nSession ended.")
            break

        if user_input.lower() == "save":
            filename = input("Save as (e.g. startup_name.txt): ").strip()
            with open(filename, "w") as f:
                f.write("═" * 50 + "\n")
                f.write("VERDIKT SESSION REPORT\n")
                f.write("═" * 50 + "\n\n")
                f.write("\n\n".join(session_log))
            print(f"Session saved to {filename}\n")
            continue

        if user_input.lower() in ["match me", "find vcs", "find vc", "match"]:
            print("\nScanning VC database and matching to your profile...\n")
            print("─" * 50)

            conversation_history.append({
                "role": "user",
                "content": "match me"
            })

            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=2000,
                system=system_prompt,
                messages=conversation_history
            )

            assistant_message = response.content[0].text
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            session_log.append(f"FOUNDER:\n[Requested VC matching]\n")
            session_log.append(f"VERDIKT:\n{assistant_message}\n")

            print(f"\nVerdikt:\n\n{assistant_message}\n")
            print("─" * 50)
            print("Type any VC name for a full profile and approach strategy.")
            print("─" * 50 + "\n")
            continue

        if not user_input:
            continue

        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        session_log.append(f"FOUNDER:\n{user_input}\n")

        print("\nVerdikt is thinking...\n")

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system=system_prompt,
            messages=conversation_history
        )

        assistant_message = response.content[0].text
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        session_log.append(f"VERDIKT:\n{assistant_message}\n")

        print("─" * 50)
        print(f"\nVerdikt:\n\n{assistant_message}\n")

if __name__ == "__main__":
    main()