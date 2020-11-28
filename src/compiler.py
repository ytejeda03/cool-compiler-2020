from sys import argv

from lexer import make_lexer
from . import parser

import type_checker
import type_builder
import type_collector

tokens = ""



def main():
    args = argv
    
    cool_program_code = ""

    # Name of the file
    p = args[2]
    print(str(p))
    if not str(p).endswith(".cl"):
        print("Cool program files must end with a \`.cl\` extension.\r\n")
        exit(1)

    try:
        with open(str(p)) as file:
            while True:
                i = file.read(1)
                if not(i):
                    break
                if i == '\0':
                    cool_program_code += r'\0'
                else:
                    cool_program_code += i
            s = cool_program_code
            
            lexer, errors = make_lexer(cool_program_code)
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)
        
            
            ast, errors = parser.parse(s)
            
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)   

            #recolectar los tipos
            _type_collector = type_collector.TypeCollectorVisitor()
            _type_collector.visit(ast)

            #construir los tipos
            _type_builder = type_builder.TypeBuilderVisitor()
            _type_builder.visit(ast, _type_collector.context)

            #chequear tipos
            _type_checker = type_checker.TypeCheckerCollector()
            errors = []
            _type_checker.visit(ast, _type_builder.context, errors)
            if len(errors) > 0:
                for er in errors:
                    print(er)
                exit(1)

                    

    except (IOError, FileNotFoundError):
        print(f"Error! File {p} not found.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred! {e}")
        exit(1)


if __name__ == "__main__":
    main()
