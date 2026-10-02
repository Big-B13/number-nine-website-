#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator voor de ROUTE NINE pop-up tour pagina.

Schrijft:
    event.html        -> de tourpagina (Engels in de HTML, NL/DE via de switcher)
    js/tour-i18n.js   -> window.__TOUR_I18N__ met alle vertalingen

Alle teksten staan hieronder in de vorm (EN, NL, DE). Pas ze daar aan en draai:

    python3 build_tour.py

De pagina gebruikt dezelfde header/footer/markup als about.html, zodat js/app.js
(menu-knop, drawer, winkelmand) zonder aanpassing blijft werken.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent

# --------------------------------------------------------------------------
# vertalingen: key -> (EN, NL, DE)
# --------------------------------------------------------------------------
TX = {}


def tx(key, en, nl, de):
    TX[key] = {"en": en, "nl": nl, "de": de}
    return key


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def el(tag, key, en, nl, de, cls=None, attrs=""):
    """Element met data-i18n-key; de Engelse tekst staat in de HTML zelf."""
    tx(key, en, nl, de)
    c = f' class="{cls}"' if cls else ""
    a = f" {attrs}" if attrs else ""
    return f'<{tag}{c}{a} data-i18n="{key}">{esc(en)}</{tag}>'


# ---------------------------------------------------------------- hero
HERO = dict(
    eyebrow=("Pop-up tour · Germany · 2027",
             "Pop-uptour · Duitsland · 2027",
             "Pop-up-Tour · Deutschland · 2027"),
    sub=("Four cities. Eleven weeks. One store that refuses to stand still.",
         "Vier steden. Elf weken. Eén winkel die weigert stil te staan.",
         "Vier Städte. Elf Wochen. Ein Laden, der nicht stillsteht."),
    lede=("Number Nine packs up the shop floor and drives it into Germany. "
          "Dortmund, Düsseldorf, Munich, Berlin — two weeks in every city, a new "
          "space at every stop, and the loudest names in scent and fashion on the "
          "invite list.",
          "Number Nine pakt de winkelvloer in en rijdt ermee naar Duitsland. "
          "Dortmund, Düsseldorf, München, Berlijn — twee weken per stad, elke stop "
          "een nieuwe ruimte, en de grootste namen uit geur en mode op de "
          "uitnodigingslijst.",
          "Number Nine packt die Ladenfläche ein und fährt damit nach Deutschland. "
          "Dortmund, Düsseldorf, München, Berlin — zwei Wochen pro Stadt, an jedem "
          "Stopp eine neue Fläche und die lautesten Namen aus Duft und Mode auf der "
          "Gästeliste."),
    status=("Status: concept. Dates, spaces and line-up are a working plan — nothing "
            "is signed, nobody is booked.",
            "Status: concept. Data, ruimtes en line-up zijn een werkplan — er is niets "
            "getekend en niemand is geboekt.",
            "Status: Konzept. Termine, Flächen und Line-up sind ein Arbeitsplan — nichts "
            "ist unterschrieben, niemand ist gebucht."),
)

STATS = [
    ("4", ("cities", "steden", "Städte")),
    ("58", ("trading days", "verkoopdagen", "Verkaufstage")),
    ("11", ("weeks on the road", "weken onderweg", "Wochen unterwegs")),
    ("25", ("creators invited", "creators uitgenodigd", "eingeladene Creator")),
    ("9M+", ("combined reach", "gezamenlijk bereik", "gemeinsame Reichweite")),
]

# ---------------------------------------------------------------- het idee
IDEA = [
    (("Why Germany", "Waarom Duitsland", "Warum Deutschland"),
     ("83 million people, the first stop an hour and a half from our own front door, "
      "and the densest fragrance-and-fashion creator scene in Europe. Almost none of "
      "them have heard of us. A webshop is never going to fix that. A room full of "
      "people might.",
      "83 miljoen mensen, de eerste stop op anderhalf uur van onze eigen voordeur, en "
      "de dichtste geur- en modecreatorscene van Europa. Bijna niemand daar kent ons. "
      "Een webshop lost dat nooit op. Een ruimte vol mensen misschien wel.",
      "83 Millionen Menschen, der erste Stopp anderthalb Stunden von unserer eigenen "
      "Haustür entfernt, und die dichteste Duft- und Mode-Creator-Szene Europas. Fast "
      "niemand dort kennt uns. Ein Webshop ändert das nie. Ein Raum voller Menschen "
      "vielleicht schon.")),
    (("Why a pop-up and not a store", "Waarom een pop-up en geen winkel",
      "Warum Pop-up und kein Laden"),
     ("We rent a raw space, build it out in four days and treat it like a stage instead "
      "of a shop. Everything in it is temporary — the rail, the drop, the people behind "
      "the counter — and that is exactly the reason anyone bothers to show up. You can "
      "visit a store next month. You cannot visit this next month.",
      "We huren een kale ruimte, bouwen hem in vier dagen op en behandelen hem als een "
      "podium in plaats van een winkel. Alles erin is tijdelijk — het rek, de drop, de "
      "mensen achter de toonbank — en precies daarom komt iemand langs. Een winkel kun "
      "je volgende maand ook bezoeken. Dit niet.",
      "Wir mieten eine rohe Fläche, bauen sie in vier Tagen auf und behandeln sie wie "
      "eine Bühne statt wie einen Laden. Alles darin ist temporär — die Stange, der "
      "Drop, die Leute hinter dem Tresen — und genau deshalb kommt überhaupt jemand "
      "vorbei. In einen Laden kannst du nächsten Monat auch noch. Hier nicht.")),
    (("Why creators carry it", "Waarom creators het dragen",
      "Warum Creator das tragen"),
     ("The fragrance corner of YouTube moves product like nothing else in retail, and "
      "the menswear channels right next to it have been selling each other's wardrobes "
      "for a decade. We are not buying a post. We are handing them a lit studio, a room "
      "full of their own audience and a bottle wall, and letting them do the thing they "
      "already do better than any agency.",
      "De geurhoek van YouTube verkoopt producten als geen ander kanaal in retail, en de "
      "menswear-kanalen ernaast verkopen elkaars garderobe al tien jaar. We kopen geen "
      "post. We geven ze een uitgelichte studio, een ruimte vol met hun eigen publiek en "
      "een muur vol flacons, en laten ze doen waar ze sowieso beter in zijn dan welk "
      "bureau dan ook.",
      "Die Duft-Ecke von YouTube verkauft Produkte wie kein anderer Kanal im Handel, und "
      "die Menswear-Kanäle daneben verkaufen sich seit zehn Jahren gegenseitig die "
      "Garderobe. Wir kaufen keinen Post. Wir geben ihnen ein ausgeleuchtetes Studio, "
      "einen Raum voll mit ihrem eigenen Publikum und eine Flakonwand — und lassen sie "
      "das tun, was sie ohnehin besser können als jede Agentur.")),
]

QUOTE = ("Two weeks is long enough to become the place everybody is talking about, and "
         "short enough that nobody gets bored of it.",
         "Twee weken is lang genoeg om de plek te worden waar iedereen het over heeft, en "
         "kort genoeg dat niemand erop uitgekeken raakt.",
         "Zwei Wochen sind lang genug, um der Ort zu werden, über den alle reden — und "
         "kurz genug, dass niemand sich daran sattsieht.")

