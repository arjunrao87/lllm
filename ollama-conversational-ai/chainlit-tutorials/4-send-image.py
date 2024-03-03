import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    image = cl.Image(path="./assets/gemma.jpeg", name="hero", display="side")

    # Attach the image to the message
    await cl.Message(
        content="This message has a hero!",
        elements=[image],
    ).send()
