



# from pydub import AudioSegment
# from pathlib import Path
# import os, glob

# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.core.files.uploadedfile import UploadedFile
# from django.core.files import File

# from radio_funk.utils.logger import LOGGER

# # from .models import Episodes

# def convert_hi_audio_files(audio_file, target_filetype="mp3", content_type='audio/mpeg', bitrate="320k"):
#     # file_path = audio_file.temporary_file_path()
#     # file_path = str(audio_file)
#     file_path = str(audio_file.path)
#     LOGGER.info(file_path)

#     original_extension = file_path.split('.')[-1]
#     mp3_converted_file = AudioSegment.from_file(file_path, original_extension)

#     new_path = file_path[:-3] + target_filetype
#     LOGGER.info(mp3_converted_file)
    
#     mp3_converted_file.export(new_path, format=target_filetype, bitrate="320k")

#     converted_audiofile = File(
#                 file=open(new_path, 'rb'),
#                 name=Path(new_path)
#             )
#     converted_audiofile.name = Path(new_path).name
#     converted_audiofile.content_type = content_type
#     converted_audiofile.size = os.path.getsize(new_path)
#     LOGGER.info(f"Hi_Fi Audio: {converted_audiofile.name} - {converted_audiofile.size}")
#     return converted_audiofile

# def convert_no_audio_files(audio_file, target_filetype="mp3", content_type='audio/mpeg', bitrate="128k"):
#     # file_path = audio_file.temporary_file_path()
#     # file_path = str(audio_file)
#     file_path = str(audio_file.path)
#     LOGGER.info(file_path)

#     original_extension = file_path.split('.')[-1]
#     mp3_converted_file = AudioSegment.from_file(file_path, original_extension)

#     new_path = file_path[:-3] + target_filetype
#     LOGGER.info(mp3_converted_file)
    
#     mp3_converted_file.export(new_path, format=target_filetype, bitrate="128k")

#     converted_audiofile = File(
#                 file=open(new_path, 'rb'),
#                 name=Path(new_path)
#             )
#     converted_audiofile.name = Path(new_path).name
#     converted_audiofile.content_type = content_type
#     converted_audiofile.size = os.path.getsize(new_path)
#     LOGGER.info(f"Audio: {new_path} {converted_audiofile.name} - {converted_audiofile.size}")
#     return converted_audiofile

# def convert_lo_audio_files(audio_file, target_filetype="mp3", content_type='audio/mpeg', bitrate="40k"):
#     # file_path = audio_file.temporary_file_path()
#     # file_path = str(audio_file)
#     file_path = str(audio_file.path)
#     LOGGER.info(file_path)

#     original_extension = file_path.split('.')[-1]
#     mp3_converted_file = AudioSegment.from_file(file_path, original_extension)

#     new_path = file_path[:-3] + target_filetype
#     mp3_converted_file.export(new_path, format=target_filetype, bitrate="40k")
#     LOGGER.info(mp3_converted_file)

#     converted_audiofile = File(
#                 file=open(new_path, 'rb'),
#                 name=Path(new_path)
#             )
#     converted_audiofile.name = Path(new_path).name
#     converted_audiofile.content_type = content_type
#     converted_audiofile.size = os.path.getsize(new_path)
#     LOGGER.info(f"Lo_Fi Audio: {converted_audiofile.name} - {converted_audiofile.size}")
#     return converted_audiofile


# @receiver(post_save, sender=Episodes)
# def podcast_audio_save_signal(sender, created, instance, *args, **kwargs):
#     if created:
#         LOGGER.info(instance.audio.path)
#         instance.audio = convert_no_audio_files(instance.audio)
#         instance.audio_lo = convert_lo_audio_files(instance.audio)
#         instance.audio_hi = convert_hi_audio_files(instance.audio)
