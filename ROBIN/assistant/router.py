from tools.command import execute_command

def router_command(text):
    text=text.lower()

    open_keywords=["open","launch","start"]


    search_keywords=["search","find","look up"]

    if any(word in text for word in open_keywords):
        command_result=execute_command(text)
        return {
            "type":"command",
            "response":command_result
        }
    
    elif any(word in text for word in search_keywords):
        command_result=execute_command(text)
        return {
            "type":"command",
            "response":command_result
        }
    

    return {
        "type":"chat"
    }