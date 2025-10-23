-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-10-2025 a las 03:42:10
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `paw_pet`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `idCarrito` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `fechaCreacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carrito`
--

INSERT INTO `carrito` (`idCarrito`, `idUsuario`, `fechaCreacion`) VALUES
(1, 14, '2025-10-21 19:19:27'),
(2, 15, '2025-10-22 09:04:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `idCategoria` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`idCategoria`, `nombre`, `descripcion`, `imagen`) VALUES
(5, 'Higiene', 'Para perro, gato y roedor ', 'higene_mascotas.webp'),
(7, 'Alimentos para perro ', 'Alimento', 'al.perros.png'),
(9, 'Medicamentos', 'Para perro, gato y roedor ', 'medicamentos_mascotas.webp'),
(10, 'Alimentos para gatos ', 'Alimento', 'comida.gatos.png'),
(11, 'Alimentos Para roedores ', 'Alimento', 'al.conejos.png'),
(12, 'Juguetes ', 'Para tu mascota', 'juguetes_mascotas.jpeg'),
(13, 'Accesorios', 'Para tu mascota', 'accesorios_mascotas.webp');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_carrito`
--

CREATE TABLE `detalle_carrito` (
  `idDetalle` int(11) NOT NULL,
  `IdCarrito` int(11) NOT NULL,
  `idProducto` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_carrito`
--

INSERT INTO `detalle_carrito` (`idDetalle`, `IdCarrito`, `idProducto`, `cantidad`) VALUES
(10, 1, 15, 1),
(11, 1, 7, 1),
(12, 1, 8, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_orden`
--

CREATE TABLE `detalle_orden` (
  `idDetalle` int(11) NOT NULL,
  `idOrden` int(11) NOT NULL,
  `idProducto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago`
--

CREATE TABLE `metodo_pago` (
  `idMetodo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenes`
--

CREATE TABLE `ordenes` (
  `idOrden` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `estado` varchar(50) DEFAULT 'pendiente',
  `total` decimal(10,2) DEFAULT NULL,
  `metodo_pago` varchar(100) DEFAULT NULL,
  `referencia_pago` varchar(100) DEFAULT NULL,
  `fecha_pago` datetime DEFAULT NULL,
  `idMetodo` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `idProducto` int(11) NOT NULL,
  `nombre_producto` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT 0,
  `fecha_vencimiento` date DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `idCategoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`idProducto`, `nombre_producto`, `descripcion`, `precio`, `cantidad`, `fecha_vencimiento`, `imagen`, `idCategoria`) VALUES
(2, 'dog chow', 'comida para perro', 5000, 8, NULL, 'descarga.jpeg', 7),
(6, 'Ringo', 'Alimento para perro', 5900, 4, NULL, 'descarga_1.jpeg', 7),
(7, 'Alpo', 'Alimento', 6700, 3, NULL, 'comidsa_perro.webp', 7),
(8, 'Dogourmet', 'Alimento', 4600, 2, NULL, 'perro3.png', 7),
(9, 'Wiskat', 'Alimento húmedo', 4000, 5, NULL, 'al.gatos.png', 10),
(10, 'Monello', 'Alimento', 8000, 10, NULL, 'cm.gatos.png', 10),
(11, 'Q-ida cat', 'Alimento', 5800, 12, NULL, 'comida.gatos.png', 10),
(12, 'Vitakraft', 'Alimento', 5000, 13, NULL, 'roedores_comioda.webp', 11),
(13, 'Riga', 'Alimento', 5400, 15, NULL, 'roedores_comida.jpg', 11),
(14, 'shampoo', 'Higiene', 7000, 7, NULL, 'shampoo.png', 5),
(15, 'Pañitos', 'Higiene', 6700, 9, NULL, 'to.higiene.png', 5),
(16, 'Peines', 'Higiene', 12000, 8, NULL, 'peines.png', 5),
(17, 'Ratones para gatos', 'Juguetes', 8900, 17, NULL, 'ratones.webp', 12),
(18, 'kit de juguetes para perro ', 'Juguetes', 20000, 20, NULL, 'kit_perro.webp', 12),
(19, 'rueda de roedores ', 'Juguetes', 25000, 5, NULL, 'rueda.webp', 12),
(20, 'Correas de perro', 'perro', 12000, 5, NULL, 'correa.png', 13),
(21, 'transportador', 'Accesorio', 55000, 18, NULL, 'transportadores.png', 13),
(22, 'Antipulgas para gatos ', 'Medicamentos', 8000, 8, NULL, 'antipulgas2.png', 9),
(23, 'Antipulgas para perros', 'Medicamentos', 8500, 12, NULL, 'antipulgas3.png', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_login`
--

CREATE TABLE `registro_login` (
  `id` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `idRol` int(11) NOT NULL,
  `nombreRol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`idRol`, `nombreRol`) VALUES
(1, 'Admin'),
(2, 'Usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `reset_token` varchar(255) DEFAULT NULL,
  `token_expiry` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `username`, `password`, `reset_token`, `token_expiry`) VALUES
(3, 'lorens', 'garcia', 'lorena@gmail.com', 'scrypt:32768:8:1$ADTT1KAVY1PYljWX$334a72bfb78fc36278de3bdedd1df1ff8ade2e95465b2cae0f11ebc3ad02094f2332b259cac7f32f10c3c3bc1fa9a9c7ece1a3b63d5b025f9bbd7d66566cbe42', NULL, NULL),
(4, 'Gabriela', 'Ortega', 'jeonmagalum@gmail.com', 'scrypt:32768:8:1$N7H3AlZZIzxM1QvV$c215430a946dad60fad3df1bf96351a1475fc72b78d9023d63a10ad418e78fe0ef7b37b602756c46636a0e8d4d1bee81a59d59be1b736122c9bf77787293407f', NULL, NULL),
(5, 'maya', 'ortega', 'magalum8gm@gmail.com', 'scrypt:32768:8:1$Vk1jg8WGADisznnr$51824822e5ea79254a1ac35e01fb17a20847793d8138e4547ee7c352f0840e690a6f33cc05545a2c6f3f0c5e9223349b74dc394d2baf78dbacbeaeb1bdd829a7', NULL, NULL),
(10, 'maya', 'ortega', 'maya@gmail.com', 'scrypt:32768:8:1$FiLVD7Ta83CF2K1C$63245d37e824ab8e58283f8d36ec9f96b3550267de8faa703add7c5bc403a4c2c92e8c7787f1e4c97cfdfe07b88c21b7bacec0b3a477708841c32cff91d65393', NULL, NULL),
(13, 'sarid', 'morales', 'saridm@g', 'scrypt:32768:8:1$ElaeWuRIxxjcPFAe$47a0346ec0b6ff0757457a5ef6059a25cb555758c038b70aac61928cd0d56c578bd1e47ad563a7f002244ae01b9ac0b27435a10297cb9a4b713e61cca46ff965', NULL, NULL),
(14, 'lorena', 'garcia', 'l@h', 'scrypt:32768:8:1$9mJA5JaySWhHG0pQ$8ef3841bb8a98c1de6c5671013439a389077a4380f0169c2400784f4f3d209c245e2cc4d600fd2fb93cb865ef3106c4a5abfe3b8785f558270df1519b11d1916', NULL, NULL),
(15, 'lorena', 'garcia', 'lorenah@gmail.com', 'scrypt:32768:8:1$9IN3z1vyjRHKJ5Sc$6134fcc0a05a9bbaafda943b06c979c26ef15161332ed6ae3244d0df0dda9294a958f536b6551867a623e438d2e91e8042be206b69b57e33458fbb5e037851e5', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_rol`
--

CREATE TABLE `usuario_rol` (
  `idUsuario` int(11) NOT NULL,
  `idRol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario_rol`
--

INSERT INTO `usuario_rol` (`idUsuario`, `idRol`) VALUES
(10, 2),
(13, 2),
(14, 1),
(15, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`idCarrito`),
  ADD KEY `idUsuario` (`idUsuario`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`idCategoria`);

--
-- Indices de la tabla `detalle_carrito`
--
ALTER TABLE `detalle_carrito`
  ADD PRIMARY KEY (`idDetalle`),
  ADD KEY `IdCarrito` (`IdCarrito`),
  ADD KEY `idProducto` (`idProducto`);

--
-- Indices de la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  ADD PRIMARY KEY (`idDetalle`),
  ADD KEY `idOrden` (`idOrden`),
  ADD KEY `idProducto` (`idProducto`);

--
-- Indices de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  ADD PRIMARY KEY (`idMetodo`);

--
-- Indices de la tabla `ordenes`
--
ALTER TABLE `ordenes`
  ADD PRIMARY KEY (`idOrden`),
  ADD KEY `idUsuario` (`idUsuario`),
  ADD KEY `idMetodo` (`idMetodo`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`idProducto`),
  ADD KEY `idCategoria` (`idCategoria`);

--
-- Indices de la tabla `registro_login`
--
ALTER TABLE `registro_login`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idUsuario` (`idUsuario`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`idRol`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuario`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `usuario_rol`
--
ALTER TABLE `usuario_rol`
  ADD PRIMARY KEY (`idUsuario`,`idRol`),
  ADD KEY `idRol` (`idRol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `idCarrito` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `idCategoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `detalle_carrito`
--
ALTER TABLE `detalle_carrito`
  MODIFY `idDetalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  MODIFY `idDetalle` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  MODIFY `idMetodo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ordenes`
--
ALTER TABLE `ordenes`
  MODIFY `idOrden` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `idProducto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `registro_login`
--
ALTER TABLE `registro_login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `idRol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`);

--
-- Filtros para la tabla `detalle_carrito`
--
ALTER TABLE `detalle_carrito`
  ADD CONSTRAINT `detalle_carrito_ibfk_1` FOREIGN KEY (`IdCarrito`) REFERENCES `carrito` (`idCarrito`),
  ADD CONSTRAINT `detalle_carrito_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idProducto`);

--
-- Filtros para la tabla `detalle_orden`
--
ALTER TABLE `detalle_orden`
  ADD CONSTRAINT `detalle_orden_ibfk_1` FOREIGN KEY (`idOrden`) REFERENCES `ordenes` (`idOrden`),
  ADD CONSTRAINT `detalle_orden_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idProducto`);

--
-- Filtros para la tabla `ordenes`
--
ALTER TABLE `ordenes`
  ADD CONSTRAINT `ordenes_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`),
  ADD CONSTRAINT `ordenes_ibfk_2` FOREIGN KEY (`idMetodo`) REFERENCES `metodo_pago` (`idMetodo`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categorias` (`idCategoria`);

--
-- Filtros para la tabla `registro_login`
--
ALTER TABLE `registro_login`
  ADD CONSTRAINT `registro_login_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuario_rol`
--
ALTER TABLE `usuario_rol`
  ADD CONSTRAINT `usuario_rol_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `usuario_rol_ibfk_2` FOREIGN KEY (`idRol`) REFERENCES `roles` (`idRol`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
