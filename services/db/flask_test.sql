-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июл 12 2021 г., 13:14
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
-- База данных: `flask`
--

-- --------------------------------------------------------

--
-- Структура таблицы `carts`
--

CREATE TABLE `carts` (
  `id` int(11) NOT NULL,
  `id_client` int(11) NOT NULL,
  `cost` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Структура таблицы `payment`
--

CREATE TABLE `payment` (
  `id` int(11) NOT NULL,
  `id_order` int(11) NOT NULL,
  `cost` double NOT NULL,
  `status` varchar(64) NOT NULL DEFAULT 'Не подтвержден'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `payment`
--

INSERT INTO `payment` (`id`, `id_order`, `cost`, `status`) VALUES
(1, 1, 502.12, 'Подтвержден');

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
-- Структура таблицы `products_of_cart`
--

CREATE TABLE `products_of_cart` (
  `id_cart` int(11) NOT NULL,
  `id_product` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Индексы таблицы `carts`
--
ALTER TABLE `carts`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category`);

--
-- Индексы таблицы `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_uindex` (`email`),
  ADD UNIQUE KEY `users_phone_num_uindex` (`phone_num`);

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `status_fk` (`status`);

--
-- Индексы таблицы `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `status_pay_fk` (`status`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `products_category` (`category`),
  ADD KEY `products_unit` (`unit`);

--
-- Индексы таблицы `products_of_cart`
--
ALTER TABLE `products_of_cart`
  ADD PRIMARY KEY (`id_cart`,`id_product`);

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
-- Индексы таблицы `units`
--
ALTER TABLE `units`
  ADD PRIMARY KEY (`name`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `carts`
--
ALTER TABLE `carts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `clients`
--
ALTER TABLE `clients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `payment`
--
ALTER TABLE `payment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
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
-- Ограничения внешнего ключа таблицы `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category`) REFERENCES `categories` (`category`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`unit`) REFERENCES `units` (`name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `products_of_cart`
--
ALTER TABLE `products_of_cart`
  ADD CONSTRAINT `products_of_cart_ibfk_1` FOREIGN KEY (`id_cart`) REFERENCES `carts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `products_of_order`
--
ALTER TABLE `products_of_order`
  ADD CONSTRAINT `products_of_order_ibfk_1` FOREIGN KEY (`id_order`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
