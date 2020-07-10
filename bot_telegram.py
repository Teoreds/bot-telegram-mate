#!/usr/bin/python
# -*- coding: utf-8 -*-
import telepot
import sys
import time
import wolframalpha
import random

client = wolframalpha.Client(app_id)

bot = telepot.Bot(bot_code)


def on_chat_message(msg):  # gestore dei messaggi inviati nella chat col bot
    content_type, chat_type, chat_id = telepot.glance(msg)

    # controllo che il messaggio sia testuale e inizi col punto
    if content_type == "text" and msg['text'][0] == '.':
        # separo il comando dall'argomento, tutto dentro un'unica lista
        # contenente i due elementi
        cmd, args = unpack(msg['text'][1:])

        if cmd in comandi:
            comandi[cmd](chat_id, args)

        else:
            bot.sendMessage(
                chat_id,
                'Comando errato. Per una lista di comandi puoi scrivere .help')


def w(chat_id, calcolo):  # passa a wolframalpha il calcolo, prende risultato in forma testuale e lo invia
    """ [calcolo] \nesegue un calcolo con wolframalpha e invia il risultato"""
    try:
        sol = client.query(calcolo)
        # mi interessa solo la parte dei risultati.
        answer = next(sol.results).text
        bot.sendMessage(chat_id, answer)

    # se qualcosa va storto col calcolo o se non trova "results", il che
    # capita spesso...
    except BaseException:

        bot.sendMessage(
            chat_id,
            'Non sono riuscito ad ottenere il risultato richiesto. Sicuro di aver formattato bene il messaggio?')


def news(chat_id, args):  # accede al file comunicazioni e restituisce tutte le news, oppure esegue un'azione sulle news
    """ <azione> \ninvia le comunicazioni recenti o (opzionale) esegue un'azione su di esse"""
    if args is None:  # comunica solamente le news

        with open("comunicazioni.txt", "r") as f:
            notizie = f.read().decode('UTF-8')

        risposta = 'Ultime comunicazioni:' + notizie

        if notizie == '':
            risposta = 'Non ci sono nuove comunicazioni.'

        bot.sendMessage(chat_id, risposta)

    else:  # è stata eseguita un'azione sulle news
        # spezziamo l'azione da l'argomento dell'azione.
        act, arg = unpack(args)

        if act in azioni:
            try:
                # come il dizionario dei comandi, qua accedo al dizionario
                # delle azioni (funzioni)
                bot.sendMessage(chat_id, azioni[act]("comunicazioni.txt", arg))
            except BaseException:
                bot.sendMessage(chat_id, 'Errore di formattazione del comando')


def frase(chat_id, args):  # accede al file delle frasi e ne restituisce una casuale, oppure esegue un'azione sulle frasi
    """ <azione> \ninvia una frase casuale o (opzionale) esegue un'azione su di esse"""
    if args is None:

        with open("frasi.txt", "r") as f:  # qui apre le frasi e le mette, separate, in una lista
            frasi = f.read().decode('UTF-8').splitlines()
        if len(frasi) > 1:

            bot.sendMessage(chat_id, random.choice(frasi[1:]))

    else:  # è stata eseguita un'azione sulle frasi
        # spezziamo l'azione dal suo argomento
        act, arg = unpack(args)

        if act in azioni:
            try:
                bot.sendMessage(chat_id, azioni[act]("frasi.txt", arg))
            except BaseException:
                bot.sendMessage(chat_id, 'Errore di formattazione del comando')


def tutte(file, useless):
    with open(file, "r") as f:
        frasi = f.read().decode('UTF-8')
    return frasi


def svuota(file, useless):
    with open(file, "w") as f:
        f.write('')
    return 'Ho svuotato il file con successo'


def cancella_riga(file, riga):
    with open(file, "r") as f:
        righe = f.read().decode('UTF-8').splitlines()

    righe.pop(int(riga))

    with open(file, "w") as f:
        f.write(('\n'.join(righe)).encode('UTF-8'))
    return 'Ho cancellato la frase con successo'


def aggiungi_frase(file, frase):
    with open(file, "a") as f:
        f.write(('\n' + frase).encode('UTF-8'))
    return 'Ho aggiunto la frase con successo'


def unpack(text):
    if text.count(' ') > 0:
        return text.split(None, 1)
    return text, None


def help(chat_id, args):
    """\nstampa questo messaggio"""
    usage_cmds = ['.' + cmd + comandi[cmd].__doc__ for cmd in comandi]
    bot.sendMessage(
        chat_id,
        "Ecco una lista dei comandi e il loro uso. N.B: le parentesi [] e i segni >< servono solo a uso notazionale: non vanno inseriti nel comando." +
        "\n\n" +
        (
            '\n\n'.join(usage_cmds)))


def plot(chat_id, function):
    """ [function] \nplotta il grafico di una funzione e restituisce immagine"""
    try:
        sol = client.query(function)
        # mi interessa solo la parte della query contente l'immagine.
        group = next(
            pod for pod in sol.pods if 'Input' not in pod.title).subpods
        answer = next(next(group).img).src
        bot.sendPhoto(chat_id, answer, function)

    # se qualcosa va storto col calcolo o se non trova l'immagine, il che
    # capita spesso...
    except BaseException:

        bot.sendMessage(
            chat_id,
            'Non sono riuscito ad ottenere il risultato richiesto. Sicuro di aver formattato bene il messaggio?')


comandi = {
    'w': w,
    'news': news,
    'frase': frase,
    'help': help,
    'plot': plot}

azioni = {
    'svuota': svuota,
    'cancella_riga': cancella_riga,
    'aggiungi_frase': aggiungi_frase,
    'tutte': tutte
}

bot.message_loop({'chat': on_chat_message})

if __name__ === "__main__":
    while True:
        time.sleep(3)

