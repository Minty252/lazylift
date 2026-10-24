#!/usr/bin/env python3
"""Builds lazylift.cc (GitHub Pages serves the generated files as they are).

    python3 build.py

Writes index.html (German) and en/index.html, plus imprint and privacy policy in both
languages. The landing page tests the market for the browser extension (repo tf-match)
with a waitlist; until 2026-10-25 it was fastpal.com/coach. The texts describe only what
the extension does today, the price is marked as planned.
"""
import hashlib
import html
import pathlib

ROOT = pathlib.Path(__file__).parent
PRODUKT = "LazyLift"
e = html.escape

TEXTE = {
    "de": {
        "titel": f"{PRODUKT}: lockerer schreiben in WhatsApp und Discord",
        "beschreibung": "Eine Browser-Erweiterung, die neben dem Chat Antworten vorschlägt, die zum Gespräch passen, und sich merkt, was du über die Leute weißt. Du schickst selbst.",
        "locale": "de_DE",
        "sprache": "Sprache",
        "warteliste": "Auf die Warteliste",
        "oben": "Browser-Erweiterung für WhatsApp Web und Discord",
        "h1": "Schreib lockerer. Mit einem Coach direkt neben dem Chat.",
        "lead": "Du weißt oft nicht, was du antworten sollst, oder Gespräche schlafen nach drei Nachrichten ein? LazyLift liest das Gespräch mit und schlägt dir zwei Antworten vor, die zum Ton passen. Du wählst eine aus, passt sie an und schickst sie selbst.",
        "preis": "Kostenlos eintragen. Geplant sind etwa 5 bis 10 EUR im Monat.",
        "demo": {"kanal": "# allgemein", "name": "kai", "nachricht": "hat schon wer die neue folge gesehen? 😭", "panel": "Entwürfe",
                 "entwuerfe": ["ja!! das ende hat mich fertig gemacht, dich auch?", "noch nicht, lohnt sich die staffel?"],
                 "einfuegen": "Einfügen", "hinweis": "Beispiel mit erfundenem Chat"},
        "kann_titel": "Was LazyLift kann",
        "kann": [
            ("Zwei Entwürfe pro Nachricht", "Passend zu Länge, Ton und Sprache des Chats. Auf eine kurze Nachricht kommt eine kurze Antwort."),
            ("Es merkt sich die Leute", "Hobbys, Pläne, Insider: LazyLift führt Notizen zu jeder Person, und die nächsten Entwürfe knüpfen daran an."),
            ("Öffentliche Discord-Kanäle", "Antworten, die auf das laufende Gespräch eingehen, statt \"Hi, ist hier jemand aus NRW?\"."),
            ("Ein Ziel pro Chat", "Du legst fest, was du erreichen willst, zum Beispiel ein Treffen ausmachen. LazyLift zeigt, was schon geklappt hat und was noch offen ist."),
            ("Übersetzung", "Nachrichten in anderen Sprachen werden übersetzt, Entwürfe kommen in der Sprache deines Gegenübers."),
            ("Du schickst selbst", "Nichts geht automatisch raus. Ein Klick setzt den Entwurf ins Eingabefeld, du liest ihn und drückst Senden."),
        ],
        "fuer_wen_titel": "Für wen",
        "fuer_wen": "Für dich, wenn du im Chat steif wirkst, lange über eine Antwort nachdenkst oder neue Leute kennenlernen willst und schwer ins Gespräch kommst. Mit der Zeit siehst du, wie lockere Antworten gebaut sind, und brauchst LazyLift seltener.",
        "ablauf_titel": "So läuft es",
        "ablauf": [
            ("Chat öffnen", "WhatsApp Web oder Discord im Browser, LazyLift sitzt in der Seitenleiste."),
            ("Analysieren klicken", "Nach ein paar Sekunden stehen zwei Entwürfe da, dazu die Übersetzung und dein Fortschritt beim Ziel."),
            ("Selbst schicken", "Entwurf einfügen, anpassen, senden. Oder nur als Anstoß nehmen und eigene Worte finden."),
        ],
        "fragen_titel": "Fragen",
        "fragen": [
            ("Merkt mein Gegenüber das?", "Es erscheint kein Hinweis im Chat. Du schickst jede Nachricht selbst und kannst sie vorher ändern."),
            ("Welche Apps gehen?", "WhatsApp Web und Discord im Browser (Chrome, Brave, Edge). Die Handy-Apps nicht."),
            ("Was passiert mit meinen Chats?", "Nur wenn du auf Analysieren klickst, geht der sichtbare Verlauf zur Auswertung an Claude, das KI-Modell von Anthropic. Verlauf und Notizen speichert die Erweiterung in deinem Browser."),
            ("Was kostet es?", "Auf der Warteliste nichts. Geplant sind etwa 5 bis 10 EUR im Monat. Wer auf der Liste steht, kann früher testen."),
            ("Wann geht es los?", "Ich nutze die Erweiterung gerade selbst jeden Tag. Sobald genug Leute auf der Warteliste stehen, lade ich die ersten zum Testen ein."),
        ],
        "liste_titel": "Trag dich ein.",
        "liste_text": "Ich melde mich per Mail, sobald du testen kannst. Sonst schreibe ich dir nichts.",
        "form": {"name": "Vorname", "name_platz": "Kim", "email": "E-Mail", "zusatz": "Wo würdest du es nutzen? (freiwillig)",
                 "zusatz_platz": "z. B. Discord, WhatsApp, Dating", "nachricht": "Nachricht (freiwillig)",
                 "nachricht_platz": "Was fällt dir beim Chatten schwer?", "hinweis": "Ich nutze deine Angaben nur für die Warteliste. Mehr dazu in der",
                 "datenschutz": "Datenschutzerklärung"},
        "fusszeile": "Ein Projekt der Hofmann GmbH.",
        "impressum": "Impressum",
        "datenschutz": "Datenschutz",
        "seiten": {"impressum": "impressum.html", "datenschutz": "datenschutz.html"},
        "startseite": "Zur Startseite",
    },
    "en": {
        "titel": f"{PRODUKT}: write more relaxed in WhatsApp and Discord",
        "beschreibung": "A browser extension that suggests replies next to the chat that fit the conversation, and remembers what you know about people. You send them yourself.",
        "locale": "en_US",
        "sprache": "Language",
        "warteliste": "Join the waitlist",
        "oben": "Browser extension for WhatsApp Web and Discord",
        "h1": "Write more relaxed. With a coach right next to the chat.",
        "lead": "You often don't know what to reply, or conversations die after three messages? LazyLift reads along and suggests two replies that fit the tone. You pick one, adjust it and send it yourself.",
        "preis": "Free to join. The plan is about €5 to €10 a month.",
        "demo": {"kanal": "# general", "name": "kai", "nachricht": "anyone seen the new episode yet? 😭", "panel": "Drafts",
                 "entwuerfe": ["yes!! that ending destroyed me, you too?", "not yet, is the season worth it?"],
                 "einfuegen": "Insert", "hinweis": "Example with a made-up chat"},
        "kann_titel": "What LazyLift does",
        "kann": [
            ("Two drafts per message", "Matching the length, tone and language of the chat. A short message gets a short reply."),
            ("It remembers people", "Hobbies, plans, inside jokes: LazyLift keeps notes on every person, and the next drafts build on them."),
            ("Public Discord channels", "Replies that join the running conversation, instead of \"Hi, anyone here from Berlin?\"."),
            ("A goal per chat", "You set what you want, for example to arrange a meetup. LazyLift shows what has worked and what is still open."),
            ("Translation", "Messages in other languages get translated, drafts come in the language of the other person."),
            ("You send it yourself", "Nothing goes out on its own. One click puts the draft into the message box, you read it and press send."),
        ],
        "fuer_wen_titel": "Who it is for",
        "fuer_wen": "For you if you come across stiff in chats, think about a reply for ages, or want to meet new people and find it hard to get into a conversation. Over time you see how relaxed replies are built, and you need LazyLift less.",
        "ablauf_titel": "How it works",
        "ablauf": [
            ("Open a chat", "WhatsApp Web or Discord in the browser, LazyLift sits in the side panel."),
            ("Click Analyze", "A few seconds later there are two drafts, plus the translation and your progress toward the goal."),
            ("Send it yourself", "Insert a draft, adjust it, send. Or just take it as a nudge and find your own words."),
        ],
        "fragen_titel": "Questions",
        "fragen": [
            ("Will the other person notice?", "Nothing shows up in the chat. You send every message yourself and can change it first."),
            ("Which apps work?", "WhatsApp Web and Discord in the browser (Chrome, Brave, Edge). Not the phone apps."),
            ("What happens to my chats?", "Only when you click Analyze does the visible history go to Claude, Anthropic's AI model, to be read. History and notes are stored by the extension in your browser."),
            ("What does it cost?", "Nothing on the waitlist. The plan is about €5 to €10 a month. People on the list get to test earlier."),
            ("When does it start?", "I use the extension myself every day right now. Once enough people are on the waitlist, I will invite the first ones to test."),
        ],
        "liste_titel": "Join the list.",
        "liste_text": "I will e-mail you once you can test it. Nothing else.",
        "form": {"name": "First name", "name_platz": "Kim", "email": "E-mail", "zusatz": "Where would you use it? (optional)",
                 "zusatz_platz": "e.g. Discord, WhatsApp, dating", "nachricht": "Message (optional)",
                 "nachricht_platz": "What do you find hard about chatting?", "hinweis": "I only use your details for the waitlist. More in the",
                 "datenschutz": "privacy policy"},
        "fusszeile": "A project of Hofmann GmbH.",
        "impressum": "Imprint",
        "datenschutz": "Privacy",
        "seiten": {"impressum": "imprint.html", "datenschutz": "privacy.html"},
        "startseite": "Back to the home page",
    },
}

