-- --------------------------- --
-- Banco de dados "jocablogdb" --
-- --------------------------- --

-- Apaga o banco de dados caso ele já exista
-- PERIGO! Não faça isso em modo de produção
DROP DATABASE IF EXISTS jocablogdb;

-- Cria o banco de dados novamente
-- PERIGO! Não faça isso em modo de produção
CREATE DATABASE jocablogdb
    -- Usando o conjunto de caracteres UTF-8
    CHARACTER SET utf8mb4
    -- Buscas em UTF-8 e case insensitive
    COLLATE utf8mb4_general_ci;

-- Seleciona o banco de dados para os próximos comandos
USE jocablogdb;

-- Cria a tabela "staff"
CREATE TABLE staff (
    sta_id INT PRIMARY KEY AUTO_INCREMENT,
    sta_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sta_name VARCHAR(127) NOT NULL,
    sta_email VARCHAR(255) NOT NULL,
    sta_password VARCHAR(63) NOT NULL,
    sta_birth DATE NOT NULL,
    sta_image VARCHAR(255),
    sta_description VARCHAR(255),
    sta_type ENUM('moderator', 'author', 'admin') DEFAULT 'moderator',
    sta_status ENUM('on', 'off', 'del') DEFAULT 'on'
);

-- Cria a tabela "article"
CREATE TABLE article (
    art_id INT PRIMARY KEY AUTO_INCREMENT,
    art_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    art_title VARCHAR(127) NOT NULL,
    art_resume VARCHAR(255) NOT NULL,
    art_thumbnail VARCHAR(255) NOT NULL,
    art_content TEXT NOT NULL,
    art_view INT DEFAULT 0,
    art_author INT,
    art_status ENUM('on', 'off', 'del') DEFAULT 'on',
    -- Chave estrangeira para "staff"
    FOREIGN KEY (art_author) REFERENCES staff (sta_id)
);

-- Cria a tabela "comment"
CREATE TABLE comment (
    com_id INT PRIMARY KEY AUTO_INCREMENT,
    com_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    com_article INT,
    com_author_name VARCHAR(127) NOT NULL,
    com_author_email VARCHAR(255) NOT NULL,
    com_comment TEXT NOT NULL,
    com_status ENUM('on', 'off', 'del') DEFAULT 'on',
    FOREIGN KEY (com_article) REFERENCES article (art_id)
);

-- Cria a tabela "contact"
CREATE TABLE contact (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(127) NOT NULL,
    email VARCHAR(127) NOT NULL,
    subject VARCHAR(127) NOT NULL,
    message TEXT NOT NULL,
    status ENUM('received', 'readed', 'responded', 'deleted') DEFAULT 'received'
);


-- ----------------------------------------- --
-- Popula as tabelas com alguns dados "fake" --
-- ----------------------------------------- --

-- Tabela "staff"
INSERT INTO staff (
    sta_name,
    sta_email,
    sta_password,
    sta_birth,
    sta_image,
    sta_description,
    sta_type
) VALUES (
    'Joca da Silva Joquinha',
    'jocadasilvajoquinha@gmail.com',
    SHA1('Senha123'),
    '2000-03-27',
    'https://randomuser.me/api/portraits/men/1.jpg',
    'Programador, escultor, pintor, preparador e enrolador.',
    'admin'
), (
    'Marineuza Siriliano',
    'marineuza@email.com',
    SHA1('Senha123'),
    '1999-08-14',
    'https://randomuser.me/api/portraits/women/1.jpg',
    'Programadora, arrumadora, colecionadora e instrutora.',
    'author'
);

-- Insersões por IA
INSERT INTO staff (
    sta_name,
    sta_email,
    sta_password,
    sta_birth,
    sta_image,
    sta_description,
    sta_type
) VALUES (
    'Maria Oliveira',
    'maria.oliveira@example.com',
    SHA1('Senha123'),
    '1985-07-15',
    'https://randomuser.me/api/portraits/women/2.jpg',
    'Escritora e revisora de textos.',
    'author'
), (
    'Carlos Pereira',
    'carlos.pereira@example.com',
    SHA1('Senha123'),
    '1990-11-22',
    'https://randomuser.me/api/portraits/men/3.jpg',
    'Moderador de conteúdo e suporte ao cliente.',
    'moderator'
), (
    'Ana Souza',
    'ana.souza@example.com',
    SHA1('Senha123'),
    '1995-05-30',
    'https://randomuser.me/api/portraits/women/4.jpg',
    'Autora de artigos e blogs.',
    'author'
), (
    'Pedro Santos',
    'pedro.santos@example.com',
    SHA1('Senha123'),
    '1988-02-14',
    'https://randomuser.me/api/portraits/men/5.jpg',
    'Moderador de fóruns e redes sociais.',
    'moderator'
), (
    'Luciana Lima',
    'luciana.lima@example.com',
    SHA1('Senha123'),
    '1992-09-05',
    'https://randomuser.me/api/portraits/women/6.jpg',
    'Escritora de ficção e poesia.',
    'author'
);

-- Tabela "article"
INSERT INTO article (
    art_date,
    art_title,
    art_resume,
    art_thumbnail,
    art_content,
    art_author
) VALUES (
    -- Gera uma data aleatória entre '2024-01-01 00:00:00' e '2024-12-31 23:59:59'
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Primeiro artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/300',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '2'
);

-- Insersões por IA
INSERT INTO article (
    art_date,
    art_title,
    art_resume,
    art_thumbnail,
    art_content,
    art_author
) VALUES (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Segundo artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/295',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '5'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Terceiro artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/296',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '2'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Quarto artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/297',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '5'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Quinto artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/298',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '2'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Sexto artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/299',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '5'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Sétimo artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/300',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '2'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Oitavo artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/301',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '2'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Nono artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/302',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '5'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Décimo artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/303',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '5'
), (
    FROM_UNIXTIME( UNIX_TIMESTAMP('2024-01-01 00:00:00') + FLOOR(RAND() * (UNIX_TIMESTAMP('2024-12-31 23:59:59') - UNIX_TIMESTAMP('2024-01-01 00:00:00'))) ),
    'Décimo primeiro artigo',
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.',
    'https://picsum.photos/304',
    '
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda placeat iure quo fugiat atque officia commodi, perspiciatis adipisci, quam a consequatur aliquam. Earum ad laborum, ut perspiciatis sit consequuntur? Modi.</p>
<p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deserunt quas optio placeat expedita repellendus sunt fugit inventore, rem necessitatibus accusantium ratione reiciendis obcaecati sint. Delectus sunt optio unde nostrum nam?</p>
<img src="https://picsum.photos/200/300" alt="Imagem aleatória">
<p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero commodi quaerat dolores sint, quis iure incidunt odit magnam ex laborum esse quo voluptatem omnis quas cum! Placeat consectetur aspernatur neque.</p>
<h4>Lista de links:</h4>
<ul>
    <li><a href="https://catabits.com.br" target="_blank">Site do Fessô</a></li>
    <li><a href="https://github.com/Luferat" target="_blank">GitHub do Fessô</a></li>
</ul>
<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Laboriosam autem animi quas optio minima reprehenderit inventore dignissimos voluptatem hic nobis facilis rerum nemo, iste fuga rem ducimus veritatis reiciendis. Ad.</p>    
    ',
    '6'
);
