# Lektion 8, undervisningsnote: inverse matricer og determinanter

Noten følger lecture-notebooken celle for celle. Cellenumre i kantede parenteser
refererer til notebookens rækkefølge (celle 0 er overskriften). Tidsforslag er
for en dobbeltlektion på 2 x 45 min; justér efter rummet.

Dagens ene idé, som alt andet hænger på: man kan ikke dividere med en matrix.
Hele lektionen handler om at bygge den ting, der gør divisionens arbejde.

---

## 1. Hvorfor vi har brug for noget nyt  [1-3]  (3 min)

Start i lektion 6: vi skrev et ligningssystem som $A\vec{x} = \vec{b}$. Hvis
det var tal, ville vi bare dividere med $A$. Det kan vi ikke med matricer.
Spørg rummet: hvad gør division egentlig? Den fjerner det, der står foran
$x$. Så det er det, vi skal finde: en matrix, der fjerner $A$.

## 2. Identitetsmatricen  [4-25]  (12 min)

$I_n$ er matrixverdenens 1-tal. Ettaller på diagonalen, nuller ellers.
Regn eksemplet i celle 7 på tavlen: $I_2 (3, 2)^T$. Hvert element rammes
præcis én gang af et 1-tal, resten ganges med nul. Derfor kommer vektoren
uændret ud. Det samme gælder, når $I$ ganges på en hel matrix.

I Python: `np.identity(n)` og `np.eye(n)` er det samme (vis begge, celle 13
og 14, så de ikke bliver forvirrede, når de ser `eye` i dokumentationen).

Øvelsen i celle 10 er en opvarmning i at bruge `@` fra lektion 7. To ting,
der er værd at stoppe ved:

Først formreglen. `i_2 @ matrix_23` virker, fordi 2x2 gange 2x3 giver 2x3.
Spørg: hvad sker der, hvis jeg bytter om og skriver `matrix_23 @ i_2`? Lad
dem gætte, kør det, se fejlen (3 passer ikke med 2). Det er lektion 7's
regel i praksis, og det er den fejl, de kommer til at lave i øvelserne.

Dernæst sammenligning. `==` på to arrays (celle 20 og 21) giver en hel matrix
af True/False, ét svar pr. element. `np.array_equal` (celle 22-25) giver ét
samlet svar. Begge dele er fine; den sidste er den, man bruger, når matricen
er 100x100 og man ikke gider kigge.

## 3. Den inverse matrix  [26-36]  (15 min)

Analogien i celle 28 bærer hele afsnittet: $5x = 10$ løses ved at gange med
$5^{-1}$ på begge sider, fordi $5^{-1} \cdot 5 = 1$. Den matrix, der
opfylder $A^{-1}A = I$, kalder vi den inverse. Så

$A^{-1} A \vec{x} = A^{-1} \vec{b}$, altså $I\vec{x} = A^{-1}\vec{b}$, altså
$\vec{x} = A^{-1}\vec{b}$.

Skriv det på tavlen i tre linjer. Det er dagens formel, og resten af
lektionen er bare den formel brugt på større og større systemer.

2x2-formlen (celle 29): byt diagonalen, skift fortegn på de to andre, divider
med $ad - bc$. Regn `matrix_a` fra celle 32 i hånden, inden I kører koden:

$A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$, $ad - bc = 4 - 6 = -2$,
$A^{-1} = -\tfrac{1}{2}\begin{bmatrix} 4 & -2 \\ -3 & 1 \end{bmatrix}
= \begin{bmatrix} -2 & 1 \\ 1.5 & -0.5 \end{bmatrix}$.

Så matcher tavlen output fra celle 34, og celle 35 viser, at produktet
faktisk giver $I$. Det er det øjeblik, hvor det hele klikker for de fleste.

