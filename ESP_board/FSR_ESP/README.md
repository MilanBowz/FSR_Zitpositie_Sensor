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

Gewicht (kg) met weegschaal | Vout (V)  | R_FSR (Ω) | voorwerp
------------------------|-----------|-------------|----------|
0                       | 0         | >2000k          | geen gewicht / kurk
1.255                    | 0.036m     |  >2000k           | gymgewicht 1.25kg
2.324                    | 0.036m     | >2000k           | gymgewicht 2.5kg
3.579                    | 0.050m | >2000kE           | gymgewicht 2.5kg + 1.25
4.655                    | 0.100m | >2000k           | 2 x gymgewicht 2.5kg
5.910                    | 0.130m | >2000k          | 2 x gymgewicht 2.5kg + 1.25
26.000                    | 0.02 | 1500-1700k          | koeler  26kg </br> aan de 2000 kE grens|
... ||| metingen puur met multimeter

... ||| best > 30 kg om te meten
65000 | x | 10k-12k | persoon x
... | x |  | persoon z
90000                    | 3.15 | 200-450          | persoon y => max. gewicht |
...

Vout ≈ 3,3 x (10/(10 + 1500)) ≈ 0.02 V </br>
Vout ≈ 3,3 x (10/(10 + 10)) ≈ 1.5 V </br>
Vout ≈ 3,3 x (10/(10+ 0,45)) ≈ 3,15 V


