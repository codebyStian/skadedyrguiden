"""Regionale fagartikler. Fakta er hentet fra FHIs Skadedyrhåndbok og andre lenkede kilder.
Bygges av scripts/page.py til site/artikler/<slug>.html."""

FHI = "https://fhi.no/sk/skadedyrhandboka"

ARTICLES = [
{
 "slug": "grevling-pa-tomta", "regions": ["ost", "sor", "vest", "midt"], "cat": "Vilt i hagen", "min": 6, "img": "grevling",
 "title": "Grevling på tomta: hva kan du gjøre – og hva har du lov til?",
 "lead": "Grevlingen er fredelig og angriper ikke mennesker, men den kan grave opp plenen og lage hi under terrassen. Her er hva som virker, når du kan tette hiet, og hva regelverket sier.",
 "body": """
<h2>Kjenn igjen grevlingen og sporene</h2>
<p>Grevlingen er det nest største mårdyret i norsk natur, etter jerven. Den har svart-hvitt hode, svart underside, grå og grov pels på rygg og sider, og korte bein med lange, kraftige klør for å grave. Kroppen er rundt 67–90 centimeter lang. Vekten er lavest om våren, etter vintersøvnen.</p>
<ul>
<li><b>Hull i plenen.</b> Grevlingen graver etter meitemark og oldenborrelarver. Graver den mye, kan det tyde på at plenen har mye larver.</li>
<li><b>Toalettgroper.</b> Grevlingen legger avføringen i små groper, opptil ti centimeter dype, utenfor hiet og langs grensene for territoriet.</li>
<li><b>Hi med jordhaug.</b> Hovedhiet har vanligvis en stor jordhaug foran inngangen, som er 30–35 centimeter bred. Det skiller det fra revehi. Grevlingen har også midlertidige hi, ofte nær bygninger.</li>
</ul>
<h2>Hvorfor kommer den akkurat til deg?</h2>
<p>Grevlingen går ikke i ekte dvale, men sover gjennom vinterhalvåret og tærer på fettreservene. Om våren er den sulten og leter etter mat, og gravingen i plenen er som regel begrenset til en periode om våren og en periode på sensommeren og høsten. Ungene fødes i hiet på senvinteren, vanligvis i februar–mars, og kommer først ut mot slutten av april eller begynnelsen av mai.</p>
<div class="box"><b>Det viktigste rådet</b>Ikke steng et grevlinghi før du er sikker på at det er tomt. Stenger du inne unger, blir det et dyrevelferdsproblem – og skaden kan bli større hvis grevlingen graver seg inn igjen.</div>
<h2>Slik får du grevlingen til å flytte</h2>
<ul>
<li>Fjern maten: lukk søppeldunker (bind dem gjerne fast), sikre kompostbingen og plukk opp nedfallsfrukt.</li>
<li>Gjør stedet ubehagelig: sterk lukt som salmiakk, plaststrimler eller folie som rasler, en radio eller lys med bevegelsessensor.</li>
<li>Legg en presenning over de mest utsatte delene av plenen i noen dager.</li>
<li>Sett opp et lavt eller elektrisk gjerde rundt hagen. Grevlingen graver fort under vanlige gjerder, så sperringen må gå ned i bakken – gjerne minst 30 centimeter, eller kraftig netting.</li>
</ul>
<p>Ultralyd- og vibrasjonsapparater anbefales ikke, fordi det ikke finnes vitenskapelig dokumentasjon på at de virker. Kjemiske avskrekkingsmidler har heller ikke vist effekt mot grevling.</p>
<h2>Når og hvordan du tetter hiet</h2>
<ol>
<li><b>Vent til høsten.</b> Om våren og sommeren kan det være unger i hiet.</li>
<li><b>Sjekk at hiet er i bruk – eller tomt.</b> Strø sand i åpningen og se etter fotspor, eller sett en lett steinhelle foran. Grevlingen velter den lett, og da ser du om den bruker hiet.</li>
<li><b>La ett hull stå åpent en periode,</b> slik at grevlingen kan forlate stedet.</li>
<li><b>Tett når grevlingen er ute,</b> helst om kvelden eller natten, og sperr så det ikke kan graves nytt hi samme sted – med netting som går ned i bakken.</li>
</ol>
<h2>Hva sier regelverket?</h2>
<p>Kommunen flytter normalt ikke grevlinger, og det er ikke lov å fange grevling levende for å flytte den et annet sted.</p>
<p>Etter viltforskriften kan den som får skade, felle grevling uten særskilt tillatelse hele året når det er nødvendig for å stanse eller avverge skade på eiendom. Men det gjelder bare når alle vilkårene er oppfylt:</p>
<ul>
<li>Skaden er, eller kan bli, av vesentlig økonomisk betydning.</li>
<li>Du har prøvd forebyggende tiltak som er rimelige ut fra verdiene og kostnadene.</li>
<li>Fellingen gjelder det dyret som gjør skade, og vil sannsynligvis stanse skaden.</li>
</ul>
<p>Hull i plenen, rot i blomsterbed, kompost eller søppel regnes <b>ikke</b> som skade av vesentlig økonomisk betydning. Det som kan gi grunnlag, er typisk at grevlingen har gravd hi under grunnmuren og skader eller truer den. Skadefelling skal rapporteres til kommunen, og i tettbygde strøk er skytevåpen som hovedregel ikke tillatt uten tillatelse fra politiet. Skadefelling skal være siste utvei – snakk med kommunen eller viltnemnda først. Ordinær jakttid er ifølge Stjørdal kommune fra 21. august til 31. januar; sjekk gjeldende jakttider før du gjør noe.</p>
<p>Grevlingen spiser også brunsnegl, så noen naboer ser den som en hjelper i hagen.</p>
""",
 "prod": ("Gjerde og sperring", "Netting og utstyr til å sperre under terrasser og boder.", "hus-og-hage"),
 "sources": [("FHI Skadedyrhåndboka: Grevling", f"{FHI}/pattedyr-andre/grevling"),
             ("Miljødirektoratet: Jeg opplever problemer med en art – hva kan jeg gjøre?", "https://www.miljodirektoratet.no/ansvarsomrader/arter-naturtyper/vilt/vilt-som-gjor-skade/Jeg-opplever-prorblemer-med-en-art-hva-kan-jeg-gjore/"),
             ("Oslo kommune: Grevling i hagen? Tips og råd", "https://www.oslo.kommune.no/get-file/1132988/bd774e75285b27dd1ef64222103ae2e43571173df64871b78a62deecd0b84a04"),
             ("Lier kommune: Grevling i hagen?", "https://www.Lier.kommune.no/globalassets/09.-teknisk-og-eiendom/landbruk/dokumenter/utmark-og-vilt/grevlingplager_infohefte_nettversjon.pdf"),
             ("Stjørdal kommune: Grevling i hagen?", "https://www.stjordal.kommune.no/_f/p3/ieb2b1edb-1630-4fc2-8b4c-0ebdb69223e0/grevling-i-hagen.pdf"),
             ("Bærum kommune: Vilt i bebyggelsen – grevling", "https://www.baerum.kommune.no/tjenester/natur-friluftsliv-og-naturmangfold/jakt-fiske-og-vilt/vilt--og-fiskeforvaltning/vilt-i-bebyggelsen-grevling/"),
             ("Asker kommune: Vilt", "https://www.asker.kommune.no/friluftsliv/jakt-fiske-og-vilt/vilt/")]},
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
 "guide": ("Slik bekjemper du maur", "https://skadedyrbutikken.no/tips-og-raad/insekter/slik-bekjemper-du-maur?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=art-stokkmaur-eller-skogsmaur"),
 "sources": [("FHI: Stokkmaur", f"{FHI}/maur/stokkmaur"), ("FHI: Rød skogsmaur", "https://www.fhi.no/sk/skadedyrveilederen/maur/rod-skogsmaur/"),
             ("FHI: Svart jordmaur", "https://www.fhi.no/nettpub/skadedyrveilederen/maur/svart-jordmaur/"), ("FHI: Statistikk om skadedyr", "https://fhi.no/tema/skadedyr/statistikk")]},
{
 "slug": "husbukk", "regions": ["sor"], "cat": "Treskadedyr", "min": 4, "img": "husbukk",
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
 "guide": ("Husbukk i huset: guide til bekjempelse", "https://skadedyrbutikken.no/tips-og-raad/insekter/husbukk-i-huset-komplett-guide-til-effektiv-bekjempelse?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=art-husbukk"),
 "sources": [("FHI: Husbukk", f"{FHI}/biller/husbukk"), ("FHI: Blåbukk", f"{FHI}/biller/blabukk"), ("FHI: Statistikk om skadedyr", "https://fhi.no/tema/skadedyr/statistikk")]},
{
 "slug": "vepsebol", "regions": ["sor", "midt"], "cat": "Veps", "min": 4, "img": "veps",
 "title": "Vepsesesongen: derfor er bolet lite i mai og stort i august",
 "lead": "Hvert vepsebol lever bare ett år. Når du vet hvordan sesongen går, skjønner du hvorfor det lønner seg å oppdage bolet tidlig – og når det kan få være i fred.",
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
 "guide": ("Veps i hagen: slik fjerner du vepsebol", "https://skadedyrbutikken.no/tips-og-raad/insekter/veps-i-hagen-slik-fjerner-du-vepsebol-og-beskytter-deg-mot-stikk-i-sommer?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=art-vepsebol"),
 "sources": [("FHI: Stikkeveps", "https://www.fhi.no/nettpub/skadedyrveilederen/veps-og-bier/stikkeveps/"), ("FHI Statistikk – Skadedyrstatistikk", "https://statistikk.fhi.no/skast/")]},
{
 "slug": "fukt-solvkre-skjeggkre", "regions": ["vest"], "cat": "Fukt", "min": 5, "img": "skjeggkre",
 "title": "Sølvkre og skjeggkre: hva fukten betyr – og hvorfor skjeggkre er vanskeligere",
 "lead": "Sølvkre er en harmløs badegjest. Skjeggkre har spredt seg kraftig de siste årene og kan bli mange. Her er hva fukt har å si for hver av dem, og hvorfor tørking ikke er nok mot skjeggkre.",
 "body": """
<h2>To arter som ligner</h2>
<p>Sølvkre er en vanlig gjest på baderom. Den gjør liten skade og regnes som harmløs. Skjeggkre ligner, men de voksne er større og mørkere, har lengre haletråder – den lengste er omtrent like lang som kroppen – og tydeligere behåring. Skjeggkre er mørkegrå og litt spraglete og mindre sølvglinsende enn sølvkre.</p>
<h2>Skjeggkre trives også der det er tørt</h2>
<p>Skjeggkre er nattaktive og oppdages ofte når du slår på lyset om natten. De trives best ved høy fuktighet, men klarer seg også i tørrere rom, i motsetning til sølvkre. De finnes oftest i nyere bygninger, og antallet bekjempelser økte kraftig etter 2016 før det flatet ut.</p>
<div class="box"><b>Fukt er ikke hele forklaringen</b>Mindre fukt hjelper mot sølvkre. Mot skjeggkre er det åte som virker best – tørking alene er ikke nok.</div>
<h2>Hva som virker – kort fortalt</h2>
<ul>
<li>Sølvkre: reduser fuktigheten og tett sprekker. Det finnes effektive åteprodukter, så sprøytemidler er unødvendig.</li>
<li>Skjeggkre: bruk forgiftet åte som små dråper mange steder langs veggene i alle rom. Det øker sjansen for at dyrene finner åten.</li>
<li>Vær tålmodig. Skjeggkre kan være vanskelige å bli helt kvitt, og i en periode må du regne med å se noen få.</li>
<li>I blokker og rekkehus bør naboene behandle samtidig.</li>
</ul>
<p>Skjeggkre kan også haike med vesker, bager og sekker, for eksempel fra arbeidsplassen. Det gjør det vanskelig å forebygge helt.</p>
""",
 "prod": ("Mot skjeggkre og sølvkre", "Åte og limfeller til overvåking.", "insekter"),
 "guide": ("Skjeggkre: slik holder du bestanden nede", "https://skadedyrbutikken.no/tips-og-raad/insekter/skjeggkre-hvordan-holde-bestanden-nede?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=art-fukt-solvkre-skjeggkre"),
 "sources": [("FHI: Skjeggkre", f"{FHI}/smadyr-andre/skjeggkre"), ("FHI: Sølvkre", "https://www.fhi.no/nettpub/skadedyrveilederen/smadyr-andre/solvkre-/"),
             ("FHI: Byggomfattende bekjempelse", f"{FHI}/forebygging-og-bekjempelse/byggomfattende-bekjempelse")]},
{
 "slug": "stripet-borebille", "regions": ["vest", "nord"], "cat": "Treskadedyr", "min": 4, "img": "borebille",
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
 "slug": "smagnagerar", "regions": ["nord"], "cat": "Gnagere", "min": 4, "img": "smagnager",
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
 "slug": "hytta-ved-sjoen", "regions": ["ost", "sor", "vest", "midt", "nord"], "months": [8, 9, 10, 11, 3, 4, 5], "cat": "Hytte", "min": 4, "img": "region-sor",
 "title": "Hytta ved sjøen: steng den riktig for vinteren – og åpne den uten overraskelser",
 "lead": "Sommerhuset ved vannet står ofte tomt fra høsten til våren. Da er det et perfekt vinterkvarter for mus. Slik stenger og åpner du hytta.",
 "body": """
<h2>Når du stenger – september og oktober</h2>
<p>For å sikre et hus mot mus må alle åpninger større enn seks millimeter stenges. Gå rundt hytta med lommelykt og se særlig på overgangen mellom grunnmur og vegg, under kledningen, rundt rør og kabler, under dører og i lufteventiler.</p>
<ul>
<li>Musebørster under kledningen og børstelister på dører.</li>
<li>Metallnetting i lufteventiler.</li>
<li>Tettemasse eller tetteremser beregnet på gnagere i overgangen mellom grunnmur og vegg.</li>
<li>Ta med deg all mat, også tørrvarer, fuglefrø og dyrefôr.</li>
<li>Sett feller langs veggene, gjerne to og to. Fleremusfeller passer i en hytte som står tom lenge.</li>
<li>Hold gresset nede og legg veden et stykke unna veggen.</li>
</ul>
<div class="box"><b>Ultralyd?</b>Det finnes apparater som skal skremme bort mus med lyd eller vibrasjoner, men ifølge Folkehelseinstituttet er det ikke dokumentert at de virker.</div>
<h2>Når du åpner – april og mai</h2>
<ul>
<li>Se etter spor etter mus: ekskrementer, gnag og bol. Bruk hansker når du rydder, og unngå å virvle opp støv.</li>
<li>Sjekk fellene og noter hvor det har vært aktivitet – der er det trolig en inngang.</li>
<li>Se etter små vepsebol under takskjegget. Dronningene kommer fram i april, og et bol på størrelse med en valnøtt er lett å fjerne.</li>
<li>Flått blir aktiv fra april. Hold gresset kort rundt hytta.</li>
</ul>
""",
 "prod": ("Hyttepakken", "Fleremusfeller, musebørster og tettemateriell.", "gnagere"),
 "sources": [("FHI: Husmus", "https://www.fhi.no/sk/skadedyrveilederen/gnagere/husmus/"), ("FHI: Stikkeveps", f"{FHI}/veps-og-bier/stikkeveps"),
             ("Huseierne: Slik holder du musene unna", "https://www.huseierne.no/nyheter/slik-holder-du-musene-unna/"),
             ("Huseierne: Mus som skadedyr", "https://www.huseierne.no/alt-om-bolig/inneklima-og-miljo/mus-som-skadedyr-forebygge-og-bekjempe/")]},
{
 "slug": "fjellhytta", "regions": ["ost", "vest", "midt", "nord", "sor"], "months": list(range(1, 13)), "cat": "Hytte", "min": 4, "img": "hytte",
 "title": "Fjellhytta: mus gjennom vinteren, besøk i skisesongen og åpning for barmark",
 "lead": "Fjellhytta brukes ofte mest om vinteren. Mellom besøkene i vinterferien og påsken står den tom og varm-kald – og i et smågnagerår er det mange mus som leter etter ly.",
 "body": """
<h2>Fjellet har sine egne mus</h2>
<p>Smågnagerne svinger kraftig i antall, med topper omtrent hvert tredje–fjerde år. Lemen lever over tregrensa, og klatremus kan påtreffes så høyt som 1400 meter over havet i Sør-Norge. Klatremus kan komme inn i bygninger, og i Nord-Norge gjelder det samme for rødmus. Begge kan være reservoar for musepest.</p>
<h2>Før skisesongen – oktober og november</h2>
<ul>
<li>Tett åpninger større enn seks millimeter: under kledningen, rundt rør og i lufteventiler.</li>
<li>Ikke la mat bli igjen mellom besøkene, heller ikke i boder og uthus.</li>
<li>Sett fleremusfeller langs veggene der du har sett spor før.</li>
</ul>
<h2>Ved hvert besøk i vinter – vinterferie og påske</h2>
<ul>
<li>Sjekk og tøm fellene, og sett dem tilbake på samme sted.</li>
<li>Se etter ferske spor: ekskrementer og gnag viser hvor musene kommer inn.</li>
<li>Rydd med hansker og unngå å virvle opp støv.</li>
</ul>
<div class="box"><b>Smågnagerår?</b>Følg med på meldingene om smågnagere. I et toppår er det klokt å sette flere feller og være ekstra nøye med tettingen.</div>
<h2>Når barmarka kommer – juni</h2>
<ul>
<li>Rydd grundig etter vinteren og tett der musene har kommet inn.</li>
<li>Se etter små vepsebol under takskjegget og i boden.</li>
<li>Bruk hansker og unngå å virvle opp støv når du rydder.</li>
</ul>
""",
 "prod": ("Hyttepakken", "Fleremusfeller, musebørster og tettemateriell.", "gnagere"),
 "sources": [("Store norske leksikon: Smågnagersvingninger", "https://snl.no/smågnagersvingninger"), ("Store norske leksikon: Lemen", "https://snl.no/lemen"),
             ("FHI: Klatremus", f"{FHI}/gnagere/klatremus"), ("FHI: Rødmus", f"{FHI}/gnagere/rodmus"), ("FHI: Husmus", "https://www.fhi.no/sk/skadedyrveilederen/gnagere/husmus/")]},
]

