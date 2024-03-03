from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import Runnable

import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    # Sending an image with the local file path
    elements = [cl.Image(name="image1", display="inline", path="assets/gemma.jpeg")]
    await cl.Message(
        content="Hello there, I am Gemma. How can I help you ?", elements=elements
    ).send()
    model = Ollama(model="mistral")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a knowledgeable historian who answers super concisely",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):

    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
    ):
        await msg.stream_token(chunk)

    await msg.send()


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")
