/*
Код для перевірки граматики заданої за допомогою РБНФ
*/




keyword =
tokenINTEGER16 |
tokenCOMMA |
tokenNOT |
tokenAND |
tokenOR |
tokenEQUAL |
tokenNOTEQUAL |
tokenLESSOREQUAL |
tokenGREATEROREQUAL |
tokenPLUS |
tokenMINUS |
tokenMUL |
tokenDIV |
tokenMOD |
tokenGROUPEXPRESSIONBEGIN |
tokenGROUPEXPRESSIONEND |
tokenLRBIND |
tokenCOLON |
tokenELSE |
tokenIF |
tokenWHILE |
tokenPUT |
tokenGET |
tokenNAME |
tokenBODY |
tokenDATA |
tokenBEGIN |
tokenEND |
tokenBEGINBLOCK |
tokenENDBLOCK |
tokenLEFTSQUAREBRACKETS |
tokenRIGHTSQUAREBRACKETS |
tokenSEMICOLON;
tokens_in_program = SAME_RULE(token_iteration);
token = keyword | ident | value;
token_iteration = token >> token_iteration | "";
digit = digit_0 | non_zero_digit;
digit_optional = digit | "";
non_zero_digit = digit_1 | digit_2 | digit_3 | digit_4 | digit_5 | digit_6 | digit_7 | digit_8 | digit_9;
unsigned_value = (non_zero_digit >> digit_optional | digit_0) >> BOUNDARIES;

value = sign_optional >> unsigned_value >> BOUNDARIES;
letter_in_lower_case = a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z;
letter_in_upper_case = A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z;
ident = letter_in_lower_case >> letter_in_lower_case >>
letter_in_lower_case >> letter_in_lower_case >>
digit >> STRICT_BOUNDARIES;
sign = sign_plus | sign_minus;
sign_optional = sign | "";
sign_plus = SAME_RULE(tokenPLUS);
sign_minus = SAME_RULE(tokenMINUS);
digit_0 = '0';
digit_1 = '1';
digit_2 = '2';
digit_3 = '3';
digit_4 = '4';
digit_5 = '5';
digit_6 = '6';
digit_7 = '7';
digit_8 = '8';
digit_9 = '9';
tokenLRBIND = ":>" >> BOUNDARIES;
tokenCOLON = ":" >> BOUNDARIES;
tokenINTEGER16 = "Integer" >> STRICT_BOUNDARIES;
tokenCOMMA = "," >> BOUNDARIES;
tokenNOT = "!!" >> STRICT_BOUNDARIES;
tokenAND = "And" >> STRICT_BOUNDARIES;
tokenOR = "||" >> STRICT_BOUNDARIES;
tokenEQUAL = "==" >> BOUNDARIES;
tokenNOTEQUAL = "!=" >> BOUNDARIES;
tokenLESSOREQUAL = "Le" >> BOUNDARIES;
tokenGREATEROREQUAL = "Ge" >> BOUNDARIES;
tokenPLUS = "+" >> BOUNDARIES;
tokenMINUS = "-" >> BOUNDARIES;
tokenMUL = "Mul" >> BOUNDARIES;
tokenDIV = "Div" >> STRICT_BOUNDARIES;
tokenMOD = "Mod" >> STRICT_BOUNDARIES;
tokenGROUPEXPRESSIONBEGIN = "(" >> BOUNDARIES;
tokenGROUPEXPRESSIONEND = ")" >> BOUNDARIES;
tokenELSE = "Else" >> STRICT_BOUNDARIES;
tokenIF = "If" >> STRICT_BOUNDARIES;
tokenWHILE = "While" >> STRICT_BOUNDARIES;
tokenGET = "Input" >> STRICT_BOUNDARIES;
tokenPUT = "Output" >> STRICT_BOUNDARIES;
tokenNAME = "Program" >> STRICT_BOUNDARIES;
tokenBODY = "Body" >> STRICT_BOUNDARIES;
tokenDATA = "Data" >> STRICT_BOUNDARIES;
tokenBEGIN = "Start" >> STRICT_BOUNDARIES;
tokenEND = "Finish" >> STRICT_BOUNDARIES;
tokenBEGINBLOCK = "{" >> BOUNDARIES;
tokenENDBLOCK = "}" >> BOUNDARIES;
tokenLEFTSQUAREBRACKETS = "[" >> BOUNDARIES;
tokenRIGHTSQUAREBRACKETS = "]" >> BOUNDARIES;
tokenSEMICOLON = ";" >> BOUNDARIES;
STRICT_BOUNDARIES = (BOUNDARY >> *(BOUNDARY)) | (!(qi::alpha | qi::char_("_")));
BOUNDARIES = (BOUNDARY >> *(BOUNDARY) | NO_BOUNDARY);
BOUNDARY = BOUNDARY_SPACE | BOUNDARY_TAB | BOUNDARY_CARRIAGE_RETURN | BOUNDARY_LINE_FEED | BOUNDARY_NULL;
BOUNDARY_SPACE = " ";
BOUNDARY_TAB = "\t";
BOUNDARY_CARRIAGE_RETURN = "\r";
BOUNDARY_LINE_FEED = "\n";
BOUNDARY_NULL = "\0";
NO_BOUNDARY = "";
tokenUNDERSCORE = "_";
A = "A";
B = "B";
C = "C";
D = "D";
E = "E";
F = "F";
G = "G";
H = "H";
I = "I";
J = "J";
K = "K";
L = "L";
M = "M";
N = "N";
O = "O";
P = "P";
Q = "Q";
R = "R";
S = "S";
T = "T";
U = "U";
V = "V";
W = "W";
X = "X";
Y = "Y";
Z = "Z";
a = "a";
b = "b";
c = "c";
d = "d";
e = "e";
f = "f";
g = "g";
h = "h";
i = "i";
j = "j";
k = "k";
l = "l";
m = "m";
n = "n";
o = "o";
p = "p";
q = "q";
r = "r";
s = "s";
t = "t";
u = "u";
v = "v";
w = "w";
x = "x";
y = "y";
z = "z";
