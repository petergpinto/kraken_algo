

```sql
CREATE TABLE `tradable_pairs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pair` varchar(10) DEFAULT NULL,
  `orderMin` double DEFAULT NULL,
  `base` varchar(10) DEFAULT NULL,
  `altname` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pair` (`pair`)
) ENGINE=InnoDB AUTO_INCREMENT=508 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```


```sql
CREATE TABLE `moving_average` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pairId` int DEFAULT NULL,
  `type` varchar(10) DEFAULT NULL,
  `period` int DEFAULT NULL,
  `value` double DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_2` (`type`,`period`,`timestamp`),
  KEY `pairId` (`pairId`),
  CONSTRAINT `moving_average_ibfk_1` FOREIGN KEY (`pairId`) REFERENCES `tradable_pairs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

