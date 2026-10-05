<?php
/**
 * Приём брифа с лендинга и отправка письма с собственного сервера.
 *
 * Положить на сервер mechta.com.kz (например /api/brief.php) и указать его
 * адрес в webhookUrl в window.MECHTA_CONFIG на лендинге. Страница шлёт
 * POST с JSON — тем же, что уходил в Make.
 *
 * Зачем свой сервер: письмо отправляется с того же домена, на который
 * приходит. Ни Яндекс, ни кто-либо ещё не видит стороннего отправителя,
 * поэтому антиспуфинг-фильтры, на которых всё ломалось, не срабатывают.
 *
 * Зависимостей нет: SMTP говорит сам, PHPMailer и composer не нужны.
 *
 * Настройки — в brief-endpoint.config.php рядом (см. .example).
 * Так пароль не попадает в репозиторий.
 */

declare(strict_types=1);

$CONFIG = [
    // Куда приходят брифы. Можно несколько.
    'to'          => ['marketing@mechta.com.kz'],

    // От кого. Должен быть ящик на этом же домене, иначе теряется весь смысл.
    'from'        => 'noreply@mechta.com.kz',
    'from_name'   => 'Mechta Inventory 2026',

    // 'smtp' — через почтовый сервер с логином и паролем;
    // 'mail' — через локальный sendmail, без пароля (если он настроен).
    'transport'   => 'smtp',

    'smtp_host'   => 'mail.mechta.com.kz',
    'smtp_port'   => 465,
    'smtp_secure' => 'ssl',          // 'ssl' для 465, 'tls' для 587, '' для 25
    'smtp_user'   => 'noreply@mechta.com.kz',
    'smtp_pass'   => '',

    // Домены, которым разрешено слать сюда из браузера. Лендинг лежит
    // на хостинге, а открывается в iframe Тильды — в Origin будет адрес
    // хостинга лендинга. Пустой список разрешает всем.
    'allow_origins' => [],

    // Не больше стольких брифов с одного IP за час.
    'rate_limit'  => 20,
];

$local = __DIR__ . '/brief-endpoint.config.php';
if (is_file($local)) {
    $CONFIG = array_merge($CONFIG, (array) require $local);
}

// ---------------------------------------------------------------- CORS ----

$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($CONFIG['allow_origins'] === []) {
    header('Access-Control-Allow-Origin: *');
} elseif ($origin !== '' && in_array($origin, $CONFIG['allow_origins'], true)) {
    header('Access-Control-Allow-Origin: ' . $origin);
    header('Vary: Origin');
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept');
header('Access-Control-Max-Age: 86400');

// Страница шлёт Content-Type: application/json, а это не «простой» запрос —
// браузер сначала спрашивает разрешение методом OPTIONS. Без ответа на него
// основной POST даже не уйдёт.
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') {
    http_response_code(204);
    exit;
}

header('Content-Type: application/json; charset=UTF-8');

function fail(int $code, string $message): never
{
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $message], JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    fail(405, 'Только POST');
}

// ------------------------------------------------------------- приём ------

$raw = file_get_contents('php://input');
if ($raw === false || $raw === '') {
    fail(400, 'Пустой запрос');
}
if (strlen($raw) > 256 * 1024) {
    fail(413, 'Слишком большой запрос');
}

$data = json_decode($raw, true);
if (!is_array($data)) {
    fail(400, 'Ожидался JSON');
}

// Ботам поле botcheck не видно, людям тоже — его заполняют только скрипты.
if (!empty($data['botcheck'])) {
    echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);  // молча не отправляем
    exit;
}

$briefText = trim((string) ($data['brief_text'] ?? ''));
if ($briefText === '') {
    fail(422, 'Пустой бриф');
}

// -------------------------------------------------------- ограничение ----

