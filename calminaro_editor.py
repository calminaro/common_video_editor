from tkinter import filedialog
from datetime import datetime
import ffmpeg
import os

def taglia_video():
    start_time = input("Inserisci il tempo d'inizio nel formato HH:MM:SS: ")
    if start_time == "":
        start_time = "00:00:00"
    t1 = datetime.strptime(start_time, "%H:%M:%S")
    end_time = input("Inserisci il tempo di fine nel formato HH:MM:SS: ")
    if end_time == "":
        end_time = "00:01:00"
    t2 = datetime.strptime(end_time, "%H:%M:%S")
    delta = t2 - t1
    tempo_secondi = int(delta.total_seconds())

    out_filename = input("Inserisci il nome del file output (lascia vuoto per il default): ")
    if out_filename == "":
        out_filename = "out_"+os.path.basename(inputfile).split('/')[-1]
    stream = ffmpeg.input(inputfile, ss=start_time, t=tempo_secondi)
    stream = ffmpeg.output(stream, filepath+"/"+out_filename)
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)


def raffica_foto():
    start_time = input("Inserisci il tempo d'inizio nel formato HH:MM:SS: ")
    if start_time == "":
        start_time = "00:00:00"
    t1 = datetime.strptime(start_time, "%H:%M:%S")
    end_time = input("Inserisci il tempo di fine nel formato HH:MM:SS: ")
    if end_time == "":
        end_time = "00:01:00"
    t2 = datetime.strptime(end_time, "%H:%M:%S")
    delta = t2 - t1
    tempo_secondi = int(delta.total_seconds())
    foto_fps = input("Numero di foto al secondo (lascia vuoto per il default): ")
    if foto_fps == "":
        foto_fps = 2
    else:
        foto_fps = int(foto_fps)
    out_filedir = input("Inserisci il nome della cartella di output (lascia vuoto per il default): ")
    if out_filedir == "":
        if not os.path.exists(filepath+"/foto"):
            os.makedirs(filepath+"/foto")
        out_filedir = "foto"
    else:
        if not os.path.exists(filepath+"/"+out_filedir):
            os.makedirs(filepath+"/"+out_filedir)
    out_filename = input("Inserisci il nome dei file output (lascia vuoto per il default): ")
    if out_filename == "":
        out_filename = os.path.basename(filepath).split('/')[-1].replace(" ", "_")+"_"
    stream = ffmpeg.input(inputfile, ss=start_time, t=tempo_secondi)
    stream = ffmpeg.filter(stream, "fps", fps=foto_fps)
    stream = ffmpeg.output(stream, filepath+"/"+out_filedir+"/"+out_filename+"%04d.png", vcodec='copy', acodec='copy')
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)


def transcodifica():
    out_filename = input("Inserisci il nome del file output (lascia vuoto per il default): ")
    if out_filename == "":
        out_filename = "out_"+os.path.basename(inputfile).split('/')[-1]
    stream = ffmpeg.input(inputfile)
    stream = ffmpeg.output(stream, filepath+"/"+out_filename, vcodec="libx264", acodec='copy')
    print("\nSto esportando...\n")
    ffmpeg.run(stream, quiet=True)


def chiedi_modalita():
    modalita = input("Press:\n- [F] to extract multiple photo from a video,\n- [C] to make a simple start-end cut,\n- [T] to change video codec to h264,\n- [Q] to exit.\n\nWhat is your choice? :").lower()
    print()
    match modalita:
        case "f":
            raffica_foto()
            exit()
        case "c":
            taglia_video()
            exit()
        case "t":
            transcodifica()
            exit()
        case "q":
            exit()
        case _:
            chiedi_modalita()

if __name__ == "__main__":
    print("\nSimple Calminaro Video Editor\n")

    inputfile = filedialog.askopenfilename()
    filepath = os.path.dirname(os.path.abspath(inputfile))

    chiedi_modalita()