IMPRESSUM = {
    "de": ("Impressum", """
<p>Angaben gemäß § 5 DDG:</p>
<p>Hofmann GmbH<br>Regerstr. 1<br>48301 Nottuln</p>
<p>Geschäftsführer: Moritz Hofmann<br>Registergericht: Amtsgericht Coesfeld, HRB 18001<br>USt-IdNr.: DE303275460</p>
<p>E-Mail: <a data-mail></a></p>
"""),
    "en": ("Imprint", """
<p>Information according to § 5 DDG (German Digital Services Act):</p>
<p>Hofmann GmbH<br>Regerstr. 1<br>48301 Nottuln<br>Germany</p>
<p>Managing director: Moritz Hofmann<br>Register court: Amtsgericht Coesfeld, HRB 18001<br>VAT ID: DE303275460</p>
<p>E-mail: <a data-mail></a></p>
"""),
}

DATENSCHUTZ = {
    "de": ("Datenschutzerklärung", """
<h2>1. Verantwortlicher</h2>
<p>Hofmann GmbH, Regerstr. 1, 48301 Nottuln, vertreten durch den Geschäftsführer Moritz Hofmann. E-Mail: <a data-mail></a></p>
<h2>2. Hosting</h2>
<p>Diese Seite liegt bei GitHub Pages (GitHub Inc., USA). Beim Aufruf verarbeitet GitHub technisch nötige Daten wie IP-Adresse, Zeitpunkt, aufgerufene Seite und Browserkennung, um die Seite auszuliefern und vor Angriffen zu schützen. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO. GitHub ist nach dem EU-US Data Privacy Framework zertifiziert.</p>
<h2>3. Keine Cookies, kein Tracking</h2>
<p>Diese Seite setzt keine Cookies und nutzt keine Analyse- oder Werbedienste. Schriften liegen auf dieser Seite selbst, es werden keine Inhalte von Dritten nachgeladen.</p>
<h2>4. Warteliste</h2>
<p>Wenn Sie sich in die Warteliste eintragen, verarbeiten wir Ihren Vornamen, Ihre E-Mail-Adresse und freiwillig, wo Sie die Erweiterung nutzen würden, und Ihre Nachricht. Das Formular sendet an einen Server der Hofmann GmbH unter fastpal.com (Vercel Inc., USA). Wir speichern die Angaben dort nicht: Sie gehen als E-Mail an Moritz Hofmann. Für den Versand nutzen wir Resend (Resend Inc., USA, Versand über Server in der EU), auf Grundlage von EU-Standardvertragsklauseln.</p>
<p>Zweck: Sie per Mail einladen, sobald Sie testen können. Rechtsgrundlage: Art. 6 Abs. 1 lit. a DSGVO (Ihre Einwilligung durch das Eintragen). Sie können sie jederzeit per Mail widerrufen. Wir löschen den Eintrag, wenn Sie widerrufen oder das Projekt endet.</p>
<h2>5. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Schreiben Sie dazu an die Adresse oben. Sie können sich außerdem bei einer Datenschutz-Aufsichtsbehörde beschweren, für uns zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen.</p>
<p>Stand: Oktober 2026</p>
"""),
    "en": ("Privacy policy", """
<h2>1. Controller</h2>
<p>Hofmann GmbH, Regerstr. 1, 48301 Nottuln, Germany, represented by its managing director Moritz Hofmann. E-mail: <a data-mail></a></p>
<h2>2. Hosting</h2>
<p>This site is hosted on GitHub Pages (GitHub Inc., USA). When you open it, GitHub processes technically necessary data such as IP address, time, page and browser, to deliver the site and protect it from attacks. Legal basis: Art. 6(1)(f) GDPR. GitHub is certified under the EU-US Data Privacy Framework.</p>
<h2>3. No cookies, no tracking</h2>
<p>This site sets no cookies and uses no analytics or advertising services. Fonts are served from this site itself, nothing is loaded from third parties.</p>
<h2>4. Waitlist</h2>
<p>If you join the waitlist, we process your first name, your e-mail address and, optionally, where you would use the extension and your message. The form sends to a server of Hofmann GmbH at fastpal.com (Vercel Inc., USA). We do not store the data there: it goes to Moritz Hofmann as an e-mail. For sending we use Resend (Resend Inc., USA, sending from servers in the EU), based on EU standard contractual clauses.</p>
<p>Purpose: inviting you by e-mail once you can test it. Legal basis: Art. 6(1)(a) GDPR (your consent by signing up), which you can withdraw at any time by e-mail. We delete the entry when you withdraw or the project ends.</p>
<h2>5. Your rights</h2>
<p>You have the right of access, rectification, erasure, restriction of processing, data portability and objection. Write to the address above. You can also complain to a data protection supervisory authority; ours is the State Commissioner for Data Protection and Freedom of Information of North Rhine-Westphalia.</p>
<p>As of October 2026</p>
"""),
}


