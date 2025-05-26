-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema morganum_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `morganum_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `morganum_db` ;

-- -----------------------------------------------------
-- Table `morganum_db`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`usuario` (
  `cpf` VARCHAR(14) NOT NULL COMMENT 'Formatado com pontos e traço (XXX.XXX.XXX-XX)',
  `nome` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `tel` VARCHAR(20) NULL COMMENT 'Formatado com código de país (+55 XX XXXX-XXXX)',
  `senha` CHAR(60) NOT NULL COMMENT 'Hash bcrypt',
  `data_nascimento` DATE NOT NULL,
  `genero` ENUM('Masculino','Feminino','Não Binário','Outro','Prefiro não informar') NULL,
  `criado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  PRIMARY KEY (`cpf`),
  UNIQUE INDEX `cpf_UNIQUE` (`cpf` ASC),
  CONSTRAINT `chk_cpf_format`
    CHECK (`cpf` REGEXP '^[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}\\-[0-9]{2}$'),
  CONSTRAINT `chk_email_format`
    CHECK (`email` REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
  CONSTRAINT `chk_tel_format`
    CHECK (`tel` IS NULL OR `tel` REGEXP '^\\+[0-9]{2} [0-9]{2} [0-9]{4,5}\\-[0-9]{4}$'),
  CONSTRAINT `chk_data_nascimento`
    CHECK (`data_nascimento` BETWEEN '1900-01-01' AND '2100-01-01') -- Data fixa
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `morganum_db`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`cliente` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `creditos` DECIMAL(10,2) UNSIGNED NULL DEFAULT 0.00,
  `ativo` TINYINT NOT NULL DEFAULT 1,
  `ultimo_acesso` TIMESTAMP NULL DEFAULT NULL,
  `atualizado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_cpf` VARCHAR(14) NOT NULL,
  UNIQUE KEY `uk_cliente_usuario` (`usuario_cpf`),  -- Garante que um usuário não seja cliente mais de uma vez
  CONSTRAINT `fk_cliente_usuario1`
    FOREIGN KEY (`usuario_cpf`)
    REFERENCES `morganum_db`.`usuario` (`cpf`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `chk_creditos_positivos`
    CHECK (`creditos` >= 0)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `morganum_db`.`funcionario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`funcionario` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `cargo` VARCHAR(45) NOT NULL,
  `salario` DECIMAL(10,2) UNSIGNED NOT NULL,
  `comissao` DECIMAL(10,2) UNSIGNED NULL DEFAULT 0.00,
  `escala` VARCHAR(45) NOT NULL,
  `data_contratado` DATE NOT NULL,
  `data_demissao` DATE NULL,
  `usuario_cpf` VARCHAR(14) NOT NULL,
  UNIQUE KEY `uk_funcionario_usuario` (`usuario_cpf`),  -- Garante que um usuário não seja funcionario mais de uma vez
  CONSTRAINT `fk_funcionario_usuario1`
    FOREIGN KEY (`usuario_cpf`)
    REFERENCES `morganum_db`.`usuario` (`cpf`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `chk_salario_positivo`
    CHECK (`salario` > 0),
  CONSTRAINT `chk_comissao_positiva`
    CHECK (`comissao` IS NULL OR `comissao` >= 0),
  CONSTRAINT `chk_datas_contratacao`
    CHECK (`data_demissao` IS NULL OR `data_demissao` >= `data_contratado`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `morganum_db`.`editora`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`editora` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `cidade` VARCHAR(45) NULL,
  `pais` VARCHAR(45) NULL,
  `ano_fundacao` SMALLINT NULL,
  `website` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nome_UNIQUE` (`nome` ASC),
  CONSTRAINT `chk_website_format`
    CHECK (`website` IS NULL OR `website` REGEXP '^(https?:\\/\\/)?([\\da-z\\.-]+)\\.([a-z\\.]{2,6})([\\/\\w \\.-]*)*\\/?$')
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `morganum_db`.`genero_literario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`genero_literario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `descricao` TEXT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nome_UNIQUE` (`nome` ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `morganum_db`.`livro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`livro` (
  `isbn_13` VARCHAR(18) NOT NULL COMMENT 'Formatado com hífens (XXX-XX-XXXX-XXX-X)',
  `isbn_10` VARCHAR(14) NULL COMMENT 'Formatado com hífens (XXX-XX-XXXX-X)',
  `titulo` VARCHAR(255) NOT NULL,
  `autor` VARCHAR(100) NOT NULL,
  `editora_id` INT NOT NULL,
  `genero_literario_id` INT NOT NULL,
  `edicao` VARCHAR(45) NULL,
  `impressao` VARCHAR(45) NULL,
  `idioma` VARCHAR(45) NOT NULL,
  `data_publicacao` DATE NULL,
  `quantidade_estoque` INT UNSIGNED NOT NULL DEFAULT 0,
  `preco_livro` DECIMAL(10,2) UNSIGNED NOT NULL,
  `descricao` TEXT NULL,
  `numero_paginas` INT UNSIGNED NULL,
  `criado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`isbn_13`),
  UNIQUE INDEX `isbn_13_UNIQUE` (`isbn_13` ASC),
  INDEX `idx_livro_titulo` (`titulo` ASC),
  INDEX `idx_livro_autor` (`autor` ASC),
  INDEX `fk_livro_editora_idx` (`editora_id` ASC),
  INDEX `fk_livro_genero_literario_idx` (`genero_literario_id` ASC),
  CONSTRAINT `fk_livro_editora`
    FOREIGN KEY (`editora_id`)
    REFERENCES `morganum_db`.`editora` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_livro_genero_literario`
    FOREIGN KEY (`genero_literario_id`)
    REFERENCES `morganum_db`.`genero_literario` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `chk_isbn13_format`
    CHECK (`isbn_13` REGEXP '^[0-9]{3}\\-[0-9]{1,2}\\-[0-9]{1,5}\\-[0-9]{1,5}\\-[0-9]$'),
  CONSTRAINT `chk_isbn10_format`
    CHECK (`isbn_10` IS NULL OR `isbn_10` REGEXP '^[0-9]{1,5}\\-[0-9]{1,5}\\-[0-9]{1,6}\\-[0-9Xx]$'),
  CONSTRAINT `chk_preco_positivo`
    CHECK (`preco_livro` > 0),
  CONSTRAINT `chk_data_publicacao`
    CHECK (`data_publicacao` IS NULL OR `data_publicacao` BETWEEN '1500-01-01' AND '2100-01-01')
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `morganum_db`.`pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`pedido` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `data` DATE NOT NULL DEFAULT (CURRENT_DATE),
  `hora` TIME NOT NULL DEFAULT (CURRENT_TIME),
  `metodo_envio` ENUM('Correio','Transportadora','Retirada','Digital') NOT NULL,
  `comment` TEXT NULL,
  `status` ENUM('Pendente','Processando','Enviado','Entregue','Cancelado') NOT NULL DEFAULT 'Pendente',
  `cliente_usuario_cpf` VARCHAR(14) NOT NULL,
  `funcionario_usuario_cpf` VARCHAR(14) NULL,
  `valor_total` DECIMAL(10,2) NOT NULL DEFAULT 0.00,  -- Coluna normal em vez de gerada
  PRIMARY KEY (`id`),
  INDEX `fk_pedido_cliente1_idx` (`cliente_usuario_cpf` ASC),
  INDEX `fk_pedido_funcionario1_idx` (`funcionario_usuario_cpf` ASC),
  INDEX `idx_pedido_status` (`status` ASC),
  INDEX `idx_pedido_data` (`data` ASC),
  CONSTRAINT `fk_pedido_cliente1`
    FOREIGN KEY (`cliente_usuario_cpf`)
    REFERENCES `morganum_db`.`cliente` (`usuario_cpf`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pedido_funcionario1`
    FOREIGN KEY (`funcionario_usuario_cpf`)
    REFERENCES `morganum_db`.`funcionario` (`usuario_cpf`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `chk_data_pedido`
    CHECK (`data` BETWEEN '2020-01-01' AND '2100-01-01')
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `morganum_db`.`endereco`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`endereco` (
  `id_end` INT NOT NULL AUTO_INCREMENT,
  `nome_end` VARCHAR(45) NOT NULL,
  `morador` VARCHAR(45) NOT NULL,
  `pais` VARCHAR(45) NOT NULL,
  `cep` VARCHAR(10) NOT NULL COMMENT 'Formatado com hífen (XXXXX-XXX)',
  `estado` ENUM('AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO') NOT NULL,
  `cidade` VARCHAR(45) NOT NULL,
  `logradouro` VARCHAR(255) NOT NULL,
  `bairro` VARCHAR(45) NOT NULL,
  `numero` INT NOT NULL,
  `complemento` VARCHAR(45) NULL DEFAULT NULL,
  `referencia` TEXT NULL,
  `envio` TINYINT NOT NULL DEFAULT 0,
  `usuario_cpf` VARCHAR(14) NOT NULL,
  `criado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_end`),
  INDEX `fk_endereco_usuario_idx` (`usuario_cpf` ASC),
  CONSTRAINT `fk_endereco_usuario`
    FOREIGN KEY (`usuario_cpf`)
    REFERENCES `morganum_db`.`usuario` (`cpf`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `chk_cep_format` 
    CHECK (`cep` REGEXP '^[0-9]{5}\\-[0-9]{3}$'),
  CONSTRAINT `chk_numero_positivo`
    CHECK (`numero` > 0)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `morganum_db`.`livro_has_pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `morganum_db`.`livro_has_pedido` (
  `livro_isbn_13` VARCHAR(17) NOT NULL,
  `pedido_id` INT NOT NULL,
  `quant` INT UNSIGNED NOT NULL,
  `valor_unit` DECIMAL(10,2) UNSIGNED NOT NULL,
  `subtotal` DECIMAL(10,2) GENERATED ALWAYS AS (`quant` * `valor_unit`) STORED,
  PRIMARY KEY (`livro_isbn_13`, `pedido_id`),
  INDEX `fk_livro_has_pedido_pedido1_idx` (`pedido_id` ASC),
  INDEX `fk_livro_has_pedido_livro1_idx` (`livro_isbn_13` ASC),
  CONSTRAINT `fk_livro_has_pedido_livro1`
    FOREIGN KEY (`livro_isbn_13`)
    REFERENCES `morganum_db`.`livro` (`isbn_13`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_livro_has_pedido_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `morganum_db`.`pedido` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `chk_quantidade_positiva`
    CHECK (`quant` > 0),
  CONSTRAINT `chk_valor_unit_positivo`
    CHECK (`valor_unit` > 0)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- View `morganum_db`.`livros_completos`
-- -----------------------------------------------------

DROP VIEW IF EXISTS `livros_completos`;

CREATE VIEW `livros_completos` AS
SELECT 
  l.*, 
  e.nome AS editora_nome, 
  e.cidade AS editora_cidade, 
  e.pais AS editora_pais,
  g.nome AS genero_literario,
  g.descricao AS genero_descricao
FROM `livro` l
JOIN `editora` e ON l.editora_id = e.id
JOIN `genero_literario` g ON l.genero_literario_id = g.id;

-- Trigger para validação dinâmica

DROP TRIGGER IF EXISTS validate_livro_data_publicacao;

DELIMITER //
CREATE TRIGGER validate_livro_data_publicacao
BEFORE INSERT ON `livro`
FOR EACH ROW
BEGIN
    IF NEW.data_publicacao IS NOT NULL AND NEW.data_publicacao > CURDATE() THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Data de publicação não pode ser no futuro';
    END IF;
END//
DELIMITER ;

-- Trigger para atualizações

DROP TRIGGER IF EXISTS validate_livro_data_publicacao_update;

DELIMITER //
CREATE TRIGGER validate_livro_data_publicacao_update
BEFORE UPDATE ON `livro`
FOR EACH ROW
BEGIN
    IF NEW.data_publicacao IS NOT NULL AND NEW.data_publicacao > CURDATE() THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Data de publicação não pode ser no futuro';
    END IF;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS validate_usuario_data_nascimento;

DELIMITER //
CREATE TRIGGER validate_usuario_data_nascimento
BEFORE INSERT ON `usuario`
FOR EACH ROW
BEGIN
    IF NEW.data_nascimento > CURDATE() THEN  -- Corrigido para usar data_nasc
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Data de nascimento não pode ser no futuro';
    END IF;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS validate_usuario_data_nascimento_update;

DELIMITER //
CREATE TRIGGER validate_usuario_data_nascimento_update
BEFORE UPDATE ON `usuario`
FOR EACH ROW
BEGIN
    IF NEW.data_nascimento > CURDATE() THEN  -- Corrigido para usar data_nasc
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Data de nascimento não pode ser no futuro';
    END IF;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS validate_pedido_data;

DELIMITER //
CREATE TRIGGER validate_pedido_data
BEFORE INSERT ON `pedido`
FOR EACH ROW
BEGIN
    IF NEW.data > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Data do pedido não pode ser no futuro';
    END IF;
END//
DELIMITER ;

-- Trigger para inserção em livro_has_pedido

DROP TRIGGER IF EXISTS atualiza_valor_total_insert;

DELIMITER //
CREATE TRIGGER atualiza_valor_total_insert
AFTER INSERT ON `livro_has_pedido`
FOR EACH ROW
BEGIN
    UPDATE `pedido` p
    SET p.valor_total = (
        SELECT COALESCE(SUM(lhp.quant * lhp.valor_unit), 0)
        FROM `livro_has_pedido` lhp
        WHERE lhp.pedido_id = NEW.pedido_id
    )
    WHERE p.id = NEW.pedido_id;
END//
DELIMITER ;

-- Trigger para atualização em livro_has_pedido

DROP TRIGGER IF EXISTS atualiza_valor_total_update;

DELIMITER //
CREATE TRIGGER atualiza_valor_total_update
AFTER UPDATE ON `livro_has_pedido`
FOR EACH ROW
BEGIN
    UPDATE `pedido` p
    SET p.valor_total = (
        SELECT COALESCE(SUM(lhp.quant * lhp.valor_unit), 0)
        FROM `livro_has_pedido` lhp
        WHERE lhp.pedido_id = NEW.pedido_id
    )
    WHERE p.id = NEW.pedido_id;
END//
DELIMITER ;

-- Trigger para exclusão em livro_has_pedido

DROP TRIGGER IF EXISTS atualiza_valor_total_delete;

DELIMITER //
CREATE TRIGGER atualiza_valor_total_delete
AFTER DELETE ON `livro_has_pedido`
FOR EACH ROW
BEGIN
    UPDATE `pedido` p
    SET p.valor_total = (
        SELECT COALESCE(SUM(lhp.quant * lhp.valor_unit), 0)
        FROM `livro_has_pedido` lhp
        WHERE lhp.pedido_id = OLD.pedido_id
    )
    WHERE p.id = OLD.pedido_id;
END//
DELIMITER ;

-- 1. Primeiro altere a estrutura da tabela
-- ALTER TABLE `editora` 
-- MODIFY COLUMN `ano_fundacao` SMALLINT NULL;

-- 1. Popular a tabela de editoras
INSERT INTO `editora` (`nome`, `cidade`, `pais`, `ano_fundacao`, `website`) VALUES
('Companhia das Letras', 'São Paulo', 'Brasil', 1986, 'https://www.companhiadasletras.com.br'),
('Editora Rocco', 'Rio de Janeiro', 'Brasil', 1975, 'https://www.rocco.com.br'),
('HarperCollins', 'Nova York', 'EUA', 1817, 'https://www.harpercollins.com'),
('Editora Arqueiro', 'Rio de Janeiro', 'Brasil', 1984, 'https://www.editoraarqueiro.com.br'),
('Intrínseca', 'Rio de Janeiro', 'Brasil', 2003, 'https://www.intrinseca.com.br'),
('Editora Record', 'Rio de Janeiro', 'Brasil', 1942, 'https://www.record.com.br'),
('Sextante', 'Rio de Janeiro', 'Brasil', 1999, 'https://www.sextante.com.br'),
('Darkside Books', 'Rio de Janeiro', 'Brasil', 2013, 'https://www.darksidebooks.com.br'),
('Editora Aleph', 'São Paulo', 'Brasil', 2004, 'https://www.editoraaleph.com.br'),
('Penguin Companhia', 'São Paulo', 'Brasil', 2013, 'https://www.penguincompanhia.com.br');

-- 2. Popular tabela de gêneros literários
INSERT INTO `genero_literario` (`nome`, `descricao`) VALUES
('Ficção Científica', 'Obras que exploram conceitos científicos imaginários e futuristas'),
('Romance', 'Narrativas longas sobre relacionamentos humanos e dramas pessoais'),
('Fantasia', 'Obras com elementos mágicos e sobrenaturais'),
('Terror', 'Obras que buscam assustar ou causar medo no leitor'),
('Autoajuda', 'Livros com conselhos para desenvolvimento pessoal'),
('Biografia', 'Narrativas sobre a vida de pessoas reais'),
('Distopia', 'Obras que retratam sociedades futuras indesejáveis'),
('Ficção Histórica', 'Narrativas ficcionais ambientadas em períodos históricos'),
('Infantil', 'Livros destinados ao público infantil'),
('Negócios', 'Obras sobre empreendedorismo e gestão'),
('Poesia', 'Obras literárias em versos e estrofes');

-- 3. Popular tabela de usuários
-- Senhas são hashes bcrypt de "senha123"
INSERT INTO `usuario` (`cpf`, `nome`, `email`, `tel`, `senha`, `data_nascimento`, `genero`) VALUES
('123.456.789-01', 'João Silva', 'joao.silva@email.com', '+55 11 98765-4321', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1985-05-15', 'Masculino'),
('234.567.890-12', 'Maria Souza', 'maria.souza@email.com', '+55 21 99876-5432', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1990-08-22', 'Feminino'),
('345.678.901-23', 'Carlos Oliveira', 'carlos.oliveira@email.com', '+55 31 98765-1234', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1978-11-30', 'Masculino'),
('456.789.012-34', 'Ana Santos', 'ana.santos@email.com', '+55 41 99654-3210', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1995-03-10', 'Feminino'),
('567.890.123-45', 'Pedro Costa', 'pedro.costa@email.com', '+55 51 98543-2109', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1982-07-25', 'Masculino'),
('678.901.234-56', 'Fernanda Lima', 'fernanda.lima@email.com', '+55 11 97654-3210', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1992-09-18', 'Feminino'),
('789.012.345-67', 'Ricardo Almeida', 'ricardo.almeida@email.com', '+55 21 98765-4321', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1988-04-25', 'Masculino'),
('890.123.456-78', 'Juliana Pereira', 'juliana.pereira@email.com', '+55 31 99876-5432', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1995-12-05', 'Feminino'),
('901.234.567-89', 'Lucas Martins', 'lucas.martins@email.com', '+55 41 98765-1234', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1980-07-30', 'Masculino'),
('012.345.678-90', 'Patrícia Nunes', 'patricia.nunes@email.com', '+55 51 99654-3210', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrU1V7H/.BzRZJfIMTb0Q7J9WXZC2qW', '1975-11-15', 'Feminino');

-- 4. Popular tabela de clientes
INSERT INTO `cliente` (`usuario_cpf`, `creditos`, `ativo`) VALUES
('123.456.789-01', 150.50, 1),
('234.567.890-12', 75.00, 1),
('345.678.901-23', 0.00, 1),
('456.789.012-34', 200.00, 1),
('567.890.123-45', 50.00, 1),
('678.901.234-56', 120.00, 1),
('789.012.345-67', 0.00, 1),
('890.123.456-78', 80.00, 0),
('901.234.567-89', 300.00, 1),
('012.345.678-90', 25.50, 1);

-- 5. Popular tabela de funcionários
INSERT INTO `funcionario` (`usuario_cpf`, `cargo`, `salario`, `comissao`, `escala`, `data_contratado`) VALUES
('234.567.890-12', 'Gerente', 5000.00, 500.00, 'Segunda a Sexta', '2018-06-15'),
('456.789.012-34', 'Vendedor', 2500.00, 300.00, 'Terça a Sábado', '2020-02-10'),
('789.012.345-67', 'Bibliotecário', 3200.00, 200.00, 'Segunda a Sexta', '2019-09-20'),
('901.234.567-89', 'Atendente', 1800.00, 150.00, 'Quarta a Domingo', '2021-05-10');

-- 6. Popular tabela de endereços
INSERT INTO `endereco` (`nome_end`, `morador`, `pais`, `cep`, `estado`, `cidade`, `logradouro`, `bairro`, `numero`, `complemento`, `referencia`, `envio`, `usuario_cpf`) VALUES
('Casa', 'João Silva', 'Brasil', '01234-567', 'SP', 'São Paulo', 'Rua das Flores', 'Centro', 123, 'Apto 101', 'Próximo ao mercado', 1, '123.456.789-01'),
('Trabalho', 'João Silva', 'Brasil', '04567-890', 'SP', 'São Paulo', 'Avenida Paulista', 'Bela Vista', 1000, 'Sala 502', 'Edifício Comercial', 0, '123.456.789-01'),
('Casa', 'Maria Souza', 'Brasil', '20000-000', 'RJ', 'Rio de Janeiro', 'Rua Copacabana', 'Copacabana', 456, NULL, 'Perto da praia', 1, '234.567.890-12'),
('Casa', 'Carlos Oliveira', 'Brasil', '30123-456', 'MG', 'Belo Horizonte', 'Rua das Palmeiras', 'Savassi', 789, 'Casa 2', NULL, 1, '345.678.901-23'),
('Casa', 'Fernanda Lima', 'Brasil', '01310-100', 'SP', 'São Paulo', 'Rua Augusta', 'Consolação', 1500, 'Apto 302', 'Próximo ao metrô', 1, '678.901.234-56'),
('Trabalho', 'Ricardo Almeida', 'Brasil', '22070-010', 'RJ', 'Rio de Janeiro', 'Avenida Atlântica', 'Copacabana', 1702, 'Sala 1204', 'Edifício comercial', 0, '789.012.345-67'),
('Casa', 'Juliana Pereira', 'Brasil', '30140-070', 'MG', 'Belo Horizonte', 'Rua da Bahia', 'Funcionários', 1200, NULL, 'Próximo à praça', 1, '890.123.456-78');

-- 7. Popular tabela de livros
INSERT INTO `livro` (`isbn_13`, `isbn_10`, `titulo`, `autor`, `editora_id`, `genero_literario_id`, `edicao`, `impressao`, `idioma`, `data_publicacao`, `quantidade_estoque`, `preco_livro`, `descricao`, `numero_paginas`) VALUES 
('978-85-359-1979-5', '85-359-197-X', 'O Hobbit', 'J.R.R. Tolkien', 3, 3, '1ª', '2020', 'Português', '1937-09-21', 50, 49.90, 'A aventura de Bilbo Bolseiro na Terra Média', 336),
('978-85-325-3028-8', '85-325-3028-1', 'O Poder do Hábito', 'Charles Duhigg', 1, 5, '3ª', '2021', 'Português', '2012-02-28', 30, 39.90, 'Por que fazemos o que fazemos na vida e nos negócios', 408),
('978-85-8057-526-6', '85-805-752-6', 'A Garota no Trem', 'Paula Hawkins', 2, 4, '1ª', '2019', 'Português', '2015-01-13', 25, 34.90, 'Um thriller psicológico cheio de reviravoltas', 320),
('978-85-7542-585-1', '85-7542-585-3', 'Sapiens', 'Yuval Noah Harari', 1, 6, '5ª', '2022', 'Português', '2011-02-10', 40, 59.90, 'Uma breve história da humanidade', 464),
('978-85-510-0244-8', '85-510-0244-5', '1984', 'George Orwell', 4, 1, '2ª', '2020', 'Português', '1949-06-08', 35, 29.90, 'Um clássico da ficção distópica', 416),
('978-85-01-11204-7', '85-01-11204-3', 'O Senhor dos Anéis', 'J.R.R. Tolkien', 3, 3, '3ª', '2021', 'Português', '1954-07-29', 40, 79.90, 'A trilogia épica da Terra Média', 1216),
('978-85-422-1843-3', '85-422-1843-9', 'A Revolução dos Bichos', 'George Orwell', 4, 1, '1ª', '2020', 'Português', '1945-08-17', 60, 24.90, 'Uma sátira política em forma de fábula', 152),
('978-85-431-0485-0', '85-431-0485-8', 'Mais Esperto que o Diabo', 'Napoleon Hill', 7, 5, '2ª', '2019', 'Português', '1938-01-01', 35, 29.90, 'O manuscrito original perdido de Napoleon Hill', 240),
('978-85-7542-823-4', '85-7542-823-6', '21 Lições para o Século 21', 'Yuval Noah Harari', 1, 6, '1ª', '2022', 'Português', '2018-08-30', 25, 49.90, 'Reflexões sobre os desafios do mundo atual', 432),
('978-85-510-0276-9', '85-510-0276-3', 'Admirável Mundo Novo', 'Aldous Huxley', 4, 1, '4ª', '2021', 'Português', '1932-01-01', 30, 34.90, 'Um clássico da ficção científica distópica', 312);

-- 8. Popular tabela de pedidos
INSERT INTO `pedido` (`data`, `hora`, `metodo_envio`, `comment`, `status`, `cliente_usuario_cpf`, `funcionario_usuario_cpf`) VALUES
('2023-01-15', '14:30:00', 'Correio', 'Embrulhar para presente', 'Entregue', '123.456.789-01', '234.567.890-12'),
('2023-02-20', '10:15:00', 'Retirada', NULL, 'Processando', '345.678.901-23', '456.789.012-34'),
('2023-03-05', '16:45:00', 'Transportadora', 'Fragil', 'Enviado', '456.789.012-34', '234.567.890-12'),
('2023-03-10', '09:00:00', 'Digital', NULL, 'Entregue', '567.890.123-45', NULL),
('2023-03-15', '11:30:00', 'Correio', 'Entregar após as 18h', 'Pendente', '123.456.789-01', '456.789.012-34'),
('2023-04-02', '15:20:00', 'Digital', 'E-book em formato EPUB', 'Entregue', '678.901.234-56', NULL),
('2023-04-10', '11:45:00', 'Correio', 'Presente de aniversário', 'Enviado', '789.012.345-67', '456.789.012-34'),
('2023-04-15', '14:10:00', 'Retirada', NULL, 'Processando', '890.123.456-78', '789.012.345-67'),
('2023-04-20', '09:30:00', 'Transportadora', 'Frágil - Vidro', 'Pendente', '901.234.567-89', '901.234.567-89'),
('2023-04-25', '16:00:00', 'Correio', NULL, 'Entregue', '012.345.678-90', '234.567.890-12');

-- 9. Popular tabela livro_has_pedido
INSERT INTO `livro_has_pedido` (`livro_isbn_13`, `pedido_id`, `quant`, `valor_unit`) VALUES
('978-85-359-1979-5', 1, 1, 49.90),
('978-85-325-3028-8', 1, 2, 39.90),
('978-85-8057-526-6', 2, 1, 34.90),
('978-85-7542-585-1', 3, 1, 59.90),
('978-85-510-0244-8', 3, 1, 29.90),
('978-85-325-3028-8', 4, 1, 39.90),
('978-85-7542-585-1', 5, 3, 59.90),
('978-85-01-11204-7', 6, 1, 79.90),
('978-85-422-1843-3', 6, 2, 24.90),
('978-85-431-0485-0', 7, 1, 29.90),
('978-85-7542-823-4', 8, 1, 49.90),
('978-85-510-0276-9', 8, 1, 34.90),
('978-85-359-1979-5', 9, 1, 49.90),
('978-85-325-3028-8', 10, 2, 39.90),
('978-85-8057-526-6', 10, 1, 34.90);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;