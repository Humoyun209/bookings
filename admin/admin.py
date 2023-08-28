from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels, Images
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    # metadata
    name = 'Пользователь'
    name_plural = 'Пользователы'
    icon = "fa-solid fa-user"
    
    # Список пользователей
    column_list = [Users.id, Users.email]
    column_default_sort = [Users.id]
    column_default_sort = [(Users.id, False), (Users.email, True)]
    column_searchable_list = [Users.email]
    
    # Информация о пользователи
    can_delete = False
    column_details_list = [Users.id, Users.email, Users.bookings]
    
class BookingsAdmin(ModelView, model=Bookings):
    # metadata
    name = 'Брон'
    name_plural = 'Броны'
    icon = "fa-solid fa-book"
    
    # Список пользователей
    column_list = [ Bookings.id, Bookings.date_from, Bookings.date_to, Bookings.user]
    column_default_sort = [(Bookings.date_from, False), (Bookings.id, True)]
    
    # Информация о пользователи
    column_details_list = [column.name for column in Bookings.__table__.c] + [Bookings.user]
    

class HotelsAdmin(ModelView, model=Hotels):
    # metadata
    name = 'Отел'
    name_plural = 'Отелы'
    icon = "fa-solid fa-hotel"
    
    # Список пользователей
    column_list = [Hotels.name, Hotels.location, Hotels.rooms_quantity]
    column_default_sort = [(Hotels.name, True), (Hotels.id, False)]
    
    # Информация о пользователи
    column_details_list = [column.name for column in Hotels.__table__.c] + [Hotels.rooms] + [Hotels.images]
    can_delete = False
    

class RoomsAdmin(ModelView, model=Rooms):
    # metadata
    name = 'Комната'
    name_plural = 'Комнаты'
    icon = "fa-solid fa-bed"
    
    # Список пользователей
    column_list = [Rooms.name, Rooms.quantity, Rooms.price] + [Rooms.hotel]
    column_default_sort = [(Rooms.name, True), (Rooms.id, False)]
    
    # Информация о пользователи
    column_details_list = [column.name for column in Rooms.__table__.c] + [Rooms.bookings] + [Rooms.hotel]
    can_delete = False
    

class ImagesAdmin(ModelView, model=Images):
    # metadata
    name = 'Фото отеля'
    name_plural = 'Фотки отеля'
    icon = "fa-solid fa-image"
    
    # Список пользователей
    column_list = [Images.name, Images.is_main] + [Images.hotel]
    column_default_sort = [(Images.name, True), (Images.id, False)]
    
    # Информация о пользователи
    column_details_list = [column.name for column in Images.__table__.c] + [Images.hotel]