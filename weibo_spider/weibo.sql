CREATE TABLE `weibo` (
  `comment_cont` varchar(1000) DEFAULT NULL,
  `comment_screen_name` varchar(255) DEFAULT NULL,
  `comment_id` varchar(30) DEFAULT NULL,
  `user_id` varchar(30) DEFAULT NULL,
  `create_time` varchar(40) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1781 DEFAULT CHARSET=utf8mb4;