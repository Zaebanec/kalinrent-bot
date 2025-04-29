def chunk_list(data, n):
    """Разбивает список на части по n элементов"""
    for i in range(0, len(data), n):
        yield data[i:i + n]
