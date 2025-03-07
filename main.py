from time import gmtime, strftime

from session import Session

newSession = Session()

print(strftime("%H:%M:%S", gmtime()))

newSession.newQuery('v', input="question.mp3")
#newSession.newQuery('v', '3', images="C:\\Users\\super\\rpi-llm-proj\\Imagem-teste.png", language="pt")