def pfad_in(lang, seite):
    return TEXTE[lang]["seiten"][seite]


def asset(up, name):
    """Asset URL with a content hash, so a changed file gets a new URL."""
    digest = hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()[:10]
    return f"{up}assets/{name}?v={digest}"


def kopf(lang, titel, beschreibung, seite, tiefe):
    up = "../" * tiefe
    t = TEXTE[lang]
    de_url = "https://lazylift.cc/" + ("" if seite == "index" else pfad_in("de", seite))
    en_url = "https://lazylift.cc/en/" + ("" if seite == "index" else pfad_in("en", seite))
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{t['locale']}">
<link rel="alternate" hreflang="de" href="{de_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="icon" href="data:,">
<link rel="stylesheet" href="{asset(up, 'fonts.css')}">
<link rel="stylesheet" href="{asset(up, 'site.css')}">
<script defer src="{asset(up, 'site.js')}"></script>
</head>
<body>
"""


def kopfleiste(lang, seite):
    t = TEXTE[lang]
    # The language switch keeps the page: imprint <-> imprint, home <-> home.
    datei = {s: "" if seite == "index" else pfad_in(s, seite) for s in ("de", "en")}
    de_link = ("../" if lang == "en" else "") + datei["de"] or "./"
    en_link = ("en/" if lang == "de" else "") + datei["en"] or "./"
    knopf = f'<a class="cc-btn-klein" href="#warteliste">{t["warteliste"]}</a>' if seite == "index" else ""
    return f"""<header class="cc-wrap cc-header">
