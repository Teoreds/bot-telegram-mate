# -*- coding: utf-8 -*-
from pprint import pprint
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import telepot
import sys, time
import wolframalpha
import random

client = wolframalpha.Client('UL7PYU-UVL7JT297V')

bot = telepot.Bot('1364584522:AAEzEOPOEWr757FakhU-s9ZLNV35UTrfU8A')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if '.' == msg['text'][0]:
        if len(msg['text']) > 3:
            try:
                if '.bot' == msg['text']:
                    bot.sendMessage(chat_id, 'Posso fare tante cose, ' + 'clicca qui per capire come sfruttarmi: \n' + 'https://t.me/c/1373295830/458' )
                elif '.news' == msg['text']:
                    f = open("comunicazioni.txt","r")
                    a = 'Ultime comunicazioni:'
                    b = f.read()
                    a += '\n' + b
                    f.close()
                    if b == '':
                        a = 'Non ci sono nuove comunicazioni.'
                    bot.sendMessage(chat_id, a)
                elif '.LPTcancella' == msg['text'][0:12]:
                    if len(msg['text']) == 12: 
                        f = open("comunicazioni.txt","w")
                        f.write('')
                        f.close()
                        bot.sendMessage(chat_id, "ok capo, ho cancellato tutte le news. Nessuno saprà mai cos'è successo realmente con quel prete dell'appennino...")
                    else:
                        f = open("comunicazioni.txt","r")
                        a = f.read()
                        b = ''
                        c = 0
                        for i in range(len(a)):
                            if c != int(msg['text'][13]):
                                b += a[i]
                            if a[i] == "-":
                                c += 1
                        f.close()
                        f = open("comunicazioni.txt","w")
                        if b[len(b)-1] == "-":
                            b = b[:len(b)-2:]
                        f.write(b)
                        f.close()
                        bot.sendMessage(chat_id, "ok capo, ho rimosso la riga numero " + msg['text'][13])                     
                elif '.LPTaggiungi' == msg['text'][0:12]:
                    f = open("comunicazioni.txt","r+")
                    if f.read() == '':
                        f.write('-' + msg['text'][12:])
                    else:
                        f.close()
                        f = open("comunicazioni.txt","a")
                        f.write('\n-'+msg['text'][12:])
                    f.close()
                    bot.sendMessage(chat_id, 'ok capo, ho cambiato le news, per vederle scrivi .news')
                elif '.frase' == msg['text'][0:6]:
                    if len(msg['text']) > 15 and msg['text'][7:15] == 'aggiungi':
                        f = open("frasi.txt","a")
                        f.write("_" + msg['text'][16:])
                        bot.sendMessage(chat_id, 'ok capo, ho aggiunto la frase')
                    else:
                        f = open("frasi.txt","r")
                        frasi = f.read()
                        b = 0
                        for el in frasi:
                            if el == "_":
                                b += 1
                        frase = random.randint(1,b)
                        d = 0
                        i = 0
                        c = ''
                        while i < len(frasi):
                            if frasi[i] == "_":
                                d += 1
                            elif d == frase:
                                c += frasi[i]
                            i += 1
                        bot.sendMessage(chat_id, c)
                elif '.comandi' == msg['text']:
                    bot.sendMessage(chat_id, 'Ecco cosa posso fare: \ntutti i comandi di matematica, ad esempio .limit .derivata .integral .converge ovviamente è importante inserire l argomento di quelle funzioni. \n\nInoltre con .news puoi controllare tutte le comunicazioni, mentre con .frase mi fai dire una frase a caso di qualche prof.')
                else:
                    i = 0
                    sol = client.query(msg['text'][1:])
                    answer = next(sol.results).text
                    bot.sendMessage(chat_id, answer)
            except:
                bot.sendMessage(chat_id, 'Comando invalido, chiedo scudo. Per capire quali sono i comandi legali digita ".bot"')


bot.message_loop({'chat': on_chat_message})

while 1:
    time.sleep(3)

