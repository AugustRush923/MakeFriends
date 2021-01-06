import wordcloud
import os
import django
from django.conf import settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makefriends.settings.develop")  # project_name 项目名称
# django.setup()

from blog.models import Tag


def generate_word_cloud():
    print("开始生成词云...")
    tag_list = Tag.get_tags()
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    with open(os.path.join(file_path, 'txt_file', 'word.txt'), 'w+', encoding='utf-8') as f:
        for tag in tag_list:
            f.write(tag.name + ',' + str(tag.num_posts) + '\n')
        txt = f.read()

    w = wordcloud.WordCloud(width=330,
                            height=236,
                            background_color='white',
                            font_path=os.path.join(file_path,  'font', 'msyh.ttf'))
    w.generate(txt)

    w.to_file(os.path.join(settings.MEDIA_ROOT, 'wordcloud.png'))
    print('生成词云结束...')


if __name__ == '__main__':
    generate_word_cloud()
