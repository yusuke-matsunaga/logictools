.PS

dnl 単位長
define(`HC_UNIT', `30 * L_unit')dnl

dnl HC_UNIT によるスケーリング(1次元)
define(`HC_scalar', `$1 * HC_UNIT')dnl

dnl HC_UNIT によるスケーリング(2次元)
define(`HC_vect', `($1 * HC_UNIT, $2 * HC_UNIT)')dnl

define(`HC_D0001', `HC_vect(2.5, 0.3)')dnl
define(`HC_D0010', `HC_vect(0, 1)')dnl
define(`HC_D0100', `HC_vect(0.6, 0.3)')dnl
define(`HC_D1000', `HC_vect(1, 0)')dnl

G0000: HC_vect(0, 0)
G0001: G0000 + HC_D0001
G0010: G0000 + HC_D0010
G0011: G0000 + HC_D0001 + HC_D0010
G0100: G0000 + HC_D0100
G0101: G0000 + HC_D0100 + HC_D0001
G0110: G0000 + HC_D0100 + HC_D0010
G0111: G0000 + HC_D0100 + HC_D0010 + HC_D0001
G1000: G0000 + HC_D1000
G1001: G0000 + HC_D1000 + HC_D0001
G1010: G0000 + HC_D0010 + HC_D1000
G1011: G0000 + HC_D0010 + HC_D1000 + HC_D0001
G1100: G0000 + HC_D0100 + HC_D1000
G1101: G0000 + HC_D0100 + HC_D1000 + HC_D0001
G1110: G0000 + HC_D0100 + HC_D0010 + HC_D1000
G1111: G0000 + HC_D0100 + HC_D0010 + HC_D1000 + HC_D0001

ZERO: G0000 + HC_vect(-1.2, 0.2)
move to ZERO
arrow right thickness 1.5
"\Large{$x_1$}" ljust
move to ZERO
arrow up right thickness 1.5
"\Large{$x_2$}" above
move to ZERO
arrow up thickness 1.5
"\Large{$x_3$}" above
move to ZERO
arrow up right 1.5 dashed thickness 1.5
"\Large{$x_4$}" ljust

define(`HC_VERTEX',`dnl
define(`m4p', $1)dnl
define(`m4col', `ifelse(`$2',,"black",`$2')')dnl
circle shaded m4col outlined "black" radius HC_scalar(0.05) at G`'m4p
"\Large{$1}" at G`'m4p + HC_vect(0.2, -0.1)
')

define(`HC_LINE', `dnl
define(`m4dotted', `ifelse(`$3',,,`$3')')dnl
line from G`'$1 to G`'$2 thickness 1.5 m4dotted chop HC_scalar(0.05)
')

HC_LINE(0000, 0001, dashed)
HC_LINE(0000, 0010)
HC_LINE(0000, 0100)
HC_LINE(0000, 1000)

HC_LINE(0001, 0011)
HC_LINE(0001, 0101)
HC_LINE(0001, 1001)

HC_LINE(0010, 0011, dashed)
HC_LINE(0010, 0110)
HC_LINE(0010, 1010)

HC_LINE(0011, 0111)
HC_LINE(0011, 1011)

HC_LINE(0100, 0101, dashed)
HC_LINE(0100, 0110)
HC_LINE(0100, 1100)

HC_LINE(0101, 0111)
HC_LINE(0101, 1101)

HC_LINE(0110, 0111, dashed)
HC_LINE(0110, 1110)

HC_LINE(0111, 1111)

HC_LINE(1000, 1001, dashed)
HC_LINE(1000, 1010)
HC_LINE(1000, 1100)

HC_LINE(1001, 1011)
HC_LINE(1001, 1101)

HC_LINE(1010, 1011, dashed)
HC_LINE(1010, 1110)

HC_LINE(1011, 1111)

HC_LINE(1100, 1101, dashed)
HC_LINE(1100, 1110)

HC_LINE(1101, 1111)

HC_LINE(1110, 1111, dashed)
HC_VERTEX(0000, "white")
HC_VERTEX(0001, "white")
HC_VERTEX(0010, "black")
HC_VERTEX(0011, "black")
HC_VERTEX(0100, "white")
HC_VERTEX(0101, "black")
HC_VERTEX(0110, "black")
HC_VERTEX(0111, "black")
HC_VERTEX(1000, "black")
HC_VERTEX(1001, "black")
HC_VERTEX(1010, "black")
HC_VERTEX(1011, "black")
HC_VERTEX(1100, "white")
HC_VERTEX(1101, "black")
HC_VERTEX(1110, "black")
HC_VERTEX(1111, "black")
.PE
