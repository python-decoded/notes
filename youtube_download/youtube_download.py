from pathlib import Path
from urllib.request import urlopen
from functools import lru_cache

from pytubefix import YouTube, Playlist
import yt_dlp
from gooey import Gooey, GooeyParser


def is_playlist(url):
    return "/playlist?list=" in url


def is_channel(url):
    return "/videos" in url


@lru_cache
def get_ranges(indexes: str) -> list[range]:

    if not indexes.strip():
        return []

    groups = indexes.replace(" ", "").split(",")
    ranges = []

    for g in groups:
        if "-" in g:
            start, end = g.split("-")
            ranges.append(range(int(start), int(end) + 1))
        else:
            ranges.append(range(int(g), int(g) + 1))
    return ranges


def in_indexes(idx, indexes):

    ranges = get_ranges(indexes)
    if not ranges:
        return True

    for r in ranges:
        if idx in r:
            return True
    return False


def get_title(url):
    if is_playlist(url):
        title = Playlist(url).title
    elif is_channel(url):
        with yt_dlp.YoutubeDL({'extract_flat': True}) as ydl:
            info = ydl.extract_info(url, download=False, process=False)
        title = info['channel']
    else:
        title = YouTube(url).title

    for i in "<>:\"/\\|?*":
        title = title.replace(i, " ")

    return title


def get_description(url):
    return YouTube(url).description


def download_video(url, path):

    try:
        ydl_opts = {
            'outtmpl': f'{path}/{get_title(url)}.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except yt_dlp.utils.DownloadError as e:
        print(f"Не зміг завантажити відео найкращої якості задопомогою yt_dlp: {e}")
        if "ffmpeg is not installed" in str(e):
            print("\nДля коректної роботи yt_dlp потрібно встановити кодек 'ffmpeg'. Деталі: 'https://www.ffmpeg.org'.")
        print("Завантаження буде виконане бібліотекою pytubefix, що не дає найкращу якість.")

        stream = YouTube(url).streams.get_highest_resolution()
        stream.download(output_path=path,
                        skip_existing=True,
                        max_retries=3)


def download_audio(url, path):

    try:
        ydl_opts = {
            'outtmpl': f'{path}/{get_title(url)}.%(ext)s',
            'format': 'bestaudio/best',
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # 128 / 192 / 320
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Не вдалося вивантажити аудіо у форматі mp3 задопомогою yt_dlp, {e}")
        if "ffmpeg is not installed" in str(e):
            print("\nДля коректної роботи yt_dlp потрібно встановити кодек 'ffmpeg'. Деталі: 'https://www.ffmpeg.org'.")
        print("Завантаження буде виконане бібліотекою pytubefix, зазвичай у форматі m4a.")

        stream = YouTube(url).streams.get_audio_only()
        stream.download(output_path=path,
                        skip_existing=True,
                        max_retries=3)


def download_info(url, path):
    file_name = get_title(url) + ".txt"
    with open(Path(path) / file_name, "wb") as file:
        file.write(f"{get_title(url)}\n\n{get_description(url)}".encode("utf-8"))


def download_thumbnail(url, path):
    file_name = get_title(url) + ".jpg"
    thumbnail_url = YouTube(url).thumbnail_url

    with urlopen(thumbnail_url) as response:
        with open(Path(path) / file_name, "wb") as image:
            image.write(response.read())


def process_list(url, args):

    playlist = Playlist(url)
    urls = playlist.video_urls

    print(f"Розраховані індекси: '{args.indexes}' {get_ranges(args.indexes)}")
    print(f"Завантаження {len(urls)} відео з плейліста: '{get_title(url)}' \nдо папки: {args.download_dir}")

    for idx, url in enumerate(urls, start=1):
        if in_indexes(idx, args.indexes):
            print(f"{idx}: '{get_title(url)}")
            process_video(url, args)


def process_all_channel_videos(url, args):

    with yt_dlp.YoutubeDL({'extract_flat': True}) as ydl:
        info = ydl.extract_info(url, download=False, process=False)

    urls = [
        f"https://www.youtube.com/watch?v={entry['id']}"
        for entry in info['entries']
    ]

    print(f"Розраховані індекси: '{args.indexes}' {get_ranges(args.indexes)}")
    print(f"Завантаження {len(urls)} відео з Каналу: '{get_title(url)}' \nдо папки: {args.download_dir}")

    for idx, url in enumerate(urls, start=1):
        if in_indexes(idx, args.indexes):
            print(f"{idx}: '{get_title(url)}")
            process_video(url, args)


def process_video(url, args):

    if args.video:
        download_video(url, args.download_dir)
    if args.audio:
        download_audio(url, args.download_dir)
    if args.thumbnail:
        download_thumbnail(url, args.download_dir)
    if args.description:
        download_info(url, args.download_dir)


@Gooey(program_name="Youtube Downloader v1.2.0",
       default_size=(500, 600),
       clear_before_run=True)
def main():
    parser = GooeyParser()
    parser.add_argument("url", action="store", help="Provide url of video", metavar="Url")
    parser.add_argument("download_dir", widget="DirChooser",
                        action="store", help="Where to save video",
                        metavar="Select Path")
    # Radio Buttons
    group = parser.add_argument_group("Format")
    group.add_argument("--video", action="store_true", help="Save as Video")
    group.add_argument("--audio", action="store_true", help="Save as Audio")
    group.add_argument("--thumbnail", action="store_true", help="Save Thumbnail")
    group.add_argument("--description", action="store_true", help="Save Description")
    group.add_argument("--indexes",
                       action="store",
                       help="Specify items indexes (for list and chanel download): 1,2,5-12")

    args = parser.parse_args()

    if is_playlist(args.url):
        process_list(args.url, args)
    elif is_channel(args.url):
        process_all_channel_videos(args.url, args)
    else:
        print(f"Завантаження: '{get_title(args.url)}' \nдо папки: {args.download_dir}")
        process_video(args.url, args)

    print("Завантаження завершено")


main()
