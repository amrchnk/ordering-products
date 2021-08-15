-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июл 08 2021 г., 14:53
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
-- База данных: `catalog_test`
--

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

CREATE TABLE `categories` (
  `category` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `categories`
--

INSERT INTO `categories` (`category`) VALUES
('Вода'),
('Все'),
('Овощи'),
('Фрукты');

-- --------------------------------------------------------

--
-- Структура таблицы `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `category` varchar(20) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `image_name` varchar(50) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `price` double NOT NULL,
  `number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `products`
--

INSERT INTO `products` (`id`, `name`, `category`, `description`, `image_name`, `unit`, `price`, `number`) VALUES
(1, 'Яблоко обычное', 'Фрукты', NULL, 'apple.png', 'кг', 120, 12),
(2, 'Банан', 'Фрукты', NULL, 'banana.png', 'кг', 60, 20),
(3, 'Апельсин', 'Фрукты', NULL, 'orange.png', 'кг', 230, 34),
(4, 'Помидоры', 'Овощи', 'Очень вкусные-превкусные помидоры с огорода моей бабушки', 'tomato.png', 'кг', 130, 6),
(5, 'Вода \"Святой источник\" 0,5л', 'Вода', NULL, 'water.png', 'шт', 15, 200);

-- --------------------------------------------------------

--
-- Структура таблицы `units`
--

CREATE TABLE `units` (
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `units`
--

INSERT INTO `units` (`name`) VALUES
('кг'),
('шт');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `products_category` (`category`),
  ADD KEY `products_unit` (`unit`);

--
-- Индексы таблицы `units`
--
ALTER TABLE `units`
  ADD PRIMARY KEY (`name`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category`) REFERENCES `categories` (`category`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`unit`) REFERENCES `units` (`name`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
