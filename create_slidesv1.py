from bs4 import BeautifulSoup
import flashtext
import argparse
import subprocess
import argparse
import http.server
import socketserver


parser = argparse.ArgumentParser()
parser.add_argument('--file', dest='file_name', type=str, help='Name of the jupyter notebook.')
parser.add_argument('--host', dest='host', type=str, help='Host address')
parser.add_argument('--port', dest='port', type=int, help='Port to serve the html')
parser.add_argument('--serve', dest='serve', type=bool, help='Port to serve the html')


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
    html_file=replace_urls(html_file)

    clean_file = (html_file.replace('<section><section><image>', '')
                  .replace('</image></section></section>', ''))
    return clean_file
def serve_html():
    if args.port==None:
        PORT=8000
    if args.host==None:
        HOST=''
    else:
        HOST,PORT=args.host,args.port
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


def main():
    """Convert the notebook to slides and then do some cleaning."""
    try:
        output = subprocess.check_output(
            ['jupyter', 'nbconvert', args.file_name, '--to', 'slides', '--reveal-prefix', 'https://cdn.jsdelivr.net/reveal.js/3.0.0',
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
    if args.serve:serve_html()