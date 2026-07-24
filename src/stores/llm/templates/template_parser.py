from .locales import ar, en
import os
# use this to make multi-language app

class TemplateParser:
    def __init__(self, language:str=None, default_language='en'):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None

        self.set_language(language=language)


    def set_language(self, language: str):

        if not language:
            self.language = self.default_language
        
        language_path = os.path.join(self.current_path, "locales", language)
        if os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language

    # group is each file inside the languages (ar/rag)
    # key the Template inside each group
    # vars for the variabels
    def get(self, group: str, key: str, vars: dict={}):
        
        if not group or not key:
            return None
        
        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py")
        targeted_language = self.language
        
        if not os.path.exists(group_path): # if the group not found in this language change to the default language
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py")
            targeted_language = self.default_language

        if not os.path.exists(group_path):
            return None
        
        # import group module in run time
        module = __import__(f"stores.llm.templates.locales.{targeted_language}.{group}", fromlist=[group])

        if not module:
            return None
        
        key_attribute = getattr(module, key)

        return key_attribute.substitute(vars)
