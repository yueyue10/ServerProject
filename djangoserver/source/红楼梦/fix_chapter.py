import json


def get_chapters():
    with open('chapter.json', 'r', encoding='utf-8') as chapterStr:
        chapter = json.load(chapterStr)
        return chapter


def get_content():
    with open('content.json', 'r', encoding='utf-8') as contentStr:
        content = json.load(contentStr)
        return content


def fix_content_chapter():
    content_obj = get_content()
    chapter_obj = get_chapters()
    # print( content['chapters'])
    chapters = chapter_obj['chapters']
    # print(chapters[0])
    for index, chapter in enumerate(content_obj['chapters']):
        # print(index, chapter)
        # print(chapter['title'])
        m_chapter = chapters[index]
        chapter['title'] = m_chapter
        # print(m_chapter)
        # print('\n\n\n')
    # print(content_obj)
    with open('content.json', 'w', encoding='utf-8') as contentFile:
        content_str = json.dumps(content_obj, ensure_ascii=False)
        contentFile.write(content_str)


if __name__ == '__main__':
    fix_content_chapter()
