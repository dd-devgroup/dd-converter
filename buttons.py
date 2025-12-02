from pykeyboard import ReplyKeyboard, ReplyButton
import helperfunctions
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# suporrted extensions
VIDAUD = ("AIFF","AAC","M4A","OGA","WMA","FLAC","WAV","OPUS","OGG","MP3","MKV","MP4","MOV","AVI","M4B","VOB","DVD","WEBM","WMV")
IMG = ("SVG","OCR","ICO","GIF","TIFF","BMP","WEBP","JP2","JPEG","JPG","PNG")
LBW = ("ODT","DOC","DOCX","DOTX","PDF","XML","HTML","DOTM","WPS","OTT","TXT")
LBI = ("ODP","PPT","PPTX","PPTM","PPSX","POTM","POTX","PPS","POT","ODG","OTP","XML","PDF")
LBC = ("ODS","XLS","HTML","XLSX","XLSM","XLTM","XLTX","OTS","XML","PDF","CSV","XLM")
FF = ("SFD","BDF","FNT","OTF","PFA","PFB","TTC","TTF","UFO","WOFF")
EB = ("EPUB","MOBI","AZW3","KFX","FB2","HTMLZ","LIT","LRF","PDB","PDF","TXT")
ARC = ("ZIP","RAR","7Z","TAR","XZ","GZ","BZ")
SUB = ("TTML","SCC","SRT","VTT")
PRO = ('C','CPP','PY','RS','JL','KT','NIM','DART','GO','JAVA','JS','TS','JAR')
T3D = ('CTM','PLY','STL','3DS','DAE','OBJ','LWO','OFF','WRL')


# buttons
VAboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
VAboard.add(
    ReplyButton('AIFF'), ReplyButton('AAC'), ReplyButton('M4A'),
    ReplyButton('OGA'), ReplyButton('WMA'), ReplyButton('FLAC'),
    ReplyButton('WAV'), ReplyButton('OPUS'), ReplyButton('OGG'),
    ReplyButton('MP3'), ReplyButton('MKV'), ReplyButton('MP4'),
    ReplyButton('MOV'), ReplyButton('AVI'), ReplyButton('GIF'),
    ReplyButton('M4B'), ReplyButton('VOB'), ReplyButton('DVD'),
    ReplyButton('WEBM'), ReplyButton('WMV'), ReplyButton('SENDVID'),
    ReplyButton('SENDDOC')
)
if config['features']['speech_to_text']:
    VAboard.add(ReplyButton('🎤 SpeechToText'))

IMGboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
IMGboard.add(
    ReplyButton('OCR'), ReplyButton('ICO'), ReplyButton('GIF'),
    ReplyButton('TIFF'), ReplyButton('BMP'), ReplyButton('WEBP'),
    ReplyButton('JPEG'), ReplyButton('JPG'), ReplyButton('PNG'),
    ReplyButton('SVG'), ReplyButton('🖼️ SENDPHOTO'), ReplyButton('📄 SENDDOC')
)
if config['features']['colorize']:
    IMGboard.add(ReplyButton('🎨 COLOR'))
if config['features']['positive']:
    IMGboard.add(ReplyButton('✨ POSITIVE'))
if config['features']['upscale']:
    IMGboard.add(ReplyButton('🖼️ UPSCALE'))
if config['features']['scan']:
    IMGboard.add(ReplyButton('🔬 SCAN'))
if config['features']['bg_remove']:
    IMGboard.add(ReplyButton('🏞️ BG REMOVE'))


LBWboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
LBWboard.add(
    ReplyButton('ODT'), ReplyButton('DOC'), ReplyButton('DOCX'),
    ReplyButton('DOTX'), ReplyButton('PDF'), ReplyButton('XML'),
    ReplyButton('HTML'), ReplyButton('DOTM'), ReplyButton('WPS'),
    ReplyButton('OTT'), ReplyButton('TXT'), ReplyButton('📖 READ')
)
if config['features']['text_to_speech']:
    LBWboard.add(ReplyButton('🗣️ TextToSpeech'))

LBIboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
LBIboard.add(
    ReplyButton('ODP'), ReplyButton('PPT'), ReplyButton('PPTX'),
    ReplyButton('PPTM'), ReplyButton('PPSX'), ReplyButton('POTM'),
    ReplyButton('POTX'), ReplyButton('PPS'), ReplyButton('POT'),
    ReplyButton('ODG'), ReplyButton('OTP'), ReplyButton('XML'),
    ReplyButton('PDF')
)

LBCboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
LBCboard.add(
    ReplyButton('ODS'), ReplyButton('XLS'), ReplyButton('HTML'),
    ReplyButton('XLSX'), ReplyButton('XLSM'), ReplyButton('XLTM'),
    ReplyButton('XLTX'), ReplyButton('OTS'), ReplyButton('XML'),
    ReplyButton('PDF'), ReplyButton('CSV'), ReplyButton('XLM')
)

FFboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
FFboard.add(
    ReplyButton('SFD'), ReplyButton('BDF'), ReplyButton('FNT'),
    ReplyButton('OTF'), ReplyButton('PFA'), ReplyButton('PFB'),
    ReplyButton('TTC'), ReplyButton('TTF'), ReplyButton('UFO'),
    ReplyButton('WOFF')
)

EBboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
EBboard.add(
    ReplyButton('EPUB'), ReplyButton('MOBI'), ReplyButton('AZW3'),
    ReplyButton('KFX'), ReplyButton('FB2'), ReplyButton('HTMLZ'),
    ReplyButton('LIT'), ReplyButton('LRF'), ReplyButton('PDB'),
    ReplyButton('PDF'), ReplyButton('TXT')
)

ARCboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
ARCboard.add(
    ReplyButton('📂 EXTRACT')
)

SUBboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
SUBboard.add(
    ReplyButton("TTML"), ReplyButton("SRT"), ReplyButton("VTT")
)

PROboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
PROboard.add(
    ReplyButton('CPP'), ReplyButton('RS'), ReplyButton('JL'),
    ReplyButton('KT'), ReplyButton('NIM'), ReplyButton('DART'),
    ReplyButton('GO'), ReplyButton('TS'), ReplyButton('JS'),
    ReplyButton('📖 READ'), ReplyButton('⚙️ COMPILE'), ReplyButton('▶️ RUN')
)

T3Dboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="конвертировать в...",resize_keyboard=True,selective=True)
T3Dboard.add(
    ReplyButton('CTM'), ReplyButton('PLY'), ReplyButton('STL'),
    ReplyButton('3DS'), ReplyButton('DAE'), ReplyButton('OBJ'),
    ReplyButton('LWO'), ReplyButton('OFF')
)

# texts
VA_TEXT = helperfunctions.give_name(VIDAUD)
IMG_TEXT = helperfunctions.give_name(IMG)
LBW_TEXT = helperfunctions.give_name(LBW)
LBC_TEXT = helperfunctions.give_name(LBC)
LBI_TEXT = helperfunctions.give_name(LBI)
FF_TEXT = helperfunctions.give_name(FF)
EB_TEXT = helperfunctions.give_name(EB)
ARC_TEXT = helperfunctions.give_name(ARC)
SUB_TEXT = helperfunctions.give_name(SUB)
PRO_TEXT = helperfunctions.give_name(PRO)
T3D_TEXT = helperfunctions.give_name(T3D)


START_TEXT = f'**Изображения** 📷\n`{IMG_TEXT}`\n\n' \
             f'**Видео/Аудио** 📹 / 🔊\n`{VA_TEXT}`\n\n' \
             f'**Документы** 💼\n`{LBW_TEXT},{LBI_TEXT},{LBC_TEXT}`\n\n' \
             f'**Шрифты** 🔤\n`{FF_TEXT}`\n\n' \
             f'**Электронные книги** 📚\n`{EB_TEXT}`\n\n' \
             f'**Архивы** 🗄\n`{ARC_TEXT}`\n\n' \
             f'**Субтитры** 🗯️\n`{SUB_TEXT}`\n\n' \
             f'**Языки программирования** 👨‍💻\n`{PRO_TEXT}`\n\n' \
             f'**3D файлы** 💠\n`{T3D_TEXT}`'

special_text = ""
if any(config['features'].values()):
    special_text = "\n\n**Специальное** 🎁\n"
    specials = []
    if config['features']['colorize']: specials.append('Colorize')
    if config['features']['positive']: specials.append('Positive')
    if config['features']['upscale']: specials.append('Upscale')
    if config['features']['text_to_speech']: specials.append('Text-to-Speech')
    if config['features']['speech_to_text']: specials.append('Speech-to-Text')
    if config['features']['imagegen']: specials.append('AI Image')
    if config['features']['ai_chat']: specials.append('Chat with AI')
    if config['features']['bloom']: specials.append('AI Article Writter')
    if config['features']['3dgen']: specials.append('Text-to-3D')
    if config['features']['musicgen']: specials.append('TEXT-to-MUSIC')
    if config['features']['bg_remove']: specials.append('BG REMOVE')
    if config['features']['scan']: specials.append('Scan')
    special_text += ", ".join(specials)

START_TEXT += special_text

extra_text = "\n\n**Дополнительно** ➕\n"
extras = []
if config['features']['tictactoe']: extras.append('Play TicTacToe')
if config['features']['guess']: extras.append('Guess Game')
extras.append('Save Restricted Content')
extras.append('Torrent <-> Magnet')
if config['features']['other_utils']: extras.append('Time or Date, Maths & Base64')
extra_text += ", ".join(extras)

START_TEXT += extra_text
