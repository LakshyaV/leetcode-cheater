import cohere

co = cohere.Client(api_key="AVd0OJeorpIMftjg4eGuT6AIJL75C8nezswvwVRU")

def get_response(dataVar):
    response = co.chat(model="command-r-plus", message=dataVar)
    return response.text