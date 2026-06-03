_processed_messages: set[str] = set()


def was_processed(message_id: str | None) -> bool:
    if not message_id:
        return False

    return message_id in _processed_messages


def mark_as_processed(message_id: str | None) -> None:
    if message_id:
        _processed_messages.add(message_id)
