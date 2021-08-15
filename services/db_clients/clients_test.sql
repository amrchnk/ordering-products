-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июл 06 2021 г., 10:57
-- Версия сервера: 10.4.14-MariaDB
-- Версия PHP: 7.4.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `clients_test`
--

-- --------------------------------------------------------

--
-- Структура таблицы `clients`
--

CREATE TABLE `clients` (
  `id` int(11) NOT NULL,
  `full_name` varchar(128) NOT NULL,
  `email` varchar(256) NOT NULL,
  `password` varchar(32) DEFAULT 'NULL',
  `phone_num` varchar(12) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `clients`
--

INSERT INTO `clients` (`id`, `full_name`, `email`, `password`, `phone_num`) VALUES
(1, 'Денис Смиянов', 'denis@example.com', '123456', '+79991230099'),
(2, 'Аня Мирченко', 'anya@example.com', '1q2w3e', '+71234567890'),
(3, 'Иванов Иван', 'ivanov@example.com', '123qwe', '+71231231223'),
(4, 'Петров Павел', 'petrov@example.com', 'petrov', '12134'),
(5, 'Мирченко Анна Григорьевна', 'mirchenko1702@gmail.com', '1234', '9879878'),
(6, 'Anek', 'anek@mail', 'aneka', '87'),
(7, 'Шельгова Дарья', 'dasha@example.com', '1611', '+79294757539'),
(8, 'Архипов Андрей', 'тест', '323', 'тест');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_uindex` (`email`),
  ADD UNIQUE KEY `users_phone_num_uindex` (`phone_num`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `clients`
--
ALTER TABLE `clients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;