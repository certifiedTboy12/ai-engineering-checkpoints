import pytextrank #text summarization
import spacy
# Load the pre-trained SpaCy model
nlp = spacy.load("en_core_web_sm")

nlp.add_pipe("textrank")


text  = ("The Eiffel Tower, located in Paris, France, was constructed between 1887 and 1889 as the entrance arch to the 1889 World’s Fair."
"It was designed by Gustave Eiffel’s engineering company and initially faced criticism from artists and intellectuals who considered it an eyesore."
 "Today, the Eiffel Tower is one of the most visited monuments in the world, attracting over 7 million visitors annually."
 "In 2015, special lighting systems were added to enhance its nighttime appearance and improve energy efficiency.")



# #Fixed sized chunking
def chunk_text(text: str, chunk_size: int):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# print(text)
chunks = chunk_text(text, chunk_size=50)


for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:\n{chunk}\n")


# Extract key points
doc = nlp(text)
# Extract and print named entities
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)


# Summary Text
print('Original Document Size:',len(text))

doc = nlp(text)
for sent in doc._.textrank.summary(limit_phrases=2, limit_sentences=2):
    print(sent)
    print('Summary Length:',len(sent))