from tkinter.filedialog import askopenfilename
from datetime import datetime
import inquirer
import ffmpeg
import json
import os

def taglia_video():
    start_time = inquirer.text(message="Inserisci il tempo d'inizio nel formato HH:MM:SS", default="00:00:00")
    t1 = datetime.strptime(start_time, "%H:%M:%S")
    end_time = inquirer.text(message="Inserisci il tempo di fine nel formato HH:MM:SS", default="00:01:00")
    t2 = datetime.strptime(end_time, "%H:%M:%S")
    delta = t2 - t1
    tempo_secondi = int(delta.total_seconds())

    out_filename = inquirer.text(message="Inserisci il nome del file output", default=f"out_{os.path.basename(filepath).split('/')[-1]}")
    stream = ffmpeg.input(filepath, ss=start_time, t=tempo_secondi)
    stream = ffmpeg.output(stream, f"{os.path.dirname(os.path.abspath(filepath))}/{out_filename}", vcodec="copy", acodec="copy")
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)
exit

def raffica_foto():
    start_time = inquirer.text(message="Inserisci il tempo d'inizio nel formato HH:MM:SS", default="00:00:00")
    t1 = datetime.strptime(start_time, "%H:%M:%S")
    end_time = inquirer.text(message="Inserisci il tempo di fine nel formato HH:MM:SS", default="00:01:00")
    t2 = datetime.strptime(end_time, "%H:%M:%S")
    delta = t2 - t1
    tempo_secondi = int(delta.total_seconds())
    foto_fps = inquirer.text(message="Numero di foto al secondo", default="2")
    foto_fps = int(foto_fps)
    out_filedir = inquirer.text(message="Inserisci il nome della cartella di output", default=f"{os.path.dirname(os.path.abspath(filepath)).split('/')[-1]} - foto")
    if not os.path.exists(f"{os.path.dirname(os.path.abspath(filepath))}/{out_filedir}"):
        os.makedirs(f"{os.path.dirname(os.path.abspath(filepath))}/{out_filedir}")
    out_filename = inquirer.text(message="Inserisci il nome del file output", default=f"{os.path.dirname(os.path.abspath(filepath)).split('/')[-1].replace(' ', '_')}_")
    stream = ffmpeg.input(filepath, ss=start_time, t=tempo_secondi)
    stream = ffmpeg.filter(stream, "fps", fps=foto_fps)
    stream = ffmpeg.output(stream, f"{os.path.dirname(os.path.abspath(filepath))}/{out_filedir}/{out_filename}%04d.png")
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)


def transcodifica264():
    out_filename = inquirer.text(message="Inserisci il nome del file output", default=f"out_{os.path.basename(filepath).split('/')[-1]}")
    stream = ffmpeg.input(filepath)
    stream = ffmpeg.output(stream, f"{os.path.dirname(os.path.abspath(filepath))}/{out_filename}", vcodec="libx264", acodec="copy")
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)

def transcodifica265():
    out_filename = inquirer.text(message="Inserisci il nome del file output", default=f"out_{os.path.basename(filepath).split('/')[-1]}")
    stream = ffmpeg.input(filepath)
    stream = ffmpeg.output(stream, f"{os.path.dirname(os.path.abspath(filepath))}/{out_filename}", vcodec="libx265", acodec="copy")
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)

def decomprimi():
    out_filename = inquirer.text(message="Inserisci il nome del file output", default=f"out_{os.path.basename(filepath).split('/')[-1]}.mov")
    stream = ffmpeg.input(filepath)
    stream = ffmpeg.output(stream, f"{os.path.dirname(os.path.abspath(filepath))}/{out_filename}", vcodec="mjpeg", acodec="pcm_s16le")
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)

if __name__ == "__main__":
    print("\nSimple Video Editor\n")

    with open("config.json", "r") as f:
        config = json.load(f)

    modalita = {
        "Estrai multiple foto dai video": raffica_foto,
        "Fai un taglio inizio-fine": taglia_video,
        "Transcodifica in h264": transcodifica264,
        "Transcodifica in h265": transcodifica265,
        #"decompress to mjpeg - pcm_s16le": decomprimi,
        "Esci": exit
        }
    
    filepath = askopenfilename(title="Scegli il video", initialdir=config["base_filepath"])

    modalita[inquirer.List("mode", message="Cosa vuoi fare?", choices=list(modalita.keys()), default="Esci")]()
