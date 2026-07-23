-- Tabela de usuários usada para autenticação (login).
-- "IF NOT EXISTS" permite rodar este script toda vez que a aplicação
-- sobe, sem apagar usuários já cadastrados.
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL
);
