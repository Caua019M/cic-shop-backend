# CIC SHOP — API

API Express de demonstração com 20 produtos, checkout e reset de estoque. Não processa pagamentos.

## Executar

```sh
npm install
npm start
```

`GET http://localhost:3001/health` deve responder `{"ok":true,"products":20}`.

## Publicar no Render

Crie um Web Service conectado a este repositório. O `render.yaml` define plano Free, build `npm install`, início `npm start` e verificação em `/health`. Na criação manual, use esses mesmos comandos. O servidor usa a variável `PORT` fornecida pelo Render.

Rotas: `GET /api/products`, `GET /api/products/:id`, `POST /api/checkout` com `{"items":{"fone-a":1}}` e `POST /api/reset` para restaurar o estoque de demonstração.

O estoque fica em memória e volta ao valor inicial quando o processo reinicia. O reset é público para uso apenas nesta demonstração.
