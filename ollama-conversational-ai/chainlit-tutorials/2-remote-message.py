import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    print("A new chat session has started")


@cl.on_message
async def on_message(message: cl.Message):
    msg1 = cl.Message(content="Processing request...")
    await msg1.send()

    msg2 = cl.Message(content="")
    await msg2.send()

    # pretend to do something remotely
    await cl.sleep(5)

    msg2.content = f"Received response {message.content}"

    await msg2.update()


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")
