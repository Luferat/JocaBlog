-- ------------------------------ --
-- Obtém todos os artigos válidos --
-- ------------------------------ --

-- Seleciona os campos abaixo
SELECT art_id, art_title, art_resume, art_thumbnail
-- desta tabela
FROM article
-- art_status é 'on'
WHERE art_status = 'on'
    -- E art_date é menor ou igual à data atual para que 
    -- não obténha artigos com data futura (agendados)
    AND art_date <= NOW()
-- Ordena pela data mais recente  
ORDER BY art_date DESC;


-- --------------------------------------------- --
-- Obtém um artigo pelo ID com os dados do autor --
-- --------------------------------------------- --

-- Campos do artigo
SELECT art_id, art_date, art_title, art_content,
    -- Obtém a data em PT-BR pelo pseudo-campo `art_datebr`
    DATE_FORMAT(art_date, '%%d/%%m/%%Y às %%H:%%i') AS art_datebr,
    -- Campos do autor
    sta_id, sta_name, sta_image, sta_description, sta_type,
    -- Calcula a idade para `sta_age` considerando ano, mês e dia de nascimento
    TIMESTAMPDIFF(YEAR, sta_birth, CURDATE()) - 
        (DATE_FORMAT(CURDATE(), '%%m%%d') < DATE_FORMAT(sta_birth, '%%m%%d')) AS sta_age
FROM article
-- Junção entre as tabelas `article` e `staff`
INNER JOIN staff ON art_author = sta_id
-- Filtra pelo id do artigo
WHERE art_id = %s
    AND art_status = 'on'
    AND art_date <= NOW();