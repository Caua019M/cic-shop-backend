# CIC SHOP — API

API Express de demonstração com 20 produtos, checkout e reset de estoque. Não processa pagamentos.

API publicada: https://cic-shop-backend.onrender.com (health check: https://cic-shop-backend.onrender.com/health).

## Executar

```sh
npm install
npm start
```

`GET http://localhost:3001/health` deve responder `{"ok":true,"products":20}`.

## Publicação no Render

O Web Service está conectado a este repositório no plano Free, com build `npm install`, início `npm start` e verificação em `/health`. O servidor usa a variável `PORT` fornecida pelo Render.

Rotas: `GET /api/products`, `GET /api/products/:id`, `POST /api/checkout` com `{"items":{"fone-a":1}}` e `POST /api/reset` para restaurar o estoque de demonstração.

O estoque fica em memória e volta ao valor inicial quando o processo reinicia. O reset é público para uso apenas nesta demonstração.

## Integração com agentes de IA

A pasta [`mcp`](mcp/README.md) contém um servidor MCP local em Python. Ele oferece busca, detalhe e consulta de estoque usando esta API publicada. Consulte o README da pasta para instalar e conectar um cliente MCP.
