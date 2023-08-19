from app.dao.base import BaseDAO
from app.hotels.models import Images


class ImagesDAO(BaseDAO):
    model = Images