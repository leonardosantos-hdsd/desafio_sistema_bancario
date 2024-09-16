saldo = 0
LIMITE_VALOR_SAQUES = 1500
valor_total_saques = 0
LIMITE_VALOR_POR_SAQUE = 500
LIMITE_SAQUES = 3
quantidade_saques = 0
SISTEMA = True
historico_transacoes = []
usuarios = []
contas = []
numero_conta = 1

menu_de_opcoes = """
    [C] Criar Usuário
    [N] Criar Conta Corrente
    [D] Depositar
    [E] Extrato
    [S] Sacar
    [L] Listar Contas
    [Q] Sair
"""

def verificar_transacao(resposta):
    match resposta:
        case "C":
            criar_usuario()
        case "N":
            criar_conta_corrente()
        case "D":
            depositar()
        case "E":
            extrato()
        case "S":
            sacar()
        case "L":
            listar_contas()
        case "Q":
            sair()
        case _:
            print("Operação inválida!\n")

def criar_usuario():
    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ")
    cpf = input("CPF: ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cpf = ''.join(filter(str.isdigit, cpf))
    if any(user['cpf'] == cpf for user in usuarios):
        print("Usuário já cadastrado com este CPF.\n")
        return
    usuarios.append({
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    })
    print(f"Usuário {nome} criado com sucesso.\n")

def criar_conta_corrente():
    global numero_conta
    cpf_usuario = input("CPF do usuário: ")
    usuario = next((u for u in usuarios if u['cpf'] == cpf_usuario), None)
    if usuario is None:
        print("Usuário não encontrado.\n")
        return
    contas.append({
        'agencia': '0001',
        'numero_conta': numero_conta,
        'usuario': usuario,
        'saldo': 0
    })
    print(f"Conta {numero_conta} criada com sucesso para o usuário {usuario['nome']}.\n")
    numero_conta += 1

def depositar():
    numero_conta = int(input("Digite o número da conta: "))
    cpf_usuario = input("Digite o CPF do usuário: ")
    conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)
    if conta is None or conta['usuario']['cpf'] != ''.join(filter(str.isdigit, cpf_usuario)):
        print("Conta ou CPF do usuário não encontrados.\n")
        return

    try:
        valor = float(input("Digite o valor que deseja depositar: "))
        if valor > 0:
            conta['saldo'] += valor
            registrar_extrato("DEPOSITAR", f"{valor:.2f}", conta['saldo'], conta['numero_conta'])
            print("Depósito realizado com sucesso.\n")
        else:
            print("O valor do depósito deve ser positivo.\n")
    except ValueError:
        print("Entrada inválida. Digite um número válido.\n")

def registrar_extrato(transacao, valor, saldo, numero_conta):
    historico_transacoes.append({
        "tipo": transacao,
        "valor": valor,
        "saldo": saldo,
        "numero_conta": numero_conta
    })

def extrato():
    numero_conta = int(input("Digite o número da conta: "))
    cpf_usuario = input("Digite o CPF do usuário: ")
    conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)
    if conta is None or conta['usuario']['cpf'] != ''.join(filter(str.isdigit, cpf_usuario)):
        print("Conta ou CPF do usuário não encontrados.\n")
        return

    transacoes = [t for t in historico_transacoes if t['numero_conta'] == numero_conta]
    if transacoes:
        for transacao in transacoes:
            print(f"Tipo: {transacao['tipo']}, Valor: R$ {transacao['valor']}, Saldo: R$ {transacao['saldo']}\n")
    else:
        print("Nenhuma transação registrada.\n")

def sacar():
    global valor_total_saques, quantidade_saques
    numero_conta = int(input("Digite o número da conta: "))
    cpf_usuario = input("Digite o CPF do usuário: ")
    conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)
    if conta is None or conta['usuario']['cpf'] != ''.join(filter(str.isdigit, cpf_usuario)):
        print("Conta ou CPF do usuário não encontrados.\n")
        return

    try:
        valor = float(input("Digite o valor que deseja sacar: "))
        if valor <= 0:
            print("O valor do saque deve ser positivo.\n")
            return

        if valor > conta['saldo']:
            print("Saldo insuficiente.\n")
            return

        if quantidade_saques >= LIMITE_SAQUES:
            print("Você ultrapassou a quantidade de saques permitida.\n")
            return

        if valor > LIMITE_VALOR_POR_SAQUE:
            print("Você ultrapassou o valor por saque permitido.\n")
            return
        
        if valor_total_saques + valor > LIMITE_VALOR_SAQUES:
            print("Você ultrapassou o valor de saques permitido por dia.\n")
            return

        conta['saldo'] -= valor
        quantidade_saques += 1
        valor_total_saques += valor
        registrar_extrato("SACAR", f"{valor:.2f}", conta['saldo'], conta['numero_conta'])
        print("Saque realizado com sucesso.\n")
        
    except ValueError:
        print("Entrada inválida. Digite um número válido.\n")

def listar_contas():
    if contas:
        for conta in contas:
            print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Cliente: {conta['usuario']['nome']}, Saldo: R$ {conta['saldo']}")
    else:
        print("Nenhuma conta registrada.\n")

def sair():
    global SISTEMA
    SISTEMA = False

def main():
    global SISTEMA
    while SISTEMA:
        try:
            resposta = input(menu_de_opcoes).upper()
            verificar_transacao(resposta)
        except Exception as e:
            print(f"Ocorreu um erro: {e}\n")

    print("Obrigado pela preferência!\n")

if __name__ == "__main__":
    main()
