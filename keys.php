<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

if (!isset($_GET['id'])) {
    echo json_encode(["error" => "Channel ID not provided"], JSON_UNESCAPED_SLASHES);
    http_response_code(400); // Bad request
    exit();
}

$channel_id = $_GET['id'];
$keys_data = json_decode(file_get_contents('keys.json'), true);

foreach ($keys_data as $item) {
    if ($item['channel_id'] == $channel_id) {
        // Ensure the keys are ordered correctly
        $keys = array_map(function($key) {
            return [
                "kty" => $key["kty"],
                "k" => $key["k"],
                "kid" => $key["kid"]
            ];
        }, $item['keys']);
        echo json_encode(["keys" => $keys, "type" => "temporary"], JSON_UNESCAPED_SLASHES);
        exit();
    }
}

echo json_encode(["error" => "Keys not found for this channel_id"], JSON_UNESCAPED_SLASHES);
http_response_code(404); // Not found
?>
