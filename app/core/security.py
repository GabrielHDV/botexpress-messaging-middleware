def mask_phone(phone: str) -> str:
    if len(phone) <= 4:
        return "****"

    return f"{phone[:4]}****{phone[-2:]}"

