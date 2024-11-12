"""
Trying out the actual pipeline here to measure progress with the creation of the final product
"""
from typing import List

from python.yt_uploader import YTConnector
from python.language_verification import LanguageVerification
from word_generator import Audio, ImageGenerator, VideoGenerator
from constants import Paths, LANGUAGE_TO_LEARN, NATIVE_LANGUAGE
from moviepy.editor import ColorClip, TextClip

# video_generator = VideoGenerator(
#     word="apropriado",
#     sentence="El tono de tu discurso no fue el más apropiado para la situación.",
#     translated_sentence="The tone of your speech was not the most appropriate for the situation",
#     image_paths=["/Users/bendsouza/PycharmProjects/yt_translator/images/11-08-2024 22:09:04.jpg"],
#     audio_filepath="/Users/bendsouza/PycharmProjects/yt_translator/audio/11-08-2024 22:08:48.wav",
#     subtitles_filepath="/Users/bendsouza/PycharmProjects/yt_translator/subtitles/11-08-2024 22:08:49.srt"
# )
#
# video_filepath = video_generator.generate_video(word_font="Toppan-Bunkyu-Gothic-Demibold")


# yt = YTConnector(
#     credentials_env=True
# )
#
# # channels = yt.list_available_channels()
# videos = yt.list_youtube_uploads(channel_id="UCQjyvCIR9IkG02Q0Wmpz9sQ")
# print(videos)

# from today.models import VideoDetails
#
#
# class Command(BaseCommand):
#     """
#     Django management command to fetch YouTube Shorts videos and save them to the database.
#
#     This command connects to the YouTube API to retrieve videos from a specific channel,
#     parses their details (title, description, upload date), and updates or creates
#     corresponding video records in the database.
#     """
#
#     help = "Fetch YT Shorts videos and save them to the database"
#
#     def handle(self, *args, **options):
#         """
#         Main logic of the command to fetch the videos and update the database.
#
#         This method:
#         1. Fetches video details from YouTube using the YTConnector.
#         2. Parses video information (title, description, upload date).
#         3. Updates or creates video records in the database.
#         4. Outputs a success message for each video processed.
#
#         :param args: Positional arguments to pass to the command
#         :param options: Keyword arguments to pass to the command
#         """
#
#         manual_upload = [
#             {
#                 "video_id": "5vgbS7WwI8k",
#                 "word": "sentimos",
#                 "sentence": "Sentimos mucho la pérdida de tu abuelo estamos aquí para apoyarte en estos momentos difíciles",
#                 "translated_sentence": "We are very sorry about the loss of your grandather, we are here to support you in this difficult time",
#                 "title": "Spanish Word of the Day: sentimos",
#                 "description": """Today's Spanish word of the day is sentimos. An example use of this word is: '"Sentimos mucho la pérdida de tu abuelo, estamos ...""",
#                 "upload_date": "2024-10-31 12:33:38",
#                 "thumbnail_url": "https://i.ytimg.com/vi/5vgbS7WwI8k/hqdefault.jpg"
#             },
#             {
#                 "video_id": "emyDzw-cErQ",
#                 "word": "sonar",
#                 "sentence": "Ayer por la noche escuché una canción que me hizo sonar a mi época de adolescencia",
#                 "translated_sentence": "Yesterday night I heard a song which reminded me of my teenage years",
#                 "title": "Spanish Word of the Day: sonar",
#                 "description": """Today's Spanish word of the day is sonar. An example use of this word is: 'Ayer por la noche escuché una canción que me hizo ...""",
#                 "upload_date": "2024-11-05 15:48:52",
#                 "thumbnail_url": "https://i.ytimg.com/vi/emyDzw-cErQ/hqdefault.jpg"
#             },
#             {
#                 "video_id": "d92Yg9jgQUI",
#                 "word": "remate",
#                 "sentence": "El remate final de la casa quedó espectacular con esos detalles de decoración tan elegantes",
#                 "translated_sentence": "The finishing touches of the house were spectacular with such elegant decorative details",
#                 "title": "Spanish Word of the Day: remate",
#                 "description": """Today's Spanish word of the day is remate. An example use of this word is: 'El remate final de la casa quedó espectacular con ...""",
#                 "upload_date": "2024-11-05 15:41:31",
#                 "thumbnail_url": "https://i.ytimg.com/vi/d92Yg9jgQUI/hqdefault.jpg"
#             }
#         ]
#
#         for upload in manual_upload:
#             vid, created = VideoDetails.objects.update_or_create(
#                 video_id=upload["video_id"],
#                 defaults={
#                     "word": upload["word"],
#                     "sentence": upload["sentence"],
#                     "translated_sentence": upload["translated_sentence"],
#                     "title": upload["title"],
#                     "description": upload["description"],
#                     "upload_date": upload["upload_date"],
#                     "thumbnail_url": upload["thumbnail_url"],
#                 }
#             )
#
#             if created:
#                 self.stdout.write(f"New video added: {vid.title}")
#             else:
#                 self.stdout.write(f"Video updated: {vid.title}")

