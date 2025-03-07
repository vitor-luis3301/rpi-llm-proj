from langdetect import detect
from time import gmtime, strftime

from llm import chat, chat_image
from audio import transcribe_audio, translate_audio, transcribe_and_translate
from record import record_audio
from text import translation_to_en, translation_to_tgt


class Session:
    def __init__(self):
        pass
    
    defaultllm = 'llama3.2:1b'
    defaultvlm = 'moondream'
    text_file_path = ''
    
    # Creating a new query on a section
    def newQuery(self, type, **kwargs):
        input = kwargs.get('input', None)
        images = kwargs.get('images', None)
        language = kwargs.get('language', None)
        
        # Select if the input is text or audio
        # [WARNING] Audio is still WIP
        if type in ['t', 'T', 'text', 'Text']:
            if images: # if images are included
                final = ''
                
                # print the input to the standard output
                input_log = f"{strftime('%H:%M:%S', gmtime())} User: {input}\n{images}"
                print(input_log)
                
                if self.defaultvlm in ['moondream', 'llava-phi3']:
                # Detect the language of the text
                    if not language:
                        language = detect(input)
                    
                    if language != "en":
                        # Translate the text to english if text is not english
                        # This is done because Moondream (the default vision model) doesn't support any other language asside from english
                        translated = translation_to_en(input, language)
                        
                        # Get the model output in a variable and translate to the detected language
                        final = chat_image(self.defaultvlm, translated, images, True, tgt=language)
                    else:
                        # If the input text is already english, there's no need to translate
                        final = chat_image(self.defaultvlm, input, images, False)
                else:
                    # If the input text is already english, there's no need to translate
                    final = chat_image(self.defaultvlm, input, images, False)
                
                # Log the model output in a variable and print to the standard output
                output_log = strftime("\n%H:%M:%S", gmtime()) + ' ' + self.defaultvlm + ': ' + final
                print(output_log)
                
            else:
                # If there's no image, I just do everything again without translating and using a different model
                input_log = f"{strftime('%H:%M:%S', gmtime())} User: {input}"
                print(input_log)
                
                answer = chat(self.defaultllm, input)
                
                output_log = strftime("\n%H:%M:%S", gmtime()) + ' ' + self.defaultllm + ': ' + answer
                print(output_log)
                
        elif type in ['v', 'V', 'voice', 'Voice']:
            #record_audio("question.mp3")            
            if images:
                input_aud = transcribe_and_translate(input, lang=language)
                answer = ''
                
                if input_aud != "en":
                    answer = chat_image(self.defaultvlm, input_aud[1], images, True, tgt=input_aud[0])
                else: 
                    answer = chat_image(self.defaultvlm, input_aud[1], images, False)
                
                output_log = strftime("\n%H:%M:%S", gmtime()) + ' ' + self.defaultvlm + ': ' + answer
                print(output_log)
            else:
                input_aud = transcribe_audio(input)
                
                answer = chat(self.defaultllm, input_aud)
                
                output_log = strftime("\n%H:%M:%S", gmtime()) + ' ' + self.defaultllm + ': ' + answer
                print(output_log)
                
                # with open(self.text_file_path, "w") as text_file:
                #     text_file.write(input_aud[1])
                #     text_file.write("\n")
                #     text_file.write(output_log)