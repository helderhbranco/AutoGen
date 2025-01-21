import asyncio
from autogen_core import SingleThreadedAgentRuntime, BaseAgent, TypeSubscription, TopicId
from autogen_agentchat.messages import TextMessage

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyAgent")
        
    async def on_message_impl(self, message, ctx):
        print(f"Received message: {message.content}")
        return TextMessage(content=f"Echo: {message.content}", source="MyAgent")
        
        
class MyAgent2(BaseAgent):
    def __init__(self):
        super().__init__("MyAgent2")

    async def on_message_impl(self, message, ctx):
        print(f"Received message: {message.content}")
        return TextMessage(content=f"Echo: {message.content}", source="MyAgent2")
    

async def main():
    # Initialize the runtime
    runtime = SingleThreadedAgentRuntime()
    runtime2 = SingleThreadedAgentRuntime()

    # Register the agent type with the runtime
    await MyAgent.register(runtime, "my_agent", lambda: MyAgent())
    await MyAgent2.register(runtime2, "my_agent2", lambda: MyAgent2 ())

    # Define a type-based subscription
    type_subscription = TypeSubscription(topic_type="com.example.my-topic", agent_type="my_agent")
    type_subscription = TypeSubscription(topic_type="com.example.my-topic2", agent_type="my_agent2")
    await runtime.add_subscription(type_subscription)

    # Create a TopicId for the message
    topic_id = TopicId(topic_type="com.example.my-topic", source="user")
    topic_id2 = TopicId(topic_type="com.example.my-topic2", source="user")
    

    # Publish a message to the topic
    await runtime.publish_message(
        TextMessage(content="Hello, how can you assist me today?", source="user"),
        topic_id=topic_id
    )
    await runtime.publish_message(
        TextMessage(content="Hello, what time is around the world?", source="user"),
        topic_id=topic_id2
    )

    # Run the runtime to process messages
    await runtime.run()
    await runtime2.run()

if __name__ == "__main__":
    asyncio.run(main())
