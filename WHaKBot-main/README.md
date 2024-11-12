# WHaKBot

The following "bot" is an AI assistant that is currently using gpt 4-o as the primary LLM. A major focus of the bot is the ability to easily switch between different models for different use cases, and as such, Mistral and Llama3.1 are also compatible.


The "create_agents.py" file is what contains the LLM, using LangChain and LangGraph to implement a variety of tools.

Current functionality includes:

- Image Generation 
  - Flux
  - DALL-E
- Video Generation
- RAG
- Calculator
  - NumPy
- TTS Generation
- DeHashed (OSINT database)

**It is important to remember that the tools provided often require their own respective API keys, and that these are not provided within the following repository.***

*Generated media is passed to an Amazon S3 bucket, so that it can be retrieved by the chat agent in the form of a link.*


-------------------

In order to run the bot, run the command:

***streamlit run create_agents.py***

into the terminal.
 