<a class="cc-marke" href="./" style="color: inherit; text-decoration: none">{PRODUKT}</a>
<div class="cc-header-rechts">
<div class="st-sprachwahl" role="group" aria-label="{t['sprache']}">
<a href="{de_link}" hreflang="de" lang="de"{' aria-current="true"' if lang == 'de' else ''}>DE</a>
<a href="{en_link}" hreflang="en" lang="en"{' aria-current="true"' if lang == 'en' else ''}>EN</a>
</div>
{knopf}
</div>
</header>
"""


def fuss(lang):
    t = TEXTE[lang]
    return f"""<footer class="cc-wrap cc-footer">
<p>{t['fusszeile']}</p>
<nav>
<a href="https://hofmannmoritz.com">Moritz Hofmann</a>
<a href="{pfad_in(lang, 'impressum')}">{t['impressum']}</a>
<a href="{pfad_in(lang, 'datenschutz')}">{t['datenschutz']}</a>
</nav>
</footer>
</div>
</body>
</html>
"""


def startseite(lang):
    t = TEXTE[lang]
    d = t["demo"]
    f = t["form"]
    entwuerfe = "".join(f'<div class="cc-entwurf"><p>{e(x)}</p><span>{e(d["einfuegen"])}</span></div>' for x in d["entwuerfe"])
    karten = "".join(f'<div class="cc-karte"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in t["kann"])
    schritte = "".join(f'<li><span class="cc-nr">{i + 1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(t["ablauf"]))
    fragen = "".join(f"<details><summary>{e(a)}</summary><p>{e(b)}</p></details>" for a, b in t["fragen"])
    return (
        kopf(lang, t["titel"], t["beschreibung"], "index", 1 if lang == "en" else 0)
        + '<div class="cc-root">\n'
        + kopfleiste(lang, "index")
        + f"""<main>
