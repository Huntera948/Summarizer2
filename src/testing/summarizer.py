from transformers import BartTokenizer, BartForConditionalGeneration

# initialize the model and tokenizer
model = BartForConditionalGeneration.from_pretrained('sshleifer/distilbart-xsum-12-6')
tokenizer = BartTokenizer.from_pretrained('sshleifer/distilbart-xsum-12-6')

# function to summarize text
def summarize_text(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=1024, truncation=True)
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)  # skip special tokens during decoding
