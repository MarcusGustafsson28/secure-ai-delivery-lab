# Secure AI Delivery Lab

**Status: MVP under utveckling**

Ett litet Python-projekt för att öva på minsta behörighet för AI-agenter och säkerhetskontroller i DevSecOps.

## Vad programmet gör

`app/policy_guard.py` granskar en syntetisk JSON-policy. Den kontrollerar tillåtna verktyg, att `read` finns med, att inga underagenter anges och att filen följer projektets enkla formatregler.

Programmet använder Pythons standardbibliotek. Det ansluter inte till en AI-tjänst eller externa system.

## Kör på macOS

Säker exempelfil: `python3 app/policy_guard.py examples/agent-policy.json`
Förväntat: `PASS`

Avsiktligt osäker exempelfil: `python3 app/policy_guard.py examples/unsafe-agent-policy.json`
Förväntat: `DENY`. Avslutskod 1 är avsiktlig för en underkänd policy.

Kör testerna: `python3 -m unittest discover -s tests -v`
De åtta befintliga testerna kontrollerar bland annat verktygslistan, underagenter och felaktiga policyfält.

## OMP

`.omp/agents/` innehåller projektspecifika Blue Team- och Red Team-instruktioner för skrivskyddad granskning. `policy_guard.py` är en utbildningsdemo; den styr inte OMP:s faktiska behörigheter.

## Begränsningar

Det här är inte en produktionssäker policy-motor eller en fullständig säkerhetsgranskning. Den granskar en förenklad JSON-fil och bevisar inte hur en agent faktiskt körs. Exemplen innehåller inga riktiga hemligheter eller personuppgifter.

## Projektfiler

- `app/policy_guard.py` — policygranskaren
- `examples/` — säkra och avsiktligt osäkra exempel
- `tests/` — enhetstester
- `docs/threat-model.md` — hotmodell
- `docs/ci-acceptance-criteria.md` — planerade CI-krav
- `.omp/agents/` — OMP-projektagenter

## Nästa utvecklingssteg

- Lägg till ett CLI-test för syntaktiskt felaktig JSON.
- Kör CI-arbetsflödet på GitHub efter uppladdning.
- Uppdatera dokumentationen efter första lyckade CI-körningen.
