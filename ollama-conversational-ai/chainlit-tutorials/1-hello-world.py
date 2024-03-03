import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    print("A new chat session has started")


@cl.on_message
async def on_message(message: cl.Message):
    print("The user sent a message = " + message.content)
    response = f"Hello, you just sent: {message.content}!"
    await cl.Message(response).send()


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")
