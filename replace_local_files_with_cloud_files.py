from bs4 import BeautifulSoup
import flashtext
import argparse
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', dest='file_name', type=str, help='Name of the jupyter notebook.')
args = parser.parse_args()
#page=open(r'D:\LA_tree_based_model\Learning_algorithms.slides.html','r').read()
#soup = BeautifulSoup(page, 'html.parser')
#a=soup.find_all('link',attrs={'rel':"stylesheet"})

def replace_urls(page):
    """
    Converts local links into cloud links (urls)
    """
    kp=flashtext.KeywordProcessor()
    kp.add_keyword("reveal.js/css/reveal.css","https://cdn.jsdelivr.net/reveal.js/3.0.0/css/reveal.min.css")
    kp.add_keyword("reveal.js/css/theme/simple.css","https://cdn.jsdelivr.net/reveal.js/3.0.0/css/theme/simple.css")
    kp.add_keyword("reveal.js/lib/js/head.min.js","https://cdn.jsdelivr.net/reveal.js/3.0.0/lib/js/head.min.js")
    kp.add_keyword("reveal.js/js/reveal.js","https://cdn.jsdelivr.net/reveal.js/3.0.0/js/reveal.min.js")
    kp.add_keyword("reveal.js/lib/js/classList.js","https://cdn.jsdelivr.net/reveal.js/3.0.0/lib/js/classList.js")
    kp.add_keyword("reveal.js/plugin/notes/notes.js","https://cdn.jsdelivr.net/reveal.js/3.0.0/plugin/notes/notes.js")
    return kp.replace_keywords(page)


def clean_html(html_file):
    """Remove unnecessary tags from slides."""
    clean_file = (html_file.replace('<section><section><image>', '')
                  .replace('</image></section></section>', ''))
    clean_file=replace_urls(clean_file)
    return clean_file


def main():
    """Convert the notebook to slides and then do some cleaning."""
    try:
        output = subprocess.check_output(
            ['jupyter', 'nbconvert', args.file_name, '--to', 'slides', '--reveal-prefix', 'reveal.js-master',
             '--config', 'static/slides_config.py'], stderr=subprocess.STDOUT).decode('utf-8')
        print(output.rstrip())

        slide_name = output.split(' ')[-1].rstrip()
        with open(slide_name, 'r') as f:
            clean_file = clean_html(f.read())
        with open(slide_name, 'w') as f:
            f.write(clean_file)
        print('Successfully adjusted.')
    except IndexError:
        print('Provide name of the slide.')

if __name__=='__main__':
    main()