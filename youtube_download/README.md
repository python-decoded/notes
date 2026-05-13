## Зібрати білд
pip install -r requirements.txt
pyinstaller --onefile --noconsole --python-option "X utf8=1" .\youtube_download.py

## Завантаження відео
Відео завантажується бібліотекою yt_dlp, яка для коректної роботи потребує кодек 'ffmpeg'. Деталі: 'https://www.ffmpeg.org'.
Якщо не вдалося використати yt_dlp, відео буде завантажене задопомогою бібліотеки 'pytubefix', що не гарантує найкращу якість відео.


## Встановлення кодеку 'ffmpeg'
- Для Windows достатньо відкрити термінал з правами адміністратора і виконати комаду
```shell
choco install ffmpeg
```


## Типи підтримуваних урл
Застосунок підтримує завантаження одного відео, плейліста, усіх відео з каналу.

Приклади очікуваного формату урл:

Відео:
https://www.youtube.com/watch?v=tge4ojz5w1w
Плейліст:
https://www.youtube.com/playlist?list=PLAMUEkIlR-Va7SZL-DeGRWYepYZa6rehF
Канал:
https://www.youtube.com/@python_decoded/videos
