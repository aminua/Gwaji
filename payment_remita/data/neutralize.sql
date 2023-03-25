-- disable remita payment provider
UPDATE payment_provider
   SET remita_public_key = NULL,
       remita_secret_key = NULL,
       remita_webhook_secret = NULL;
