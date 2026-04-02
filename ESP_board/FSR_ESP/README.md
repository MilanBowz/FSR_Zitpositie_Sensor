# Resultaten FSR met simpele pull-down weerstand (10kE)

F: R = U/I

Rpulldown = 10kE | Rfsr (noload) > 2000 kE

## Als Rf/R2 niet ingedrukt

Vout ~= 0 V

## Als Rf/R2 ingedrukt
Vin >= Vout > 0 V 

## Testen met vaste gewichten Vin = 3.3V
Testmethode: Vcc = 3.3V altijd gewichten verwijderen voor volgend testresultaat</br>
Vout = Vcc * R0/(R0+Rs) = 3.3 * 10000/(10000+Rs)

### Sensor 2 Newton (~2kg)
Rfsr (noload) > 2000 kE

Gewicht (g) met weegschaal | Vout(min) (V) | Vout(rms) (V) | R_FSR (Ω)| voorwerp
------------------------|----------|---------|------------------------|----------|
0                       | 0        | 0 | >2000kE            | geen gewicht 
20                      | 1.44      | 1.52 | x           | glazen kurk
24                      | 2.00      | 2.08 | x          | glazen kurk + plastiek gadget
31                      | 2.24      | 2.32 | x           | glazen kurk + plastieke munt
35                      | 2.40      | 2.48 | x          | glazen kurk + plastieke munt + plastiek gadget
42                      | 2.56      | 2.64 | x          | glazen kurk + 2 plastieke munt
46                      | 2.64      | 2.72 | 3k          | glazen kurk + 2 plastieke munt + plastiek gadget
114                      | 2.72      | 2.84 | 500E         | glazen kurk + kaars 1
236                     | 2.96      | 3.04 | 300E          | glazen kurk + kaars 2
498 +20                     | 2.96      | 3.04 | 300E        | glazen kurk + kaars 3
?                    | 3.04      | 3.12 | x           | glazen kurk + max pressure human
...


### Sensor 1 (0-150kg)
Rfsr (noload) > 2000 kE

Gewicht (g) met weegschaal | Vout (V)  | R_FSR (Ω) | voorwerp
------------------------|-----------|-------------|----------|
0                       | 0         | >2000k          | geen gewicht / kurk
1255                    | 0.036     |  >2000k           | gymgewicht 1.25kg
2324                    | 0.036     | >2000k           | gymgewicht 2.5kg
3579                    | 0.050 | >2000kE           | gymgewicht 2.5kg + 1.25
4655                    | 0.100 | >2000k           | 2 x gymgewicht 2.5kg
5910                    | 0.130 | >2000k          | 2 x gymgewicht 2.5kg + 1.25
26000                    | x | 1500-1700k          | koeler  26kg </br> aan de 2000 kE grens|
... ||| best > 30 kg om te meten
65000 | x | 100k-120k | persoon x
... | x |  | persoon z
90000                    | x | 200-450          | persoon y => max. gewicht |
...

## Nadelen