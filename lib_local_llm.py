from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM

def LocalLLM():
    model_id = 'google/flan-t5-large'# go for a smaller model if you dont have the VRAM
    tokenizer = AutoTokenizer.from_pretrained(model_id) 
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id) #load_in_8bit=True, device_map='auto'
    pipe = pipeline(
        "text2text-generation",
        model=model, 
        tokenizer=tokenizer, 
        max_length=100
    )
    return HuggingFacePipeline(pipeline=pipe)