SET @@auto_increment_increment=9;

DROP TABLE IF EXISTS `tb_user`;
DROP TABLE IF EXISTS `tb_cate`;
DROP TABLE IF EXISTS `tb_article`;
DROP TABLE IF EXISTS `news_comment`;

CREATE TABLE `tb_user` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(20) COMMENT '登陆用户名',
  `email` varchar(20) COMMENT '邮箱',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态，是否可用，0-不可用，1-可用',
  `password` varchar(93) NULL COMMENT '密码',
  `nickname` varchar(32) NOT NULL COMMENT '昵称',
  `user_pic` varchar(128) NULL COMMENT '头像',
  `last_login` datetime NULL COMMENT '最后登录时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户信息表';

CREATE TABLE `tb_cate` (
  `cate_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `cate_name` varchar(32) NOT NULL COMMENT '分类名称',
  `alias` varchar(32) NOT NULL COMMENT '分类别名',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除：0-未删除、1-已删除、2-不可删除',
  PRIMARY KEY (`cate_id`),
  UNIQUE KEY `cate_name` (`cate_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='文章分类表';

CREATE TABLE `tb_article` (
  `article_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '文章ID',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `cate_id` int(11) unsigned NOT NULL COMMENT '分类ID',
  `title` varchar(128) NOT NULL COMMENT '标题',
  `content` longtext NOT NULL COMMENT '文章内容',
  `cover_img` varchar(128) COMMENT '封面',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '文章状态，0-草稿，1-已发布',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除：0-未删除、1-已删除',
  PRIMARY KEY (`article_id`),
  KEY `user_id` (`user_id`),
  KEY `article_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章内容表';

CREATE TABLE `news_comment` (
  `comment_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '评论id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `article_id` bigint(20) unsigned NOT NULL COMMENT '文章ID',
  `parent_id` bigint(20) unsigned NULL COMMENT '评论ID',
  `content` varchar(200) NOT NULL COMMENT '评论内容',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除：0-未删除、1-已删除、2-不可删除',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`comment_id`),
  KEY `article_id` (`article_id`),
  KEY `parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章评论';

LOCK TABLES `tb_cate` WRITE;
INSERT INTO `tb_cate` VALUES (1,'最新','ZuiXin',DEFAULT,DEFAULT,2), (2,'科技','KeJi',DEFAULT,DEFAULT,2);
UNLOCK TABLES;