# ---------------------------------------------------------------- de route
CITIES = [
    dict(
        n="01", city="Dortmund", img="img/tour/dortmund.jpg",
        dates=("Fri 23 April – Thu 6 May 2027", "vr 23 april – do 6 mei 2027",
               "Fr 23. April – Do 6. Mai 2027"),
        days=("14 days open", "14 dagen open", "14 Tage geöffnet"),
        badge=("The opener", "De opener", "Der Auftakt"),
        district=("Unionviertel / Rheinische Straße, in the shadow of the Dortmunder U. "
                  "Fallback: the Brückstraßenviertel.",
                  "Unionviertel / Rheinische Straße, in de schaduw van de Dortmunder U. "
                  "Terugvaloptie: het Brückstraßenviertel.",
                  "Unionviertel / Rheinische Straße, im Schatten des Dortmunder U. "
                  "Ausweichoption: das Brückstraßenviertel."),
        space=("300–400 m² former industrial unit. Raw concrete, roller shutter, loading "
               "access, nothing precious.",
               "300–400 m² voormalige bedrijfsruimte. Ruw beton, roldeur, laad- en "
               "losmogelijkheid, niks kostbaars.",
               "300–400 m² ehemalige Gewerbefläche. Roher Beton, Rolltor, Ladezone, "
               "nichts Empfindliches."),
        hook=("We open where nobody opens. Dortmund is the youngest big city in the Ruhr: "
              "600,000 people, a huge student population at TU Dortmund, and a retail "
              "scene that every brand doing a \"German tour\" skips straight past. We go "
              "first, we go loud, and from one van we reach Essen, Bochum and Duisburg in "
              "under half an hour by train.",
              "We openen waar niemand opent. Dortmund is de jongste grote stad van het "
              "Ruhrgebied: 600.000 inwoners, een enorme studentenpopulatie aan de TU "
              "Dortmund, en een retailscene die elk merk met een \"Duitslandtour\" "
              "overslaat. Wij gaan als eerste, we gaan hard, en vanuit één busje zitten "
              "Essen, Bochum en Duisburg op nog geen half uur met de trein.",
              "Wir eröffnen dort, wo niemand eröffnet. Dortmund ist die jüngste Großstadt "
              "des Ruhrgebiets: 600.000 Einwohner, eine riesige Studierendenschaft an der "
              "TU Dortmund und eine Handelsszene, die jede Marke auf \"Deutschlandtour\" "
              "einfach überspringt. Wir kommen zuerst, wir kommen laut, und von einem "
              "Transporter aus sind Essen, Bochum und Duisburg in unter einer halben "
              "Stunde mit dem Zug erreichbar."),
        night=("Opening night Friday 23 April, 19:00 — invite only, 150 heads, local DJ, "
               "first city drop at midnight.",
               "Openingsavond vrijdag 23 april, 19:00 — alleen op uitnodiging, 150 man, "
               "lokale dj, eerste citydrop om middernacht.",
               "Eröffnungsabend Freitag, 23. April, 19:00 — nur mit Einladung, 150 Leute, "
               "lokaler DJ, erster City-Drop um Mitternacht."),
        note=("Matchday note: if BVB play at home that weekend there are 81,000 people in "
              "town. The drop gets planned around it.",
              "Wedstrijdnotitie: als BVB dat weekend thuis speelt, zijn er 81.000 mensen in "
              "de stad. De drop plannen we daaromheen.",
              "Spieltag-Notiz: Wenn der BVB an dem Wochenende zu Hause spielt, sind 81.000 "
              "Menschen in der Stadt. Der Drop wird darum herum geplant."),
    ),
    dict(
        n="02", city="Düsseldorf", img="img/tour/dusseldorf.jpg",
        dates=("Fri 14 May – Thu 27 May 2027", "vr 14 mei – do 27 mei 2027",
               "Fr 14. Mai – Do 27. Mai 2027"),
        days=("14 days open", "14 dagen open", "14 Tage geöffnet"),
        badge=("The industry stop", "De branchestop", "Der Branchenstopp"),
        district=("Flingern-Nord around the Ackerstraße for the creative crowd, or a side "
                  "street off the Kö for the luxury crowd. We would take either.",
                  "Flingern-Nord rond de Ackerstraße voor het creatieve publiek, of een "
                  "zijstraat van de Kö voor het luxepubliek. Allebei prima.",
                  "Flingern-Nord rund um die Ackerstraße für das kreative Publikum oder "
                  "eine Seitenstraße der Kö für das Luxuspublikum. Beides nehmen wir."),
        space=("200–300 m² showroom with floor-to-ceiling glass. The window is the "
               "campaign here.",
               "200–300 m² showroom met glas van vloer tot plafond. De etalage ís hier de "
               "campagne.",
               "200–300 m² Showroom mit raumhoher Verglasung. Das Schaufenster ist hier "
               "die Kampagne."),
        hook=("This is where German fashion does business: showrooms, agencies, buying "
              "offices, the trade-fair calendar. It is also the home turf of the German "
              "beauty industry — Henkel is headquartered here and L'Oréal runs its German "
              "business from the city. Everything that happens in this room happens in "
              "front of the people who can put us in other rooms. Smaller space, sharper "
              "guest list.",
              "Hier doet de Duitse mode zaken: showrooms, agentschappen, inkooporganisaties, "
              "de beurskalender. Het is ook het thuisfront van de Duitse beauty-industrie — "
              "Henkel heeft er zijn hoofdkantoor en L'Oréal runt er zijn Duitse tak. Alles "
              "wat in deze ruimte gebeurt, gebeurt voor de ogen van de mensen die ons in "
              "andere ruimtes kunnen krijgen. Kleinere ruimte, scherpere gastenlijst.",
              "Hier macht die deutsche Mode Geschäfte: Showrooms, Agenturen, Einkaufsbüros, "
              "der Messekalender. Es ist außerdem das Heimspielfeld der deutschen "
              "Beauty-Industrie — Henkel hat hier seinen Hauptsitz und L'Oréal steuert von "
              "hier das Deutschlandgeschäft. Alles, was in diesem Raum passiert, passiert "
              "vor den Leuten, die uns in andere Räume bringen können. Kleinere Fläche, "
              "schärfere Gästeliste."),
        night=("Industry evening Wednesday 19 May — buyers, agencies, press. 80 seats, "
               "one short talk, no pitch deck.",
               "Branche-avond woensdag 19 mei — inkopers, bureaus, pers. 80 stoelen, één "
               "korte talk, geen pitchdeck.",
               "Branchenabend Mittwoch, 19. Mai — Einkäufer, Agenturen, Presse. 80 Plätze, "
               "ein kurzer Talk, kein Pitchdeck."),
        note=("Calendar check: the Düsseldorf trade-fair and Japan-Tag weekends pull huge "
              "crowds in May. If we can overlap one, we extend by three days.",
              "Agendacheck: de Düsseldorfse beursweekenden en Japan-Tag trekken in mei enorme "
              "drukte. Als we er één kunnen overlappen, verlengen we met drie dagen.",
              "Kalender-Check: Die Düsseldorfer Messewochenenden und der Japan-Tag ziehen im "
              "Mai enorme Menschenmengen an. Wenn wir eines davon treffen, verlängern wir um "
              "drei Tage."),
    ),
    dict(
        n="03", city="München", img="img/tour/munich.jpg",
        dates=("Fri 4 June – Wed 16 June 2027", "vr 4 juni – wo 16 juni 2027",
               "Fr 4. Juni – Mi 16. Juni 2027"),
        days=("13 days open", "13 dagen open", "13 Tage geöffnet"),
        badge=("The money stop", "De geldstop", "Der Geldstopp"),
        district=("Glockenbachviertel — Hans-Sachs-Straße or Reichenbachstraße. "
                  "Fallback: Maxvorstadt near the academy.",
                  "Glockenbachviertel — Hans-Sachs-Straße of Reichenbachstraße. "
                  "Terugvaloptie: Maxvorstadt bij de academie.",
                  "Glockenbachviertel — Hans-Sachs-Straße oder Reichenbachstraße. "
                  "Ausweichoption: Maxvorstadt nahe der Akademie."),
        space=("150–250 m² boutique. Daylight, wooden floor, a door people are not afraid "
               "to walk through.",
               "150–250 m² boutique. Daglicht, houten vloer, een deur waar mensen zonder "
               "drempel doorheen lopen.",
               "150–250 m² Boutique. Tageslicht, Holzboden, eine Tür, durch die man ohne "
               "Hemmschwelle geht."),
        hook=("The highest purchasing power in Germany and a clientele that already buys "
              "niche perfume at €250 a bottle without blinking. So we turn the volume "
              "down instead of up: mornings by appointment, afternoons open to the "
              "street, a perfumer masterclass instead of a DJ. Smallest room of the tour, "
              "highest average basket.",
              "De hoogste koopkracht van Duitsland en een klantenkring die nicheparfum van "
              "€250 per flacon koopt zonder met de ogen te knipperen. Dus draaien we het "
              "volume omlaag in plaats van omhoog: ochtenden op afspraak, middagen open "
              "voor de straat, een parfumeur-masterclass in plaats van een dj. De kleinste "
              "ruimte van de tour, het hoogste gemiddelde mandje.",
              "Die höchste Kaufkraft Deutschlands und eine Kundschaft, die Nischenparfum für "
              "250 € pro Flakon kauft, ohne mit der Wimper zu zucken. Also drehen wir die "
              "Lautstärke herunter statt hoch: vormittags nach Termin, nachmittags offen für "
              "die Straße, eine Parfumeur-Masterclass statt eines DJs. Der kleinste Raum der "
              "Tour, der höchste Durchschnittsbon."),
        night=("Masterclass Saturday 12 June — scent building with a working perfumer. "
               "24 seats, ticketed, sells out or we are doing it wrong.",
               "Masterclass zaterdag 12 juni — geur bouwen met een werkende parfumeur. "
               "24 plekken, met ticket, uitverkocht of we doen iets verkeerd.",
               "Masterclass Samstag, 12. Juni — Duftaufbau mit einem arbeitenden Parfumeur. "
               "24 Plätze, ticketpflichtig, ausverkauft oder wir machen etwas falsch."),
        note=("Appointment mornings double as the shoot slot: quiet room, best light of "
              "the day, no queue in the background.",
              "De afspraakochtenden zijn tegelijk het shootmoment: stille ruimte, het beste "
              "licht van de dag, geen rij op de achtergrond.",
              "Die Termin-Vormittage sind zugleich das Shooting-Fenster: ruhiger Raum, bestes "
              "Licht des Tages, keine Schlange im Hintergrund."),
    ),
    dict(
        n="04", city="Berlin", img="img/tour/berlin.jpg",
        dates=("Fri 25 June – Sun 11 July 2027", "vr 25 juni – zo 11 juli 2027",
               "Fr 25. Juni – So 11. Juli 2027"),
        days=("17 days open — the finale", "17 dagen open — de finale",
              "17 Tage geöffnet — das Finale"),
        badge=("The finale", "De finale", "Das Finale"),
        district=("Mitte around Torstraße / Mulackstraße, or Kreuzberg on the "
                  "Oranienstraße. Neukölln if the right building turns up.",
                  "Mitte rond Torstraße / Mulackstraße, of Kreuzberg aan de Oranienstraße. "
                  "Neukölln als het juiste pand opduikt.",
                  "Mitte rund um Torstraße / Mulackstraße oder Kreuzberg an der "
                  "Oranienstraße. Neukölln, wenn das richtige Gebäude auftaucht."),
        space=("400–600 m², two floors if we can get them. An old Kaufhaus, a gallery or "
               "a showroom with a basement.",
               "400–600 m², twee verdiepingen als het kan. Een oud Kaufhaus, een galerie of "
               "een showroom met kelder.",
               "400–600 m², zwei Etagen, wenn möglich. Ein altes Kaufhaus, eine Galerie oder "
               "ein Showroom mit Keller."),
        hook=("The loudest room of the lot, and the only stop where people turn up to a "
              "pop-up precisely because it is one. We stay the longest, we bring every "
              "creator who joined us earlier in the tour back for the closing weekend, and "
              "we aim the end of the run at the Berlin Fashion Week window in early July. "
              "If the calendar falls the way it usually does, the entire industry is "
              "already in town and we do not have to invite them.",
              "De luidste ruimte van allemaal, en de enige stop waar mensen naar een pop-up "
              "komen juist ómdat het er een is. We blijven het langst, we halen elke creator "
              "die eerder in de tour meedeed terug voor het slotweekend, en we mikken het "
              "einde van de run op het Berlin Fashion Week-venster begin juli. Als de "
              "kalender valt zoals meestal, is de hele branche al in de stad en hoeven we ze "
              "niet uit te nodigen.",
              "Der lauteste Raum von allen und der einzige Stopp, zu dem Leute gerade deshalb "
              "kommen, weil es ein Pop-up ist. Wir bleiben am längsten, holen jeden Creator, "
              "der früher auf der Tour dabei war, zum Abschlusswochenende zurück und legen das "
              "Ende des Laufs auf das Fenster der Berlin Fashion Week Anfang Juli. Fällt der "
              "Kalender wie üblich, ist die halbe Branche ohnehin in der Stadt."),
        night=("Closing weekend Fri 9 – Sun 11 July — full roster, a live recording, the "
               "last numbered drop and a party we are not announcing the address of until "
               "that afternoon.",
               "Slotweekend vr 9 – zo 11 juli — volledige line-up, een live-opname, de laatste "
               "genummerde drop en een feest waarvan we het adres pas die middag bekendmaken.",
               "Abschlusswochenende Fr 9. – So 11. Juli — komplettes Line-up, eine "
               "Live-Aufnahme, der letzte nummerierte Drop und eine Party, deren Adresse wir "
               "erst an jenem Nachmittag bekannt geben."),
        note=("Berlin is also where the recap film gets cut. Two editors travel with the "
              "tour from Dortmund onwards.",
              "In Berlijn wordt ook de recapfilm gemonteerd. Twee editors reizen vanaf "
              "Dortmund met de tour mee.",
              "In Berlin wird auch der Recap-Film geschnitten. Zwei Editoren reisen ab "
              "Dortmund mit der Tour mit."),
    ),
]

