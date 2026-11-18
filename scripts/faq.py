"""Spørsmål og svar (FAQ-side). Svarene bygger på artiklene og FHI-kildene som er lenket der.
Hvert spørsmål lenker til artikkelen som utdyper svaret. Brukes også til FAQPage-strukturdata."""

FAQ = [
 ("Mus og rotter", [
  ("Hvor små hull kan en mus komme gjennom?", "For å sikre et hus mot husmus må alle åpninger større enn 6 millimeter stenges, ifølge Folkehelseinstituttet.", "mus-om-hosten"),
  ("Hvorfor kommer musene inn om høsten?", "Når nettene blir kalde og maten ute blir knappere, søker musene mot varme og ly i bygninger. Kjellere, loft, garasjer og tomme hytter er de første stedene de prøver.", "mus-om-hosten"),
  ("Hvordan ser museekskrementer ut?", "Ekskrementer fra mus er små og mørke, omtrent på størrelse med riskorn. Ekskrementer på én til to centimeter tyder på rotter.", "mus-om-hosten"),
  ("Hvor skal musefellene stå?", "Langs veggene der musene ferdes, med utløseren inn mot veggen. Sett gjerne to feller ved siden av hverandre, og sett dem tett, fordi mus ofte bare beveger seg noen meter fra bolet.", "mus-pa-garden"),
  ("Hvor mange musefeller trenger jeg?", "Det avhenger av hvor du har sett spor og hvor mye. Bruk fellekalkulatoren vår for et forslag til antall og plassering.", None),
  ("Virker ultralydapparater mot mus?", "Ifølge Folkehelseinstituttet er det ikke dokumentert at apparater med ultralyd eller vibrasjoner virker.", "hytta-ved-sjoen"),
  ("Hvem har ansvaret hvis det er rotter på eiendommen?", "På privat eiendom er det huseier eller beboer som har ansvaret for å forebygge og bekjempe rotter. Kommunen tilbyr som regel ikke bekjempelse på privat eiendom.", "rotter-i-byen"),
  ("Hvorfor er rotter vanskeligere å fange enn mus?", "Brunrotter kan være redde for ukjent mat, nye gjenstander og fremmede lukter (neofobi). Feller kan derfor bli stående urørt i dager før de virker.", "rotter-i-byen"),
  ("Hva er et smågnagerår?", "Smågnagere som mus og lemen svinger kraftig i antall, med topper omtrent hvert tredje–fjerde år. I toppår er det flere mus som leter etter ly om høsten.", "smagnagerar"),
 ]),
 ("Insekter i huset", [
  ("Hva er forskjellen på sølvkre og skjeggkre?", "Skjeggkre er større, mørkere og mer hårete enn sølvkre, og har lengre haletråder – den lengste omtrent like lang som kroppen. Sølvkre er mindre og mer sølvglinsende.", "fukt-solvkre-skjeggkre"),
  ("Hjelper det å tørke ut badet mot skjeggkre?", "Mindre fukt hjelper mot sølvkre, men skjeggkre klarer seg også i tørre rom. Mot skjeggkre virker forgiftet åte best, plassert som små dråper mange steder langs veggene.", "fukt-solvkre-skjeggkre"),
  ("Hvordan sjekker jeg hotellrommet for veggedyr?", "Sett bagasjen unna sengen, trekk av lakenet i ett hjørne og se langs madrassens sømmer etter små svarte prikker, hudskall eller levende dyr.", "veggedyr-pa-reise"),
  ("Dreper frysing veggedyr?", "Ifølge Folkehelseinstituttet vil frysing slik at alt innholdet oppnår −18 °C i tre døgn drepe veggedyr og mange andre skadedyr.", "veggedyr-pa-reise"),
  ("Hvordan ser et veggedyr ut?", "Veggedyret er rødbrunt med oval og sterkt flattrykt kropp. Voksne er 5–6 millimeter lange og 3 millimeter brede.", "veggedyr-pa-reise"),
  ("Er det stokkmaur eller skogsmaur?", "Stokkmaur har helt svart hode og jevnt krummet rygg. Rød skogsmaur har tofarget hode og humpete rygg.", "stokkmaur-eller-skogsmaur"),
  ("Må jeg bekjempe små svarte maur på kjøkkenet?", "Svart jordmaur kommer ofte inn om våren på jakt etter mat. Slike tilfeldige gjester trenger man ikke å bekjempe, men tørk opp søl og tett der de kommer inn.", "stokkmaur-eller-skogsmaur"),
  ("Hvorfor er det plutselig så mange fluer på loftet om høsten?", "Det er ofte loftsfluer som kryper inn i uoppvarmede rom for å overvintre. De gjør ingen materiell skade.", "fluer-om-hosten"),
  ("Hvor kommer fruktfluene fra?", "Fruktfluer formerer seg på gjærende frukt, skvetter i tomflasker og søppel. Finn og fjern kilden – det er der larvene er.", "fluer-om-hosten"),
  ("Hva lager hull i ullgenseren?", "Ofte klesmøll, som er insektet som gjør størst skade på tekstiler i Norge. Det er larvene som spiser ull og pels.", "klesmoll-og-pelsbille"),
  ("Hva er brun pelsbille?", "En liten, rundaktig bille på 2,5–4 millimeter med brun bakkropp og svart forkropp. Den ble først funnet på Majorstuen i Oslo og sprer seg nå til tettsteder i resten av landet.", "klesmoll-og-pelsbille"),
 ]),
 ("Veps, bier og humler", [
  ("Når er det best å fjerne et vepsebol?", "Tidlig i sesongen. Dronningene kommer fram i april, og et bol på størrelse med en valnøtt er lett å fjerne. Bol inne i vegger bør fagfolk ta.", "vepsebol"),
  ("Blir vepsebolet brukt igjen neste år?", "Nei. Alle stikkevepskolonier i Norge er ettårige, og gamle bol brukes aldri på nytt.", "vepsebol"),
  ("Er det humler eller veps i veggen?", "Humler har tykk, tett behåret kropp. Veps har glatt bakkropp med sterkt gule og svarte striper og lager papiraktige bol – det gjør ikke humler eller bier.", "humler-og-bier-i-veggen"),
 ]),
 ("Vilt i hage og hus", [
  ("Er grevling farlig?", "Nei. Grevlingen er fredelig og angriper ikke mennesker. Den kan derimot grave opp plenen og lage hi under bygninger.", "grevling-pa-tomta"),
  ("Når kan jeg tette grevlinghiet?", "Ikke før du er sikker på at det er tomt. Ungene fødes på senvinteren og kommer ut mot slutten av april eller i mai. Vent til høsten, sjekk med sand eller en lett helle om hiet er i bruk, og tett når grevlingen er ute.", "grevling-pa-tomta"),
  ("Kan jeg felle grevling som graver i plenen?", "Nei. Skader på plen, blomsterbed, kompost eller søppel regnes ikke som skade av vesentlig økonomisk betydning, og gir ikke grunnlag for skadefelling.", "grevling-pa-tomta"),
  ("Hva gjør jeg med flaggermus på loftet?", "Alle flaggermus i Norge er fredet. Tett innflygingshullene først når flaggermusene har forlatt huset, så du ikke stenger dem inne.", "flaggermus-pa-loftet"),
  ("Hva gjør jeg hvis jeg blir bitt av hoggorm?", "Kontakt lege eller Giftinformasjonen på 22 59 13 00, og ring 113 ved alvorlige symptomer. Hold deg i ro, og ikke klem, skjær eller sug på bittstedet.", "hoggorm"),
  ("Når kan jeg gjøre noe med måker på taket?", "Før hekkingen starter. Når måkene har begynt å bygge reir, er det forbudt å fjerne eller forstyrre det.", "maker-pa-taket"),
  ("Når legger brunsneglen egg?", "De fleste eggene legges fra slutten av august til slutten av september. Hver snegl du fjerner før det, betyr mye for neste års bestand.", "brunskogsnegl"),
 ]),
 ("Flått og hytte", [
  ("Hvor i Norge finnes flått?", "Skogflått finnes langs kysten fra svenskegrensen i Østfold og nord til Bodø i Nordland, særlig i kyst- og dalområder med løvskog og kratt.", "flatt-langs-kysten"),
  ("Når er flåtten aktiv?", "Flått i Norge er aktiv fra april til november, når lufttemperaturen er over sju–åtte grader.", "flatt-langs-kysten"),
  ("Hvordan sikrer jeg fjellhytta mot mus gjennom vinteren?", "Tett åpninger over seks millimeter før skisesongen, ikke la mat bli igjen, og sjekk fellene ved hvert besøk.", "fjellhytta"),
  ("Hva bør jeg gjøre før jeg stenger hytta ved sjøen?", "Tett under dører og rundt rør, ta med all mat og sett fleremusfeller langs veggene.", "hytta-ved-sjoen"),
 ]),
 ("Fagfolk og regler", [
  ("Når bør jeg ringe en skadedyrtekniker?", "Hvis du ser rotter innendørs, mistenker veggedyr, har veps inne i en vegg, eller problemet kommer tilbake etter at du har tettet og satt feller.", "rotter-i-byen"),
  ("Hvor kan jeg få gratis råd om skadedyr?", "Folkehelseinstituttet har skadedyrtelefon på 21 07 77 00 på hverdager kl. 13–14, og e-post skadedyr@fhi.no. Du kan også sende inn bilder for identifisering.", None),
 ]),
]
