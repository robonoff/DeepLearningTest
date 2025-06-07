import autogen
import json
from datetime import datetime
from config_list import config_list

# Configure agents with the LLM configuration
assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. Your goal is to help the user solve problems."
)

# Disable Docker usage in the UserProxyAgent by setting code_execution_config
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # No human input needed
    system_message="You are a comedian interested to make jokes about Artificial intelligence and Machine Learning",
    default_auto_reply="That's interesting. Nice joke!",
    code_execution_config={"use_docker": False}  # Disable Docker requirement
)

# Initialize conversation history that will be saved to JSON
conversation_history = []

# Override the receive method to save messages
original_receive = user_proxy.receive

def receive_and_save(message, sender, request_reply=False, silent=False):
    conversation_history.append({
        "timestamp": datetime.now().isoformat(),
        "sender": sender.name,
        "message": message
    })
    return original_receive(message, sender, request_reply, silent)

user_proxy.receive = receive_and_save

# Override assistant's receive method too
original_assistant_receive = assistant.receive

def assistant_receive_and_save(message, sender, request_reply=False, silent=False):
    conversation_history.append({
        "timestamp": datetime.now().isoformat(),
        "sender": sender.name,
        "message": message
    })
    return original_assistant_receive(message, sender, request_reply, silent)

assistant.receive = assistant_receive_and_save

# Start the conversation with max_turns=2 to limit to 2 exchanges
user_proxy.initiate_chat(
    assistant,
    message="Can you tell me what clustering and regression have in common? Make me laugh a lot!",
    max_turns=2  # Limit to 2 exchanges (1 from user, 1 from assistant)
)

# Save the conversation to a JSON file
with open("agent_conversation.json", "w") as f:
    json.dump(conversation_history, f, indent=2)

print("Conversation completed and saved to agent_conversation.json")