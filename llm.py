import ollama

from text import translation_to_tgt

def chat(llmodel, message):
    answer = ollama.chat(
        model=llmodel,
        messages=[{
            'role': 'user',
            'content': message
        }]
    )
    
    return answer['message']['content']

def chat_image(vlmodel, question, images, translate, **kwargs):
    tgt = kwargs.get('tgt', None)
    
    answer = ollama.chat(
        model=vlmodel,
        messages=[{
            'role': 'user',
            'content': question, 
            'images': [images]
        }],
    )
    if translate:
        final = translation_to_tgt(answer['message']['content'], tgt)
        return final
    else:
        return answer['message']['content']