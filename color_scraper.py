from html.parser import HTMLParser
import urllib.request

class ColorScraperHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.colors = {}
        self.hex = ''

    def get_colors(self):
        return self.colors

    def handle_starttag(self, tag, attrs):
        if tag!='a' or len(attrs) != 2:
            return

        first_attr_name = attrs[0][0]
        first_attr_value = attrs[0][1]
        second_attr_name = attrs[1][0]
        second_attr_value = attrs[1][1]

        if first_attr_name != 'class' or second_attr_name != 'href':
            return
        if first_attr_value not in ['tw', 'tb']:
            return

        if self.recording:
            self.reording += 1
            return

        self.hex = '#' + second_attr_value[1:]
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'a' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.colors[data] = self.hex

if __name__=="__main__":
    myparser = ColorScraperHTMLParser()
    with urllib.request.urlopen ('https://www.colorhexa.com/color-names') as response:
        html = str(response.read())
    myparser.feed(html)
    colors = myparser.get_colors()
    print(colors)
    print(len(colors))
