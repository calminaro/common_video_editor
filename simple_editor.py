from tkinter import filedialog
from datetime import datetime
import inquirer
import ffmpeg
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


def raffica_foto():
    start_time = inquirer.text(message="Inserisci il tempo d'inizio nel formato HH:MM:SS", default="00:00:00")
    t1 = datetime.strptime(start_time, "%H:%M:%S")
    end_time = inquirer.text(message="Inserisci il tempo di fine nel formato HH:MM:SS", default="00:01:00")
    t2 = datetime.strptime(end_time, "%H:%M:%S")
    delta = t2 - t1
    tempo_secondi = int(delta.total_seconds())
    foto_fps = inquirer.text(message="Numero di foto al secondo", default="2")
    foto_fps = int(foto_fps)
    out_filedir = inquirer.text(message="Inserisci il nome della cartella di output", default="foto")
    print(filepath)
    print(os.path.abspath(filepath))
    print(os.path.dirname(os.path.abspath(filepath)))
    print(f"{os.path.dirname(os.path.abspath(filepath))}/{out_filedir}")
    if not os.path.exists(f"{os.path.dirname(os.path.abspath(filepath))}/{out_filedir}"):
        os.makedirs(f"{os.path.dirname(os.path.abspath(filepath))}/{out_filedir}")
    out_filename = inquirer.text(message="Inserisci il nome del file output", default=f"{os.path.basename(filepath).split('/')[-1].replace(' ', '_')}_")
    stream = ffmpeg.input(filepath, ss=start_time, t=tempo_secondi)
    stream = ffmpeg.filter(stream, "fps", fps=foto_fps)
    stream = ffmpeg.output(stream, f"{os.path.dirname(os.path.abspath(filepath))}/{out_filedir}/{out_filename}%04d.png")
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)


def transcodifica():
    out_filename = inquirer.text(message="Inserisci il nome del file output", default=f"out_{os.path.basename(filepath).split('/')[-1]}")
    stream = ffmpeg.input(filepath)
    stream = ffmpeg.output(stream, f"{os.path.dirname(os.path.abspath(filepath))}/{out_filename}", vcodec="libx264", acodec="copy")
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)


def chiedi_modalita():
    modalita = answers["mode"]

    match modalita:
        case "extract multiple photo from a video":
            raffica_foto()
            exit()
        case "make a simple start-end cut":
            taglia_video()
            exit()
        case "change video codec to h264":
            transcodifica()
            exit()
        case "quit":
            exit()
        case _:
            chiedi_modalita()

if __name__ == "__main__":
    print("\nSimple Video Editor\n")

    questions = [
        inquirer.Path("file_path", message="File Path?", normalize_to_absolute_path=True, exists=True, path_type=inquirer.Path.FILE),
        inquirer.List("mode", message="What do you want to do?", choices=["extract multiple photo from a video", "make a simple start-end cut", "change video codec to h264", "quit"], default="quit"),
    ]
    answers = inquirer.prompt(questions)
    filepath = answers["file_path"]

    chiedi_modalita()