$ip = (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$bucket = sys_get_temp_dir() . '/brief_rl_' . sha1($ip) . '.txt';
$now = time();
$hits = is_file($bucket)
    ? array_filter(
        array_map('intval', explode(',', (string) file_get_contents($bucket))),
        static fn(int $t): bool => $t > $now - 3600
    )
    : [];
if (count($hits) >= (int) $CONFIG['rate_limit']) {
    fail(429, 'Слишком много заявок, попробуйте позже');
}
$hits[] = $now;
@file_put_contents($bucket, implode(',', $hits), LOCK_EX);

// ---------------------------------------------------------- письмо -------

/** Заголовок с кириллицей по RFC 2047, иначе в теме письма будет каша. */
function mimeHeader(string $value): string
{
    return preg_match('//u', $value) && preg_match('/[^\x20-\x7E]/', $value)
        ? '=?UTF-8?B?' . base64_encode($value) . '?='
        : $value;
}

/** Защита от подстановки чужих заголовков через перевод строки. */
function headerSafe(string $value): string
{
    return trim(str_replace(["\r", "\n"], ' ', $value));
}

function validEmail(string $value): ?string
{
    $value = headerSafe($value);
    return filter_var($value, FILTER_VALIDATE_EMAIL) ? $value : null;
}

$subject = headerSafe((string) ($data['subject'] ?? 'Бриф кампании — Mechta Inventory 2026'));
$replyTo = validEmail((string) ($data['contact_email'] ?? ''));

$to = array_values(array_filter(array_map(
    static fn($a): ?string => validEmail((string) $a),
    (array) $CONFIG['to']
)));
if ($to === []) {
    fail(500, 'Получатель не настроен');
}

$from = validEmail((string) $CONFIG['from']);
if ($from === null) {
    fail(500, 'Отправитель не настроен');
}

$headers = [
    'From: ' . mimeHeader(headerSafe((string) $CONFIG['from_name'])) . ' <' . $from . '>',
    'To: ' . implode(', ', $to),
    'Subject: ' . mimeHeader($subject),
    'Date: ' . date('r'),
    'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . substr(strrchr($from, '@') ?: '@local', 1) . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
];
if ($replyTo !== null) {
    $headers[] = 'Reply-To: ' . $replyTo;
}

// base64 с переносами: длинные строки брифа иначе рубит сам SMTP.
$body = rtrim(chunk_split(base64_encode($briefText), 76, "\r\n"));

// ------------------------------------------------------------ отправка ---

/** Читает ответ SMTP, включая многострочный (250-FOO ... 250 BAR). */
function smtpRead($socket): string
{
    $out = '';
    while (($line = fgets($socket, 1024)) !== false) {
        $out .= $line;
        if (strlen($line) < 4 || $line[3] !== '-') {
            break;
        }
    }
    return $out;
}

function smtpCmd($socket, string $cmd, string $expect): void
{
    if ($cmd !== '') {
        fwrite($socket, $cmd . "\r\n");
    }
    $reply = smtpRead($socket);
    if (!str_starts_with(trim($reply), $expect)) {
        throw new RuntimeException('SMTP: ожидался ' . $expect . ', получено: ' . trim($reply));
    }
}

function sendSmtp(array $cfg, array $to, array $headers, string $body, string $from): void
{
    $prefix = $cfg['smtp_secure'] === 'ssl' ? 'ssl://' : '';
    $socket = @stream_socket_client(
        $prefix . $cfg['smtp_host'] . ':' . $cfg['smtp_port'],
        $errno, $errstr, 20
    );
    if (!$socket) {
        throw new RuntimeException('Не удалось подключиться к SMTP: ' . $errstr);
    }
    stream_set_timeout($socket, 20);

    try {
        smtpCmd($socket, '', '220');
        $ehlo = 'EHLO ' . (gethostname() ?: 'localhost');
        smtpCmd($socket, $ehlo, '250');

        if ($cfg['smtp_secure'] === 'tls') {
            smtpCmd($socket, 'STARTTLS', '220');
            if (!stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new RuntimeException('Не удалось включить TLS');
            }
            smtpCmd($socket, $ehlo, '250');   // после STARTTLS EHLO повторяют
        }

        if (($cfg['smtp_user'] ?? '') !== '') {
            smtpCmd($socket, 'AUTH LOGIN', '334');
            smtpCmd($socket, base64_encode((string) $cfg['smtp_user']), '334');
            smtpCmd($socket, base64_encode((string) $cfg['smtp_pass']), '235');
        }

        smtpCmd($socket, 'MAIL FROM:<' . $from . '>', '250');
        foreach ($to as $rcpt) {
            smtpCmd($socket, 'RCPT TO:<' . $rcpt . '>', '250');
        }
        smtpCmd($socket, 'DATA', '354');

        // Точка в начале строки завершила бы письмо — её удваивают.
        $payload = implode("\r\n", $headers) . "\r\n\r\n" . $body . "\r\n";
        $payload = preg_replace('/^\./m', '..', $payload);
        fwrite($socket, $payload . ".\r\n");
        smtpCmd($socket, '', '250');

        fwrite($socket, "QUIT\r\n");
    } finally {
        fclose($socket);
    }
}

try {
    if ($CONFIG['transport'] === 'mail') {
        $head = array_values(array_filter(
            $headers,
            static fn(string $h): bool => !str_starts_with($h, 'To: ') && !str_starts_with($h, 'Subject: ')
        ));
        if (!mail(implode(', ', $to), mimeHeader($subject), $body, implode("\r\n", $head))) {
            throw new RuntimeException('mail() вернул false');
        }
    } else {
        sendSmtp($CONFIG, $to, $headers, $body, $from);
    }
} catch (Throwable $e) {
    error_log('[brief] ' . $e->getMessage());
    // Наружу подробности не отдаём: по ним видно устройство почты.
    fail(502, 'Письмо не отправлено');
}

echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);