# ---------------------------------------------------------------- in de ruimte
FORMAT = [
    (("01", "The Scent Bar", "De Geurbar", "Die Duftbar"),
     ("Forty-eight bottles on a lit back wall. Blind flights of five, scored on a card, "
      "and a one-page scent profile you take home. Nobody sells you anything until you "
      "ask what number three was.",
      "Achtenveertig flacons tegen een uitgelichte achterwand. Blind ruiken in rondes van "
      "vijf, scoren op een kaart, en een geurprofiel van één A4 dat je meeneemt. Niemand "
      "verkoopt je iets tot jij vraagt wat nummer drie was.",
      "Achtundvierzig Flakons an einer beleuchteten Rückwand. Blindverkostung in Fünferrunden, "
      "Bewertung auf einer Karte und ein einseitiges Duftprofil zum Mitnehmen. Niemand "
      "verkauft dir etwas, bis du fragst, was Nummer drei war.")),
    (("02", "The Fitting Salon", "Het Pashuis", "Der Anproberaum"),
     ("Three curtained booths, two stylists, twenty-minute slots you book at the door. "
      "Walk in with nothing in mind, walk out knowing your size in every label we carry.",
      "Drie pashokjes met gordijn, twee stylisten, slots van twintig minuten die je aan de "
      "deur boekt. Je komt binnen zonder idee en gaat weg met je maat in elk label dat we "
      "voeren.",
      "Drei Kabinen mit Vorhang, zwei Stylistinnen, 20-Minuten-Slots, die du an der Tür "
      "buchst. Du kommst ohne Plan rein und gehst mit deiner Größe in jedem Label, das wir "
      "führen, wieder raus.")),
    (("03", "Studio Nine", "Studio Nine", "Studio Nine"),
     ("A lit corner with a backdrop, a mic and a ring of chairs. Free for every invited "
      "creator, all day, every day of the run. Film the haul, record the podcast, go live. "
      "We never see the edit before you post it.",
      "Een uitgelichte hoek met achtergrond, microfoon en een kring stoelen. Gratis voor "
      "elke uitgenodigde creator, de hele dag, elke dag van de run. Film de haul, neem de "
      "podcast op, ga live. Wij zien de montage nooit voordat jij hem post.",
      "Eine ausgeleuchtete Ecke mit Hintergrund, Mikro und Stuhlkreis. Kostenlos für jeden "
      "eingeladenen Creator, den ganzen Tag, jeden Tag des Laufs. Dreh den Haul, nimm den "
      "Podcast auf, geh live. Wir sehen den Schnitt nie, bevor du ihn postest.")),
    (("04", "The Drop Wall", "De Dropmuur", "Die Drop-Wand"),
     ("One city-exclusive piece per stop, numbered 1 to 99, sold in that room, in that "
      "city, in those two weeks only. Dortmund 01/99 does more for us than any press "
      "release ever will.",
      "Eén stadsexclusief item per stop, genummerd 1 tot 99, alleen te koop in die ruimte, "
      "in die stad, in die twee weken. Dortmund 01/99 doet meer voor ons dan welk "
      "persbericht dan ook.",
      "Ein stadtexklusives Teil pro Stopp, nummeriert von 1 bis 99, verkauft nur in diesem "
      "Raum, in dieser Stadt, in diesen zwei Wochen. Dortmund 01/99 bringt uns mehr als jede "
      "Pressemitteilung.")),
    (("05", "The Programme", "Het Programma", "Das Programm"),
     ("Evenings earn their keep: a perfumer masterclass, a styling battle with the local "
      "scene, a sneaker-care clinic, one open creator Q&A and two DJ nights per stop.",
      "De avonden verdienen zichzelf terug: een parfumeur-masterclass, een stylingbattle met "
      "de lokale scene, een sneakercare-clinic, één open creator-Q&A en twee dj-avonden per "
      "stop.",
      "Die Abende verdienen ihr Geld: eine Parfumeur-Masterclass, ein Styling-Battle mit der "
      "lokalen Szene, eine Sneaker-Care-Clinic, ein offenes Creator-Q&A und zwei DJ-Abende "
      "pro Stopp.")),
    (("06", "The Back Room", "De Achterkamer", "Der Hinterraum"),
     ("Coffee, sofas, phone chargers and absolutely nobody selling you anything. It is the "
      "reason people stay two hours instead of ten minutes, and two hours is the whole "
      "point.",
      "Koffie, banken, telefoonladers en helemaal niemand die je iets verkoopt. Het is de "
      "reden dat mensen twee uur blijven in plaats van tien minuten, en om die twee uur is "
      "het ons te doen.",
      "Kaffee, Sofas, Handyladegeräte und absolut niemand, der dir etwas verkauft. Deshalb "
      "bleiben Leute zwei Stunden statt zehn Minuten — und um diese zwei Stunden geht es.")),
]

