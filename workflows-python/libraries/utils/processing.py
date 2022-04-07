import logging

def get_doc_content(path):
    with open(path, 'r') as f:
        content = f.read()    
    return content

def process_doc(path):
    try:
        content = get_doc_content(path)
        new_content = content[::-1]
        logging.info(f"Processed content:\n{new_content}")
        return new_content
    except Exception as e:
        logging.error(f"Error processing document.")
    return None
