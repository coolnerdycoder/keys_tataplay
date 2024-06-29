<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

function load_keys() {
    $json_data = file_get_contents('keys.json');
    return json_decode($json_data, true);
}

function get_keys_by_channel_id($channel_id) {
    $keys_data = load_keys();
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
            return json_encode(["keys" => $keys, "type" => "temporary"]);
        }
    }
    return json_encode(["error" => "Keys not found for this channel_id"], JSON_UNESCAPED_SLASHES);
}

if (!isset($_GET['id'])) {
    echo json_encode(["error" => "Channel ID not provided"], JSON_UNESCAPED_SLASHES);
    http_response_code(400); // Bad request
    exit();
}

$channel_id = $_GET['id'];
echo get_keys_by_channel_id($channel_id);
?>