# ---------------------------------------------------------------- line-up
LINEUP_TIERS = [
    (("Tier A — the headliners", "Tier A — de headliners", "Tier A — die Headliner"),
     ("One per city if we land them. Approached first, through management, in December.",
      "Eén per stad als het lukt. Als eerste benaderd, via management, in december.",
      "Einer pro Stadt, wenn es klappt. Zuerst angefragt, über das Management, im Dezember."),
     [("Jeremy Fragrance", "2.5M YouTube",
       ("German, and the single biggest name in fragrance on the planet. Dream slot: "
        "Düsseldorf or the Berlin finale.",
        "Duitser, en de grootste naam in geur ter wereld. Droomslot: Düsseldorf of de "
        "Berlijnse finale.",
        "Deutscher und der größte Name im Duftbereich weltweit. Wunschslot: Düsseldorf oder "
        "das Berliner Finale.")),
      ("Lorenz Wiedenmann", "~900k",
       ("Costa Rican-German, minimalist menswear, taste that lines up almost exactly with "
        "our buying. Munich.",
        "Costa Ricaans-Duits, minimalistische menswear, smaak die bijna precies op onze inkoop "
        "aansluit. München.",
        "Costa-ricanisch-deutsch, minimalistische Menswear, Geschmack, der fast exakt zu "
        "unserem Einkauf passt. München.")),
      ("Gents Scents", "646k",
       ("A pure fragrance audience with unusually high trust. Natural fit for the scent bar.",
        "Een puur geurpubliek met ongewoon veel vertrouwen. Logische match met de geurbar.",
        "Ein reines Duftpublikum mit ungewöhnlich hohem Vertrauen. Natürliche Besetzung für "
        "die Duftbar.")),
      ("CurlyFragrance (Michella)", "592k",
       ("The biggest female voice in the men's fragrance world and a brand founder herself.",
        "De grootste vrouwelijke stem in de herengeurwereld en zelf merkoprichter.",
        "Die größte weibliche Stimme in der Herrenduftwelt und selbst Markengründerin."))]),
    (("Tier B — the scent floor", "Tier B — de geurvloer", "Tier B — die Duft-Etage"),
     ("Reviewers and collectors. The people whose opinion decides whether a bottle sells out.",
      "Reviewers en verzamelaars. De mensen wier oordeel bepaalt of een flacon uitverkoopt.",
      "Rezensenten und Sammler. Die Leute, deren Urteil entscheidet, ob ein Flakon ausverkauft "
      "ist."),
     [("Max Forti", "442k", ("Long-running, high engagement, European base.",
                            "Al jaren bezig, hoge betrokkenheid, Europese basis.",
                            "Seit Jahren dabei, hohe Interaktion, europäische Basis.")),
      ("Triple B", "362k", ("Grooming and fragrance, strong male 18–34 audience.",
                           "Grooming en geur, sterk mannelijk publiek van 18–34.",
                           "Grooming und Duft, starkes männliches Publikum 18–34.")),
      ("Olivia Olfactory", "~400k", ("Enormous average views per video. Berlin finale.",
                                     "Enorme gemiddelde views per video. Berlijnse finale.",
                                     "Enorme Durchschnittsaufrufe pro Video. Berliner Finale.")),
      ("Demi Rawling", "368k", ("Luxury fragrance reviews, international reach.",
                               "Luxe geurreviews, internationaal bereik.",
                               "Luxus-Duftkritiken, internationale Reichweite.")),
      ("Soki London", "UK", ("Founder-creator. Perfect for the masterclass in Munich.",
                            "Oprichter én creator. Perfect voor de masterclass in München.",
                            "Gründerin und Creatorin. Perfekt für die Masterclass in München.")),
      ("Monika Cioch", "120k", ("Luxury and niche, a female audience we underserve.",
                               "Luxe en niche, een vrouwelijk publiek dat we onderbedienen.",
                               "Luxus und Nische, ein weibliches Publikum, das wir "
                               "vernachlässigen.")),
      ("The Scented (Yana)", "127k", ("Unfiltered reviews. Credibility we cannot buy.",
                                      "Ongefilterde reviews. Geloofwaardigheid die je niet "
                                      "koopt.",
                                      "Ungefilterte Reviews. Glaubwürdigkeit, die man nicht "
                                      "kaufen kann."))]),
    (("Tier C — the fashion floor", "Tier C — de modevloer", "Tier C — die Mode-Etage"),
     ("Menswear and style channels. These are the people who make a rail look worth flying for.",
      "Menswear- en stijlkanalen. Dit zijn de mensen die een rek de moeite van een vlucht waard "
      "laten lijken.",
      "Menswear- und Stilkanäle. Diese Leute lassen eine Kleiderstange nach einer Reise wert "
      "aussehen."),
     [("Tim Dessaint", "YouTube", ("The European benchmark for men's style content.",
                                  "De Europese maatstaf voor mannenstijlcontent.",
                                  "Der europäische Maßstab für Herrenstil-Content.")),
      ("Daniel Simmons", "YouTube", ("Street style, fitness, lifestyle crossover.",
                                    "Streetstyle, fitness, lifestyle-crossover.",
                                    "Streetstyle, Fitness, Lifestyle-Crossover.")),
      ("Jesper Søndergaard", "IG 900k+", ("Scandinavian minimalism, huge short-form reach.",
                                          "Scandinavisch minimalisme, enorm bereik in "
                                          "short-form.",
                                          "Skandinavischer Minimalismus, riesige "
                                          "Short-Form-Reichweite.")),
      ("Kosta Williams", "YouTube", ("Educational menswear. Ideal for the Düsseldorf talk.",
                                    "Educatieve menswear. Ideaal voor de talk in Düsseldorf.",
                                    "Lehrreiche Menswear. Ideal für den Talk in Düsseldorf.")),
      ("One Dapper Street (Marcel Floruss)", "DE/US",
       ("German-born, New York-based, the bridge to the US audience.",
        "Duitse roots, gevestigd in New York, de brug naar het Amerikaanse publiek.",
        "Deutsche Wurzeln, New Yorker Basis, die Brücke zum US-Publikum.")),
      ("Vintagebursche (Niklas)", "DE", ("Classic German menswear and tailoring nerdery.",
                                        "Klassieke Duitse menswear en maatwerk-nerderij.",
                                        "Klassische deutsche Menswear und Schneider-Nerdtum.")),
      ("Der Stilberater (Justus Hansen)", "DE", ("Style education in German. Dortmund opener.",
                                                 "Stijladvies in het Duits. Opener in Dortmund.",
                                                 "Stilberatung auf Deutsch. Auftakt in Dortmund.")),
      ("Joshiiks", "DE", ("Gen-Z streetwear. The one who brings the queue.",
                         "Gen-Z streetwear. Degene die de rij meebrengt.",
                         "Gen-Z-Streetwear. Der, der die Schlange mitbringt.")),
      ("Johannes Huebl", "IG 1.1M", ("Elevated classic menswear. Munich, by appointment.",
                                     "Verheven klassieke menswear. München, op afspraak.",
                                     "Gehobene klassische Menswear. München, nach Termin."))]),
    (("Tier D — the city locals", "Tier D — de lokale helden", "Tier D — die Locals"),
     ("The ones who actually fill the room on a Tuesday. Smaller numbers, far better turnout.",
      "Degenen die de ruimte op een dinsdag echt vullen. Kleinere cijfers, veel betere opkomst.",
      "Die, die den Raum an einem Dienstag wirklich füllen. Kleinere Zahlen, deutlich bessere "
      "Beteiligung."),
     [("Dortmund", "shortlist open",
       ("Ruhr-based creators plus TU Dortmund student media. Scouting trip in November.",
        "Creators uit het Ruhrgebied plus studentenmedia van de TU Dortmund. Scoutingtrip in "
        "november.",
        "Creator aus dem Ruhrgebiet plus Studierendenmedien der TU Dortmund. Scouting-Trip im "
        "November.")),
      ("Düsseldorf", "industry",
       ("The showroom and agency scene, plus NRW street-style creators.",
        "De showroom- en agentschapscene, plus NRW-streetstylecreators.",
        "Die Showroom- und Agenturszene plus NRW-Streetstyle-Creator.")),
      ("München", "Mitsou Jung · Jacqueline Krapf",
       ("Munich fashion and lifestyle voices with a genuinely local following.",
        "Münchense mode- en lifestylestemmen met een echt lokaal publiek.",
        "Münchner Mode- und Lifestyle-Stimmen mit wirklich lokalem Publikum.")),
      ("Berlin", "TingTing Lai · Mari Rassis · woistlena · Dalia Mya",
       ("Four very different Berlin audiences. Together they are the closing weekend.",
        "Vier heel verschillende Berlijnse publieken. Samen zijn zij het slotweekend.",
        "Vier sehr unterschiedliche Berliner Publika. Zusammen sind sie das "
        "Abschlusswochenende."))]),
]

CREATOR_OFFER = [
    ("Travel and hotel covered, every time, no exceptions.",
     "Reis en hotel betaald, elke keer, zonder uitzondering.",
     "Reise und Hotel bezahlt, jedes Mal, ohne Ausnahme."),
    ("A lit studio they can use unsupervised, all day, every day of the run.",
     "Een uitgelichte studio die ze onbegeleid mogen gebruiken, de hele dag, elke dag van de run.",
     "Ein ausgeleuchtetes Studio, das sie unbeaufsichtigt nutzen können, den ganzen Tag, jeden "
     "Tag des Laufs."),
    ("A numbered drop piece, with their name on the tag if they want one.",
     "Een genummerd dropstuk, met hun naam op het label als ze dat willen.",
     "Ein nummeriertes Drop-Teil, auf Wunsch mit ihrem Namen auf dem Etikett."),
    ("A flat fee for a confirmed appearance. We do not pay in exposure.",
     "Een vaste vergoeding voor een bevestigd optreden. Wij betalen niet in zichtbaarheid.",
     "Ein Festhonorar für einen bestätigten Auftritt. Wir zahlen nicht in Reichweite."),
    ("Zero content approval. We do not read it before it goes up, ever.",
     "Nul contentgoedkeuring. We lezen het nooit voordat het online gaat.",
     "Keinerlei Freigabe von Inhalten. Wir lesen nichts, bevor es online geht."),
]

# ---------------------------------------------------------------- weekritme
WEEK = [
    (("Mon", "ma", "Mo"), ("Closed", "Gesloten", "Geschlossen"),
     ("Restock, repairs, creator filming day in an empty room.",
      "Bijvullen, reparaties, filmdag voor creators in een lege ruimte.",
      "Auffüllen, Reparaturen, Dreh-Tag für Creator im leeren Raum.")),
    (("Tue", "di", "Di"), ("12:00 – 19:00", "12:00 – 19:00", "12:00 – 19:00"),
     ("Scent bar open, styling slots bookable at the door.",
      "Geurbar open, stylingslots te boeken aan de deur.",
      "Duftbar offen, Styling-Slots an der Tür buchbar.")),
    (("Wed", "wo", "Mi"), ("12:00 – 19:00", "12:00 – 19:00", "12:00 – 19:00"),
     ("Industry and press evening from 19:30.",
      "Branche- en persavond vanaf 19:30.",
      "Branchen- und Presseabend ab 19:30.")),
    (("Thu", "do", "Do"), ("12:00 – 21:00", "12:00 – 21:00", "12:00 – 21:00"),
     ("Late night. Workshop slot at 19:00.",
      "Koopavond. Workshopslot om 19:00.",
      "Langer Abend. Workshop-Slot um 19:00.")),
    (("Fri", "vr", "Fr"), ("12:00 – 22:00", "12:00 – 22:00", "12:00 – 22:00"),
     ("Creator takeover, DJ from 20:00.",
      "Creator-takeover, dj vanaf 20:00.",
      "Creator-Takeover, DJ ab 20:00.")),
    (("Sat", "za", "Sa"), ("11:00 – 20:00", "11:00 – 20:00", "11:00 – 20:00"),
     ("The big one. Drop release at 13:00 sharp.",
      "De grote dag. Droprelease om klokslag 13:00.",
      "Der große Tag. Drop-Release pünktlich um 13:00.")),
    (("Sun", "zo", "So"), ("13:00 – 18:00", "13:00 – 18:00", "13:00 – 18:00"),
     ("Slow Sunday: coffee, the archive rail, no music over 70 dB.",
      "Trage zondag: koffie, het archiefrek, geen muziek boven 70 dB.",
      "Langsamer Sonntag: Kaffee, die Archivstange, keine Musik über 70 dB.")),
]

