from googletrans import Translator

text = "my name is ai"
translator = Translator()

try:
    detection = translator.detect(text)
    print("Detected language:", detection.lang)

    translation_default = translator.translate(text)
    print("Translation (default):", translation_default.text)

    translation_es_to_en = translator.translate(text, src='en', dest='es')
    print("Translation (ES to EN):", translation_es_to_en.text)

except Exception as e:
    print("An error occurred:", str(e))