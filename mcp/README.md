# CIC SHOP — servidor MCP

Adaptação do [exemplo de MCP da aula](https://github.com/renatoviolin/mcp-encontrabilidade/tree/main/src) para a CIC SHOP. O servidor consulta a [API publicada](https://cic-shop-backend.onrender.com/health) em cada chamada. Assim, o agente vê os mesmos produtos, preços e estoques da loja, sem uma lista duplicada.

## Ferramentas

| Tool | O que faz |
| --- | --- |
| `somar(a, b)` | Verifica a conexão MCP somando dois números |
| `buscar_produtos(termo?, preco_max?)` | Pesquisa o catálogo e filtra pelo preço máximo |
| `detalhar_produto(id)` | Mostra todos os dados de um produto |
| `consultar_estoque(id)` | Mostra quantidade e disponibilidade atuais |

As ferramentas consultam dados; elas não fazem compras nem resetam o estoque.

## Rodar no Windows

Requer Python 3.11 ou superior. Abra o PowerShell nesta pasta (`backend/mcp`) e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "mcp>=2.0.0,<3"
.\.venv\Scripts\python.exe app.py
```

Deixe o terminal aberto. O endpoint MCP ficará em `http://127.0.0.1:8141/mcp`. Abrir `/mcp` numa aba comum não mostra a loja: o endereço é para clientes MCP. A loja continua em https://caua019m.github.io/cic-shop-frontend/.

Opcionalmente, com `uv` instalado, execute `uv sync` e `uv run python app.py` nesta pasta.

## Conectar um agente

Para o OpenCode, adicione ao `opencode.json` do projeto:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "cic-shop": {
      "type": "remote",
      "url": "http://127.0.0.1:8141/mcp",
      "enabled": true
    }
  }
}
```

Inicie `app.py` antes de abrir o agente. Experimente pedir: “Use `buscar_produtos` para encontrar fones até R$ 200” ou “Use `consultar_estoque` para verificar `fone-a`”. O [MCP Inspector](https://github.com/modelcontextprotocol/inspector) também pode listar e chamar as tools nesse endpoint.

## Trocar a API consultada

Por padrão, o MCP usa `https://cic-shop-backend.onrender.com`. Para testar uma API local, defina a variável antes de iniciar:

```powershell
$env:CIC_SHOP_API_URL = 'http://127.0.0.1:3001'
.\.venv\Scripts\python.exe app.py
```

Este MCP roda somente no seu computador. A URL pública da API não é um endpoint MCP; não use `https://cic-shop-backend.onrender.com/mcp`. Não exponha o servidor MCP à internet sem autenticação e configuração de segurança adequadas.

Se a porta 8141 estiver ocupada, defina `$env:CIC_SHOP_MCP_PORT = '8142'` antes de executar `app.py` e use a mesma porta na URL do cliente MCP.