# ---------------------------------------------------------------- cijfers
TARGETS = [
    ("5,600", ("visitors across four stops", "bezoekers over vier stops",
               "Besucher über vier Stopps")),
    ("25", ("creators hosted", "creators ontvangen", "Creator empfangen")),
    ("150+", ("pieces of content", "stuks content", "Content-Beiträge")),
    ("25M+", ("impressions", "impressies", "Impressionen")),
    ("6,000", ("email signups", "e-mailaanmeldingen", "E-Mail-Anmeldungen")),
    ("396", ("numbered drop pieces", "genummerde dropstukken", "nummerierte Drop-Teile")),
]

BUDGET = [
    (("Space rental — 4 × 2 weeks, incl. deposits", "Huur ruimtes — 4 × 2 weken, incl. borg",
      "Flächenmiete — 4 × 2 Wochen, inkl. Kaution"), "€48,000"),
    (("Build, interior, transport", "Opbouw, inrichting, transport",
      "Aufbau, Einrichtung, Transport"), "€32,000"),
    (("Crew, travel, accommodation", "Crew, reizen, overnachting",
      "Crew, Reisen, Unterkunft"), "€36,000"),
    (("Creator hosting and fees", "Creators ontvangen en vergoeden",
      "Creator-Hosting und Honorare"), "€40,000"),
    (("Programme and production", "Programma en productie", "Programm und Produktion"),
     "€18,000"),
    (("Content, film, paid amplification", "Content, film, betaalde versterking",
      "Content, Film, bezahlte Verstärkung"), "€25,000"),
    (("Contingency 10%", "Onvoorzien 10%", "Puffer 10 %"), "€20,000"),
]

# ---------------------------------------------------------------- ruimtebrief
SPACE_BRIEF = [
    ("150–600 m² on the ground floor, with street-facing windows.",
     "150–600 m² op de begane grond, met ramen aan de straat.",
     "150–600 m² im Erdgeschoss, mit Fenstern zur Straße."),
    ("Temporary lease of 18–21 days, including build-up and strike.",
     "Tijdelijke huur van 18–21 dagen, inclusief op- en afbouw.",
     "Zwischenmiete von 18–21 Tagen, inklusive Auf- und Abbau."),
    ("Three-phase power, 32A. A water connection if it exists.",
     "Krachtstroom, 32A. Een wateraansluiting als die er is.",
     "Starkstrom, 32 A. Wasseranschluss, falls vorhanden."),
    ("Ceiling height from 3.2 m and access for a loading van.",
     "Plafondhoogte vanaf 3,2 m en toegang voor een bestelbus.",
     "Deckenhöhe ab 3,2 m und Zufahrt für einen Transporter."),
    ("Ten minutes on foot from the main shopping or creative district.",
     "Tien minuten lopen van het belangrijkste winkel- of creatieve district.",
     "Zehn Gehminuten vom wichtigsten Einkaufs- oder Kreativviertel."),
    ("Fully insured, professional build crew, handed back exactly as found.",
     "Volledig verzekerd, professionele opbouwploeg, opgeleverd zoals aangetroffen.",
     "Vollständig versichert, professionelles Aufbauteam, Übergabe im Originalzustand."),
]

# ---------------------------------------------------------------- roadmap
ROADMAP = [
    (("Oct 2026", "okt 2026", "Okt. 2026"),
     ("Concept locked, budget approved, city shortlist agreed.",
      "Concept vastgelegd, budget goedgekeurd, shortlist van steden rond.",
      "Konzept fixiert, Budget freigegeben, Städte-Shortlist steht.")),
    (("Nov 2026", "nov 2026", "Nov. 2026"),
     ("Agents briefed in all four cities. First viewings and a scouting trip.",
      "Makelaars gebriefd in alle vier de steden. Eerste bezichtigingen en een scoutingtrip.",
      "Makler in allen vier Städten gebrieft. Erste Besichtigungen und ein Scouting-Trip.")),
    (("Dec 2026", "dec 2026", "Dez. 2026"),
     ("Letters of intent on four spaces. First creator approaches through management.",
      "Intentieverklaringen op vier ruimtes. Eerste creatorbenaderingen via management.",
      "Absichtserklärungen für vier Flächen. Erste Creator-Anfragen über das Management.")),
    (("Jan – Feb 2027", "jan – feb 2027", "Jan. – Feb. 2027"),
     ("Contracts signed, build designed, brand partners on board.",
      "Contracten getekend, opbouw ontworpen, merkpartners aan boord.",
      "Verträge unterschrieben, Aufbau entworfen, Markenpartner an Bord.")),
    (("Mar 2027", "mrt 2027", "März 2027"),
     ("Public announcement, guest list opens, press embargo lifts.",
      "Publieke aankondiging, gastenlijst opent, persembargo eraf.",
      "Öffentliche Ankündigung, Gästeliste öffnet, Presse-Embargo fällt.")),
    (("Apr 2027", "apr 2027", "Apr. 2027"),
     ("Dortmund opens. Everything after this is live.",
      "Dortmund opent. Alles daarna is live.",
      "Dortmund eröffnet. Alles danach ist live.")),
    (("Jul 2027", "jul 2027", "Juli 2027"),
     ("Berlin finale, recap film, and the decision on tour number two.",
      "Berlijnse finale, recapfilm, en het besluit over tour nummer twee.",
      "Berliner Finale, Recap-Film und die Entscheidung über Tour Nummer zwei.")),
]

# ---------------------------------------------------------------- partners
PARTNERS = [
    (("Title partner", "Titelpartner", "Titelpartner"), ("1 available", "1 plek", "1 Platz"),
     ("Your name next to the tour name, on every asset in all four cities, plus one evening "
      "of the programme that is entirely yours.",
      "Jouw naam naast de tournaam, op elke uiting in alle vier de steden, plus één "
      "programma-avond die volledig van jou is.",
      "Dein Name neben dem Tournamen, auf jedem Asset in allen vier Städten, plus ein "
      "Programmabend, der ganz dir gehört.")),
    (("Floor partner", "Vloerpartner", "Flächenpartner"), ("4 available", "4 plekken",
                                                           "4 Plätze"),
     ("One city each. A product wall in the space, a co-branded numbered drop and your team "
      "on the guest list.",
      "Eén stad per partner. Een productmuur in de ruimte, een co-branded genummerde drop en "
      "jouw team op de gastenlijst.",
      "Je eine Stadt. Eine Produktwand in der Fläche, ein co-gebrandeter nummerierter Drop und "
      "dein Team auf der Gästeliste.")),
    (("Friends of the tour", "Vrienden van de tour", "Freunde der Tour"),
     ("open", "open", "offen"),
     ("Coffee, drinks, sound, print, transport. You supply it, we use it in front of "
      "everybody and credit you properly.",
      "Koffie, drank, geluid, drukwerk, transport. Jij levert, wij gebruiken het voor het oog "
      "van iedereen en vermelden je netjes.",
      "Kaffee, Getränke, Ton, Druck, Transport. Du lieferst, wir nutzen es vor aller Augen und "
      "nennen dich ordentlich.")),
]

