from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


# Initialize the LLM
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)


# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant. Answer the user's questions clearly and accurately."
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


# Create the LCEL chain
chain = prompt | llm


# Store conversation history
chat_history: list[HumanMessage | AIMessage] = []


while True:
    user_input = input("Ask AI: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input:
        print("Please enter a question.")
        continue

    # Invoke the chain
    response = chain.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    # Display response
    print(f"AI: {response.content}")

    # Save the conversation
    chat_history.append(
        HumanMessage(content=user_input)
    )

    chat_history.append(
        AIMessage(content=response.content)
    )

    # print(f"chat history:  {chat_history}")