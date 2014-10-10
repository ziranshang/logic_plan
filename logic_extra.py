from logic import Expr
from logic import conjuncts
from logic import disjuncts
from logic import is_symbol

def is_valid_cnf(exp):
    if not isinstance(exp, Expr):
        print "Input is not an expression."
        return False
    
    clauses = conjuncts(exp);
    
    for c in clauses:
        literals = disjuncts(c)
        
        for lit in literals:
            if len(lit.args) == 0:
                symbol = lit;
            elif len(lit.args) == 1:
                symbol = lit.args[0]
                
                if len(symbol.args) != 0:
                    print "Found a NOT outside of %s" % symbol
                    return False
                
            else:
                print "Found %s where only a literal should be." % lit
                return False
    
            symbol_str = str(symbol)
    
            if not is_symbol(symbol_str):
                print "%s is not a valid symbol." % symbol_str
                return False
            elif not symbol_str[0].isupper():
                print "The symbol %s must begin with an upper-case letter." % symbol_str
                return False
            elif symbol_str == 'TRUE':
                print "TRUE is not a valid symbol." % symbol_str
                return False
            elif symbol_str == 'FALSE':
                print "FALSE is not a valid symbol." % symbol_str
                return False
        
    return True