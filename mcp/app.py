"""Servidor MCP da CIC SHOP, alimentado pela API da loja.

Execute: python app.py
Endpoint local: http://127.0.0.1:8141/mcp
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from mcp.server.mcpserver import MCPServer


API_BASE_URL = os.getenv("CIC_SHOP_API_URL", "https://cic-shop-backend.onrender.com").rstrip("/")
mcp = MCPServer("cic-shop")


def _get(path: str) -> object:
    request = Request(f"{API_BASE_URL}{path}", headers={"Accept": "application/json"})
    try:
        # O plano gratuito do Render pode demorar para acordar.
        with urlopen(request, timeout=90) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise ValueError("Produto não encontrado na CIC SHOP.") from error
        raise RuntimeError(f"A API da CIC SHOP respondeu HTTP {error.code}.") from error
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Não foi possível consultar a API da CIC SHOP: {error}") from error


@mcp.tool()
def somar(a: float, b: float) -> float:
    """Soma dois números; ferramenta simples para testar a conexão MCP."""
    return a + b


@mcp.tool()
def buscar_produtos(termo: str | None = None, preco_max: float | None = None) -> list[dict]:
    """Busca produtos reais da CIC SHOP por nome ou descrição e preço máximo em reais.

    Sem filtros, devolve todo o catálogo, incluindo o estoque atual.
    """
    if preco_max is not None and preco_max < 0:
        raise ValueError("preco_max deve ser maior ou igual a zero.")

    query = urlencode({"q": termo.strip()}) if termo and termo.strip() else ""
    products = _get(f"/api/products?{query}" if query else "/api/products")
    if not isinstance(products, list):
        raise RuntimeError("A API devolveu um catálogo em formato inesperado.")
    if preco_max is not None:
        products = [product for product in products if product["price"] <= preco_max]
    return products


@mcp.tool()
def detalhar_produto(id: str) -> dict:
    """Mostra detalhes, preço e estoque atual de um produto pelo seu ID."""
    product = _get(f"/api/products/{quote(id, safe='')}")
    if not isinstance(product, dict):
        raise RuntimeError("A API devolveu um produto em formato inesperado.")
    return product


@mcp.tool()
def consultar_estoque(id: str) -> dict:
    """Consulta a disponibilidade atual de um produto da CIC SHOP pelo ID."""
    product = detalhar_produto(id)
    return {
        "id": product["id"],
        "nome": product["name"],
        "estoque": product["stock"],
        "disponivel": product["stock"] > 0,
    }


if __name__ == "__main__":
    # A conexão MCP fica restrita à máquina local, como no projeto de referência.
    mcp.run(transport="streamable-http", host="127.0.0.1", port=int(os.getenv("CIC_SHOP_MCP_PORT", "8141")))
