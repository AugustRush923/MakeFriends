import wordcloud
import os
import logging
import django
from django.conf import settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makefriends.settings.develop")  # project_name 项目名称
# django.setup()

from blog.models import Tag

logger = logging.getLogger('django')


def generate_word_cloud():
    logger.info("开始生成词云...")
    tag_list = Tag.get_tags()
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    with open(os.path.join(file_path, 'txt_file', 'word.txt'), 'w+', encoding='utf-8') as f:
        for tag in tag_list:
            f.write(f'{tag.name},{tag.num_posts}\n')
        f.seek(0)
        txt = f.read()

    w = wordcloud.WordCloud(width=330,
                            height=236,
                            background_color='white',
                            font_path=os.path.join(file_path, 'font', 'msyh.ttf'))
    w.generate(txt)
    img_path = os.path.join(settings.MEDIA_ROOT, 'wordcloud.png')
    w.to_file(os.path.join(settings.MEDIA_ROOT, 'wordcloud.png'))
    logger.info('生成词云结束...')
    return img_path


if __name__ == '__main__':
    print(generate_word_cloud())
