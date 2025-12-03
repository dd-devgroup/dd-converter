# File-Converter-Bot

**Телеграм бот для конвертации изображений, видео, аудио, шрифтов, документов и электронных книг.**

**_Посмотреть бота в действии [@DDConverterBot](https://t.me/DDConverterBot)_**

---

## Переменные окружения

Для запуска бота необходимо создать файл `.env` в корне проекта и указать в нем следующие переменные:

```
TOKEN=ВАШ_ТЕЛЕГРАМ_ТОКЕН
HASH=ВАШ_API_HASH
ID=ВАШ_API_ID
```

- `TOKEN` **_Токен вашего бота от [@BotFather](https://t.me/botfather)_**
- `HASH` **_Ваш API Hash с [my.telegram.org](https://my.telegram.org)_**
- `ID` **_Ваш API ID с [my.telegram.org](https://my.telegram.org)_**

---

## Локальный запуск через Docker

Это рекомендуемый способ запуска, который автоматически настраивает все необходимое окружение.

1.  **Установите Docker и Docker Compose.**
2.  **Склонируйте репозиторий:**
    ```sh
    git clone https://github.com/dd-devgroup/dd-converter.git
    cd dd-converter
    ```
3.  **Создайте и заполните `.env` файл**:
    ```sh
    nano .env
    ```
4.  **Отредактируйте файл `config.yaml`**:
    ```sh
    nano config.yaml
    ```
5.  **Запустите бота:**
    ```sh
    docker-compose up --build -d
    ```


---

## Поддерживаемые форматы

**Изображения**: *OCR, ICO, GIF, TIFF, BMP, WEBP, JP2, JPEG, JPG, PNG*

**Видео/Аудио**: *AIFF, AAC, M4A, OGA, WMA, FLAC, WAV, OPUS, OGG, MP3, MKV, MP4, MOV, AVI, M4B, VOB, DVD, WEBM, WMV*

**Документы**: *ODT, DOC, DOCX, DOTX, PDF, XML, HTML, DOTM, WPS, OTT, TXT, ODP, PPT, PPTX, PPTM, PPSX, POTM, POTX, PPS, POT, ODG, OTP, XML, ODS, XLS, HTML, XLSX, XLSM, XLTM, XLTX, OTS, XML, CSV, XLM*

**Шрифты**: *SFD, BDF, FNT, OTF, PFA, PFB, TTC, TTF, UFO, WOFF*

**Электронные книги**: *EPUB, MOBI, AZW3, KFX, FB2, HTMLZ, LIT, LRF, PDB, PDF, TXT*

**Архивы**: *ZIP, RAR, 7Z, TAR, XY, GZ, BZ*

**Субтитры**: *TTML, SCC, SRT, VTT*

**Языки программирования**: *C, CPP, PY, RS, JL, KT, NIM, DART, GO, JAVA, JS, TS, JAR*

**3D файлы**: *CTM, PLY, STL, 3DS, DAE, OBJ, LWO, OFF, WRL*

---

## Специальные функции

**COLORIZE** - *Раскрашивание ваших старых черно-белых изображений*

**TEXT-to-IMAGE** - *Создание изображений с помощью ИИ по вашему запросу*

**POSITIVE** - *Конвертация негативных изображений в позитивные*

**SPEECH-to-TEXT** - *Транскрибация аудио в текст*

**TEXT-to-SPEECH** - *Генерация речи из текстового файла*

**UPSCALE** - *Увеличение разрешения изображений*

**TEXT-to-VIDEO** - *Создание видео с помощью ИИ по вашему запросу*

**SCAN** - *Сканирование QR-кодов и штрих-кодов*

**COMPILE** - *Создание самодостаточных исполняемых файлов для Linux*

**RUN** - *Запуск Python программ*

**Chat with AI** - *Общение с саркастическим чат-ботом*

**AI Article Writter** - *Завершение ваших статей с помощью ИИ*

**TEXT-to-MUSIC** - *Генерация музыки из текста*

---

## Дополнительные функции

**Крестики-нолики** - *Игра в крестики-нолики с ботом или другими игроками*

**Угадай число** - *Бот угадает ваше число*

**SAVE RESTRICTED** - *Отправьте ссылку на пост из публичного чата с ограничениями, бот отправит вам этот пост*

**Torrent <-> Magnet** - *Отправьте торрент-файл для получения Magnet-ссылки и наоборот*

**Время и дата** - *Отправьте 'Time' или 'Date' для получения текущего времени и даты в различных часовых поясах*

**Математика** - *Отправьте математическое выражение (в формате Python) для получения результата*

**Base64** - *Отправьте 'b64e строка' для кодирования строки и 'b64d строка' для декодирования строки*

---

# Используемые технологии

- для конвертации **изображений** используется **[ImageMagic](https://imagemagick.org/)**

- для **OCR** чтения **изображений** используется **[Tesseract-OCR](https://github.com/tesseract-ocr/tesseract/)**

- для конвертации **видео** и **аудио** используется **[FFmpeg](https://ffmpeg.org/)**

- для конвертации **документов** используется **[LibreOffice](https://www.libreoffice.org/)**

- для конвертации **шрифтов** используется **[FontForge](https://fontforge.org/)**

- для конвертации **электронных книг** используется **[Calibre](https://calibre-ebook.com/)**

- для извлечения **архивов** используется **[7zip](https://www.7-zip.org/)**

- для конвертации **субтитров** используется **[TTconv](https://github.com/sandflow/ttconv/)**

- для конвертации **3D моделей** используется **[OpenCTM-Tools](https://github.com/Danny02/OpenCTM/)**

- для конвертации **TGS** используется **[TGSconverter](https://github.com/Benau/tgsconverter/)**

- для транспиляции **Python программ** используется **[Py2Many](https://github.com/py2many/py2many/)**

- для транспиляции **C программ** используется **[C4Go](https://github.com/Konstantin8105/c4go/)**

- для транспиляции **Java программ** используется **[Jsweet](https://github.com/cincheo/jsweet/)**

- для сканирования **QR и штрих-кодов** используется **[PyzBar](https://github.com/NaturalHistoryMuseum/pyzbar/)**

- для компиляции **JAR** используется **[Warp4j](https://github.com/guziks/warp4j/)**

- для компиляции **C & C++** используется **[G++](https://gcc.gnu.org/)**

- для компиляции **Python** используется **[PyInstaller](https://github.com/pyinstaller/pyinstaller/)**

- для **раскрашивания изображений** используется **[DeOldify](https://github.com/jantic/DeOldify/)** размещенный на **[Hugging Face](https://huggingface.co/spaces/PaddlePaddle/deoldify/)** и **[Photo-Colorizer](https://github.com/PySimpleGUI/PySimpleGUI-Photo-Colorizer)**

- для генерации **ИИ изображений** используется **[Craiyon](https://www.craiyon.com/)** (также известный как Dalle-Mini) и **[Stable Diffusion](https://github.com/Stability-AI/stablediffusion)** размещенный на **[Hugging Face](https://huggingface.co/spaces/stabilityai/stable-diffusion)**

- для генерации **позитивных изображений** используется **[C41lab или C41](https://gist.github.com/stollcri/1aaec353a0e883888920c1b501cc1484/)**, **[Open-CV](https://opencv.org/)** и **[Negfix8](https://github.com/chrishunt/negfix8/)**

- для **речи в текст** используется **[Google's API](https://github.com/Uberi/speech_recognition)** и **[Open-AI's Whisper](https://github.com/openai/whisper)** размещенный на **[Hugging Face](https://huggingface.co/spaces/Amrrs/openai-whisper-live-transcribe)**

- для **текста в речь** используется **[Google's gTTS API](https://github.com/pndurette/gTTS)** 

- для **увеличения разрешения изображений** используется **[Zyro's Image-Upscaller](https://zyro.com/in/tools/image-upscaler)** 

- для работы с **торрентами** используется **[iTorrents](https://itorrents.org/)** и **[Torrent2Magnet](https://github.com/repolho/torrent2magnet)**

- для работы с **датой и временем** используется **[Arrow](https://github.com/arrow-py/arrow)**

- для **математики** и **RUN** используется **[ASTeval](https://github.com/newville/asteval)**

- для генерации **3D моделей** используется **[Point-E](https://github.com/openai/point-e/)** размещенный на **[Hugging Face](https://huggingface.co/spaces/openai/point-e)**

- для **общения с ИИ** используется **V23 CHATBOT размещенный на [Hugging Face](https://huggingface.co/spaces/VISION23/V23ChatBot)**

- для **написания статей с ИИ** используется **Bloom размещенный на [Hugging Face](https://huggingface.co/spaces/huggingface/bloom_demo)**

- для **TEXT-to-MUSIC** используется **[Riffusion](https://github.com/riffusion/riffusion) размещенный на [HuggingFace](https://huggingface.co/spaces/fffiloni/spectrogram-to-music)**

- для **УДАЛЕНИЯ ФОНА** используется **[MODNet](https://github.com/ZHKKKe/MODNet) размещенный на [HuggingFace](https://huggingface.co/spaces/nateraw/background-remover)**
