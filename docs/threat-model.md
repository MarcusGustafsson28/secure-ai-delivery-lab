# Hotmodell: Secure AI Delivery Lab

**Status:** beskriver den lokala MVP:n och planerade CI-kontroller.

## Syfte och omfattning

Projektet är en lokal utbildningsdemo. `app/policy_guard.py` granskar en JSON-fil med en förenklad agentpolicy. Den använder inte en AI-modell, kör inte policyverktygen och ansluter inte till externa system.

Exempelfilerna innehåller påhittade data. Inga API-nycklar eller personuppgifter behövs.

## Tillgångar

- Källkod, tester och projektets OMP-instruktioner.
- Integriteten hos policyfiler och testresultat.
- GitHub-repot och framtida CI-arbetsflöden.

## Dataflöde och förtroendegränser

Användaren anger en policyfil → programmet kontrollerar sökvägen och läser JSON → policyn jämförs med tillåtna verktyg och fält → programmet visar PASS eller DENY.

Policyfilens innehåll och sökväg behandlas som opålitlig indata. Programmet ska bara läsa JSON-filer inom projektmappen. CI är en separat förtroendegräns. Arbetsflödet är definierat lokalt men har ännu inte körts på GitHub.

## Risker och skydd

### Policyn begär otillåtna verktyg eller underagenter
**Påverkan:** En osäker policy kan annars misstas för en godkänd policy.
**Skydd:** Granskaren använder en tillåtelselista och underkänner okända verktyg och underagenter. Säkra och osäkra exempel demonstrerar utfallet.

### Sökvägen pekar utanför projektet
**Påverkan:** Programmet kan annars läsa en fil som inte hör till labben.
**Skydd:** Granskaren kontrollerar att filen finns inom projektmappen och är en JSON-fil. Tester för sökvädsbegränsningen återstår.

### JSON är felaktig eller har dubbla nycklar
**Påverkan:** Tvetydig indata kan ge oväntad bedömning.
**Skydd:** Felaktiga JSON-filer och dubbla nycklar ska avvisas. Tester för dessa fall återstår.

### Resultatet tolkas som en faktisk OMP-behörighetskontroll
**Påverkan:** En godkänd JSON-fil kan ge falsk trygghet om hur en agent faktiskt körs.
**Skydd:** `policy_guard.py` är bara en utbildningskontroll. Den ändrar eller verkställer inte OMP:s behörigheter.

### CI får onödiga behörigheter eller osäkra beroenden
**Påverkan:** Ett felkonfigurerat arbetsflöde kan ge kod i CI större åtkomst än testerna behöver.
**Skydd:** Arbetsflödet är definierat enligt kraven, men GitHub-körning och granskning återstår.

## Verifiering

- Den säkra exempelfilen har gett PASS.
- Den avsiktligt osäkra exempelfilen har gett DENY.
- De tio befintliga enhetstesterna har passerat.
- Lägg till ett CLI-test för syntaktiskt felaktig JSON. Dubbla nycklar och externa sökvägar har nu tester.
- Efter uppladdning: kontrollera att GitHub kör testerna och att arbetsflödet endast har contents: read.

## Begränsningar

Det här är inte en fullständig säkerhetsgranskning eller en produktionssäker policy-motor. Den bedömer en förenklad JSON-fil och bevisar inte att en agent följer policyn vid körning.
