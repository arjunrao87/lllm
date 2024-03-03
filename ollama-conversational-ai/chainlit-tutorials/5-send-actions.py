import chainlit as cl


@cl.on_chat_start
async def on_chat_start():

    actions = [
        cl.Action(name="Click Me!!!", value="sample value", description="Click Me!")
    ]
    # Attach the image to the message
    await cl.Message(
        content="Here",
        actions=actions,
    ).send()


@cl.action_callback("Click Me!!!")
async def handle_user_input():
    print("Clicked the button!!")
    await cl.sleep(5)
    await cl.Message(content="Completed processing!").send()
