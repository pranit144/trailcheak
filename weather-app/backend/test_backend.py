
with open("output.txt", encoding='utf-8') as f:
    content = f.read()
    start = content.find("Unavailable: ") + len("Unavailable: ")
    end = content.find(" - Direct Result")
    print("ERROR_MSG:", content[start:end])