target_word = "poner"
# real_word = LanguageVerification("es").get_spanish_dictionary_definition("poner")
# print(real_word)

data = [{'meta': {'id': 'poner', 'uuid': 'e56d685f-f239-4274-b4bd-a60a71fbd8a8', 'lang': 'es', 'sort': '2617720000', 'src': 'spanish', 'section': 'alpha', 'stems': ['poner', 'poner a', 'poner de', 'poner en', 'ponerse'], 'offensive': False}, 'hwi': {'hw': 'poner', 'prs': [{'sound': {'audio': 'poner01sp'}}]}, 'fl': 'transitive verb', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{sx|colocar||} {bc}to {a_link|put}, to {a_link|place} '], ['vis', [{'t': 'pon el libro en la mesa', 'tr': 'put the book on the table'}]]]}]], [['sense', {'sn': '2', 'dt': [['text', '{sx|agregar||}, {sx|añadir||} {bc}to {a_link|put in}, to {a_link|add} (an ingredient, etc.)']]}]], [['sense', {'sn': '3', 'dt': [['text', '{bc}to {a_link|put on} (clothes) '], ['vis', [{'t': 'le puse el suéter', 'tr': 'I put her sweater on (her)'}]]]}]], [['sense', {'sn': '4', 'dt': [['text', '{sx|contribuir||} {bc}to {a_link|contribute}']]}]], [['sense', {'sn': '5', 'dt': [['text', '{sx|escribir||} {bc}to put in writing '], ['vis', [{'t': 'no le puso su nombre', 'tr': "he didn't put his name on it"}]]]}]], [['sense', {'sn': '6', 'dt': [['text', '{bc}to {a_link|give} (a task, etc.), to {a_link|impose} (a fine)']]}]], [['sense', {'sn': '7', 'dt': [['text', '{bc}to {a_link|prepare}, to {a_link|arrange} '], ['vis', [{'t': 'poner la mesa', 'tr': 'to set the table'}]]]}]], [['sense', {'sn': '8', 'dt': [['text', '{bc}to {a_link|name} '], ['vis', [{'t': 'le pusimos Ana', 'tr': 'we called her Ana'}]]]}]], [['sense', {'sn': '9', 'dt': [['text', '{sx|establecer||} {bc}to {a_link|set up}, to {a_link|establish} '], ['vis', [{'t': 'puso un restaurante', 'tr': 'he opened up a restaurant'}]]]}]], [['sense', {'sn': '10', 'dt': [['text', '{sx|instalar||} {bc}to {a_link|install}, to {a_link|put in}']]}]], [['sense', {'sn': '11', 'sls': ['(with an adjective or adverb)'], 'dt': [['text', '{bc}to {a_link|make} '], ['vis', [{'t': 'me pone nervioso', 'tr': 'it makes me nervous'}, {'t': 'siempre lo pones de mal humor', 'tr': 'you always put him in a bad mood'}]]]}]], [['sense', {'sn': '12', 'dt': [['text', '{bc}to {a_link|turn on}, to {a_link|switch on}']]}]], [['sense', {'sn': '13', 'dt': [['text', '{bc}to {a_link|set} (an alarm, etc.) '], ['vis', [{'t': 'pon la música más alta/fuerte', 'tr': 'turn up the music'}]]]}]], [['sense', {'sn': '14', 'dt': [['text', '{sx|suponer||} {bc}to {a_link|suppose} '], ['vis', [{'t': 'pongamos que no viene', 'tr': "supposing he doesn't come"}]]]}]], [['sense', {'sn': '15', 'dt': [['text', '{bc}to {a_link|give} (an example)']]}]], [['sense', {'sn': '16', 'dt': [['text', '{bc}to {a_link|raise} (objections), to {a_link|create} (problems, etc.)']]}]], [['sense', {'sn': '17', 'dt': [['text', '{bc}to {a_link|lay} (eggs)']]}]], [['sense', {'sn': '18', 'vrs': [{'va': 'poner a', 'vac': '~ a'}], 'dt': [['text', '{bc}to {a_link|start} (someone doing something) '], ['vis', [{'t': 'lo puse a trabajar', 'tr': 'I put him to work'}]]]}]], [['sense', {'sn': '19', 'vrs': [{'va': 'poner de', 'vac': '~ de'}], 'dt': [['text', '{bc}to place as '], ['vis', [{'t': 'la pusieron de directora', 'tr': 'they made her director'}]]]}]], [['sense', {'sn': '20', 'vrs': [{'va': 'poner en', 'vac': '~ en'}], 'dt': [['text', '{bc}to {a_link|put in} (a state or condition) '], ['vis', [{'t': 'poner en duda', 'tr': 'to call into question'}, {'t': 'lo puso en peligro', 'tr': 'she put him in danger'}]]]}]]]}, {'vd': 'intransitive verb', 'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}to {a_link|contribute}']]}]], [['sense', {'sn': '2', 'dt': [['text', '{bc}to {a_link|lay eggs}']]}]]]}], 'dros': [{'drp': 'ponerse', 'fl': 'reflexive verb', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}to {a_link|move} (into a position) '], ['vis', [{'t': 'ponerse de pie', 'tr': 'to stand up'}]]]}]], [['sense', {'sn': '2', 'dt': [['text', '{bc}to {a_link|put on}, to {a_link|wear}']]}]], [['sense', {'sn': '3', 'dt': [['text', '{bc}to {a_link|become}, to {a_link|turn} '], ['vis', [{'t': 'se puso colorado', 'tr': 'he turned red'}]]]}]], [['sense', {'sn': '4', 'dt': [['text', '{bc}to {a_link|start} '], ['vis', [{'t': 'me puse a llorar', 'tr': 'I started to cry'}]]]}]], [['sense', {'sn': '5', 'dt': [['text', '{bc}to {a_link|set} (of the sun or moon)']]}]]]}]}], 'suppl': {'cjts': [{'cjid': 'gppt', 'cjfs': ['poniendo', 'puesto']}, {'cjid': 'pind', 'cjfs': ['pongo', 'pones', 'pone', 'ponemos', 'ponéis', 'ponen']}, {'cjid': 'pret', 'cjfs': ['ponía', 'ponías', 'ponía', 'poníamos', 'poníais', 'ponían']}, {'cjid': 'pprf', 'cjfs': ['puse', 'pusiste', 'puso', 'pusimos', 'pusisteis', 'pusieron']}, {'cjid': 'futr', 'cjfs': ['pondré', 'pondrás', 'pondrá', 'pondremos', 'pondréis', 'pondrán']}, {'cjid': 'cond', 'cjfs': ['pondría', 'pondrías', 'pondría', 'pondríamos', 'pondríais', 'pondrían']}, {'cjid': 'psub', 'cjfs': ['ponga', 'pongas', 'ponga', 'pongamos', 'pongáis', 'pongan']}, {'cjid': 'pisb1', 'cjfs': ['pusiera', 'pusieras', 'pusiera', 'pusiéramos', 'pusierais', 'pusieran']}, {'cjid': 'pisb2', 'cjfs': ['pusiese', 'pusieses', 'pusiese', 'pusiésemos', 'pusieseis', 'pusiesen']}, {'cjid': 'fsub', 'cjfs': ['pusiere', 'pusieres', 'pusiere', 'pusiéremos', 'pusiereis', 'pusieren']}, {'cjid': 'ppci', 'cjfs': ['he puesto', 'has puesto', 'ha puesto', 'hemos puesto', 'habéis puesto', 'han puesto']}, {'cjid': 'ppsi', 'cjfs': ['había puesto', 'habías puesto', 'había puesto', 'habíamos puesto', 'habíais puesto', 'habían puesto']}, {'cjid': 'pant', 'cjfs': ['hube puesto', 'hubiste puesto', 'hubo puesto', 'hubimos puesto', 'hubisteis puesto', 'hubieron puesto']}, {'cjid': 'fpin', 'cjfs': ['habré puesto', 'habrás puesto', 'habrá puesto', 'habremos puesto', 'habréis puesto', 'habrán puesto']}, {'cjid': 'cpef', 'cjfs': ['habría puesto', 'habrías puesto', 'habría puesto', 'habríamos puesto', 'habríais puesto', 'habrían puesto']}, {'cjid': 'ppfs', 'cjfs': ['haya puesto', 'hayas puesto', 'haya puesto', 'hayamos puesto', 'hayáis puesto', 'hayan puesto']}, {'cjid': 'ppss1', 'cjfs': ['hubiera puesto', 'hubieras puesto', 'hubiera puesto', 'hubiéramos puesto', 'hubierais puesto', 'hubieran puesto']}, {'cjid': 'ppss2', 'cjfs': ['hubiese puesto', 'hubieses puesto', 'hubiese puesto', 'hubiésemos puesto', 'hubieseis puesto', 'hubiesen puesto']}, {'cjid': 'fpsb', 'cjfs': ['hubiere puesto', 'hubieres puesto', 'hubiere puesto', 'hubiéremos puesto', 'hubiereis puesto', 'hubieren puesto']}, {'cjid': 'impf', 'cjfs': ['-', 'pon', 'ponga', 'pongamos', 'poned', 'pongan']}]}, 'shortdef': ['colocar : to put, to place', 'agregar, añadir : to put in, to add (an ingredient, etc.)', 'to put on (clothes)']}, {'meta': {'id': 'atencion:1', 'uuid': '92c80876-e0b9-4022-a6fe-8524c3b73129', 'lang': 'es', 'sort': '2602274000', 'src': 'spanish', 'section': 'alpha', 'stems': ['atención', 'atenciones', 'poner atención', 'prestar atención', 'llamar la atención', 'en atención a'], 'offensive': False}, 'hom': 1, 'hwi': {'hw': 'atención', 'prs': [{'sound': {'audio': 'atenc01sp'}}]}, 'fl': 'feminine noun', 'ins': [{'il': 'plural', 'ifc': '-ciones', 'if': 'atenciones'}], 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}{a_link|attention}']]}]], [['sense', {'sn': '2', 'vrs': [{'va': 'poner atención'}, {'vl': 'or', 'va': 'prestar atención'}], 'dt': [['text', '{bc}to {a_link|pay attention}']]}]], [['sense', {'sn': '3', 'vrs': [{'va': 'llamar la atención'}], 'dt': [['text', '{bc}to {a_link|attract attention}']]}]], [['sense', {'sn': '4', 'vrs': [{'va': 'en atención a'}], 'dt': [['text', '{bc}{a_link|in view of}']]}]]]}], 'shortdef': ['attention', 'to pay attention', 'to attract attention']}, {'meta': {'id': 'coto', 'uuid': 'b19c5ed3-13b9-4a0c-abce-bffc0fb4bbdd', 'lang': 'es', 'sort': '2606042000', 'src': 'spanish', 'section': 'alpha', 'stems': ['coto', 'poner coto a'], 'offensive': False}, 'hwi': {'hw': 'coto', 'prs': [{'sound': {'audio': 'coto001sp'}}]}, 'fl': 'masculine noun', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}{a_link|enclosure}, {a_link|reserve}']]}]], [['sense', {'sn': '2', 'vrs': [{'va': 'poner coto a'}], 'dt': [['text', '{bc}to put a stop to']]}]]]}], 'shortdef': ['enclosure, reserve', 'to put a stop to']}, {'meta': {'id': 'evidencia', 'uuid': 'bff1418f-32eb-4265-9264-4c60cd84b91f', 'lang': 'es', 'sort': '2609548000', 'src': 'spanish', 'section': 'alpha', 'stems': ['evidencia', 'poner en evidencia'], 'offensive': False}, 'hwi': {'hw': 'evidencia', 'prs': [{'sound': {'audio': 'evide01sp'}}]}, 'fl': 'feminine noun', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}{a_link|evidence}, {a_link|proof}']]}]], [['sense', {'sn': '2', 'vrs': [{'va': 'poner en evidencia'}], 'dt': [['text', '{bc}to {a_link|demonstrate}, to make clear']]}]]]}], 'shortdef': ['evidence, proof', 'to demonstrate, to make clear']}, {'meta': {'id': 'lumbre', 'uuid': 'b79b970b-fe9c-4250-9e9a-2b51363d7963', 'lang': 'es', 'sort': '2614062000', 'src': 'spanish', 'section': 'alpha', 'stems': ['lumbre', 'poner en la lumbre'], 'offensive': False}, 'hwi': {'hw': 'lumbre', 'prs': [{'sound': {'audio': 'lumbr01sp'}}]}, 'fl': 'feminine noun', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{sx|fuego||} {bc}{a_link|fire}']]}]], [['sense', {'sn': '2', 'dt': [['text', '{bc}{a_link|brilliance}, {a_link|splendor}']]}]], [['sense', {'sn': '3', 'vrs': [{'va': 'poner en la lumbre'}], 'dt': [['text', '{bc}to put on the stove, to {a_link|warm up}']]}]]]}], 'shortdef': ['fuego : fire', 'brilliance, splendor', 'to put on the stove, to warm up']}, {'meta': {'id': 'obra', 'uuid': '2c57a1c3-32f1-4a7d-8948-7bd4cba6f1d0', 'lang': 'es', 'sort': '2615997000', 'src': 'spanish', 'section': 'alpha', 'stems': ['obra', 'obra maestra', 'obras públicas', 'poner en obra', 'por obra de'], 'offensive': False}, 'hwi': {'hw': 'obra', 'prs': [{'sound': {'audio': 'obra001sp'}}]}, 'fl': 'feminine noun', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}{a_link|work} '], ['vis', [{'t': 'obra de arte', 'tr': 'work of art'}, {'t': 'obra de teatro', 'tr': 'play'}, {'t': 'obra de consulta', 'tr': 'reference work'}]]]}]], [['sense', {'sn': '2', 'dt': [['text', '{bc}{a_link|deed} '], ['vis', [{'t': 'una buena obra', 'tr': 'a good deed'}]]]}]], [['sense', {'sn': '3', 'dt': [['text', '{bc}construction work '], ['vis', [{'t': 'en obra(s)', 'tr': 'under construction'}, {'t': 'obras viales', 'tr': 'roadwork'}]]]}]], [['sense', {'sn': '4', 'dt': [['text', '{bc}construction site, building site']]}]], [['sense', {'sn': '5', 'vrs': [{'va': 'obra maestra'}], 'dt': [['text', '{bc}{a_link|masterpiece}']]}]], [['sense', {'sn': '6', 'vrs': [{'va': 'obras públicas'}], 'dt': [['text', '{bc}public works']]}]], [['sense', {'sn': '7', 'vrs': [{'va': 'poner en obra'}], 'dt': [['text', '{bc}to put into effect']]}]], [['sense', {'sn': '8', 'vrs': [{'va': 'por obra de'}], 'dt': [['text', '{bc}thanks to, {a_link|because of}']]}]]]}], 'shortdef': ['work', 'deed', 'construction work']}, {'meta': {'id': 'picota', 'uuid': '5599152e-2e21-4feb-976e-9846da376501', 'lang': 'es', 'sort': '2617328000', 'src': 'spanish', 'section': 'alpha', 'stems': ['picota', 'poner a alguien en la picota'], 'offensive': False}, 'hwi': {'hw': 'picota'}, 'fl': 'feminine noun', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}{a_link|pillory}, {a_link|stock}']]}]], [['sense', {'sn': '2', 'vrs': [{'va': 'poner a alguien en la picota'}], 'dt': [['text', '{bc}to put someone on the spot']]}]]]}], 'shortdef': ['pillory, stock', 'to put someone on the spot']}, {'meta': {'id': 'prueba:2', 'uuid': '3ddcba59-b1d5-4253-a237-7b7bef2295b7', 'lang': 'es', 'sort': '2618392000', 'src': 'spanish', 'section': 'alpha', 'stems': ['prueba', 'a prueba', 'a prueba de agua', 'prueba de fuego', 'poner a prueba'], 'offensive': False}, 'hom': 2, 'hwi': {'hw': 'prueba', 'prs': [{'sound': {'audio': 'prueb02sp'}}]}, 'fl': 'feminine noun', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}{a_link|proof}, (piece of) {a_link|evidence} '], ['vis', [{'t': 'como prueba de', 'tr': 'as proof of'}, {'t': 'pruebas científicas', 'tr': 'scientific evidence'}]]]}]], [['sense', {'sn': '2', 'dt': [['text', '{bc}{a_link|trial}, {a_link|test} '], ['vis', [{'t': 'prueba del embarazo', 'tr': 'pregnancy test'}, {'t': 'vamos a hacer la prueba', 'tr': "let's try it"}]]]}]], [['sense', {'sn': '3', 'dt': [['text', '{bc}{a_link|proof} (in printing or photography)']]}]], [['sense', {'sn': '4', 'dt': [['text', '{bc}{a_link|event}, qualifying round (in sports)']]}]], [['sense', {'sn': '5', 'vrs': [{'va': 'a prueba', 'vac': 'a ~'}], 'dt': [['text', '{bc}on a trial basis']]}]], [['sense', {'sn': '6', 'vrs': [{'va': 'a prueba de agua'}], 'dt': [['text', '{bc}{a_link|waterproof}']]}]], [['sense', {'sn': '7', 'vrs': [{'va': 'prueba de fuego'}], 'dt': [['text', '{bc}{a_link|acid test}']]}]], [['sense', {'sn': '8', 'vrs': [{'va': 'poner a prueba'}], 'dt': [['text', '{bc}to put to the test']]}]]]}], 'shortdef': ['proof, (piece of) evidence', 'trial, test', 'proof (in printing or photography)']}, {'meta': {'id': 'relieve', 'uuid': 'bb5c03ff-0726-4713-bc0b-5997639f3bc0', 'lang': 'es', 'sort': '2619302000', 'src': 'spanish', 'section': 'alpha', 'stems': ['relieve', 'poner en relieve'], 'offensive': False}, 'hwi': {'hw': 'relieve'}, 'fl': 'masculine noun', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}{a_link|relief}, {a_link|projection} '], ['vis', [{'t': 'mapa en relieve', 'tr': 'relief map'}, {'t': 'letras en relieve', 'tr': 'embossed letters'}]]]}]], [['sense', {'sn': '2', 'dt': [['text', '{bc}{a_link|prominence}, {a_link|importance}']]}]], [['sense', {'sn': '3', 'vrs': [{'va': 'poner en relieve'}], 'dt': [['text', '{bc}to {a_link|highlight}, to {a_link|emphasize}']]}]]]}], 'shortdef': ['relief, projection', 'prominence, importance', 'to highlight, to emphasize']}, {'meta': {'id': 'remedio', 'uuid': '182908f5-57ca-437d-8b8e-0b38d80d287e', 'lang': 'es', 'sort': '2619336000', 'src': 'spanish', 'section': 'alpha', 'stems': ['remedio', 'poner remedio a', 'sin remedio'], 'offensive': False}, 'hwi': {'hw': 'remedio', 'prs': [{'sound': {'audio': 'remed01sp'}}]}, 'fl': 'masculine noun', 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [['text', '{bc}{a_link|remedy}, {a_link|cure}']]}]], [['sense', {'sn': '2', 'dt': [['text', '{bc}{a_link|solution}']]}]], [['sense', {'sn': '3', 'dt': [['text', '{bc}{a_link|option} '], ['vis', [{'t': 'no me quedó más remedio', 'tr': 'I had no other choice'}, {'t': 'no hay remedio', 'tr': "it can't be helped"}]]]}]], [['sense', {'sn': '4', 'vrs': [{'va': 'poner remedio a'}], 'dt': [['text', '{bc}to put a stop to']]}]], [['sense', {'sn': '5', 'vrs': [{'va': 'sin remedio', 'vac': 'sin ~'}], 'dt': [['text', '{bc}{a_link|unavoidable}, {a_link|inevitable}']]}]]]}], 'shortdef': ['remedy, cure', 'solution', 'option']}]

