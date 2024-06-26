from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load tokenizer and model
model_name = "Kiran2004/GPT2_MentalHealth_ChatBot"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)