from collections import deque

# Estrutura dos itens: [codigo, nome, descricao, preco, estoque]
itens = [
    [1, "Pizza Calabresa", "Pizza grande de calabresa com queijo.", 40.0, 10],
    [2, "Refrigerante Lata", "Lata de refrigerante 350ml (Coca, Guaraná, Fanta).", 6.0, 20],
    [3, "Hambúrguer Artesanal", "Pão, carne bovina, queijo, salada e molho especial.", 18.0, 15],
    [4, "Batata Frita", "Porção média de batata frita crocante.", 10.0, 25],
    [5, "Suco Natural", "Copo 300ml (laranja, acerola ou abacaxi).", 8.0, 12],
    [6, "Pastel de Queijo", "Pastel frito recheado com queijo.", 7.0, 18],
    [7, "Salada Caesar", "Alface, frango grelhado, croutons e molho Caesar.", 22.0, 8],
    [8, "Água Mineral", "Garrafa de água mineral 500ml.", 4.0, 30]
]
codigo_item = 9

# Estrutura dos pedidos: [codigo, cliente, lista_itens, status, cupom, desconto, total]
# lista_itens: lista de [nome, qtd, preco]
fila_pendentes = deque()
fila_aceitos = deque()
fila_prontos = deque()
pedidos = []
codigo_pedido = 1

def cadastrar_item():
    global codigo_item
    nome = input("Nome do produto: ")
    descricao = input("Descrição: ")
    preco = float(input("Preço: "))
    estoque = int(input("Quantidade em estoque: "))
    item = [codigo_item, nome, descricao, preco, estoque]
    itens.append(item)
    print(f"Item cadastrado com sucesso! Código: {codigo_item}")
    codigo_item += 1

def atualizar_item():
    cod = int(input("Digite o código do item a atualizar: "))
    for item in itens:
        if item[0] == cod:
            print("Item encontrado:", item)
            item[1] = input("Novo nome: ")
            item[2] = input("Nova descrição: ")
            item[3] = float(input("Novo preço: "))
            item[4] = int(input("Novo estoque: "))
            print("Item atualizado com sucesso!")
            return
    print("Item não encontrado.")

def consultar_itens():
    print("\nItens disponíveis:")
    for item in itens:
        print(f'Código: {item[0]} | Nome: {item[1]} | Preço: R${item[3]} | Estoque: {item[4]} | Desc: {item[2]}')

def criar_pedido():
    global codigo_pedido
    if not itens:
        print("Não há itens cadastrados.")
        return
    nome_cliente = input("Nome do cliente: ")
    pedido_itens = []
    while True:
        for item in itens:
            print(f'{item[0]} - {item[1]} (R${item[3]}, Estoque: {item[4]})')
        try:
            cod_item = int(input("Digite o código do item (0 para finalizar): "))
        except ValueError:
            print("Digite um número válido.")
            continue
        if cod_item == 0:
            if not pedido_itens:
                print("Pedido não pode ser finalizado vazio!")
                continue
            else:
                break
        item_encontrado = None
        for item in itens:
            if item[0] == cod_item:
                item_encontrado = item
                break
        if not item_encontrado:
            print("Código de item inválido.")
            continue
        try:
            qtd = int(input("Quantidade: "))
        except ValueError:
            print("Digite uma quantidade válida.")
            continue
        if qtd <= 0:
            print("Quantidade deve ser maior que zero.")
            continue
        if qtd > item_encontrado[4]:
            print("Quantidade maior que o estoque disponível.")
            continue
        pedido_itens.append([item_encontrado[1], qtd, item_encontrado[3]])
        item_encontrado[4] -= qtd

    # Cupom de desconto
    cupom = input("Deseja aplicar cupom de desconto? (Digite o código ou ENTER para ignorar): ").strip()
    desconto = 0.0
    if cupom:
        if cupom.upper() == "DESC10":
            desconto = 0.10
            print("Cupom DESC10 aplicado: 10% de desconto.")
        else:
            print("Cupom inválido. Nenhum desconto aplicado.")

    total = sum(item[1] * item[2] for item in pedido_itens)
    if desconto > 0:
        total = total * (1 - desconto)

    pedido = [codigo_pedido, nome_cliente, pedido_itens, "AGUARDANDO APROVACAO", cupom if desconto > 0 else None, desconto, total]
    pedidos.append(pedido)
    fila_pendentes.append(pedido)
    print(f"Pedido criado com sucesso! Código do pedido: {codigo_pedido}")
    print(f"Cliente: {nome_cliente}")
    print(f"Total do pedido: R${total:.2f}")
    codigo_pedido += 1

def processar_pedidos_pendentes():
    if not fila_pendentes:
        print("Nenhum pedido pendente.")
        return
    while fila_pendentes:
        pedido = fila_pendentes[0]
        print(f"\nPedido #{pedido[0]} - Cliente: {pedido[1]}")
        for item in pedido[2]:
            print(f'  {item[1]}x {item[0]} - R${item[2]}')
        print(f"Total: R${pedido[6]:.2f}")
        decisao = input("Aceitar (A) ou Rejeitar (R)? ").strip().upper()
        if decisao == "A":
            pedido[3] = "ACEITO"
            fila_aceitos.append(pedido)
            print("Pedido aceito e movido para preparo (FAZENDO).")
        else:
            pedido[3] = "REJEITADO"
            print("Pedido rejeitado.")
        fila_pendentes.popleft()

