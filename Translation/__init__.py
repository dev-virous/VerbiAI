from transformers import MBart50Tokenizer, MBartForConditionalGeneration
import langid, torch

class Translation:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = MBart50Tokenizer.from_pretrained(
            "facebook/mbart-large-50-many-to-many-mmt"
        )
        self.model = MBartForConditionalGeneration.from_pretrained(
            "facebook/mbart-large-50-many-to-many-mmt"
        )
        self.model.to(self.device)
        self.__langs = {}
        for lang_code, lang_id in self.tokenizer.lang_code_to_id.items():
            lang = lang_code.split("_")[0].lower()
            self.__langs[lang] = {
                "lang_code": lang_code,
                "lang_id": lang_id
            }
    def get_lang_id(self, lang):
        lang = lang.lower()
        if self.__langs.get(lang):
            return self.__langs[lang]["lang_id"]
        return self.__langs["en"]["lang_id"]
    def detect_lang(self, text):
        lang, confidence = langid.classify(text)
        return lang.lower()
    def translate(
        self,
        query: str,
        target_language_code: str,
        source_language_code: str = None,
    ):
        if not source_language_code:
            source_language_code = self.detect_lang(query)
            self.detection_lang = source_language_code
        source_lang_code = self.__langs.get(source_language_code, {}).get("lang_code", "en_XX")
        target_lang_id = self.get_lang_id(target_language_code)
        self.tokenizer.src_lang = source_lang_code
        inputs = self.tokenizer(
            query,
            return_tensors="pt",
        ).to(self.device)
        generated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=target_lang_id
        )
        translated_text = self.tokenizer.decode(
            generated_tokens[0],
            skip_special_tokens=True
        )
        return translated_text
    def get_langs(self):
        return self.__langs

model = Translation()