# for entry in data:
#     # print(f"Headword: {entry.get('meta', {}).get('id')}")
#
#     # Print short definitions (quick meanings)
#     print("Short definitions:")
#     for shortdef in entry.get("shortdef", []):
#         print(f"- {shortdef}")
#
#     # Full definitions
#     print("\nFull definitions:")
#     for sense_group in entry.get("def", []):
#         for sseq in sense_group.get("sseq", []):
#             for sense in sseq:
#                 sense_data = sense[1]
#                 for dt in sense_data.get("dt", []):
#                     if dt[0] == "text":
#                         print(f"- Spanish: {dt[1]}")
#                     elif dt[0] == "vis":
#                         for example in dt[1]:
#                             print(f"  Example in English: {example.get('t')}")
#                             print(f"  Translation in Spanish: {example.get('tr')}")

result = {}
for entry in data:
    # Print the main headword
    headword = entry.get('meta', {}).get('id')
    if headword != target_word:
        continue
    print(f"Headword: {headword}\n")

    result["short"] = []
    for shortdef in entry.get("shortdef", []):
        result["short"].append(shortdef)
    print()

    # Full definitions with Spanish text and example translations
    print("Full definitions:")
    for sense_group in entry.get("def", []):
        for sseq in sense_group.get("sseq", []):
            for sense in sseq:
                sense_data = sense[1]
                for dt in sense_data.get("dt", []):
                    # Spanish definition text
                    if dt[0] == "text":
                        english_definition = dt[1]
                        # Clean special characters in the definition
                        cleaned_english_definition = (
                            english_definition
                                .replace("{a_link|", "")
                                .replace("{bc}", "")
                                .replace("}", "")
                                .replace("{sx|", "")
                                .replace("||", "")
                        )
                        print(f"- English Definition: {cleaned_english_definition.strip()}")
                    # Example sentences
                    elif dt[0] == "vis":
                        for example in dt[1]:
                            # Example in English and Spanish translation
                            spanish_example = example.get('t')
                            english_translation = example.get('tr')
                            print(f"  Example in Spanish: {spanish_example}")
                            print(f"  Translation in English: {english_translation}")
    print("\n" + "=" * 40 + "\n")

print(result)

