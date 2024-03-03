import chainlit as cl


@cl.step
async def process():
    # pretend to do something remotely
    await cl.sleep(5)
    return "Response from Process"


@cl.on_chat_start
async def on_chat_start():
    print("Onstart")


@cl.on_message
async def on_message(message: cl.Message):
    response = await process()

    msg = cl.Message(content="Final response")
    await msg.send()
