-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июл 08 2021 г., 22:41
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
-- База данных: `orders_test`
--

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `id_client` int(11) NOT NULL,
  `cost` double NOT NULL,
  `status` varchar(64) NOT NULL,
  `address` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `orders`
--

INSERT INTO `orders` (`id`, `id_client`, `cost`, `status`, `address`) VALUES
(1, 5, 502.12, 'Готовится', 'ул. Ленина, дом 12, кв. 45'),
(5, 5, 195.15, 'Ожидает оплаты', 'пер. Космонавтов, дом 17, кв. 78');

-- --------------------------------------------------------

--
-- Структура таблицы `products_of_order`
--

CREATE TABLE `products_of_order` (
  `id_order` int(11) NOT NULL,
  `id_product` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `typical_order_statuses`
--

CREATE TABLE `typical_order_statuses` (
  `status_name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `typical_order_statuses`
--

INSERT INTO `typical_order_statuses` (`status_name`) VALUES
('В пути'),
('Выполнен'),
('Готовится'),
('Ожидает оплаты'),
('Оплачен');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `status_fk` (`status`);

--
-- Индексы таблицы `products_of_order`
--
ALTER TABLE `products_of_order`
  ADD PRIMARY KEY (`id_order`,`id_product`);

--
-- Индексы таблицы `typical_order_statuses`
--
ALTER TABLE `typical_order_statuses`
  ADD PRIMARY KEY (`status_name`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `status_fk` FOREIGN KEY (`status`) REFERENCES `typical_order_statuses` (`status_name`) ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `products_of_order`
--
ALTER TABLE `products_of_order`
  ADD CONSTRAINT `products_of_order_ibfk_1` FOREIGN KEY (`id_order`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
