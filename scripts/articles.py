"""Regionale fagartikler. Fakta er hentet fra FHIs Skadedyrhåndbok og andre lenkede kilder.
Bygges av scripts/page.py til site/artikler/<slug>.html."""

FHI = "https://fhi.no/sk/skadedyrhandboka"

ARTICLES = [
{
 "slug": "rotter-i-byen", "regions": ["ost", "vest"], "cat": "Gnagere", "min": 5, "img": "rotte",
 "title": "Rotter i byen: hva er ditt ansvar, og hva gjør kommunen?",
 "lead": "Ser du en rotte i hagen eller bakgården, er det huseier eller beboer som må ta tak i det. Slik forebygger du – og slik vet du når det er på tide å ringe en fagperson.",
 "body": """
<h2>Brunrotta lever der vi lever</h2>
<p>Brunrotta er den vanligste rotta i Norge. Den er hovedsakelig aktiv om natten, og som andre gnagere har den store, krumme fortenner som vokser hele livet. De er sterke nok til å gnage gjennom treverk, plast, aluminiumsbeslag og porøs betong.</p>
<p>Rottene blir kjønnsmodne allerede ved to–tre måneders alder. Med god tilgang på mat kan de få flere kull i året, og ser du én rotte, er det trolig flere i nærheten.</p>
<h2>Hvem har ansvaret?</h2>
<p>På privat eiendom er det huseier eller beboer som har ansvaret for å forebygge og bekjempe rotter. Kommunen tilbyr som regel ikke bekjempelse på privat eiendom, men miljørettet helsevern i kommunen kan gi råd.</p>
<div class="box"><b>Tommelfingerregel</b>Et rotteproblem skyldes nesten alltid at dyrene har god tilgang på mat, vann og skjul. Fjern det, så fjerner du grunnlaget.</div>
<h2>Slik forebygger du</h2>
<ul>
<li>Hold avfallsbeholdere lukket, og ikke la sekker stå på bakken.</li>
<li>Ikke mat fugler på bakken – bruk fôrbrett eller heng opp maten.</li>
<li>Ikke la mat til katt, hund eller kanin stå ute.</li>
<li>Tett sprekker og åpninger rundt rør og avløp, og sørg for at dører slutter tett.</li>
<li>Rydd bort ved, materialer og kratt inntil husveggen der rotter kan gjemme seg.</li>
</ul>
<h2>Rotter er sky for det nye</h2>
<p>Brunrotter kan være redde for ukjent mat, nye gjenstander og fremmede lukter. Det kalles neofobi, og det er en av grunnene til at rotter er vanskeligere å bekjempe enn mus. Feller kan bli stående urørt i dager før de virker.</p>
<h2>Når bør du ringe en fagperson?</h2>
<p>Ser du rotter innendørs, finner du ekskrementer på én til to centimeter, eller kommer problemet tilbake etter at du har tettet og ryddet, bør du kontakte en skadedyrbekjemper. For å drive ervervsmessig skadedyrbekjempelse kreves det godkjenning i Norge.</p>
""",
 "prod": ("Feller og tetting mot rotter", "Rottefeller, åtestasjoner til proffbruk og tettematerialer.", "gnagere"),
 "sources": [("FHI: Brunrotte", f"{FHI}/gnagere/brunrotte"), ("Asker kommune: Spørsmål om skadedyr", "https://www.asker.kommune.no/helse-og-omsorg/miljorettet-helsevern/sporsmal-om-skadedyr/"),
             ("FHI: Skadedyr – håndbok for helsepersonell", "https://fhi.no/sm/smittevernhandboka/temakapitler/skadedyr")]},
{
 "slug": "flatt-langs-kysten", "regions": ["ost", "sor"], "cat": "Flått", "min": 4, "img": "region-sor",
 "title": "Flått langs kysten: sjekk deg selv etter turen",
 "lead": "Skogflåtten trives i kystnære strøk med løvskog og kratt. På Sørlandet og rundt Oslofjorden finnes også skogflåttencefalitt (TBE). Slik beskytter du deg.",
 "body": """
<h2>Hvor finnes flåtten?</h2>
<p>I Norge finnes skogflått langs kysten fra svenskegrensen i Østfold og nord til Bodø i Nordland. Den trives best i kyst- og dalområder med løvskog, kratt og frodig undervegetasjon, der vintrene ikke er for lange og kalde. Forekomsten kan variere mye, også innenfor samme kommune.</p>
<p>Flåtten er aktiv fra april til november, og den blir aktiv når lufttemperaturen er over sju–åtte grader.</p>
<h2>Skogflåttencefalitt på Sørlandet og rundt Oslofjorden</h2>
<p>Skogflåttencefalitt (TBE) er påvist langs kysten fra Flekkefjord til gamle Hurum kommune og langs østsiden av Oslofjorden fra Vestby til svenskegrensen. Folkehelseinstituttet anbefaler at de som ofte blir bitt av flått i disse områdene, vurderer TBE-vaksine. Snakk med legen eller apoteket om det gjelder deg.</p>
<div class="box"><b>Viktigste råd</b>Det beste vernet er å unngå å bli bitt: dekk til bar hud i flåttområder, og sjekk kroppen etter turen.</div>
<h2>Slik unngår du flåttbitt</h2>
<ul>
<li>Bruk lange bukser og lukkede sko i høyt gress og kratt.</li>
<li>Insektmiddel på hud og klær kan redusere antall flått som fester seg.</li>
<li>Sjekk hele kroppen etter turen, også i hårfestet, bak ørene og i knehasene.</li>
<li>Dusj etter opphold i områder med mye flått.</li>
<li>Hold gresset kort rundt huset og hytta, særlig der barn leker.</li>
</ul>
<h2>Har du fått flått?</h2>
<p>Fjern flåtten så raskt som mulig med en pinsett eller flåttfjerner. Følg med på bittstedet de neste ukene, og kontakt lege hvis du får et rødt utslett som brer seg, eller blir syk.</p>
""",
 "prod": ("Utstyr mot flått", "Flåttfjernere og verneutstyr til tur og hage.", "hus-og-hage"),
 "sources": [("FHI: Skogflåttencefalitt – håndbok for helsepersonell", "https://www.fhi.no/sm/smittevernveilederen/sykdommer-a-a/skogflattencefalitt-tbe-virusinfeks/"),
             ("FHI: Skogflåttencefalittvaksine (TBE-vaksine)", "https://www.fhi.no/va/voksenvaksinasjon/skogflattencefalittvaksine-tbe-vaksine"),
             ("FHI: Lyme borreliose – håndbok for helsepersonell", "https://www.fhi.no/sm/smittevernveilederen/sykdommer-a-a/lyme-borreliose---veileder-for-hels/")]},
{
 "slug": "stokkmaur-eller-skogsmaur", "regions": ["ost", "midt"], "cat": "Maur", "min": 4, "img": "maur",
 "title": "Stokkmaur eller skogsmaur? Slik ser du forskjellen",
 "lead": "Store maur inne i huset eller hytta kan bety stokkmaur, som gnager ut reir i treverk. Men ofte er det ufarlig skogsmaur. To kjennetegn avgjør.",
 "body": """
<h2>Se på hodet og ryggen</h2>
<p>Stokkmaur har helt svart hode og jevnt krummet rygg. Rød skogsmaur har tofarget hode – rødt og svart – og humpete rygg. Arbeiderne hos rød skogsmaur er 4,5–9 millimeter lange.</p>
<div class="box"><b>Pirketesten</b>Pirker du borti en levende rød skogsmaur, bøyer den bakkroppen inn mellom beina og spruter maursyre. Det gjør ikke stokkmauren.</div>
<h2>Hvorfor stokkmaur er et problem</h2>
<p>Skaden kommer når stokkmauren gnager ut tre eller isolasjon for å lage reir. Ser du stokkmaur innendørs, kan det bety at samfunnet ligger i bygningen. Antall bekjempelser av stokkmaur i Norge har ligget stabilt, rundt tusen i året de siste årene.</p>
<h2>Små svarte maur på kjøkkenbenken</h2>
<p>De små, helsvarte mauren som lager travle maurstier mot søt mat, er som regel svart jordmaur. De er tre–fem millimeter lange og kommer ofte inn om våren på jakt etter mat. Slike tilfeldige gjester trenger du ikke å bekjempe, men tørk opp søl og tett der de kommer inn.</p>
<h2>Hva gjør du?</h2>
<ul>
<li>Studer maurene: hvor går de, og når er de mest aktive? Det er nyttig informasjon for en skadedyrbekjemper.</li>
<li>Se etter sagflisaktig gnag ved vegger, karmer og takbjelker.</li>
<li>Stokkmaur kan være vanskelige å bekjempe, så kontakt gjerne et skadedyrfirma.</li>
</ul>
""",
 "prod": ("Mot maur", "Åte og utstyr mot maur innendørs.", "insekter"),
 "sources": [("FHI: Stokkmaur", f"{FHI}/maur/stokkmaur"), ("FHI: Rød skogsmaur", "https://www.fhi.no/sk/skadedyrveilederen/maur/rod-skogsmaur/"),
             ("FHI: Svart jordmaur", "https://www.fhi.no/nettpub/skadedyrveilederen/maur/svart-jordmaur/"), ("FHI: Statistikk om skadedyr", "https://fhi.no/tema/skadedyr/statistikk")]},
{
 "slug": "husbukk", "regions": ["sor"], "cat": "Treskadedyr", "min": 4, "img": "region-sor",
 "title": "Husbukk langs kysten av Telemark og Agder: tegn du ser etter",
 "lead": "Husbukken er en stor bille som spiser tørt treverk i bygninger. Den har en flekkvis utbredelse i Sør-Norge, og angrepene utvikler seg sakte over mange år.",
 "body": """
<h2>Hva er husbukk?</h2>
<p>Husbukken er en avlang, relativt stor bille med lange antenner. Voksne biller er 8–20 millimeter lange og lever bare et par uker. Det er larvene som gjør skaden: de lever av tørt bartrevirke, og en fullvoksen larve er opptil 25 millimeter lang.</p>
<p>Husbukken har en flekkvis utbredelse i Sør-Norge og er knyttet til bebyggelse. Ifølge FHI er bekjempelsene særlig konsentrert langs kysten av Telemark og Agder. Det utføres under hundre bekjempelser i året, men de kan være arbeidskrevende.</p>
<h2>Slik kjenner du igjen spor etter husbukk</h2>
<ul>
<li>Ovale flygehull med litt flisete kant, omtrent 5–8 millimeter brede og 3–4 millimeter høye.</li>
<li>Boremel fra gangene inne i treverket.</li>
<li>Angrepet sitter i splintveden. Husbukk kan ikke gnage i kjerneved.</li>
</ul>
<div class="box"><b>Ikke forveksle med blåbukk</b>Blåbukk lager furer i overflaten av ved med bark og gjør ingen skade utover å spise tørr bark. Spor etter blåbukk forveksles ofte med husbukk.</div>
<h2>Hva gjør du?</h2>
<p>Det kan være vanskelig å skille mellom aktive og gamle angrep. Finner du ovale flygehull i konstruksjonen, bør du få en fagperson til å vurdere om angrepet er aktivt. Angrep utvikler seg sakte fordi livssyklusen er lang, så du har tid til å gjøre det riktig.</p>
""",
 "prod": None,
 "sources": [("FHI: Husbukk", f"{FHI}/biller/husbukk"), ("FHI: Blåbukk", f"{FHI}/biller/blabukk"), ("FHI: Statistikk om skadedyr", "https://fhi.no/tema/skadedyr/statistikk")]},
{
 "slug": "vepsebol", "regions": ["sor", "midt"], "cat": "Veps", "min": 4, "img": "veps",
 "title": "Vepsebolet: fjern det tidlig i sesongen",
 "lead": "Et lite bol i mai er en helt annen jobb enn et fullt bol i august. Slik fungerer vepsesesongen – og slik tar du det trygt.",
 "body": """
<h2>Ett år, ett bol</h2>
<p>På våre breddegrader er alle stikkevepskolonier ettårige. Bare unge dronninger overvintrer, og de kommer fram fra vinterdvalen i april. Hver dronning finner et sted og begynner å bygge et nytt bol av papiraktig materiale laget av tygde trefibre. Gamle bol brukes aldri på nytt.</p>
<p>Kolonien vokser gjennom sommeren og dør ut i løpet av høsten. Det er sent på sommeren og om høsten at vepsene blir mest plagsomme, når de leter etter sukkerholdig mat. Ifølge FHIs statistikk skjer de fleste bekjempelsene i juli og august.</p>
<div class="box"><b>Tidlig er best</b>Ser du en veps som flyr inn og ut på samme sted i mai eller juni, er bolet fortsatt lite. Da er det enklest å fjerne.</div>
<h2>Kjenn igjen stikkevepsen</h2>
<p>Stikkeveps har glatt, ikke-behåret bakkropp med svarte og gule ringer. Vingene brettes på langs og ser smale ut i hvile. Arbeiderne er 11–19 millimeter lange. Stikkeveps kan stikke flere ganger, i motsetning til bier.</p>
<h2>Slik tar du det trygt</h2>
<ul>
<li>Hold avstand og ikke slå mot bolet.</li>
<li>Fjern små bol tidlig i sesongen, gjerne om kvelden når vepsene er rolige.</li>
<li>Bol inne i vegger, tak eller luftekanaler bør en fagperson ta.</li>
<li>Er du allergisk mot vepsestikk, skal du ikke fjerne bol selv.</li>
</ul>
<p>Husk at veps også gjør nytte i naturen. Et bol langt unna der folk ferdes, kan ofte bare få være.</p>
""",
 "prod": ("Mot veps", "Vepsefeller og utstyr til trygg fjerning av små bol.", "insekter"),
 "sources": [("FHI: Stikkeveps", "https://www.fhi.no/nettpub/skadedyrveilederen/veps-og-bier/stikkeveps/"), ("FHI Statistikk – Skadedyrstatistikk", "https://statistikk.fhi.no/skast/")]},
{
 "slug": "fukt-solvkre-skjeggkre", "regions": ["vest"], "cat": "Fukt", "min": 5, "img": "skjeggkre",
 "title": "Sølvkre og skjeggkre: hva er forskjellen, og hva hjelper?",
 "lead": "Sølvkre er en harmløs badegjest. Skjeggkre har spredt seg kraftig de siste årene og kan bli mange. Slik skiller du dem – og slik blir du kvitt dem.",
 "body": """
<h2>To arter som ligner</h2>
<p>Sølvkre er en vanlig gjest på baderom. Den gjør liten skade og regnes som harmløs. Skjeggkre ligner, men de voksne er større og mørkere, har lengre haletråder – den lengste er omtrent like lang som kroppen – og tydeligere behåring. Skjeggkre er mørkegrå og litt spraglete og mindre sølvglinsende enn sølvkre.</p>
<h2>Skjeggkre trives også der det er tørt</h2>
<p>Skjeggkre er nattaktive og oppdages ofte når du slår på lyset om natten. De trives best ved høy fuktighet, men klarer seg også i tørrere rom, i motsetning til sølvkre. De finnes oftest i nyere bygninger, og antallet bekjempelser økte kraftig etter 2016 før det flatet ut.</p>
<div class="box"><b>Fukt er ikke hele forklaringen</b>Mindre fukt hjelper mot sølvkre. Mot skjeggkre er det åte som virker best – tørking alene er ikke nok.</div>
<h2>Slik blir du kvitt dem</h2>
<ul>
<li>Sølvkre: reduser fuktigheten og tett sprekker. Det finnes effektive åteprodukter, så sprøytemidler er unødvendig.</li>
<li>Skjeggkre: bruk forgiftet åte som små dråper mange steder langs veggene i alle rom. Det øker sjansen for at dyrene finner åten.</li>
<li>Vær tålmodig. Skjeggkre kan være vanskelige å bli helt kvitt, og i en periode må du regne med å se noen få.</li>
<li>I blokker og rekkehus bør naboene behandle samtidig.</li>
</ul>
<p>Skjeggkre kan også haike med vesker, bager og sekker, for eksempel fra arbeidsplassen. Det gjør det vanskelig å forebygge helt.</p>
""",
 "prod": ("Mot skjeggkre og sølvkre", "Åte og limfeller til overvåking.", "insekter"),
 "sources": [("FHI: Skjeggkre", f"{FHI}/smadyr-andre/skjeggkre"), ("FHI: Sølvkre", "https://www.fhi.no/nettpub/skadedyrveilederen/smadyr-andre/solvkre-/"),
             ("FHI: Byggomfattende bekjempelse", f"{FHI}/forebygging-og-bekjempelse/byggomfattende-bekjempelse")]},
{
 "slug": "stripet-borebille", "regions": ["vest", "nord"], "cat": "Treskadedyr", "min": 4, "img": "region-vest",
 "title": "Små runde hull i treverket? Det kan være stripet borebille",
 "lead": "Stripet borebille – også kalt mit, mott eller mår – er vanligst i fuktige kyststrøk og finnes nord til og med Troms. Hullene er ofte spor etter gamle angrep.",
 "body": """
<h2>Kjenn igjen sporene</h2>
<p>De sirkelrunde hullene på én–to millimeter, som ofte sees i møbler og treverk, er bedre kjent enn billen selv. Det er flygehull der voksne biller har gnaget seg ut. Oftest er de spor etter tidligere angrep.</p>
<p>Den voksne billen er 2,5–4 millimeter lang, brun, med mange langsgående striper på dekkvingene. Larvene lever inne i treverket og blir høyst fem–seks millimeter lange.</p>
<h2>Hvor finnes den?</h2>
<p>I Norge finnes stripet borebille nord til og med Troms. Den er vanligst i kyststrøk med høy luftfuktighet. Angrepene er vanligst i kjellere, men i kyststrøk på Vestlandet kan den også finnes andre steder i huset.</p>
<div class="box"><b>Ikke forveksle</b>Myk borebille lager hull på to–tre millimeter og lever bare i bark. Råteborebille lever i råteskadet treverk og etterlater mørkt gult boremel. Stripet borebille gir mindre hull og helt lyst boremel.</div>
<h2>Er angrepet aktivt?</h2>
<ul>
<li>Ferskt, lyst boremel under hullene tyder på aktivitet.</li>
<li>Mange blågrønne, metallskinnende biller innendørs kan være et tegn på borebilleangrep – blågrønn skinkebille jakter på borebillene.</li>
<li>Lavere fuktighet i kjeller og krypkjeller gjør treverket mindre attraktivt.</li>
</ul>
<p>Er du usikker, bør en fagperson vurdere om angrepet er aktivt før du gjør tiltak.</p>
""",
 "prod": None,
 "sources": [("FHI: Stripet borebille", f"{FHI}/biller/stripet-borebille"), ("FHI: Råteborebille", "https://www.fhi.no/sk/skadedyrhandboka/biller/rateborebille/"),
             ("FHI: Myk borebille", f"{FHI}/biller/myk-borebille"), ("FHI: Blågrønn skinkebille", f"{FHI}/biller/blagronn-skinkebille")]},
{
 "slug": "mus-pa-garden", "regions": ["midt"], "cat": "Gnagere", "min": 4, "img": "region-midt",
 "title": "Mus på gården: låve, stabbur og fôrlager",
 "lead": "Der det er fôr og korn, er det mus. På gården er det ofte skogmus og klatremus som kommer inn – og de har kort vei mellom bolet og maten.",
 "body": """
<h2>Flere arter enn husmusa</h2>
<p>Husmus yngler bare innendørs her i landet. På gårder og i hytter er det ofte skogmus og klatremus som kommer inn. Klatremus finnes helt nord til nord i Nordland og kan også komme inn i bygninger.</p>
<h2>Kort aksjonsradius – sett fellene tett</h2>
<p>En skogmus har vanligvis en aksjonsradius på bare noen få meter fra bolet hvis den har nok mat rundt seg. Derfor må fellene stå tett, der du faktisk ser spor. Jo flere feller, jo bedre blir bekjempelsen.</p>
<div class="box"><b>Slik setter du fellene</b>Sett klappfeller langs veggene, på gulvet og gjerne oppe ved taket der musene ferdes, med utløseren inn mot veggen. Sett gjerne to feller ved siden av hverandre, to–tre centimeter fra hverandre.</div>
<h2>Fjern maten</h2>
<ul>
<li>Oppbevar fôr og korn i lukkede beholdere av metall eller tett plast.</li>
<li>Rydd opp søl rundt fôringsplasser.</li>
<li>Husk at åten i fellene må konkurrere med all annen mat musene har tilgang på.</li>
<li>Tett åpninger større enn seks millimeter i bygninger der du ikke vil ha mus.</li>
</ul>
<h2>Vær forsiktig med lort og urin</h2>
<p>Klatremus kan være reservoar for musepest, som kan smitte til mennesker. Bruk hansker når du rydder der det har vært mye mus, og unngå å virvle opp støv.</p>
""",
 "prod": ("Feller for gård og hytte", "Klappfeller, fleremusfeller og tettemateriell.", "gnagere"),
 "sources": [("FHI: Husmus", f"{FHI}/gnagere/husmus"), ("FHI: Klatremus", f"{FHI}/gnagere/klatremus"), ("FHI: Småskogmus", f"{FHI}/gnagere/smaskogmus")]},
{
 "slug": "smagnagerar", "regions": ["nord"], "cat": "Gnagere", "min": 4, "img": "region-nord",
 "title": "Smågnagerår: når det kryr av mus og lemen",
 "lead": "Mus og lemen svinger kraftig i antall, med topper hvert tredje–fjerde år. I toppårene øker også presset mot hytter og hus.",
 "body": """
<h2>Hvorfor svinger bestandene?</h2>
<p>Smågnagere har regelmessige svingninger med topper omtrent hvert tredje–fjerde år. Fenomenet ble først lagt merke til hos lemen, men finnes hos de fleste smågnagerarter i nordlige strøk. I Skandinavia kan toppene bre seg nordover som bølger: et toppår i Sør-Norge kan følges av et i Trøndelag året etter og i Nord-Norge året etter det.</p>
<p>Bestandene overvåkes i fjellet med kamerafeller i et nasjonalt program finansiert av Miljødirektoratet.</p>
<h2>Hva betyr det for hytta?</h2>
<p>I et toppår er det rett og slett flere mus som leter etter mat og ly når høsten kommer. En hytte som står tom over vinteren, er et ideelt vinterkvarter.</p>
<div class="box"><b>Rødmus i nord</b>Rødmus finnes over hele Nord-Norge ned til Salten i Nordland. Den kan komme inn i bygninger og være reservoar for musepest. Den ligner klatremus, men har kortere og tett behåret hale.</div>
<h2>Slik forbereder du deg</h2>
<ul>
<li>Tett åpninger større enn seks millimeter før du stenger for vinteren.</li>
<li>Fjern all mat, også i boder og uthus.</li>
<li>Sett feller tett langs veggene der du har sett spor tidligere.</li>
<li>Bruk hansker når du rydder etter mus, og unngå å virvle opp støv.</li>
</ul>
""",
 "prod": ("Feller for hytta", "Fleremusfeller og tettemateriell til vinterstengning.", "gnagere"),
 "sources": [("Store norske leksikon: Smågnagersvingninger", "https://snl.no/smågnagersvingninger"),
             ("Jeger.no / NINA: Mus og lemen kan få topper i Sør-Norge", "https://www.jeger.no/jakt-og-samfunn/viltforvaltning/mus-og-lemen-kan-fa-toppar-i-sor-norge-hvis-vinteren-holder-seg-kald"),
             ("FHI: Rødmus", f"{FHI}/gnagere/rodmus")]},
{
 "slug": "hytta-for-vinteren", "regions": ["nord", "ost", "midt"], "cat": "Hytte", "min": 4, "img": "hytte",
 "title": "Før du stenger hytta: sikre den mot mus på 20 minutter",
 "lead": "En kald, tom hytte er perfekt vinterkvarter for mus. Gjør disse tingene før du låser døra for sesongen.",
 "body": """
<h2>Tett åpningene</h2>
<p>For å sikre et hus mot mus må alle åpninger større enn seks millimeter stenges. Gå rundt hytta med lommelykt og se særlig på overgangen mellom grunnmur og vegg, under kledningen, rundt rør og kabler, under dører og i lufteventiler.</p>
<ul>
<li>Musebørster under kledningen og børstelister på dører.</li>
<li>Metallnetting i lufteventiler.</li>
<li>Tettemasse eller tetteremser beregnet på gnagere i overgangen mellom grunnmur og vegg.</li>
</ul>
<h2>Fjern alt som kan spises</h2>
<p>Ta med deg all mat, også tørrvarer, fuglefrø og dyrefôr. Musene trenger mat, vann og bolplass. Fjerner du disse og stenger inngangene, har du tatt bort grunnlaget.</p>
<div class="box"><b>Ultralyd?</b>Det finnes apparater som skal skremme bort mus med lyd eller vibrasjoner, men ifølge Folkehelseinstituttet er det ikke dokumentert at de virker.</div>
<h2>Sett feller som står over vinteren</h2>
<p>Sett feller langs veggene der musene ferdes, gjerne to og to. Fleremusfeller som ikke må tømmes etter hver fangst, passer godt i en hytte som står tom lenge. Sjekk dem neste gang du er der.</p>
<h2>Rydd rundt hytta</h2>
<p>Høyt gress og vedstabler inntil veggen gir skjul. Hold gresset nede og legg veden et stykke unna.</p>
""",
 "prod": ("Hyttepakken", "Fleremusfeller, musebørster og tettemateriell.", "gnagere"),
 "sources": [("FHI: Husmus", "https://www.fhi.no/sk/skadedyrveilederen/gnagere/husmus/"),
             ("Huseierne: Slik holder du musene unna", "https://www.huseierne.no/nyheter/slik-holder-du-musene-unna/"),
             ("Huseierne: Mus som skadedyr", "https://www.huseierne.no/alt-om-bolig/inneklima-og-miljo/mus-som-skadedyr-forebygge-og-bekjempe/")]},
]

REGION_ARTICLES = {r: [a for a in ARTICLES if r in a["regions"]][:3] for r in ["ost", "sor", "vest", "midt", "nord"]}
