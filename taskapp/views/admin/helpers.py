import taskapp.conf as conf


def get_extension(content_type: str) -> str:
    """
    Получает расширение файла, по content_type.
    """
    return content_type.split("/")[-1]


def create_telegram_photo_url(file_id: str):
    """
    Собирает ссылку на фотографию из telegram.
    """
    return f"{conf.BACKEND_BASE_URL}_internal_/tphoto/{file_id}"
