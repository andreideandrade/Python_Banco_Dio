import textwrap

def menu():
    menu = """\n
    ===================== MENU =======================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def titulo(titulo_nome):
    print('\n\n')
    print(titulo_nome.center(50, "="))
    
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        titulo(" Depósito realizado com sucesso! ") 
    else:
        titulo(" Operação falhou! O valor informado é inválido. ")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    if excedeu_saldo:
        titulo(" Operação falhou! Conta sem saldo suficiente. ")
    elif excedeu_limite:
        titulo(" Operação falhou! O valor excedeu o limite. ")
    elif excedeu_saques:
        titulo(" Operação falhou! Número de saques excedido. ")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        titulo(" Saque realizado com sucesso! ")
    else:
        titulo(" Operação falhou! O valor informado é inválido. ")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    titulo(" EXTRATO ")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("=" * 50)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        titulo(" Já existe usuário com esse CPF! ")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    titulo(" Usuário criado com sucesso! ")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        titulo(" Conta criada com sucesso! ")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    titulo(" Usuário não encontrado, processo encerrado! ")

def listar_contas(contas):
    if contas != []:
        for conta in contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 50)
            print(textwrap.dedent(linha))
    else :
        print("=" * 50)
        print("|        Não a contas registradas ainda.         |")           
        print("=" * 50)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d" or opcao == "D":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "s"or opcao == "S":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e" or opcao == "E":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "nu" or opcao == "NU":
            criar_usuario(usuarios)
        elif opcao == "nc" or opcao == "NC":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "lc" or opcao == "LC":
            listar_contas(contas)
        elif opcao == "q" or opcao == "Q":
            break
        else:
            titulo("Operação inválida, por favor selecione uma operação válida.")

main()
