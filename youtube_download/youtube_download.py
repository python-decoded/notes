from pathlib import Path
from urllib.request import urlopen

from pytubefix import YouTube
import yt_dlp
from gooey import Gooey, GooeyParser


def get_title(url):
    return YouTube(url).title


def get_description(url):
    return YouTube(url).description


def download_video(url, path):

    try:
        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
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
            'outtmpl': f'{path}/%(title)s.%(ext)s',
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
    file_name = get_title(url).replace("/", "") + ".txt"
    with open(Path(path) / file_name, "wb") as file:
        file.write(f"{get_title(url)}\n\n{get_description(url)}".encode("utf-8"))


def download_thumbnail(url, path):
    file_name = get_title(url).replace("/", "") + ".jpg"
    thumbnail_url = YouTube(url).thumbnail_url

    with urlopen(thumbnail_url) as response:
        with open(Path(path) / file_name, "wb") as image:
            image.write(response.read())


@Gooey(program_name="Youtube Downloader v1.1.0",
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

    args = parser.parse_args()

    print(f"Завантаження: '{get_title(args.url)}' \nдо папки: {args.download_dir}")

    if args.video:
        download_video(args.url, args.download_dir)
    if args.audio:
        download_audio(args.url, args.download_dir)
    if args.thumbnail:
        download_thumbnail(args.url, args.download_dir)
    if args.description:
        download_info(args.url, args.download_dir)

    print("Завантаження завершено")


main()
