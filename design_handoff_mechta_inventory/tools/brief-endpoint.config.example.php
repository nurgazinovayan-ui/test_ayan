<?php
/**
 * Скопировать в brief-endpoint.config.php рядом и заполнить.
 * Настоящий файл в репозиторий не попадает — в нём пароль.
 */
return [
    'to'        => ['marketing@mechta.com.kz'],
    'from'      => 'noreply@mechta.com.kz',

    'transport' => 'smtp',              // 'smtp' или 'mail' (локальный sendmail)

    'smtp_host'   => 'mail.mechta.com.kz',
    'smtp_port'   => 465,
    'smtp_secure' => 'ssl',             // 'ssl' для 465, 'tls' для 587, '' для 25
    'smtp_user'   => 'noreply@mechta.com.kz',
    'smtp_pass'   => 'сюда-пароль',

    // Домен, с которого открывается лендинг. Пустой список разрешает всем.
    'allow_origins' => ['https://ваш-хостинг-лендинга'],

    'rate_limit' => 20,
];