# ---------------------------------------------------------------- faq
FAQ = [
    (("Is any of this actually booked?", "Is hier al iets van geboekt?",
      "Ist davon schon etwas gebucht?"),
     ("No. Every date, every space and every name on this page is a plan. Nothing is signed "
      "and no creator has been approached yet. This page exists so that everybody involved is "
      "looking at the same plan.",
      "Nee. Elke datum, elke ruimte en elke naam op deze pagina is een plan. Er is niets "
      "getekend en nog geen creator benaderd. Deze pagina bestaat zodat iedereen naar hetzelfde "
      "plan kijkt.",
      "Nein. Jedes Datum, jede Fläche und jeder Name auf dieser Seite ist ein Plan. Nichts ist "
      "unterschrieben und noch kein Creator wurde angefragt. Diese Seite gibt es, damit alle "
      "auf denselben Plan schauen.")),
    (("Why not one big store for two months?", "Waarom niet één grote winkel voor twee maanden?",
      "Warum nicht ein großer Laden für zwei Monate?"),
     ("Because week five in the same city is dead. Week one is curiosity, week two is word of "
      "mouth, and then it flattens. We leave while there is still a queue — that queue is the "
      "entire marketing budget.",
      "Omdat week vijf in dezelfde stad dood is. Week één is nieuwsgierigheid, week twee is "
      "mond-tot-mondreclame, en daarna vlakt het af. We vertrekken terwijl er nog een rij staat "
      "— die rij ís het marketingbudget.",
      "Weil Woche fünf in derselben Stadt tot ist. Woche eins ist Neugier, Woche zwei ist "
      "Mundpropaganda, danach flacht es ab. Wir gehen, solange noch eine Schlange steht — diese "
      "Schlange ist das gesamte Marketingbudget.")),
    (("Why these four cities?", "Waarom deze vier steden?", "Warum diese vier Städte?"),
     ("Reach in the Ruhr (Dortmund), the industry (Düsseldorf), the money (Munich) and the "
      "noise (Berlin). Between them they cover the north-west, the south and the capital, and "
      "they are all within a day's drive of each other and of us.",
      "Bereik in het Ruhrgebied (Dortmund), de branche (Düsseldorf), het geld (München) en het "
      "lawaai (Berlijn). Samen dekken ze het noordwesten, het zuiden en de hoofdstad, en ze "
      "liggen allemaal op een dagrit van elkaar en van ons.",
      "Reichweite im Ruhrgebiet (Dortmund), die Branche (Düsseldorf), das Geld (München) und der "
      "Lärm (Berlin). Zusammen decken sie den Nordwesten, den Süden und die Hauptstadt ab — und "
      "liegen alle eine Tagesfahrt voneinander und von uns entfernt.")),
    (("Can I just walk in?", "Kan ik gewoon binnenlopen?", "Kann ich einfach reinkommen?"),
     ("Yes. Everything during opening hours is free to walk into. Opening nights, the masterclass "
      "and the closing party are RSVP, and the guest list opens in March 2027.",
      "Ja. Alles tijdens openingstijden is vrij toegankelijk. Openingsavonden, de masterclass en "
      "het slotfeest zijn op uitnodiging; de gastenlijst opent in maart 2027.",
      "Ja. Alles während der Öffnungszeiten ist frei zugänglich. Eröffnungsabende, die Masterclass "
      "und die Abschlussparty laufen über Anmeldung; die Gästeliste öffnet im März 2027.")),
    (("Do you sell the whole collection there?", "Verkopen jullie daar de hele collectie?",
      "Verkauft ihr dort die ganze Kollektion?"),
     ("No. A curated rail per city plus one numbered city drop. The full collection stays online, "
      "and the room stays a room instead of a warehouse.",
      "Nee. Een samengesteld rek per stad plus één genummerde citydrop. De volledige collectie "
      "blijft online, en de ruimte blijft een ruimte in plaats van een magazijn.",
      "Nein. Eine kuratierte Stange pro Stadt plus ein nummerierter City-Drop. Die ganze Kollektion "
      "bleibt online, und der Raum bleibt ein Raum statt ein Lager.")),
    (("How do creators get involved?", "Hoe doen creators mee?", "Wie machen Creator mit?"),
     ("Through the form below or through management. We cover travel and hotel, we pay a fee for "
      "a confirmed appearance, and we never ask to see the content before it goes up.",
      "Via het formulier hieronder of via management. Wij betalen reis en hotel, we vergoeden een "
      "bevestigd optreden, en we vragen nooit om de content vooraf te zien.",
      "Über das Formular unten oder über das Management. Wir übernehmen Reise und Hotel, zahlen ein "
      "Honorar für bestätigte Auftritte und wollen den Content nie vorab sehen.")),
]


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------
def nav_markup():
    """Zelfde header/drawers als about.html, zodat js/app.js blijft werken."""
    return """
<header class="hdr">
  <div class="hdr__inner">
    <button class="menu-btn" data-open="menu">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      <span>Menu</span>
    </button>
    <a class="logo" href="index.html">BETA STORE</a>
    <div class="hdr__actions">
      <button class="icon-btn" aria-label="Zoeken" data-open="search">
        <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      </button>
      <a class="icon-btn" href="account.html" aria-label="Account">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/></svg>
      </a>
      <button class="icon-btn" aria-label="Winkelmand" data-open="cart">
        <svg viewBox="0 0 24 24"><path d="M6 7h12l-1 13H7L6 7z"/><path d="M9 7V5a3 3 0 016 0v2"/></svg>
        <span class="cart-count" data-cart-count>0</span>
      </button>
    </div>
  </div>
</header>

<div class="drawer" id="menu" hidden>
  <div class="drawer__panel drawer__panel--nav">
    <div class="drawer__head"><strong>Menu</strong><button class="icon-btn" data-close>&times;</button></div>
    <nav class="drawer__nav"><a class="drawer__top" href="index.html">Home</a><details><summary>Dames</summary><div class="drawer__sub"><a href="collection.html?c=dames"><strong>Alles in Dames</strong></a><a href="collection.html">Jassen</a><a href="collection.html">Truien &amp; vesten</a><a href="collection.html">Tops &amp; blouses</a><a href="collection.html">Jurken &amp; rokken</a><a href="collection.html">Broeken</a><a href="collection.html">Jeans</a><a href="collection.html">Tassen</a><a href="collection.html">Schoenen</a></div></details><details><summary>Heren</summary><div class="drawer__sub"><a href="collection.html?c=heren"><strong>Alles in Heren</strong></a><a href="collection.html">Jassen</a><a href="collection.html">Truien &amp; vesten</a><a href="collection.html">Overhemden</a><a href="collection.html">T-shirts</a><a href="collection.html">Broeken</a><a href="collection.html">Jeans</a><a href="collection.html">Tassen</a><a href="collection.html">Schoenen</a></div></details><a class="drawer__top" href="brands.html">Merken</a><a class="drawer__top" href="collection.html?c=sale">Sale</a><a class="drawer__top" href="stores.html">Winkels</a><a class="drawer__top is-active" href="event.html">Pop-up Tour</a><a class="drawer__top" href="about.html">Over ons</a></nav>
  </div>
</div>

<div class="drawer" id="search" hidden>
  <div class="drawer__panel drawer__panel--top">
    <div class="drawer__head"><strong>Zoeken</strong><button class="icon-btn" data-close>&times;</button></div>
    <input class="search-input" type="search" placeholder="Zoek op product of merk..." data-search-input>
    <div class="search-results" data-search-results><p class="muted">Begin met typen om de testcatalogus te doorzoeken.</p></div>
  </div>
</div>

<div class="drawer" id="cart" hidden>
  <div class="drawer__panel drawer__panel--right">
    <div class="drawer__head"><strong>Winkelmand</strong><button class="icon-btn" data-close>&times;</button></div>
    <div class="cart-lines" data-cart-lines></div>
    <div class="cart-foot">
      <div class="cart-total"><span>Subtotaal</span><span data-cart-total>&euro;0,00</span></div>
      <p class="muted small">Betaomgeving &mdash; afrekenen is uitgeschakeld.</p>
      <a class="btn btn--block" href="cart.html">Naar winkelmand</a>
    </div>
  </div>
</div>
"""


FOOTER = """
<footer class="ftr">
  <div class="ftr__grid">
    <div><h4>Klantenservice</h4>
      <a href="#">Verzending</a><a href="#">Retourneren</a><a href="#">Maattabel</a>
      <a href="#">Veelgestelde vragen</a><a href="#">Contact</a></div>
    <div><h4>Shoppen</h4>
      <a href="collection.html?c=dames">Dames</a><a href="collection.html?c=heren">Heren</a>
      <a href="brands.html">Merken</a><a href="collection.html?c=sale">Sale</a>
      <a href="#">Cadeaubon</a></div>
    <div><h4>Over</h4>
      <a href="about.html">Over ons</a><a href="stores.html">Onze winkels</a>
      <a href="event.html">Pop-up Tour</a><a href="#">Werken bij</a><a href="#">Privacy</a></div>
    <div class="ftr__news"><h4>Nieuwsbrief</h4>
      <p class="muted small">Placeholder-formulier &mdash; verstuurt niets.</p>
      <form class="news" onsubmit="return false;">
        <input type="email" placeholder="jouw@email.nl" required>
        <button class="btn" type="submit">Aanmelden</button>
      </form>
      <div class="pay"><span>iDEAL</span><span>Klarna</span><span>PayPal</span><span>Visa</span></div>
    </div>
  </div>
  <div class="ftr__bar">
    <span>&copy; 2026 BETA STORE &mdash; Concept store testomgeving</span>
    <span>Prijzen incl. btw &bull; Geen offici&euml;le shop</span>
  </div>
</footer>
"""


