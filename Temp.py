import chardet
with open("esg-daip-core-web.csv", 'rb') as f:
    result = chardet.detect(f.read())

print(result)