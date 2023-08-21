import translators as ts

text = "2023년 종묘 묘현례 일정 안내"
print(ts.translate_text(query_text=text, target_lang="en", source_lang="ko", translator='papago'))