def build():
    S = []
    add = S.append

    # ---------------- hero
    add('<section class="tour-hero">')
    add('  <img class="tour-hero__bg" src="img/tour/hero.jpg" alt="">')
    add('  <div class="tour-hero__inner">')
    add('    ' + el("p", "hero.eyebrow", *HERO["eyebrow"], cls="tour-eyebrow"))
    add('    <h1 class="tour-title">ROUTE <span>NINE</span></h1>')
    add('    ' + el("p", "hero.sub", *HERO["sub"], cls="tour-sub"))
    add('    ' + el("p", "hero.lede", *HERO["lede"], cls="tour-lede"))
    add('    <div class="tour-cities">Dortmund <i>/</i> Düsseldorf <i>/</i> München <i>/</i> Berlin</div>')
    add('    <div class="tour-cta">')
    add('      ' + el("a", "cta.guestlist", "Join the guest list", "Op de gastenlijst",
                      "Auf die Gästeliste", cls="btn btn--light", attrs='href="#rsvp"'))
    add('      ' + el("a", "cta.space", "We need a space", "Wij zoeken ruimte",
                      "Wir suchen Fläche", cls="btn btn--outline-light", attrs='href="#space"'))
    add('    </div>')
    add('    ' + el("p", "hero.status", *HERO["status"], cls="tour-status"))
    add('  </div>')
    add('</section>')

    # ---------------- stats
    add('<section class="tour-stats">')
    for i, (num, lab) in enumerate(STATS):
        k = tx(f"stat.{i}", *lab)
        add(f'  <div class="tour-stat"><strong>{num}</strong>'
            f'<span data-i18n="{k}">{esc(lab[0])}</span></div>')
    add('</section>')

    add('<div class="tour-page">')

    # ---------------- idee
    add('<section class="tour-section" id="idea">')
    add('  ' + el("p", "idea.eyebrow", "The idea", "Het idee", "Die Idee", cls="tour-eyebrow"))
    add('  ' + el("h2", "idea.h", "We are not opening a shop. We are going on tour.",
                  "We openen geen winkel. We gaan op tournee.",
                  "Wir eröffnen keinen Laden. Wir gehen auf Tour.", cls="tour-h2"))
    add('  <div class="idea-grid">')
    for i, (head, body) in enumerate(IDEA):
        add('    <article class="idea-card">')
        add('      ' + el("h3", f"idea.{i}.h", *head))
        add('      ' + el("p", f"idea.{i}.p", *body))
        add('    </article>')
    add('  </div>')
    add('  ' + el("blockquote", "idea.quote", *QUOTE, cls="tour-quote"))
    add('</section>')

    # ---------------- route
    add('<section class="tour-section" id="route">')
    add('  ' + el("p", "route.eyebrow", "The route", "De route", "Die Route", cls="tour-eyebrow"))
    add('  ' + el("h2", "route.h", "Four stops, back to back, April to July 2027",
                  "Vier stops, aaneengesloten, april tot juli 2027",
                  "Vier Stopps, direkt hintereinander, April bis Juli 2027", cls="tour-h2"))
    add('  ' + el("p", "route.sub",
                  "Two weeks open, four days to build, three days to strike and drive. "
                  "Same crew, same van, a different city every fortnight.",
                  "Twee weken open, vier dagen opbouwen, drie dagen afbreken en rijden. "
                  "Dezelfde crew, hetzelfde busje, elke twee weken een andere stad.",
                  "Zwei Wochen offen, vier Tage Aufbau, drei Tage Abbau und Fahrt. Dieselbe Crew, "
                  "derselbe Transporter, alle zwei Wochen eine andere Stadt.",
                  cls="tour-lede-dark"))

    for c in CITIES:
        p = f'city.{c["n"]}'
        add('  <article class="stop">')
        add(f'    <div class="stop__media"><img src="{c["img"]}" alt="{c["city"]}" loading="lazy">')
        add(f'      <span class="stop__num">{c["n"]}</span></div>')
        add('    <div class="stop__body">')
        add(f'      <div class="stop__head"><h3>{c["city"]}</h3>'
            + el("span", p + ".badge", *c["badge"], cls="stop__badge") + '</div>')
        add('      <div class="stop__meta">'
            + el("span", p + ".dates", *c["dates"], cls="stop__dates")
            + el("span", p + ".days", *c["days"], cls="stop__days") + '</div>')
        add('      ' + el("p", p + ".hook", *c["hook"], cls="stop__hook"))
        add('      <dl class="stop__specs">')
        for field, label in (("district", ("District", "Wijk", "Viertel")),
                             ("space", ("Space", "Ruimte", "Fläche"))):
            lk = tx(f"{p}.{field}.l", *label)
            add(f'        <dt data-i18n="{lk}">{esc(label[0])}</dt>'
                + el("dd", f"{p}.{field}", *c[field]))
        add('      </dl>')
        add('      ' + el("p", p + ".night", *c["night"], cls="stop__night"))
        add('      ' + el("p", p + ".note", *c["note"], cls="stop__note"))
        add('    </div>')
        add('  </article>')
    add('</section>')

    # ---------------- format
    add('<section class="tour-section" id="format">')
    add('  ' + el("p", "fmt.eyebrow", "Inside the space", "In de ruimte", "In der Fläche",
                  cls="tour-eyebrow"))
    add('  ' + el("h2", "fmt.h", "Six things in every room, in every city",
                  "Zes dingen in elke ruimte, in elke stad",
                  "Sechs Dinge in jedem Raum, in jeder Stadt", cls="tour-h2"))
    add('  <div class="fmt-grid">')
    for i, ((num, en_t, nl_t, de_t), body) in enumerate(FORMAT):
        add('    <article class="fmt-card">')
        add(f'      <span class="fmt-card__num">{num}</span>')
        add('      ' + el("h3", f"fmt.{i}.h", en_t, nl_t, de_t))
        add('      ' + el("p", f"fmt.{i}.p", *body))
        add('    </article>')
    add('  </div>')
    add('  <div class="fmt-media">')
    add('    <figure><img src="img/tour/scentbar.jpg" alt="" loading="lazy">'
        + el("figcaption", "fmt.cap1", "The scent bar — 48 bottles, blind, scored on a card.",
             "De geurbar — 48 flacons, blind, gescoord op een kaart.",
             "Die Duftbar — 48 Flakons, blind, auf einer Karte bewertet.") + '</figure>')
    add('    <figure><img src="img/tour/studio.jpg" alt="" loading="lazy">'
        + el("figcaption", "fmt.cap2",
             "Studio Nine — lit, free, and off limits to our marketing team.",
             "Studio Nine — uitgelicht, gratis, en verboden terrein voor onze marketingafdeling.",
             "Studio Nine — ausgeleuchtet, kostenlos und für unser Marketing tabu.") + '</figure>')
    add('  </div>')
    add('</section>')

    # ---------------- line-up
    add('<section class="tour-section" id="lineup">')
    add('  ' + el("p", "line.eyebrow", "The line-up", "De line-up", "Das Line-up",
                  cls="tour-eyebrow"))
    add('  ' + el("h2", "line.h", "Who we are going after",
                  "Wie we willen hebben", "Wen wir wollen", cls="tour-h2"))
    add('  <div class="wishlist-warn">'
        + el("strong", "line.warn.t", "Wishlist, not a line-up.",
             "Wenslijst, geen line-up.", "Wunschliste, kein Line-up.")
        + el("span", "line.warn.b",
             " Nobody on this page has been contacted, let alone booked. These are the names we "
             "want and the order we want them in. Approaches go out through management from "
             "December 2026. Follower counts are public figures from autumn 2026 and move "
             "constantly.",
             " Niemand op deze pagina is benaderd, laat staan geboekt. Dit zijn de namen die we "
             "willen en de volgorde waarin we ze willen. Benaderingen gaan vanaf december 2026 via "
             "management. Volgersaantallen zijn openbare cijfers uit het najaar van 2026 en "
             "bewegen continu.",
             " Niemand auf dieser Seite wurde kontaktiert, geschweige denn gebucht. Das sind die "
             "Namen, die wir wollen, und die Reihenfolge, in der wir sie wollen. Anfragen gehen ab "
             "Dezember 2026 über das Management raus. Followerzahlen sind öffentliche Angaben aus "
             "dem Herbst 2026 und ändern sich ständig.") + '</div>')

    for ti, (title, intro, people) in enumerate(LINEUP_TIERS):
        add('  <div class="tier">')
        add('    ' + el("h3", f"line.t{ti}.h", *title, cls="tier__title"))
        add('    ' + el("p", f"line.t{ti}.p", *intro, cls="tier__intro"))
        add('    <div class="tier__grid">')
        for pi, (name, meta, blurb) in enumerate(people):
            add('      <article class="person">')
            add(f'        <h4>{esc(name)}</h4>')
            add(f'        <span class="person__meta">{esc(meta)}</span>')
            add('        ' + el("p", f"line.t{ti}.p{pi}", *blurb))
            add('        ' + el("span", f"line.t{ti}.s{pi}", "Invite planned",
                                "Uitnodiging gepland", "Einladung geplant",
                                cls="person__status"))
            add('      </article>')
        add('    </div>')
        add('  </div>')

    add('  <div class="offer">')
    add('    ' + el("h3", "offer.h", "What a creator actually gets",
                    "Wat een creator echt krijgt", "Was ein Creator wirklich bekommt"))
    add('    <ul>')
    for i, item in enumerate(CREATOR_OFFER):
        add('      ' + el("li", f"offer.{i}", *item))
    add('    </ul>')
    add('  </div>')
    add('</section>')

    # ---------------- weekritme
    add('<section class="tour-section" id="rhythm">')
    add('  ' + el("p", "week.eyebrow", "The rhythm", "Het ritme", "Der Rhythmus",
                  cls="tour-eyebrow"))
    add('  ' + el("h2", "week.h", "One week in a pop-up", "Eén week in een pop-up",
                  "Eine Woche im Pop-up", cls="tour-h2"))
    add('  <div class="week">')
    for i, (day, hours, what) in enumerate(WEEK):
        dk = tx(f"week.{i}.d", *day)
        hk = tx(f"week.{i}.h", *hours)
        add(f'    <div class="week__row"><span class="week__day" data-i18n="{dk}">{esc(day[0])}</span>'
            f'<span class="week__hours" data-i18n="{hk}">{esc(hours[0])}</span>'
            + el("span", f"week.{i}.w", *what, cls="week__what") + '</div>')
    add('  </div>')
    add('</section>')

    # ---------------- cijfers
    add('<section class="tour-section" id="numbers">')
    add('  ' + el("p", "num.eyebrow", "The numbers", "De cijfers", "Die Zahlen",
                  cls="tour-eyebrow"))
    add('  ' + el("h2", "num.h", "What we are aiming at", "Waar we op mikken",
                  "Worauf wir zielen", cls="tour-h2"))
    add('  ' + el("p", "num.sub", "Targets, not promises. If we hit two thirds of this, tour two "
                  "happens in 2028.",
                  "Doelen, geen beloftes. Halen we twee derde, dan komt tour twee er in 2028.",
                  "Ziele, keine Versprechen. Schaffen wir zwei Drittel, kommt Tour zwei 2028.",
                  cls="tour-lede-dark"))
    add('  <div class="target-grid">')
    for i, (num, lab) in enumerate(TARGETS):
        k = tx(f"target.{i}", *lab)
        add(f'    <div class="target"><strong>{num}</strong>'
            f'<span data-i18n="{k}">{esc(lab[0])}</span></div>')
    add('  </div>')

    add('  ' + el("h3", "budget.h", "Indicative budget", "Indicatief budget",
                  "Indikatives Budget", cls="budget-h"))
    add('  <table class="budget"><tbody>')
    for i, (lab, amount) in enumerate(BUDGET):
        k = tx(f"budget.{i}", *lab)
        add(f'    <tr><td data-i18n="{k}">{esc(lab[0])}</td><td>{amount}</td></tr>')
    add('    <tr class="budget__total"><td>'
        + f'<span data-i18n="{tx("budget.total", "Total, indicative", "Totaal, indicatief", "Gesamt, indikativ")}">Total, indicative</span>'
        + '</td><td>≈ €219,000</td></tr>')
    add('  </tbody></table>')
    add('  ' + el("p", "budget.note",
                  "Placeholder figures for the planning conversation — not a quote. Rent is the "
                  "number that moves most; a Berlin ground floor in July can swing it by €15,000 "
                  "on its own.",
                  "Placeholdercijfers voor het planningsgesprek — geen offerte. De huur beweegt het "
                  "meest; een Berlijnse begane grond in juli kan er in zijn eentje €15.000 "
                  "bijgooien.",
                  "Platzhalterzahlen für das Planungsgespräch — kein Angebot. Die Miete bewegt sich "
                  "am stärksten; ein Berliner Erdgeschoss im Juli kann allein 15.000 € ausmachen.",
                  cls="muted small"))
    add('</section>')

    # ---------------- ruimte
    add('<section class="tour-section tour-section--blue" id="space">')
    add('  ' + el("p", "space.eyebrow", "For landlords and agents",
                  "Voor verhuurders en makelaars", "Für Vermieter und Makler",
                  cls="tour-eyebrow"))
    add('  ' + el("h2", "space.h", "This is the space we are looking for",
                  "Dit is de ruimte die we zoeken", "Das ist die Fläche, die wir suchen",
                  cls="tour-h2"))
    add('  <ul class="space-list">')
    for i, item in enumerate(SPACE_BRIEF):
        add('    ' + el("li", f"space.{i}", *item))
    add('  </ul>')
    add('  <div class="tour-cta">'
        + el("a", "space.cta", "Send us a space", "Stuur ons een ruimte",
             "Schick uns eine Fläche", cls="btn btn--light", attrs='href="#rsvp"') + '</div>')
    add('</section>')

    # ---------------- roadmap
    add('<section class="tour-section" id="roadmap">')
    add('  ' + el("p", "road.eyebrow", "The road to opening", "De weg naar de opening",
                  "Der Weg zur Eröffnung", cls="tour-eyebrow"))
    add('  ' + el("h2", "road.h", "From this page to a queue in Dortmund",
                  "Van deze pagina naar een rij in Dortmund",
                  "Von dieser Seite zur Schlange in Dortmund", cls="tour-h2"))
    add('  <ol class="road">')
    for i, (when, what) in enumerate(ROADMAP):
        wk = tx(f"road.{i}.w", *when)
        add(f'    <li><span class="road__when" data-i18n="{wk}">{esc(when[0])}</span>'
            + el("span", f"road.{i}.t", *what, cls="road__what") + '</li>')
    add('  </ol>')
    add('</section>')

    # ---------------- partners
    add('<section class="tour-section" id="partners">')
    add('  ' + el("p", "part.eyebrow", "Partners", "Partners", "Partner", cls="tour-eyebrow"))
    add('  ' + el("h2", "part.h", "Three ways to stand in the room with us",
                  "Drie manieren om met ons in de ruimte te staan",
                  "Drei Wege, mit uns im Raum zu stehen", cls="tour-h2"))
    add('  <div class="partner-grid">')
    for i, (name, slots, body) in enumerate(PARTNERS):
        add('    <article class="partner">')
        add('      ' + el("h3", f"part.{i}.h", *name))
        add('      ' + el("span", f"part.{i}.s", *slots, cls="partner__slots"))
        add('      ' + el("p", f"part.{i}.p", *body))
        add('    </article>')
    add('  </div>')
    add('</section>')

    # ---------------- faq
    add('<section class="tour-section" id="faq">')
    add('  ' + el("p", "faq.eyebrow", "Questions", "Vragen", "Fragen", cls="tour-eyebrow"))
    add('  ' + el("h2", "faq.h", "The ones everybody asks first",
                  "Die iedereen als eerste stelt", "Die alle zuerst stellen", cls="tour-h2"))
    add('  <div class="faq">')
    for i, (q, a) in enumerate(FAQ):
        qk = tx(f"faq.{i}.q", *q)
        add(f'    <details><summary data-i18n="{qk}">{esc(q[0])}</summary>'
            + el("p", f"faq.{i}.a", *a) + '</details>')
    add('  </div>')
    add('</section>')

    # ---------------- rsvp
    add('<section class="tour-section rsvp" id="rsvp">')
    add('  ' + el("p", "rsvp.eyebrow", "Stay close", "Blijf dichtbij", "Bleib dran",
                  cls="tour-eyebrow"))
    add('  ' + el("h2", "rsvp.h", "Guest list, creators, partners, spaces",
                  "Gastenlijst, creators, partners, ruimtes",
                  "Gästeliste, Creator, Partner, Flächen", cls="tour-h2"))
    add('  ' + el("p", "rsvp.p",
                  "One form for all four. Tell us which city you are in and what you want to do "
                  "there — we read every one of these ourselves.",
                  "Eén formulier voor alle vier. Zeg in welke stad je zit en wat je daar wilt doen "
                  "— we lezen ze allemaal zelf.",
                  "Ein Formular für alle vier. Sag uns, in welcher Stadt du bist und was du dort "
                  "machen willst — wir lesen jede Zuschrift selbst.", cls="tour-lede-dark"))
    add('  <form class="rsvp-form" onsubmit="return false;">')
    add(f'    <input type="text" placeholder="Name" data-i18n-ph="{tx("rsvp.ph.name", "Name", "Naam", "Name")}" required>')
    add(f'    <input type="email" placeholder="Email" data-i18n-ph="{tx("rsvp.ph.mail", "Email", "E-mail", "E-Mail")}" required>')
    add('    <select>')
    for v, (en_o, nl_o, de_o) in [
        ("guest", ("I want to visit", "Ik wil langskomen", "Ich will vorbeikommen")),
        ("creator", ("I am a creator", "Ik ben creator", "Ich bin Creator")),
        ("partner", ("I want to partner", "Ik wil partner worden", "Ich will Partner werden")),
        ("space", ("I have a space", "Ik heb een ruimte", "Ich habe eine Fläche")),
        ("press", ("Press", "Pers", "Presse"))]:
        k = tx(f"rsvp.opt.{v}", en_o, nl_o, de_o)
        add(f'      <option value="{v}" data-i18n="{k}">{esc(en_o)}</option>')
    add('    </select>')
    add('    <select>')
    for v, (en_o, nl_o, de_o) in [
        ("all", ("Any city", "Alle steden", "Alle Städte")),
        ("dortmund", ("Dortmund", "Dortmund", "Dortmund")),
        ("dusseldorf", ("Düsseldorf", "Düsseldorf", "Düsseldorf")),
        ("munich", ("München", "München", "München")),
        ("berlin", ("Berlin", "Berlijn", "Berlin"))]:
        k = tx(f"rsvp.city.{v}", en_o, nl_o, de_o)
        add(f'      <option value="{v}" data-i18n="{k}">{esc(en_o)}</option>')
    add('    </select>')
    add('    ' + el("button", "rsvp.send", "Put me on the list", "Zet me op de lijst",
                    "Setz mich auf die Liste", cls="btn", attrs='type="submit"'))
    add('  </form>')
    add('  ' + el("p", "rsvp.note",
                  "Placeholder form — nothing is sent anywhere yet. Until it is wired up, mail "
                  "tour@numbernine.example.",
                  "Placeholderformulier — er wordt nog niets verstuurd. Tot het werkt: mail "
                  "tour@numbernine.example.",
                  "Platzhalter-Formular — es wird noch nichts versendet. Bis dahin: Mail an "
                  "tour@numbernine.example.", cls="muted small"))
    add('</section>')

    add('</div>')  # /tour-page
    return "\n".join(S)