Funktionen `matrix_inverse_two` i celle 31 er der for at vise, hvad NumPy gør
under motorhjelmen, og for at gøre determinantens rolle synlig: vi dividerer
med den, så den må ikke være nul. Bed om en 2x2-matrix med determinant nul.
Hvis ingen byder ind: $\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$ (anden
række er to gange den første). Kør funktionen, se `ValueError`. Forklar hvad
det betyder økonomisk/geometrisk: de to ligninger siger det samme, så der er
ikke én løsning. Det er lektion 5's parallelle linjer, set fra matrixsiden.

Celle 36 er pointen: `np.linalg.inv(matrix_a)` gør det hele i ét kald. Fra nu
af bruger vi den.

## 4. Løs lektion 6-systemet  [37-40]  (5 min)

Systemet $150x_1 - x_2 = -1000$ og $200x_1 - x_2 = -500$ er det, de allerede
har set. Nu løses det med `np.linalg.inv(A) @ b`, svar $(10, 2500)$.

Én ting at understrege: rækkefølgen. Det er $A^{-1}\vec{b}$, altså
`inv(A) @ b`, ikke `b @ inv(A)`. Matrixprodukt kommuterer ikke, og her ville
det andet enten fejle eller give noget forkert.

(Bogløsningerne til 7.2.6 bruger `np.linalg.solve(A, b)`. Hvis nogen
spørger: det er samme idé, bare uden at danne den inverse eksplicit. Det er
det, man bruger i praksis, men vi vil se den inverse i dag, fordi vi skal
bruge den som objekt i Leontief.)

## 5. Determinant og invers for 3x3 og større  [41-56]  (12 min)

Celle 42: determinanten af en 3x3 udregnes ved at gå langs første række og for
hvert element skjule dets række og kolonne, tage determinanten af det, der er
tilbage (en 2x2, som de kan), og gange med elementet. Fortegnene skifter plus,
minus, plus. Det er alt, de behøver at kunne forklare.

Det konkrete eksempel i celle 44 er værd at regne færdig på tavlen, fordi
resultatet er en overraskelse:

$1(45 - 48) - 2(36 - 42) + 3(32 - 35) = -3 + 12 - 9 = 0$.

Matricen med tallene 1 til 9 har determinant nul og kan altså ikke inverteres.
Hvorfor? Række 3 minus række 2 er $(3,3,3)$, og det er række 2 minus række 1
også. Rækkerne er afhængige af hinanden, præcis som i 2x2-eksemplet ovenfor.
Det er et godt sted at sige, at determinanten er en test: nul betyder, at
matricen indeholder overflødig information.

Celle 46-53: NumPy på tilfældige heltalsmatricer. Læg mærke til output i celle
49: `-26.000000000000014`. Determinanten af en heltalsmatrix er et heltal, så
hvorfor de decimaler? Fordi NumPy regner med kommatal og laver bittesmå
afrundingsfejl undervejs. Det har en praktisk konsekvens: testen
`det == 0` i celle 70 er ikke helt sikker. En matrix med determinant nul kan
komme ud som `0.0000000000000004`. Den sikre version er
`np.isclose(det, 0)`. Det er ikke pensum, men nævn det, så de ikke bliver
snydt i øvelse 1.2 og 3.

Diagrammet i celle 55 er kun en skitse af ideen (små determinanter for hver
position). Sig det højt: ingen skal regne en 3x3-invers i hånden her, og
diagrammet er ufuldstændigt (fortegn og en transponering mangler). Budskabet i
celle 56 er det, de skal tage med: `np.linalg.inv` virker for enhver
kvadratisk matrix med determinant forskellig fra nul.

Celle 57 og 58 gentager 2x2-formlen og determinantdefinitionen. Spring dem
over eller opsummer i én sætning: kun kvadratiske matricer har en invers, og
kun hvis determinanten ikke er nul. Ordene "singulær" og "inverterbar" kan de
få med her.

## 6. Leontief  [59-64]  (18 min)

Det er her, lineær algebra bliver til økonomi, så giv det tid.

Fortæl historien før formlen. Tre sektorer. For at producere for 1 krone
handel skal handelssektoren selv købe for 25 øre handel og 15 øre transport.
Hver sektors produktion skal altså dække to ting: det, forbrugerne vil have
(endelig efterspørgsel $D$), og det, de andre sektorer skal bruge som input.

