import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'CLASS', 'PUBLIC', 'VOID', 'IDENTIFIER', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON',
)

# Expresiones regulares para tokens simples
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'

# Reglas para tokens más complejos
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == 'class':
        t.type = 'CLASS'
    elif t.value == 'public':
        t.type = 'PUBLIC'
    elif t.value == 'void':
        t.type = 'VOID'
    return t

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Regla para manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Error handling
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Definición de la gramática
def p_class_declaration(p):
    '''class_declaration : CLASS IDENTIFIER LBRACE method_declaration_list RBRACE'''
    p[0] = ('class_declaration', p[2], p[4])

def p_method_declaration(p):
    '''method_declaration : PUBLIC VOID IDENTIFIER LPAREN RPAREN LBRACE RBRACE'''
    p[0] = ('method_declaration', p[3])

def p_method_declaration_list(p):
    '''method_declaration_list : method_declaration 
                                | method_declaration_list method_declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Otras reglas gramaticales pueden ser añadidas aquí

# Error handling
def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Función para analizar el código fuente y construir el AST
def parse(source_code):
    return parser.parse(source_code)

# Ejemplo de uso
source_code = '''
public class ParsingImgLink {
    String url, imgLink, line;

    public ParsingImgLink( String baseURL, String str ) {
        url = baseURL;
        line = str;
        parsingLine();
    }

    public void parsingLine() {
        int end;
        String imgURLStr = null;
        if( ( url = line.indexOf("src=\"") ) != -1 ) {
            String subStr = line.substring(+5);
            end = subStr.indexOf("\"");
            imgURLStr = subStr.substring( 0, end );
            System.out.println(imgURLStr);
        }
        else if( ( end = line.indexOf("SRC=\"")) != -1 ) {
            String subStr = line.substring(+5);
            end = subStr.indexOf("\"");
            imgURLStr = subStr.substring( 0, end );
            System.out.println(imgURLStr);
        }

        if( imgURLStr.indexOf("://") == -1 ) {
            try {
                URL baseURL = new URL( url );
                URL imgURL = new URL( baseURL, imgURLStr );
                imgLink = imgURL.toString();
            }
            catch( MalformedURLException mue ) {
                String msg = "Unable parse URL !";
                System.err.println( msg );
            }
        }
    }

    public String getImgLink() {
        return imgLink;
    }
}
'''

result = parse(source_code)
print(result)