REGION_ARTICLES = {r: [a for a in ARTICLES if r in a["regions"]][:3] for r in ["ost", "sor", "vest", "midt", "nord"]}

ARTICLES += [
{
 "slug": "flaggermus-pa-loftet", "regions": ["ost", "sor", "vest", "midt"], "months": [5, 6, 7, 8, 9], "cat": "Vilt i huset", "min": 4, "img": "flaggermus",
 "title": "Flaggermus på loftet: fredet, nyttig – og slik gjør du det riktig",
 "lead": "Alle flaggermus i Norge er fredet. Har de slått seg ned på loftet eller i veggen, må du vente til de har forlatt huset før du tetter.",
 "body": """
<h2>Fredet og nyttig</h2>
<p>Det er registrert elleve arter flaggermus i Norge, og alle er fredet. Flere står også på Norsk rødliste. Det betyr at du ikke har lov til å fange eller avlive dem uten tillatelse. Flaggermus spiser store mengder insekter, blant annet mygg.</p>
<h2>Hvorfor velger de huset ditt?</h2>
<p>Flaggermus kan bruke loft for å hvile på dagtid, og noen ganger lager de ynglekolonier i bygninger. Koloniene foretrekker varme, tørre og mørke steder, som mørkeloft og hulrom mellom ytter- og innervegg. Flere arter liker seg under pipebeslaget eller rundt pipa på loftet.</p>
<div class="box"><b>Ikke steng unger inne</b>Innflygingshull kan bare tettes når flaggermusene ikke er i huset. Stenger du dem inne, kan dyrene dukke opp andre steder i huset eller dø i veggen.</div>
<h2>Hva er problemet?</h2>
<p>Det største problemet er som regel møkk og urin, som kan gi vond lukt og misfarging der koloniene er store og ventilasjonen er dårlig. Du risikerer ikke rabiessmitte ved å ha flaggermus i huset der du bor.</p>
<h2>Slik gjør du</h2>
<ul>
<li>Følg med på når flaggermusene flyr ut om kvelden, og finn inngangene.</li>
<li>Tett først når de har forlatt huset for sesongen.</li>
<li>Sett gjerne opp flaggermuskasser ute, så har de et annet sted å være.</li>
<li>Bruk hansker som hindrer bitt og væske hvis du må håndtere en flaggermus, også en død. Vask søl med klorin eller alkoholbasert desinfeksjon.</li>
<li>Ikke vekk flaggermus i dvale om vinteren – det tærer på energien de trenger for å overleve.</li>
</ul>
""",
 "prod": None,
 "sources": [("FHI Skadedyrhåndboka: Flaggermus", f"{FHI}/pattedyr-andre/flaggermus"), ("Miljødirektoratet: Flaggermus", "https://www.miljodirektoratet.no/ansvarsomrader/arter-naturtyper/truede-arter-og-naturtyper/flaggermus/"),
             ("Statsforvalteren: Flaggermus i hus (brosjyre)", "https://www.statsforvalteren.no/link/4347ce71843c4d238ee6a2ec6b0c8efa.pdf")]},
{
 "slug": "hoggorm", "regions": ["ost", "sor", "vest", "midt"], "months": [4, 5, 6, 7, 8, 9], "cat": "Vilt i hagen", "min": 4, "img": "hoggorm",
 "title": "Hoggorm i hagen og på hytta: kjennetegn og hva du gjør ved bitt",
 "lead": "Hoggormen er Norges eneste giftige slange. Den er fredet, sjelden aggressiv – og et bitt skal alltid tas på alvor.",
 "body": """
<h2>Kjenn igjen hoggormen</h2>
<p>Det mest karakteristiske kjennetegnet er et svart sikksakkbånd langs ryggen. Grunnfargen er grå (mest hanner) eller brun (mest hunner), og det finnes også helt svarte hoggormer. Hoggorm finnes over det meste av Sør-Norge. I kulturlandskapet liker den brakklagte enger, gjerne nær steingjerder, bringebærkratt eller annet skjul.</p>
<h2>Hoggormen er fredet</h2>
<p>Hoggorm er fredet, som de andre slangene i Norge. Må du flytte en hoggorm, er det greit å sette den ut noen hundre meter unna stedet der du fant den.</p>
<div class="box"><b>Blir du bitt</b>Kontakt lege eller Giftinformasjonen på 22 59 13 00. Ved alvorlige symptomer: ring 113. Hold deg mest mulig i ro – ikke klem, skjær eller sug på bittstedet. Barn som er bitt, bør bæres.</div>
<h2>Slik unngår du bitt</h2>
<ul>
<li>Hold gresset kort og rydd bort kratt og steinhauger nær huset og der barn leker.</li>
<li>Bruk støvler eller kraftige sko i lyng og høyt gress.</li>
<li>Se deg for når du plukker bær eller løfter på steiner og materialer.</li>
<li>Rundt 30 prosent av hoggormbitt er tørrbitt uten gift, men du kan ikke vite det på forhånd. Ta derfor alle bitt på alvor.</li>
</ul>
""",
 "prod": None,
 "sources": [("FHI Skadedyrhåndboka: Hoggorm", "https://www.fhi.no/sk/skadedyrhandboka/krypdyr-reptiler/hoggorm/"), ("FHI Skadedyrveilederen: Hoggorm", "https://www.fhi.no/nettpub/skadedyrveilederen/krypdyr-reptiler/hoggorm/"),
             ("TU/NTB: Færre hoggorm-henvendelser hos FHI", "https://www.tu.no/nyhetsstudio/faerre-hoggorm-henvendelser-hos-fhi-i-sommer-hadde-ventet-flere/126310")]},
{
 "slug": "fluer-om-hosten", "regions": ["ost", "sor", "vest", "midt", "nord"], "months": [9, 10, 11, 3, 4], "cat": "Insekter", "min": 4, "img": "loftsfluer",
 "title": "Plutselig fullt av fluer om høsten? Loftsfluer, gressfluer og fruktfluer",
 "lead": "Når det blir kaldt, søker flere fluearter inn i hus for å overvintre. De fleste gjør ingen skade – men det hjelper å vite hvilken flue du har.",
 "body": """
<h2>Loftsfluer: mørke fluer i vinduene på loftet</h2>
<p>Loftsfluer er mørke og grålige og forveksles ofte med vanlig husflue. Forkroppen er tett dekket av gylne, krøllete hår. Om høsten kryper de inn i uoppvarmede rom i hus og hytter og sitter tett samlet i hulrom, kroker og sprekker. De gjør ingen materiell skade, men kan være til sjenanse når de blir mange.</p>
<p>Det er ikke alltid mulig å stenge dem helt ute fra et loft med mange sprekker, men å tette det du kan, reduserer problemet betraktelig.</p>
<h2>Gressfluer: små, gulsvarte fluer i enorme mengder</h2>
<p>Gressfluer kan om høsten samle seg i enorme ansamlinger nær høye hus, gjerne på varme dager i oktober. De gjør ingen skade på personer eller bygning. Invasjonen varer bare noen få dager, og fluer som kommer inn i oppvarmede rom, dør etter kort tid. Hold vinduer og dører lukket mens det står på, eller bruk myggnetting.</p>
<h2>Fruktfluer: små fluer på kjøkkenet</h2>
<p>Fruktfluer er vanligst om høsten, fra september til november. De formerer seg på gjærende frukt, skvetter i tomflasker og søppel. Finn og fjern kilden – det er der larvene er. Selv etter at kilden er borte, kan det sverme fruktfluer i flere uker.</p>
<div class="box"><b>Store spyfluer innendørs?</b>Mange spyfluer inne i et rom kan bety et dødt dyr i nærheten, for eksempel en mus eller fugl i veggen eller en luftekanal.</div>
""",
 "prod": ("Mot fluer", "Fluenetting, feller og lysfeller.", "insekter"),
 "sources": [("FHI: Loftsfluer", f"{FHI}/fluer-og-mygg/loftsfluer"), ("FHI: Gressflue", f"{FHI}/fluer-og-mygg/gressflue"),
             ("FHI: Fruktfluer, eddikfluer", f"{FHI}/fluer-og-mygg/fruktfluer-eddikfluer"), ("FHI: Spyfluer", f"{FHI}/fluer-og-mygg/spyfluer")]},
{
 "slug": "klesmoll-og-pelsbille", "regions": ["ost", "sor", "vest", "midt", "nord"], "months": list(range(1, 13)), "cat": "Tekstiler", "min": 4, "img": "klesmoll",
 "title": "Hull i ullgenseren? Klesmøll og brun pelsbille",
 "lead": "Klesmøll er insektet som gjør størst skade på tekstiler i Norge. Brun pelsbille har spredt seg fra Oslo til tettsteder i resten av landet.",
 "body": """
<h2>Klesmøll</h2>
<p>Klesmøll finnes innendørs over hele landet, men overlever ikke ute fordi vinteren er for kald. Det er larvene som gjør skaden: de lever av materialer fra dyr, som ull og pels. Voksne klesmøll er 5–8 millimeter lange, med gylne, blekt gulbrune forvinger og rødgule hår på hodet. Larvene er hvite med lysebrunt hode og spinner ofte et rør de spiser fra.</p>
<p>Klesmøll foretrekker skitne tekstiler, og ullplagg som blir liggende bortglemt lenge, er et perfekt oppvekststed. Ser du en klesmøll som flyr, er det mest sannsynlig en hann.</p>
<h2>Brun pelsbille – «Majorstu-billen»</h2>
<p>Brun pelsbille ble funnet første gang i Norge på Majorstuen i Oslo i 1983. Nå er den svært vanlig i Oslo og sprer seg til tettsteder i resten av landet. Billen er 2,5–4 millimeter, rundaktig, med brun bakkropp og svart forkropp. Larven blir rundt åtte millimeter, er brun med gullaktig behåring og har en lang haledusk.</p>
<div class="box"><b>Kulde virker</b>Gjenstander kan fryses, men de må bli gjennomkalde. En bylt med klær bruker lang tid på å bli like kald i midten som på utsiden.</div>
<h2>Slik forebygger du</h2>
<ul>
<li>Vask eller rens ulltøy før du legger det bort.</li>
<li>Pakk ull, pels og fjær i tette plastposer eller bokser.</li>
<li>Støvsug grundig langs lister, i skap og under møbler.</li>
<li>Rist og luft plagg som henger lenge urørt.</li>
</ul>
""",
 "prod": ("Mot møll og pelsbiller", "Feromonfeller og oppbevaring.", "insekter"),
 "guide": ("Hvordan bli kvitt klesmøll", "https://skadedyrbutikken.no/tips-og-raad/insekter/hvordan-bli-kvitt-klesmoell?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=art-klesmoll-og-pelsbille"),
 "sources": [("FHI: Klesmøll", f"{FHI}/moll-og-sommerfugler/klesmoll"), ("FHI Skadedyrveilederen: Klesmøll", "https://www.fhi.no/sk/skadedyrveilederen/moll-og-sommerfugler/klesmoll-/"),
             ("FHI: Brun pelsbille", f"{FHI}/biller/brun-pelsbille"), ("FHI: Forebygging av skadedyrangrep", f"{FHI}/forebygging-og-bekjempelse/forebygging-av-skadedyrangrep"),
             ("FHI: Bekjempelse av skadedyr", f"{FHI}/forebygging-og-bekjempelse/bekjempelse-av-skadedyr")]},
{
 "slug": "brunskogsnegl", "regions": ["ost", "sor", "vest", "midt", "nord"], "months": [4, 5, 6, 7, 8, 9, 10], "cat": "Hage", "min": 5, "img": "snegl",
 "title": "Brunsnegl i hagen: når og hvordan du tar dem",
 "lead": "Brunskogsneglen – også kalt brunsnegl eller mordersnegl – er en fremmed art med svært høy risiko. Timing er alt: hver snegl du tar før egglegging, teller.",
 "body": """
<h2>Hva er brunskogsnegl?</h2>
<p>Brunskogsnegl (Arion vulgaris) ble registrert i Norge første gang i 1988 og har spredt seg over store deler av landet. Den regnes som en invaderende art med svært høy risiko. Den er vanlig langs kysten fra svenskegrensen til Troms, med spredte forekomster i innlandet.</p>
<h2>Sneglens år</h2>
<ul>
<li><b>Vår:</b> Når temperaturen stiger over rundt fem grader, blir sneglene aktive og vokser raskt.</li>
<li><b>Sommer:</b> I løpet av sommeren blir de utvokst og kjønnsmodne.</li>
<li><b>August–september:</b> Paring og egglegging. De fleste eggene legges fra slutten av august til slutten av september.</li>
<li><b>Høst:</b> De voksne dør som regel i oktober. Små snegler overvintrer i jordhuler, steinhauger og komposthauger.</li>
</ul>
<div class="box"><b>Ta dem tidlig</b>Hver snegl kan legge opptil 400 egg. Hver snegl du fjerner før egglegging, betyr mye for neste års bestand.</div>
<h2>Tiltak som virker best sammen</h2>
<ul>
<li>Plukk snegler tidlig, gjerne om kvelden eller etter regn.</li>
<li>Løft på bøtter, potter og planker, og fjern snegler og egg.</li>
<li>Klipp plenen ofte, så jorda holder seg tørrere.</li>
<li>Rydd hageavfall og fuktige, skyggefulle gjemmesteder.</li>
<li>Samarbeid med naboene – det hjelper lite at bare én hage gjør tiltak.</li>
</ul>
<p>Bekjempelse er krevende og krever flere tiltak samtidig. Nærmere råd kan du få fra NIBIO.</p>
""",
 "prod": ("Mot snegler", "Sneglefeller og sperrer til hage og bed.", "hus-og-hage"),
 "sources": [("Store norske leksikon: Brunskogsnegl", "https://snl.no/brunskogsnegl"), ("Bergen kommune / NIBIO: Brunskogsnegl (brosjyre)", "https://bergen.kommune.no/api/rest/filer/V56473"),
             ("Bærum kommune: Tiltak mot brunsnegle", "https://www.Baerum.kommune.no/contentassets/183c7a16d9304602a014dbddb0daa51b/tiltak-mot-brunsnegle.pdf"),
             ("Midt-Telemark kommune: Brunsneglekampanje", "https://midt-telemark.kommune.no/_f/p5/icf4effcc-acfd-44a8-b3ec-b724813a29c9/brunsnegle-kampanje.pdf"),
             ("Handlingsplan for bekjempelse av iberiaskogsnegl (regjeringen.no)", "https://www.regjeringen.no/globalassets/upload/lmd/vedlegg/brosjyrer_veiledere_rapporter/handlingsplan_iberia_kortversjon.pdf")]},
{
 "slug": "maker-pa-taket", "regions": ["ost", "sor", "vest", "midt", "nord"], "months": [2, 3, 4, 5, 6, 7], "cat": "Fugler", "min": 4, "img": "maker",
 "title": "Måker på taket: gjør tiltak før hekkingen starter",
 "lead": "Måker er fredet. Når de først har begynt å bygge reir, må du la dem være i fred – derfor er det før hekkingen du kan gjøre noe.",
 "body": """
<h2>Hvorfor bråker måkene?</h2>
<p>Flere måkearter hekker i byer og tettsteder for å finne mat og beskyttelse. Bråket skjer særlig i hekkeperioden, som i store deler av landet er fra mai til midten av juli. Flate tak er et yndet hekkested.</p>
<div class="box"><b>Fristen er før reiret</b>Når reirbyggingen er i gang, skal måkene få hekke i fred, og det er forbudt å fjerne eller forstyrre reir. Forebyggende tiltak må gjøres før hekkingen starter.</div>
<h2>Det du kan gjøre i god tid</h2>
<ul>
<li>Finn ut hvor på taket måkene hekket i fjor. Det er ofte få steder det er mulig å lage reir.</li>
<li>Gjør disse stedene utilgjengelige før sesongen, for eksempel med nett, vaier eller netting.</li>
<li>Ikke mat måkene, og vær nøye med søppel og matavfall.</li>
<li>Fjern gamle reir om vinteren, når fuglene ikke hekker. Da risikerer du heller ikke fuglelopper.</li>
</ul>
<h2>Hva gjelder hvis måkene allerede hekker?</h2>
<p>Måker er totalfredet. Støy, ekskrementer eller at måkene stuper mot folk, gir ikke grunnlag for skadefelling. Hold avstand til reiret, så går hekkeperioden over. Forstyrrer du måkene, varer bråket ofte lenger.</p>
<p>Finner du syke eller døde måker og mistenker smittsom sykdom, for eksempel fugleinfluensa, skal du varsle Mattilsynet.</p>
""",
 "prod": ("Fuglesikring", "Pigger, nett og vaier til tak og fasader.", "fugler"),
 "sources": [("Miljødirektoratet: Forebyggende måketiltak må gjøres før hekkingen starter", "https://www.miljodirektoratet.no/aktuelt/fagmeldinger/2026/april-2026/forebyggende-maketiltak-ma-gjores-for-hekkingen-starter/"),
             ("Mattilsynet: Spørsmål og svar om måker", "https://mattilsynet.no/dyr/dyrevelferd/sporsmal-og-svar-om-maker"), ("FHI: Måker", f"{FHI}/fugler/maker"),
             ("BirdLife Norge: Hekketid og måker", "https://www.birdlife.no/innhold/bilder/2022/05/10/8819/maker_og_hekketid.pdf")]},
{
 "slug": "humler-og-bier-i-veggen", "regions": ["ost", "sor", "vest", "midt", "nord"], "months": [4, 5, 6, 7, 8], "cat": "Insekter", "min": 4, "img": "humle",
 "title": "Humler eller bier i veggen: hva gjør du?",
 "lead": "Humler og bier er nyttige pollinatorer og sjelden et problem. Men de kan bygge bol i husvegger. Først må du vite om det er humler, bier eller veps.",
 "body": """
<h2>Humle, bie eller veps?</h2>
<ul>
<li><b>Humler</b> har robust, tykk og tett behåret kropp, ofte med hvite, gule eller røde bånd. Det finnes 35 arter humler i Norge.</li>
<li><b>Honningbier</b> er mer behåret enn veps og har lang tunge. Brodden har kraftige mothaker.</li>
<li><b>Veps</b> har sterkt gule og svarte, sparsomt behårede striper og lager papiraktige bol. Det gjør ikke bier eller humler.</li>
</ul>
<h2>Humler i veggen</h2>
<p>Om våren kommer humledronninger ofte inn gjennom åpne vinduer og dører når de leter etter et sted å anlegge bol. Bolet kan ligge i en steinrøys, et gammelt musebol, et fuglereir eller en isolert vegg. Trehumla bygger gjerne bol i hulrom i vegger eller fuglekasser og kan få store bol i løpet av sommeren. Humlene er fredelige, men kan stikke hvis de plages.</p>
<div class="box"><b>Ofte er det beste å vente</b>Et humlebol varer bare én sesong. Er det ikke i veien, kan det få være til høsten. Tett hullet når bolet er forlatt.</div>
<h2>Bier i veggen</h2>
<p>En bisverm som finner et egnet hulrom i en vegg, tak eller pipe, kan slå seg ned permanent og bli i mange år. Da bør du kontakte en birøkter eller skadedyrfirma tidlig. Kuben kan ofte finnes ved å kjenne etter varme på veggen.</p>
<h2>Tips om våren</h2>
<ul>
<li>Bruk insektnett i vinduer som står åpne.</li>
<li>Tett sprekker i kledning og rundt ventiler før dronningene leter etter bolplass.</li>
</ul>
""",
 "prod": None,
 "sources": [("FHI: Humler", f"{FHI}/veps-og-bier/humler"), ("FHI: Honningbie", f"{FHI}/veps-og-bier/honningbie"), ("FHI Skadedyrveilederen: Humler", "https://www.fhi.no/sk/skadedyrveilederen/veps-og-bier/humler/")]},
]