Udled formlen på tavlen, det tager to minutter og gør resten gennemsigtigt:

samlet produktion = input til andre sektorer + endelig efterspørgsel
$X = MX + D$
$X - MX = D$
$(I - M)X = D$
$X = (I - M)^{-1} D$.

Peg på, at linje fire er dagens $A\vec{x} = \vec{b}$ med $A = I - M$. Det er
derfor, vi har brugt en time på den inverse.

Matricen $M$ (celle 61, nu med kommentarer i koden): kolonner er den sektor,
der producerer, rækker er den sektor, inputtet kommer fra. Læs teksten i celle
60 sætning for sætning og udfyld én kolonne ad gangen på tavlen. Første
sætning giver kolonne H: 0.25 fra H, 0.15 fra T, 0 fra S. Anden sætning giver
kolonne T, tredje giver kolonne S. Gør en pointe ud af det, for det er dagens
klassiske fejl: udfylder man rækker i stedet for kolonner, får man en
transponeret matrix og forkerte tal, og koden brokker sig ikke. Det er
også fælden i øvelse 2.

Output (celle 64) for $D = (15, 5, 25)$ er $X \approx (30.4, 12.1, 39.0)$.
Tre ting at læse ud af tallene:

Hvert tal i $X$ er større end det tilsvarende i $D$. Det skal det være:
handel skal producere for 30.4 mia. for at kunne levere 15 til forbrugerne,
fordi de resterende 15.4 ædes af handel selv og af sundhedssektoren.

Diagonalen i $(I - M)^{-1}$ er over 1. Element $(i, j)$ fortæller, hvor meget
sektor $i$ skal producere ekstra, når den endelige efterspørgsel i sektor $j$
stiger med 1 krone. Det er en multiplikator, og det er hele grunden til, at
økonomer bruger modellen.

Og hvis $M$ havde så store tal, at $\det(I - M)$ gik mod nul, ville
økonomien æde mere, end den producerede. Modellen bryder sammen, og
determinanten er det, der siger det.

## 7. 4x4-eksemplet  [65-75]  (7 min)

Samme opskrift, større system, og nu med en vagt: udregn determinanten, tjek
at den ikke er nul, og først derefter inverter. Celle 70 gør det i én celle;
celle 72-75 gør det trin for trin. Determinanten er $-169$, pænt helt tal, så
`== 0`-testen virker her. Løsningen er cirka $(1.44, 0.57, 2.19, 2.78)$.
Øvelse 3.1 er præcis dette system, så lad dem selv regne det efter.

## 8. Opsummering og bogopgaver  [76]  (5 min)

Opsummeringen i celle 76 er dækkende. Tre sætninger, de skal kunne sige selv:
den inverse gør for matricer, hvad $1/a$ gør for tal; den findes kun for
kvadratiske matricer med determinant forskellig fra nul; løsningen på
$A\vec{x} = \vec{b}$ er $\vec{x} = A^{-1}\vec{b}$.

Jacques 7.2.6 (s. 571) er to varer i ligevægt, 2x2, kan gøres i hånden:
$\det = 27 - 1 = 26$, priser $P_1 = 25$, $P_2 = 5$.

Eksamensspørgsmål 5 (s. 595) er en god afslutning, hvis der er tid, fordi
den giver den inverse en ny betydning. Overgangsmatricen flytter kunder én
måned frem; `np.linalg.matrix_power(P, 3)` flytter dem tre måneder frem; og
den inverse flytter dem én måned tilbage. Invers betyder "fortryd". Det er
den samme idé som $A^{-1}$, der fortryder $A$, og det er en pæn cirkel at
slutte på.

---

## Hvad der er ændret i notebooken i dag

Inputmatricen i Leontief-eksemplet (celle 61) og i løsningssættets øvelse 2
stod transponeret (rækker i stedet for kolonner). Begge er rettet og kørt
igen, så de printede tal passer med teksten. Opgaveteksterne er uændrede.
