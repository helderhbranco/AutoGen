import asyncio
from autogen_agentchat.agents import UserProxyAgent, AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models import OpenAIChatCompletionClient

async def main():
    # Create a UserProxyAgent
    user_proxy_agent = UserProxyAgent("user_proxy")

    # Create two AssistantAgents
    assistant_agent1 = AssistantAgent(
        name="assistant1",
        model_client=OpenAIChatCompletionClient(
            model="gpt-3.5-turbo",
            api_key="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"
        ),
        system_message="You are an assistant that helps users with their questions."
    )
    assistant_agent2 = AssistantAgent(
        name="assistant2",
        model_client=OpenAIChatCompletionClient(
            model="gpt-3.5-turbo",
            api_key="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"
        ),
        system_message="You are a assistant that helps users with their questions."
    )

    # Example interaction with the UserProxyAgent
    while True:
        # Prompt user to select an assistant or both
        assistant_choice = input("Choose an assistant (1, 2, or just enter for both) or type 'exit' to quit: ")
        if assistant_choice.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break

        # Validate the choice
        if assistant_choice not in ['1', '2', '']:
            print("Invalid choice. Please enter 1, 2, or both.")
            continue

        # Prompt user for the message
        user_input = input("Enter your message: ")

        # Create a message for the assistants
        user_message = TextMessage(content=user_input, source="user")

        # Send the message based on the user's choice
        if assistant_choice == '1':
            response = await assistant_agent1.on_messages([user_message], cancellation_token=CancellationToken())
            print(f"Assistant 1's response: {response.chat_message.content}")
        elif assistant_choice == '2':
            response = await assistant_agent2.on_messages([user_message], cancellation_token=CancellationToken())
            print(f"Assistant 2's response: {response.chat_message.content}")
        elif assistant_choice == '':
            responses = await asyncio.gather(
                assistant_agent1.on_messages([user_message], cancellation_token=CancellationToken()),
                assistant_agent2.on_messages([user_message], cancellation_token=CancellationToken())
            )
            print(f"Assistant 1's response: {responses[0].chat_message.content}")
            print(f"Assistant 2's response: {responses[1].chat_message.content}")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