<section class="cc-wrap cc-hero">
<div class="cc-hero-text">
<p class="cc-oben">{e(t['oben'])}</p>
<h1>{e(t['h1'])}</h1>
<p class="cc-lead">{e(t['lead'])}</p>
<a class="cc-btn" href="#warteliste">{t['warteliste']}</a>
<p class="cc-preis">{e(t['preis'])}</p>
</div>
<figure class="cc-vorschau" aria-label="{e(d['hinweis'])}">
<div class="cc-fenster">
<div class="cc-chat"><p class="cc-kanal">{e(d['kanal'])}</p><div class="cc-blase"><span class="cc-autor">{e(d['name'])}</span>{e(d['nachricht'])}</div></div>
<div class="cc-panel"><p class="cc-panel-titel">{e(d['panel'])}</p>{entwuerfe}</div>
</div>
<figcaption>{e(d['hinweis'])}</figcaption>
</figure>
</section>
<section class="cc-wrap cc-abschnitt">
<h2>{e(t['kann_titel'])}</h2>
<div class="cc-karten">{karten}</div>
</section>
<section class="cc-band">
<div class="cc-wrap cc-fuer-wen">
<h2>{e(t['fuer_wen_titel'])}</h2>
<p>{e(t['fuer_wen'])}</p>
</div>
</section>
<section class="cc-wrap cc-abschnitt">
<h2>{e(t['ablauf_titel'])}</h2>
<ol class="cc-schritte">{schritte}</ol>
</section>
<section class="cc-wrap cc-abschnitt">
<h2>{e(t['fragen_titel'])}</h2>
<div class="cc-fragen">{fragen}</div>
</section>
<section class="cc-liste" id="warteliste">
<div class="cc-wrap cc-liste-innen">
<h2>{e(t['liste_titel'])}</h2>
<p>{e(t['liste_text'])}</p>
<form class="cc-form" data-anfrage="warteliste">
<label><span>{f['name']}</span><input name="name" required autocomplete="given-name" placeholder="{f['name_platz']}" maxlength="100"></label>
<label><span>{f['email']}</span><input name="email" type="email" required autocomplete="email" maxlength="200"></label>
<label><span>{e(f['zusatz'])}</span><input name="zusatz" placeholder="{e(f['zusatz_platz'])}" maxlength="200"></label>
<label class="cc-form-breit"><span>{f['nachricht']}</span><textarea name="nachricht" rows="4" maxlength="3000" placeholder="{e(f['nachricht_platz'])}"></textarea></label>
<label class="cc-form-falle" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
<div class="cc-form-breit cc-form-ende">
<button type="submit">{t['warteliste']}</button>
<p class="cc-form-hinweis">{e(f['hinweis'])} <a href="{pfad_in(lang, 'datenschutz')}">{f['datenschutz']}</a>.</p>
</div>
</form>
</div>
</section>
</main>
"""
        + fuss(lang)
    )


def rechtsseite(lang, seite, titel, inhalt):
    t = TEXTE[lang]
    return (
        kopf(lang, f"{titel} | {PRODUKT}", titel, seite, 1 if lang == "en" else 0)
        + '<div class="cc-root">\n'
        + kopfleiste(lang, seite)
        + f"""<main class="cc-wrap cc-recht">
<a href="./">{t['startseite']}</a>
<h1>{titel}</h1>
{inhalt}</main>
"""
        + fuss(lang)
    )


def main():
    for lang, ziel in (("de", ROOT), ("en", ROOT / "en")):
        ziel.mkdir(exist_ok=True)
        (ziel / "index.html").write_text(startseite(lang))
        titel, inhalt = IMPRESSUM[lang]
        (ziel / pfad_in(lang, "impressum")).write_text(rechtsseite(lang, "impressum", titel, inhalt))
        titel, inhalt = DATENSCHUTZ[lang]
        (ziel / pfad_in(lang, "datenschutz")).write_text(rechtsseite(lang, "datenschutz", titel, inhalt))
    print("built index.html, en/index.html and the legal pages")


if __name__ == "__main__":
    main()
