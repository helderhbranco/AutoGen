import asyncio
from autogen_agentchat.agents import UserProxyAgent, AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models import OpenAIChatCompletionClient

async def user_proxy_run() -> None:
    try:
        # Create a UserProxyAgent
        user_proxy_agent = UserProxyAgent("user_proxy")

        # Create an AssistantAgent
        assistant_agent = AssistantAgent(
            name="assistant",
            model_client=OpenAIChatCompletionClient(
                model="gpt-3.5-turbo",  # Specify the model you want to use
                api_key="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"  # Ensure you have your API key set
            ),
            system_message="You are an assistant that helps users with their questions."
        )

        while True:
            # Prompt the user to enter a message
            user_input = input("Enter your message for the assistant (or type 'exit' to quit): ")

            # Check if the user wants to exit
            if user_input.lower() == 'exit':
                print("Exiting the chat. Goodbye!")
                break

            # Create a TextMessage with the user's input
            user_message = TextMessage(content=user_input, source="user")
            
            # Send the message to the assistant agent
            response = await assistant_agent.on_messages([user_message], cancellation_token=CancellationToken())

            # Print the assistant's response
            print(f"Assistant's response: {response.chat_message.content}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Use asyncio.run(user_proxy_run()) when running in a script.
if __name__ == "__main__":
    asyncio.run(user_proxy_run())
