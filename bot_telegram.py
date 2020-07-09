#!/usr/bin/python
# -*- coding: utf-8 -*-
import telepot
import sys, time
import wolframalpha
import random

client = wolframalpha.Client(##############)

bot = telepot.Bot(####################)

def on_chat_message(msg):                #gestore dei messaggi inviati nella chat col bot
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == "text" and msg['text'][0] == '.':                #controllo che il messaggio sia testuale e inizi col punto
        msg_text = msg['text'][1:].lower().split(None, 1)                #separo il comando dall'argomento, tutto dentro un'unica lista contenente i due elementi
        
        if msg_text[0] in comandi:                #controllo che il comando sia legale            
            comandi[msg_text[0]](msg_text[-1], chat_id)                #accedo al dizionario comandi, eseguo la funzione associata a msg_txt[0] con argomenti il resto del comando e la chat_id
        
        else:            
            bot.sendMessage(chat_id, 'Comando errato. Per una lista di comandi puoi scrivere .comandi')


def w(calcolo, chat_id):                #passa a wolframalpha il calcolo, prende risultato in forma testuale e lo invia
    try:                #spesso wolframalpha fa brutti scherzi
        sol = client.query(calcolo)
        answer = next(sol.results).text                #mi interessa solo la parte dei risultati. Notare anche che tutte le immagini che restituisce sono fallate e i link non funzionano.
        
        bot.sendMessage(chat_id, answer)                #restituisco il risultato
        
    except:                #se qualcosa va storto col calcolo o se non trova "results", il che capita spesso...
        
        bot.sendMessage(chat_id, 'Non sono riuscito ad ottenere il risultato richiesto. Sicuro di aver formattato bene il messaggio?')


def news(action, chat_id):                #accede al file comunicazioni e restituisce tutte le news, oppure esegue un'azione sulle news'''
    if action == 'news':                #comunica solamente le news
        
        with open("comunicazioni.txt","r") as f:                #qui apre le news e le raccoglie in una stringa chiamata notizie    
            notizie = f.read().decode('UTF-8')

        risposta = 'Ultime comunicazioni:' + notizie                #concatena le notizie in modo elegante
        
        if notizie == '':        
            risposta = 'Non ci sono nuove comunicazioni.'                #se non c'erano notizie restituisce un messaggio particolare
            
        bot.sendMessage(chat_id, risposta)
           
    else:                #è stata eseguita un'azione sulle news
        action_list = action.split(None, 1)                #spezziamo l'azione da l'argomento dell'azione.
    
        if action_list[0] in azioni:                #controllo legalità dell'azione        
            try:
                azioni[action_list[0]]("comunicazioni.txt", action_list[-1])                #come il dizionario dei comandi, qua accedo al dizionario delle azioni (funzioni)
	        bot.sendMessage(chat_id, 'Fatto. Posso fare altro per lei, padrone?')
            except:
                bot.sendMessage(chat_id, 'Errore di formattazione del comando')


def frase(action, chat_id):                #accede al file delle frasi e ne restituisce una casuale, oppure esegue un'azione sulle frasi
    if action == 'frase':                #sceglie una frase random e la scrive
        
        with open("frasi.txt","r") as f:                #qui apre le frasi e le mette, separate, in una lista    
            frasi = f.read().decode('UTF-8').splitlines()
        if len(frasi) > 1:
            numero = random.randint(1,len(frasi)-1)                #scelgo un numero casuale, che corrisponde alla frase casuale che scelgo        
            bot.sendMessage(chat_id, frasi[numero])

    else:                #è stata eseguita un'azione sulle frasi
        action_list = action.split(None, 1)                #spezziamo l'azione dal suo argomento
        
        if action_list[0] in azioni:                #controllo la legalità dell'azione        
            try:
                azioni[action_list[0]]("frasi.txt", action_list[-1])                #come il dizionario dei comandi, qua $
                bot.sendMessage(chat_id, 'Fatto. Posso fare altro per lei, padrone?')
            except:
                bot.sendMessage(chat_id, 'Errore di formattazione del comando')


def svuota(file, h=None):                #accede al file e lo svuota
    with open(file, "w") as f:                #apre il file e ci scrive '' al posto di tutto il resto
        f.write('')


def cancella_riga(file, riga):                #accede al file ed elimina la riga richiesta     
    with open(file, "r") as f:                #apre il file e separa le righe diverse, ottengo una lista con tutte le righe
        righe = f.read().decode('UTF-8').splitlines()
    
    righe.pop(int(riga)-1)                #rimuovo la riga richiesta
        
    with open(file, "w") as f:                #"ricompilo" le righe senza quella rimossa
        f.write(('\n'.join(righe)).encode('UTF-8'))

def aggiungi_frase(file, frase):                #accede al file e appende una nuova frase
    with open(file, "a") as f:                #apro il file richiesto e appendo la frase
        f.write(('\n'+frase).encode('UTF-8'))

def help(comando, chat_id):                #printa una leggenda dei comandi eseguibili
    bot.sendMessage(chat_id, "I comandi disponibili sono '.news', '.frase', '.comandi', '.w argomento' (l'argomento deve essere il calcolo che si vuole eseguire, ad esempio limit(x->0)[x*log(x)] o derivata x^2 o integral sen(x)...)")
    
    
comandi = {
    'w':w,
    'news':news,
    'frase':frase,
    'help':help
    }

azioni = {
    'svuota':svuota,
    'cancella_riga':cancella_riga,
    'aggiungi_frase':aggiungi_frase
    }


bot.message_loop({'chat': on_chat_message})

while 1:
    time.sleep(3)
