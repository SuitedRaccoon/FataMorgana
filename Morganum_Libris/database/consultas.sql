-- ============================================
-- 4.1 CONSULTAS BÁSICAS: SELECT, FROM
-- ============================================

-- Exemplo 1: Selecionar todos os livros
SELECT * FROM books;

-- Exemplo 2: Selecionar apenas os títulos e autores
SELECT title, author FROM books;



-- ============================================
-- 4.2 CONSULTAS INTERMEDIÁRIAS
-- DISTINCT, WHERE, OPERADORES, LIKE, GROUP BY, etc.
-- ============================================

-- Exemplo 3: Contar livros planejados por gênero e calcular média de idade
SELECT
  b.genre,                                           -- Gênero do livro
  COUNT(*) AS quantidade,                            -- Quantidade por gênero
  AVG(YEAR(CURDATE()) - b.year_published) AS media_anos_desde_publicacao
FROM user_books ub
JOIN books b ON b.id = ub.book_id
WHERE ub.status = 'completed'                           -- Apenas livros planejados
  AND b.genre IN ('Fantasy', 'Philosophy')                -- Apenas alguns gêneros
GROUP BY b.genre                                      -- Agrupar por gênero
HAVING COUNT(*) >= 2                                  -- Filtrar gêneros com pelo menos 2 livros
ORDER BY quantidade DESC;                             -- Ordenar por quantidade



-- Exemplo 4: Buscar livros cujo título contenha "lordr" e publicados entre 1950 e 1970
SELECT title, author, year_published
FROM books
WHERE title LIKE '%lord%'                            
  AND year_published BETWEEN 1950 AND 1970;          



-- ============================================
-- 4.3 CONSULTAS AVANÇADAS
-- TRIGGER e STORED PROCEDURE
-- ============================================

-- Exemplo 5: Trigger para definir automaticamente a posição do livro na fila ao inserir
-- Trigger
DELIMITER //
CREATE TRIGGER atualiza_posicao_fila
BEFORE INSERT ON user_books
FOR EACH ROW
BEGIN
  DECLARE maior_pos INT;

  SELECT COALESCE(MAX(queue_position), 0) + 1 INTO maior_pos
  FROM user_books
  WHERE user_id = NEW.user_id;

  SET NEW.queue_position = maior_pos;
END;
//
DELIMITER ;

-- Teste
INSERT INTO user_books (user_id, book_id, status)
VALUES (1, 101, 'planned'); 

SELECT * FROM user_books WHERE user_id = 1 ORDER BY queue_position;



-- Exemplo 6: Stored Procedure para adicionar livro a uma lista salva com posição automática
DELIMITER //
CREATE PROCEDURE adicionar_livro_lista (
  IN p_list_id INT,         -- ID da lista
  IN p_book_id INT          -- ID do livro
)
BEGIN
  DECLARE nova_pos INT;

  -- Encontra a próxima posição disponível na lista
  SELECT COALESCE(MAX(position), 0) + 1 INTO nova_pos
  FROM saved_list_books
  WHERE list_id = p_list_id;

  -- Insere o livro na lista com a posição calculada
  INSERT INTO saved_list_books (list_id, book_id, position)
  VALUES (p_list_id, p_book_id, nova_pos);
END;
//
DELIMITER ;

-- Exemplo de chamada da stored procedure:
-- CALL adicionar_livro_lista(2, 5);

-- Trigger
DELIMITER //

CREATE PROCEDURE livros_por_status_usuario(
    IN p_user_id INT,
    IN p_status VARCHAR(20)
)
BEGIN
    SELECT b.title AS titulo, b.author AS autor, b.genre AS genero
    FROM user_books ub
    JOIN books b ON b.id = ub.book_id
    WHERE ub.user_id = p_user_id
      AND ub.status = p_status
    ORDER BY b.title;
END;
//

DELIMITER ;

-- Teste
CALL livros_por_status_usuario(1, 'reading');
