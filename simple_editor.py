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
    out_filedir = inquirer.text(message="Inserisci il nome della cartella di output", default="foto")
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

    modalita = {
        "extract multiple photo from a video": raffica_foto,
        "make a simple start-end cut": taglia_video,
        "transcode to h264": transcodifica264,
        "transcode to h265": transcodifica265,
        #"decompress to mjpeg - pcm_s16le": decomprimi,
        "quit": exit
        }

    questions = [
        inquirer.Path("file_path", message="File Path?", normalize_to_absolute_path=True, exists=True, path_type=inquirer.Path.FILE),
        inquirer.List("mode", message="What do you want to do?", choices=list(modalita.keys()), default="quit"),
    ]
    answers = inquirer.prompt(questions)
    filepath = answers["file_path"]

    modalita[answers["mode"]]()
