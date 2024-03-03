# Running a finance model using Ollama

- Search for the model from Hugging Face [Link](https://huggingface.co/TheBloke/finance-LLM-13B-GGUF/tree/main)
- Go to the `Files` tab and download the .gguf file for the right level of quantization
- Create a `Modelfile` to describe how to use this downloaded model (see [this](./Modelfile))
- Create the Ollama model `ollama create financellm -f Modelfile` and reference the downloaded model
- Confirm your model shows up in ollama using `ollama list`
- Run the Ollama model `ollama run financellm`
