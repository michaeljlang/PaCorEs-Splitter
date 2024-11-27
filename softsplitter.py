import re
from sentence_splitter import SentenceSplitter

def softsplit(text,lang):

    """
    This will segment a text string twice, first using SentenceSplitter, and then with additional 
    segmentation for colons, semicolons, and other soft punctuation, such as quotations marks
    that SentenceSplitter will have ignored. The aim is to provide a cleaner and more granular split 
    in order to yield smaller bitexts upon alignment.
    
    Args:
        text - string with text to split
        lang - language code
        
            Language codes include:
            
                Spanish - "es"
                English - "en"
                German - "de"
            
    Returns:
        segmented text - string with additional segmentation

    """
 
    splitter = SentenceSplitter(language=lang)
    segmented = splitter.split(text=text)
    segmented = [line.strip() for line in segmented if line != ""]
    segmented = "\n".join(segmented)

    replacements = [
        ("; ",";\n"),
        (": ",":\n")
    ]
    
    for old, new in replacements:
        segmented = re.sub(old, new, segmented)
        
    segments = segmented.split("\n")
    final_text = ""
    for item in segments:
        if item.count(")") != item.count("("):
            final_text = final_text + item + " "
        elif item.count("]") != item.count("["):
            final_text = final_text + item + " "
        elif "i.e." in item[-5:]:
            final_text = final_text + item + " "
        else:
            final_text = final_text + item +"\n"
            
    # for German
    if lang == "de":
        while re.search("\w[.?!«] [„»]", final_text) != None:
            instance_lowcomma = re.search("\w[.?!«] [»„]", final_text)
            final_text = final_text[:instance_lowcomma.span()[0]+2]+"\n"+final_text[instance_lowcomma.span()[0]+3:]
            
        total_cases_endquote = re.findall("« [^a-z(]", final_text)
        for item in total_cases_endquote:
            instance_endquote = re.search(re.escape(item),final_text).span()[0]
            final_text = final_text[:instance_endquote+1]+"\n"+final_text[instance_endquote+2:]
    
    # for Spanish
    if lang == "es":
        while re.search("[.?!»] [—][A-Z¡¿].*\n", final_text) != None:
            instance_emdash = re.search("[.?!»] [—][A-Z¡¿].*\n", final_text)
            final_text = final_text[:instance_emdash.span()[0]+1]+"\n"+final_text[instance_emdash.span()[0]+2:] 
                   
    return final_text