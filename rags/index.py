from rag_pipeline import RAGPipeline


# ============================================================
# 8. MAIN
# ============================================================

def main():


    while True:
        query = input("Ask AI: ")

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            print("Please enter a question")
            continue

        pipeline = RAGPipeline()


    

        pipeline.build(query)



        response = pipeline.query(query)

        print("\n" + "=" * 60)
        print(f"Query: {query}")
        print("=" * 60)
        print(f"Response: {response}")
        print("=" * 60)


if __name__ == "__main__":
    main()