MONTHS = {
 "grevling-pa-tomta": [3, 4, 5, 6, 7, 8, 9, 10], "rotter-i-byen": [10, 11, 12, 1, 2, 3], "flatt-langs-kysten": [4, 5, 6, 7, 8, 9, 10],
 "stokkmaur-eller-skogsmaur": [4, 5, 6, 7, 8], "husbukk": list(range(1, 13)), "vepsebol": [4, 5, 6, 7, 8, 9],
 "fukt-solvkre-skjeggkre": list(range(1, 13)), "stripet-borebille": list(range(1, 13)), "mus-pa-garden": [9, 10, 11, 12, 1, 2, 3],
 "smagnagerar": [8, 9, 10, 11],
}
for a in ARTICLES:
    a.setdefault("months", MONTHS.get(a["slug"], list(range(1, 13))))
ARTICLES[[a["slug"] for a in ARTICLES].index("flatt-langs-kysten")]["regions"] = ["ost", "sor", "vest", "midt", "nord"]

# Eldre artikler som ligger i page.py, men skal med i oversikten
EXTRA = [
 {"slug": "mus-om-hosten", "title": "Mus i huset om høsten: finn hullet før musa gjør det", "cat": "Gnagere", "img": "mus", "regions": ["ost", "sor", "vest", "midt", "nord"], "months": [9, 10, 11, 12, 1, 2]},
 {"slug": "veggedyr-pa-reise", "title": "Veggedyr på hotellet: sjekk rommet på to minutter", "cat": "Insekter", "img": "veggedyr", "regions": ["ost", "sor", "vest", "midt", "nord"], "months": [6, 7, 8, 9, 10]},
]
REGION_ARTICLES = {r: [a for a in ARTICLES if r in a["regions"]] for r in ["ost", "sor", "vest", "midt", "nord"]}