def page_html(body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="description" content="ROUTE NINE — the Number Nine pop-up tour through Dortmund, Düsseldorf, Munich and Berlin, spring and summer 2027.">
<title>ROUTE NINE | Pop-up Tour Germany 2027</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2032%2032%22%3E%3Crect%20width%3D%2232%22%20height%3D%2232%22%20fill%3D%22%2315130f%22/%3E%3Ctext%20x%3D%2216%22%20y%3D%2222%22%20text-anchor%3D%22middle%22%20font-family%3D%22Helvetica%2CArial%22%20font-size%3D%2217%22%20font-weight%3D%22700%22%20fill%3D%22%23ffffff%22%3EB%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
{nav_markup()}
<main id="main">
{body}
</main>
{FOOTER}
<script src="js/data.js"></script>
<script src="js/tour-i18n.js"></script>
<script src="js/i18n.js"></script>
<script src="js/app.js"></script>
</body>
</html>
"""


if __name__ == "__main__":
    body = build()
    (ROOT / "event.html").write_text(page_html(body), encoding="utf-8")
    (ROOT / "js" / "tour-i18n.js").write_text(
        "/* Gegenereerd door build_tour.py — niet handmatig bewerken. */\n"
        "window.__TOUR_I18N__ = " + json.dumps(TX, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    print(f"event.html geschreven ({len(body.splitlines())} regels body)")
    print(f"js/tour-i18n.js geschreven ({len(TX)} keys × 3 talen)")
