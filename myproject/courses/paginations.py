from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинация для вывода всех уроков и курсов."""
    page_size = 5  # Количество элементов на странице по умолчанию
    page_size_query_param = 'page_size'  # Клиент может указать свой размер страницы
    max_page_size = 10  # Максимальное количество элементов на странице
