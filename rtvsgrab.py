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

    metadata = json.loads(http.request(
        "GET", video_metadata_url).data.decode('utf-8'))
    date = metadata['clip']['datetime_create'].split()[0]
    videosource = next(filter(
        lambda s: s['type'] == 'application/x-mpegurl', metadata['clip']['sources']))['src']
    videofilename = '/mnt/caladan/rtvs/'+date+'.mkv'

    ffmpeg.input(videosource).output(
        videofilename, vcodec='copy', acodec='copy').run(quiet=True)


if __name__ == "__main__":
    main()