def atualizar_status_pedido():
    cod = int(input("Digite o código do pedido: "))
    for pedido in pedidos:
        if pedido[0] == cod:
            print(f"Pedido atual: Status {pedido[3]}")
            print("1 - FAZENDO (preparar pedido)")
            print("2 - FEITO (pedido pronto)")
            print("3 - ESPERANDO ENTREGADOR")
            print("4 - SAIU PARA ENTREGA")
            print("5 - ENTREGUE")
            print("6 - CANCELADO")
            novo = input("Escolha o novo status: ")
            if novo == "1":
                if pedido[3] == "ACEITO":
                    pedido[3] = "FAZENDO"
                    print("Status atualizado para FAZENDO.")
                else:
                    print("Só pode preparar pedidos ACEITOS.")
            elif novo == "2":
                if pedido[3] == "FAZENDO":
                    pedido[3] = "FEITO"
                    fila_prontos.append(pedido)
                    print("Status atualizado para FEITO e movido para fila de prontos.")
                else:
                    print("Só pode finalizar pedidos FAZENDO.")
            elif novo == "3":
                if pedido[3] == "FEITO":
                    pedido[3] = "ESPERANDO ENTREGADOR"
                    print("Status atualizado para ESPERANDO ENTREGADOR.")
                else:
                    print("Só pode esperar entregador para pedidos FEITO.")
            elif novo == "4":
                if pedido[3] == "ESPERANDO ENTREGADOR":
                    pedido[3] = "SAIU PARA ENTREGA"
                    print("Status atualizado para SAIU PARA ENTREGA.")
                else:
                    print("Só pode sair para entrega pedidos ESPERANDO ENTREGADOR.")
            elif novo == "5":
                if pedido[3] == "SAIU PARA ENTREGA":
                    pedido[3] = "ENTREGUE"
                    print("Status atualizado para ENTREGUE.")
                else:
                    print("Só pode entregar pedidos que saíram para entrega.")
            elif novo == "6":
                if pedido[3] in ["AGUARDANDO APROVACAO", "ACEITO"]:
                    pedido[3] = "CANCELADO"
                    print("Pedido cancelado.")
                else:
                    print("Só pode cancelar pedidos aguardando aprovação ou aceitos.")
            else:
                print("Opção inválida.")
            return
    print("Pedido não encontrado.")

def cancelar_pedido():
    cod = int(input("Digite o código do pedido a cancelar: "))
    for pedido in pedidos:
        if pedido[0] == cod:
            if pedido[3] in ["AGUARDANDO APROVACAO", "ACEITO"]:
                pedido[3] = "CANCELADO"
                print("Pedido cancelado.")
            else:
                print("Não é possível cancelar, já está em preparo ou finalizado.")
            return
    print("Pedido não encontrado.")

def exibir_pedidos(filtro_status=None):
    print("\n--- LISTA DE PEDIDOS ---")
    encontrados = False
    for pedido in pedidos:
        if filtro_status and pedido[3] != filtro_status:
            continue
        encontrados = True
        print(f"\nPedido #{pedido[0]} - Cliente: {pedido[1]} - Status: {pedido[3]}")
        for item in pedido[2]:
            print(f'  {item[1]}x {item[0]} - R${item[2]}')
        print(f"Total: R${pedido[6]:.2f}")
        if pedido[4]:
            print(f"Cupom aplicado: {pedido[4]} ({int(pedido[5]*100)}% off)")
        print("-" * 40)
    if not encontrados:
        print("Nenhum pedido encontrado.")

def menu_consulta_pedidos():
    print("\n1 - Exibir todos os pedidos")
    print("2 - Filtrar por status")
    op = input("Escolha uma opção: ")
    if op == "1":
        exibir_pedidos()
    elif op == "2":
        print("Status possíveis: AGUARDANDO APROVACAO, ACEITO, FAZENDO, FEITO, ESPERANDO ENTREGADOR, SAIU PARA ENTREGA, ENTREGUE, CANCELADO, REJEITADO")
        status = input("Digite o status desejado: ").strip().upper()
        exibir_pedidos(filtro_status=status)
    else:
        print("Opção inválida.")

while True:
    print("\n=== MENU PRINCIPAL ===")
    print("1 - Gerenciar Menu de Itens")
    print("2 - Gerenciar Menu de Pedidos")
    print("3 - Consultar Pedidos")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print("\n--- GERENCIAR ITENS ---")
        print("1 - Cadastrar Item")
        print("2 - Atualizar Item")
        print("3 - Consultar Itens")
        sub = input("Escolha uma opção: ")
        if sub == "1":
            cadastrar_item()
        elif sub == "2":
            atualizar_item()
        elif sub == "3":
            consultar_itens()
        else:
            print("Opção inválida.")

    elif opcao == "2":
        print("\n--- GERENCIAR PEDIDOS ---")
        print("1 - Criar Pedido")
        print("2 - Processar Pedidos Pendentes")
        print("3 - Atualizar Status de Pedido")
        print("4 - Cancelar Pedido")
        sub = input("Escolha uma opção: ")
        if sub == "1":
            criar_pedido()
        elif sub == "2":
            processar_pedidos_pendentes()
        elif sub == "3":
            atualizar_status_pedido()
        elif sub == "4":
            cancelar_pedido()
        else:
            print("Opção inválida.")

    elif opcao == "3":
        menu_consulta_pedidos()

    elif opcao == "0":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida.")