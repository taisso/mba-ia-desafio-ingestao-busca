from search import search_prompt

OUT_OF_CONTEXT_TEXT = "Não tenho informações necessárias para responder sua pergunta."

def main():
    while True:
        print("1 - Para fazer sua pergunta")
        print("2 - Sair")
        option = input("Escolha uma opção: ")

        if option == "2":
            print("Saindo...")
            break

        if option != "1":
            print("Opção inválida. Tente novamente.\n")
            continue

        question = input("Faça sua pergunta: ")

        if not question:
            print("Pergunta não pode ser vazia!")

        chain = search_prompt(question)

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return
        

        if OUT_OF_CONTEXT_TEXT in chain:
            print("\nPerguntas fora do contexto:\n")
        else:
            print("\n")
        
        print(f"PERGUNTA: {question}")
        print(f"RESPOSTA: {chain}")
        print("\n---\n")

    
     
    
if __name__ == "__main__":
    main()
