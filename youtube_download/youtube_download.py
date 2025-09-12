from pytubefix import YouTube


def get_title(url):
    return YouTube(url).title


def download(url, path=None):
    stream = YouTube(url).streams.get_highest_resolution()
    stream.download(output_path=path,
                    skip_existing=True,
                    max_retries=3)


from gooey import Gooey, GooeyParser


@Gooey(program_name="Youtube Downloader",
       default_size=(500, 400),
       clear_before_run=True)
def main():
    parser = GooeyParser()
    parser.add_argument("url", action="store", help="Provide url of video", metavar="Url")
    parser.add_argument("download_dir", widget="DirChooser",
                        action="store", help="Where to save video",
                        metavar="Select Path")

    args = parser.parse_args()
    print(f"Завантаження відео: '{get_title(args.url)}' \nдо папки: {args.download_dir}")

    download(args.url, args.download_dir)
    print("Завантаження завершено")


main()
