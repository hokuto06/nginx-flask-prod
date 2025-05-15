<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'vendor/autoload.php';

header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
  http_response_code(405);
  echo json_encode(["error" => "Method not allowed"]);
  exit;
}

// Sanitización
$name = strip_tags(trim($_POST["name"] ?? ''));
$email = filter_var(trim($_POST["email"] ?? ''), FILTER_SANITIZE_EMAIL);
$subject = strip_tags(trim($_POST["subject"] ?? ''));
$message = trim($_POST["message"] ?? '');

if (empty($name) || empty($message) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  echo json_encode(["error" => "Invalid input"]);
  exit;
}

$mail = new PHPMailer(true);

try {
  // Configuración SMTP
  $mail->isSMTP();
  $mail->Host = 'smtp.gmail.com';
  $mail->SMTPAuth = true;
  $mail->Username = 'emartins.ecnex@gmail.com';
  $mail->Password = 'fopc bdns udew rbit';
  $mail->SMTPSecure = 'tls';
  $mail->Port = 587;

  // Cabeceras
  $mail->setFrom('emartins.ecnex@gmail.com', 'Portfolio Web');
  $mail->addAddress('esteban.a.martins@gmail.com');
  $mail->addReplyTo($email, $name);
  $mail->Subject = "Nuevo mensaje desde tu sitio: $subject";
  $mail->Body    = "Nombre: $name\nEmail: $email\n\nMensaje:\n$message";

  $mail->send();
  echo json_encode(["success" => "Message sent successfully"]);
} catch (Exception $e) {
  http_response_code(500);
  echo json_encode(["error" => "Mailer Error: " . $mail->ErrorInfo]);
}
