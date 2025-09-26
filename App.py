import flet as ft
import requests

BASE_URL = "http://10.135.235.27:5002"


def main(page: ft.Page):
    page.title = "SmartSell"
    page.session.set("token", None)
    page.session.set("user", None)
    page.window.height = 800
    page.window.width = 378

    def api_request(method, endpoint, data=None):
        headers = {}
        token = page.session.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        url = f"{BASE_URL}{endpoint}"
        try:
            r = requests.request(method, url, json=data, headers=headers, timeout=8)
            try:
                return r.status_code, r.json()
            except:
                return r.status_code, {"msg": r.text}
        except requests.exceptions.RequestException as e:
            return 0, {"msg": f"Erro de conexão: {e}"}

    # ---------------- VIEWS ----------------
    def login_view():
        email = ft.TextField(
            label="EMAIL",
            prefix_icon=ft.Icons.EMAIL,
            border_color=ft.Colors.AMBER,
            border_radius=10,
            focused_border_color=ft.Colors.AMBER,
            width=300,
            color = ft.Colors.BLACK
        )

        senha = ft.TextField(
            label="SENHA",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            border_color=ft.Colors.AMBER,
            border_radius=10,
            focused_border_color=ft.Colors.AMBER,
            width=300,
            color = ft.Colors.BLACK
        )
        def do_login(e):
            status, res = api_request("POST", "/login", {
                "email": email.value,
                "senha": senha.value
            })
            if status == 200:
                page.session.set("token", res["access_token"])
                st, rme = api_request("GET", "/me")
                if st == 200:
                    page.session.set("user", rme)
                else:
                    page.session.set("user", {"nome": res.get("nome"), "email": email.value})
                page.snack_bar = ft.SnackBar(ft.Text("Login realizado!"), open=True)
                page.update()
                go_menu()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(res.get("msg", "Credenciais inválidas")), open=True)
                page.update()

        return ft.View(
            "/login",
            bgcolor=ft.Colors.AMBER_50,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE,
                                size=120,
                                color=ft.Colors.RED
                            ),
                            email,
                            senha,
                            ft.ElevatedButton(
                                "ENTRAR",
                                on_click=do_login,
                                bgcolor=ft.Colors.RED,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=20
                                ),
                                width=150
                            ),
                            ft.Text(
                                "NOVO USUÁRIO?\nENTÃO",
                                size=14,
                                weight="bold",
                                text_align="center",
                                color=ft.Colors.BLACK,
                                spans=[
                                    ft.TextSpan(
                                        " CADASTRE-SE",
                                        ft.TextStyle(color=ft.Colors.RED),
                                        on_click=lambda _: go_cadastro()  # <<< aqui troca de rota
                                    )
                                ]
                            ),
                        ],
                        alignment="center",
                        horizontal_alignment="center",
                        spacing=25
                    )
                )
            ]
        )

    def cadastro_view():
        nome = ft.TextField(
            label="NOME",
            label_style=ft.TextStyle( weight="bold"),
            prefix_icon=ft.Icons.PERSON,
            border_color=ft.Colors.AMBER,
            border_radius=10,
            focused_border_color=ft.Colors.AMBER,
            color=ft.Colors.BLACK,
            width=300
        )

        email = ft.TextField(
            label="EMAIL",
            label_style=ft.TextStyle( weight="bold"),
            prefix_icon=ft.Icons.EMAIL,
            border_color=ft.Colors.AMBER,
            border_radius=10,
            focused_border_color=ft.Colors.AMBER,
            color=ft.Colors.BLACK,
            width=300
        )

        telefone = ft.TextField(
            label="TELEFONE",
            label_style=ft.TextStyle( weight="bold"),
            prefix_icon=ft.Icons.PHONE,
            border_color=ft.Colors.AMBER,
            border_radius=10,
            focused_border_color=ft.Colors.AMBER,
            color=ft.Colors.BLACK,
            width=300
        )

        senha = ft.TextField(
            label="SENHA",
            label_style=ft.TextStyle( weight="bold"),
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            border_color=ft.Colors.AMBER,
            border_radius=10,
            focused_border_color=ft.Colors.AMBER,
            color=ft.Colors.BLACK,
            width=300
        )
        def do_cadastro(e):
            status, res = api_request("POST", "/cadastro/usuario", {
                "nome": nome.value,
                "telefone": telefone.value,
                "email": email.value,
                "senha": senha.value
            })
            if status == 201:
                page.snack_bar = ft.SnackBar(ft.Text("Cadastro realizado! Faça login."), open=True)
                page.update()
                go_login()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(res.get("msg", "Erro no cadastro")), open=True)
                page.update()

        return ft.View(
            "/cadastro",
            bgcolor=ft.Colors.AMBER_50,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        [
                            # Ícone topo
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE,
                                size=120,
                                color=ft.Colors.RED
                            ),

                            # Campos
                            nome,
                            email,
                            telefone,
                            senha,

                            # Texto "já tem uma conta? entre agora"
                            ft.Text(
                                spans=[
                                    ft.TextSpan("JÁ TEM UMA CONTA?",
                                                ft.TextStyle(color=ft.Colors.BLACK, weight="bold")),
                                    ft.TextSpan(" "),
                                    ft.TextSpan(
                                        "ENTRE AGORA",
                                        ft.TextStyle(color=ft.Colors.RED, weight="bold"),
                                        on_click=lambda _: go_login()
                                    )
                                ],
                                text_align="center"
                            ),

                            # Botão Criar
                            ft.ElevatedButton(
                                "CRIAR",
                                on_click=do_cadastro,
                                bgcolor=ft.Colors.RED,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=20
                                ),
                                width=150
                            ),
                        ],
                        alignment="center",
                        horizontal_alignment="center",
                        spacing=20
                    )
                )
            ]
        )
    def menu_view():
        user = page.session.get("user") or {}
        bem = f"Bem-vindo, {user.get('nome','Usuário')}!"
        return ft.View(
            "/menu",
            controls=[
                ft.AppBar(title=ft.Text("Menu Principal")),
                ft.Column([
                    ft.Text(bem, size=20, weight="bold"),
                    ft.ElevatedButton("Cardápio", on_click=lambda _: go_cardapio()),
                    ft.ElevatedButton("Pedidos", on_click=lambda _: go_pedidos()),
                    ft.ElevatedButton("Editar Usuário", on_click=lambda _: go_editar_usuario()),
                    ft.ElevatedButton("Sair", on_click=lambda _: do_logout())
                ], alignment="center", horizontal_alignment="center")
            ]
        )

    page.session.set("carrinho", [])

    def cardapio_view():
        user = page.session.get("user") or {}
        nome = user.get("nome", "Usuário").upper()

        st, res = api_request("GET", "/cardapio")
        itens = res.get("cardapio", []) if st == 200 else []

        lista = []
        for item in itens:
            def make_handler(pid):
                return lambda e: go_comprar(pid)

            lista.append(
                ft.Container(
                    content=ft.Row([
                        ft.Image(src="https://cdn-icons-png.flaticon.com/512/3075/3075977.png", width=60, height=60),
                        ft.Column([
                            ft.Text(item["nome"], weight="bold", size=16),
                            ft.Text(f"R$ {item.get('preco', 0):.2f}", color=ft.Colors.RED),
                        ]),
                        ft.Row([
                            ft.IconButton(ft.Icons.SHOPPING_CART, on_click=lambda e, it=item: add_to_carrinho(it))
                        ], spacing=5),
                            ft.ElevatedButton("COMPRAR", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE,
                                              on_click=make_handler(item["id"])),


                    ], alignment="spaceBetween"),
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    margin=5
                )
            )

        return ft.View(
            "/cardapio",
            bgcolor=ft.Colors.AMBER_50,
            controls=[
                ft.Column([
                    # TOPO vermelho
                    ft.Container(
                        bgcolor=ft.Colors.RED,
                        padding=15,
                        alignment=ft.alignment.center,
                        content=ft.Text(f"OLÁ {nome}", size=20, weight="bold", color=ft.Colors.WHITE)
                    ),

                    # Abas PROMOÇÃO e MENU
                    ft.Row([
                        ft.Container(
                            content=ft.Text("PROMOÇÃO", size=22, weight="bold", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.AMBER,
                            expand=True,
                            padding=10,
                            alignment=ft.alignment.center,
                            on_click=lambda _: go_promocoes()
                        ),
                        ft.Container(
                            content=ft.Text("MENU", size=22, weight="bold", color=ft.Colors.RED),
                            bgcolor=ft.Colors.AMBER_50,
                            expand=True,
                            padding=10,
                            alignment=ft.alignment.center,
                            on_click=lambda _: go_cardapio()
                        ),
                    ], spacing=5),

                    # Lista rolável
                    ft.Column(lista, scroll="auto", expand=True) if lista else ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Text("Nenhum item no cardápio.")
                    ),

                    # Rodapé
                    ft.Container(
                        bgcolor=ft.Colors.AMBER_100,
                        padding=10,
                        content=ft.Row(
    [
        ft.IconButton(ft.Icons.RESTAURANT_MENU, on_click=lambda _: go_cardapio()),
        ft.IconButton(ft.Icons.HOME, on_click=lambda _: go_menu()),
        ft.IconButton(ft.Icons.SHOPPING_CART, on_click=lambda _: go_carrinho()),  # novo ícone
        ft.IconButton(ft.Icons.PERSON, on_click=lambda _: go_editar_usuario())
    ],
    alignment="spaceAround"
)

                    )
                ], expand=True, spacing=0)
            ]
        )

    def add_to_carrinho(item):
        carrinho = page.session.get("carrinho") or []

        # Verifica se já existe no carrinho
        for c in carrinho:
            if c["id"] == item["id"]:
                c["quantidade"] += 1
                break
        else:
            carrinho.append({
                "id": item["id"],
                "nome": item["nome"],
                "preco": item.get("preco", 0),
                "quantidade": 1
            })

        page.session.set("carrinho", carrinho)
        page.snack_bar = ft.SnackBar(ft.Text(f"{item['nome']} adicionado ao carrinho!"), open=True)
        page.update()

    def promocoes_view():
        user = page.session.get("user") or {}
        nome = user.get("nome", "Usuário").upper()

        st, res = api_request("GET", "/cardapio")
        itens = res.get("cardapio", []) if st == 200 else []

        promocoes = [p for p in itens if p.get("status_promocao")]

        lista = []
        for p in promocoes:
            def make_handler(pid):
                return lambda e: go_comprar(pid)

            preco = p.get("preco", 0)
            preco_final = p.get("preco_final", preco)

            preco_texto = ft.Row([
                ft.Text(
                    f"De: R$ {preco:.2f}",
                    color=ft.Colors.BLACK54,
                    size=10,  # menor
                    style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
                ),
                ft.Text(
                    f"  Por: R$ {preco_final:.2f}",
                    color=ft.Colors.RED,
                    weight="bold",
                    size=12  # menor
                ),
            ])

            lista.append(
                ft.Container(
                    content=ft.Row([
                        ft.Image(src="https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
                                 width=40, height=40),  # imagem menor
                        ft.Column([
                            ft.Text("🔥 Promoção do Dia 🔥", weight="bold", size=12, color=ft.Colors.RED),
                            ft.Text(p["nome"], weight="bold", size=14),  # menor
                            preco_texto
                        ]),
                        ft.ElevatedButton("COMPRAR",
                                          bgcolor=ft.Colors.RED,
                                          color=ft.Colors.WHITE,
                                          on_click=make_handler(p["id"]),
                                          style=ft.ButtonStyle(padding=5))  # botão menor
                    ], alignment="spaceBetween"),
                    padding=5,  # padding menor
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    margin=5
                )
            )

        return ft.View(
            "/promocoes",
            bgcolor=ft.Colors.AMBER_50,
            controls=[
                ft.Column([
                    ft.Container(
                        bgcolor=ft.Colors.RED,
                        padding=15,
                        alignment=ft.alignment.center,
                        content=ft.Text(f"OLÁ {nome}", size=20, weight="bold", color=ft.Colors.WHITE)
                    ),
                    ft.Row([
                        ft.Container(
                            content=ft.Text("PROMOÇÃO", size=22, weight="bold", color=ft.Colors.RED),
                            bgcolor=ft.Colors.AMBER_50,
                            expand=True,
                            padding=10,
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            content=ft.Text("MENU", size=22, weight="bold", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.AMBER,
                            expand=True,
                            padding=10,
                            alignment=ft.alignment.center,
                            on_click=lambda _: go_cardapio()
                        ),
                    ], spacing=0),
                    ft.Column(lista, scroll="auto", expand=True) if lista else ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Text("Nenhuma promoção disponível.")
                    ),
                    ft.Container(
                        bgcolor=ft.Colors.AMBER_100,
                        padding=10,
                        content=ft.Row(
    [
        ft.IconButton(ft.Icons.RESTAURANT_MENU, on_click=lambda _: go_cardapio()),
        ft.IconButton(ft.Icons.HOME, on_click=lambda _: go_menu()),
        ft.IconButton(ft.Icons.SHOPPING_CART, on_click=lambda _: go_carrinho()),  # novo ícone
        ft.IconButton(ft.Icons.PERSON, on_click=lambda _: go_editar_usuario())
    ],
    alignment="spaceAround"
)

                    )
                ], expand=True, spacing=0)
            ]
        )

    def carrinho_view():
        carrinho = page.session.get("carrinho") or []

        def comprar_tudo(e):
            # faz pedidos para todos os itens do carrinho
            sucesso = 0
            falha = 0
            for item in carrinho:
                st, res = api_request("POST", "/cadastrar/pedido/logado", {
                    "produto_id": item["id"],
                    "quantidade": item["quantidade"]
                })
                if st in (200, 201):
                    sucesso += 1
                else:
                    falha += 1
            # limpa carrinho
            page.session.set("carrinho", [])
            msg = f"{sucesso} pedido(s) realizado(s) com sucesso!"
            if falha:
                msg += f" {falha} falharam."
            page.snack_bar = ft.SnackBar(ft.Text(msg), open=True)
            page.update()
            go_pedidos()

        lista = []
        for i, item in enumerate(carrinho):
            lista.append(
                ft.Card(
                    ft.Container(
                        ft.Row([
                            ft.Text(f"{item['nome']} (x{item['quantidade']}) - R$ {item['preco']:.2f}")
                        ]),
                        padding=10
                    )
                )
            )

        return ft.View(
            "/carrinho",
            controls=[
                ft.AppBar(title=ft.Text("Carrinho")),
                ft.Column(lista) if lista else ft.Text("Carrinho vazio."),
                ft.Row([
                    ft.ElevatedButton("Comprar Tudo", on_click=comprar_tudo) if carrinho else ft.Text(""),
                    ft.TextButton("Voltar", on_click=lambda _: go_cardapio())
                ], alignment="center")
            ]
        )

    def pedidos_view():
        user = page.session.get("user") or {}
        nome = user.get("nome", "Usuário").upper()

        st, res = api_request("GET", "/pedidos/logado")
        pedidos = res.get("pedidos", []) if st == 200 else []

        lista = []
        for p in pedidos:
            entregue = (p.get("status", "").lower() == "entregue")

            lista.append(
                ft.Container(
                    content=ft.Row(
                        [
                            # Ícone / Imagem produto
                            ft.Container(
                                content=ft.Image(
                                    src="https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
                                    width=40,
                                    height=40,
                                    fit=ft.ImageFit.COVER
                                ),
                                width=50,
                                height=50,
                                bgcolor=ft.Colors.BROWN_200,
                                border_radius=25,
                                alignment=ft.alignment.center
                            ),

                            # Informações do pedido
                            ft.Column(
                                [
                                    ft.Text(
                                        f"{p.get('produto', 'Produto')} {p.get('valor_total', 0):.2f}",
                                        weight="bold",
                                        size=14,
                                        color=ft.Colors.BLACK
                                    ),
                                    ft.Text(
                                        f"{p.get('status', '').upper()}: {p.get('data', '')}",
                                        size=12,
                                        color=ft.Colors.BLUE if entregue else ft.Colors.BLACK54
                                    )
                                ],
                                alignment="center",
                                expand=True
                            ),

                            # Check verde se entregue
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE,
                                color=ft.Colors.GREEN,
                                size=22
                            ) if entregue else ft.Icon(
                                ft.Icons.HOURGLASS_BOTTOM,
                                color=ft.Colors.AMBER,
                                size=22
                            )
                        ],
                        alignment="spaceBetween",
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=10,
                    margin=5
                )
            )

        return ft.View(
            "/pedidos",
            bgcolor=ft.Colors.AMBER_50,
            controls=[
                ft.Column(
                    [
                        # TOPO vermelho
                        ft.Container(
                            bgcolor=ft.Colors.RED,
                            padding=15,
                            alignment=ft.alignment.center,
                            content=ft.Text(f"OLÁ {nome}", size=20, weight="bold", color=ft.Colors.WHITE)
                        ),

                        # Faixa "PEDIDOS"
                        ft.Container(
                            bgcolor=ft.Colors.AMBER_50,
                            padding=10,
                            alignment=ft.alignment.center,
                            content=ft.Text("MEUS PEDIDOS", size=18, weight="bold", color=ft.Colors.RED)
                        ),

                        # Lista expansiva
                        ft.Column(lista, scroll="auto", expand=True) if lista else ft.Container(
                            expand=True,
                            alignment=ft.alignment.center,
                            content=ft.Text("Nenhum pedido realizado.")
                        ),

                        # BARRA INFERIOR fixa
                        ft.Container(
                            bgcolor=ft.Colors.AMBER_100,
                            padding=10,
                            content=ft.Row(
    [
        ft.IconButton(ft.Icons.RESTAURANT_MENU, on_click=lambda _: go_cardapio()),
        ft.IconButton(ft.Icons.HOME, on_click=lambda _: go_menu()),
        ft.IconButton(ft.Icons.SHOPPING_CART, on_click=lambda _: go_carrinho()),  # novo ícone
        ft.IconButton(ft.Icons.PERSON, on_click=lambda _: go_editar_usuario())
    ],
    alignment="spaceAround"
)

                        )
                    ],
                    expand=True,
                    spacing=0
                )
            ]
        )

    def editar_usuario_view():
        user = page.session.get("user") or {}
        nome = ft.TextField(label="Nome", value=user.get("nome",""))
        telefone = ft.TextField(label="Telefone", value=user.get("telefone",""))
        email = ft.TextField(label="Email", value=user.get("email",""))
        senha = ft.TextField(label="Senha (deixe vazio se não trocar)", password=True, can_reveal_password=True)

        def salvar(e):
            payload = {
                "nome": nome.value,
                "telefone": telefone.value,
                "email": email.value
            }
            if senha.value and senha.value.strip():
                payload["senha"] = senha.value.strip()

            st, res = api_request("PUT", "/editar/usuario/logado", payload)
            if st == 200:
                # atualiza sessão com o objeto retornado (res["usuario"])
                page.session.set("user", res.get("usuario", payload))
                page.snack_bar = ft.SnackBar(ft.Text("Dados atualizados com sucesso!"), open=True)
            else:
                page.snack_bar = ft.SnackBar(ft.Text(res.get("msg", "Erro ao atualizar")), open=True)
            page.update()

        return ft.View(
            "/editar_usuario",
            controls=[
                ft.AppBar(title=ft.Text("Editar Usuário")),
                ft.Column([nome, telefone, email, senha, ft.ElevatedButton("Salvar", on_click=salvar),
                           ft.TextButton("Voltar", on_click=lambda _: go_menu())], alignment="center")
            ],


        )

    ft.Row(
        [
            ft.IconButton(ft.Icons.RESTAURANT_MENU, on_click=lambda _: go_cardapio()),
            ft.IconButton(ft.Icons.HOME, on_click=lambda _: go_menu()),
            ft.IconButton(ft.Icons.SHOPPING_CART, on_click=lambda _: go_carrinho()),  # novo ícone
            ft.IconButton(ft.Icons.PERSON, on_click=lambda _: go_editar_usuario())
        ],
        alignment="spaceAround"
    )

    def comprar_view(item_id):
        quantidade = ft.TextField(label="Quantidade", value="1")

        def confirmar(e):
            try:
                qtd = int(quantidade.value)
                if qtd <= 0:
                    qtd = 1
            except:
                qtd = 1

            payload = {
                "produto_id": item_id,
                "quantidade": qtd,
                "metodo_pagamento": "pix"  # ou "cartao", conforme API
            }

            st, res = api_request("POST", "/cadastrar/pedido/logado", payload)
            if st in (200, 201):
                page.snack_bar = ft.SnackBar(ft.Text("Pedido realizado com sucesso!"), open=True)
                page.update()
                go_pedidos()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(res.get("msg", "Erro ao efetuar pedido")), open=True)
                page.update()

        return ft.View(
            f"/comprar/{item_id}",
            controls=[
                ft.AppBar(title=ft.Text("Comprar Produto")),
                ft.Column([ft.Text(f"Confirmar compra do produto ID {item_id}"), quantidade,
                           ft.ElevatedButton("Confirmar Compra", on_click=confirmar),
                           ft.TextButton("Voltar", on_click=lambda _: go_cardapio())], alignment="center")
            ]

        )

    # ---------- helpers de navegação ----------
    def do_logout():
        page.session.set("token", None)
        page.session.set("user", None)
        page.snack_bar = ft.SnackBar(ft.Text("Desconectado"), open=True)
        page.update()
        go_login()

    def go_login(): page.go("/login")
    def go_cadastro(): page.go("/cadastro")
    def go_menu(): page.go("/menu")
    def go_cardapio(): page.go("/cardapio")
    def go_pedidos(): page.go("/pedidos")
    def go_editar_usuario(): page.go("/editar_usuario")
    def go_comprar(pid): page.go(f"/comprar/{pid}")
    def go_carrinho(): page.go("/carrinho")
    def go_promocoes(): page.go("/promocoes")



    def route_change(e):
        route = page.route
        page.views.clear()
        if route == "/login":
            page.views.append(login_view())
        elif route == "/cadastro":
            page.views.append(cadastro_view())
        elif route == "/menu":
            page.views.append(menu_view())
        elif route == "/cardapio":
            page.views.append(cardapio_view())
        elif route == "/pedidos":
            page.views.append(pedidos_view())
        elif route == "/editar_usuario":
            page.views.append(editar_usuario_view())
        elif route == "/promocoes":
            page.views.append(promocoes_view())
        elif route == "/carrinho":
            page.views.append(carrinho_view())
        elif route.startswith("/comprar/"):
            pid = int(route.split("/")[-1])
            page.views.append(comprar_view(pid))
        page.update()

    page.on_route_change = route_change
    page.go("/login")


ft.app(target=main)