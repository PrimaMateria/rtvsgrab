import urllib3
import re
import json
import ffmpeg

http = urllib3.PoolManager()


def main():
    grab("https://www.rtvs.sk/televizia/archiv/13986")


def grab(url):
    response = http.request("GET", url)
    source = response.data.decode('utf-8')
    urlline = re.findall(r"^.*var url =.*$", source, re.MULTILINE)[0]
    video_metadata_url = re.match(r"^.*var url = \"(.*)\".*$", urlline)[1]
    video_data = get_video_data(video_metadata_url)
    save_video(video_data['date'], video_data['src'])


def save_video(date, source):
    file_path = '/mnt/caladan/rtvs/' + date + '.mkv'
    ffmpeg.input(source).output(file_path, vcodec='copy',
                                acodec='copy').run()


def get_video_data(url):
    metadata = json.loads(http.request("GET", url).data.decode('utf-8'))
    source = metadata['clip']['sources']
    data = dict()
    def type_filter(s): return s['type'] == 'application/x-mpegurl'
    data['src'] = next(filter(type_filter, sources))['src']
    data['date'] = metadata['clip']['datetime_create'].split()[0]

    return data


if __name__ == "__main__":
    main()
