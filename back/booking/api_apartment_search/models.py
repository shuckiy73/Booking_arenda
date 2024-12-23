from datetime import datetime, timedelta  # Добавлен импорт datetime и timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CountryModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Страна")
    geographic_coordinates = models.CharField(max_length=100, null=True, blank=True, verbose_name="Географические координаты")

    class Meta:
        db_table = 'api_countries'  # Удалены лишние кавычки
        verbose_name_plural = 'Страны'
        verbose_name = 'Страна'

    def __str__(self):
        return self.name


class RegionModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название региона")
    geographic_coordinates = models.CharField(max_length=100, null=True, blank=True, verbose_name="Географические координаты")
    country = models.ForeignKey(CountryModel, on_delete=models.DO_NOTHING, related_name='regions', verbose_name="Страна")

    class Meta:
        db_table = 'api_regions'  # Удалены лишние кавычки
        verbose_name_plural = 'Регионы'
        verbose_name = 'Регион'

    def __str__(self):
        return f"{self.name} - {self.country}"


class CityModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название города")
    geographic_coordinates = models.CharField(max_length=100, null=True, blank=True, verbose_name="Географические координаты")
    region = models.ForeignKey(RegionModel, on_delete=models.DO_NOTHING, related_name='cities', verbose_name="Регион")
    country = models.ForeignKey(CountryModel, on_delete=models.DO_NOTHING, related_name='cities', verbose_name="Страна")

    class Meta:
        db_table = 'api_cities'  # Удалены лишние кавычки
        verbose_name_plural = 'Города'
        verbose_name = 'Город'

    def __str__(self):
        return f"{self.name} - {self.country}"


class StreetTypeModel(models.Model):
    """
    бульвар
    переулок
    проспект
    улица
    шоссе
    другое:   # TODO пока что сделано без другого, все в одном
        аллея
        дорога
        дорожка
        жилмассив
        киломерт
        линия
        набережная
        площадь
        проезд
        просека
        просёлок
        проулок
        спуск
        трасса
        тупик
    """
    street_type = models.CharField(max_length=100, verbose_name="Тип улицы")

    class Meta:
        db_table = 'api_streettypes'  # Удалены лишние кавычки
        verbose_name_plural = 'Типы улиц'
        verbose_name = 'Тип улицы'

    def __str__(self):
        return self.street_type


class AddressModel(models.Model):
    street_name = models.CharField(max_length=100, verbose_name="Название улицы")
    building_number = models.IntegerField(blank=True, null=True, verbose_name="Номер дома")
    corps = models.IntegerField(blank=True, null=True, verbose_name="Корпус")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Местоположение")
    street_type = models.ForeignKey(StreetTypeModel, on_delete=models.DO_NOTHING, verbose_name="Тип улицы")
    has_elevator = models.BooleanField(default=False, verbose_name="Наличие лифта")

    class Meta:
        db_table = 'api_addresses'  # Удалены лишние кавычки
        verbose_name_plural = "Адреса зданий"
        verbose_name = "Адрес здания"

    def __str__(self):
        corps = f"к. {self.corps}" if self.corps else ''
        return f"{self.street_type} {self.street_name} {self.building_number} {corps}"


class BuildingGroupTypeModel(models.Model):
    """
    Номера, спальные места - в отеле, гостевом доме или хостеле - desc Гостям будет предоставлен номер в отеле, гостевом доме или спальное место в хостеле
    Квартиры, апартаменты - целиком - desc Гости снимут квартиру целиком. Вместе со всеми удобствами и кухней
    Дома, коттеджи - целиком - desc Гости снимут дом целиком. Вместе с пристройками
    Отдельные комнаты - целиком - desc Гости снимут отдельную комнату со спальным местом
    """
    building_group_type = models.CharField(max_length=100, unique=True, verbose_name="Группа строения")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        db_table = 'api_buildinggrouptypes'  # Удалены лишние кавычки
        verbose_name_plural = 'Группы строений'
        verbose_name = 'Группа строения'

    def __str__(self):
        return self.building_group_type


class BuildingTypeModel(models.Model):
    """
    Номера, спальные места -
        Отель
        Апарт-отель
        Капсюльный отель
        Санаторий
        Гостиница
        Мини-гостиница
        Хостел
        База отдыха
        Апартамент
        Гостевой дом
        Отель эконом-класса
        Пансионат
        Глэмпинг
    Квартиры, апартаменты
        Квартира
        Апартамент
        Студия
    Дома, коттеджи
        Коттедж
        Часть дома с отдельным входом
        Таунхаус
        Шале
        Особняк
        Дом
        Эллинг
        Целый этаж в доме
        Бунгало
        Яхта
        Вилла
        Деревенский дом
        Гестхаус
        Дом на колёсах
        Дача
    Отдельные комнаты
        Комната в квартире
        Комната в частном доме
        Комната в коттедже
    """
    building_type_name = models.CharField(max_length=100, verbose_name="Тип строения")
    building_type_group = models.ForeignKey(BuildingGroupTypeModel, on_delete=models.DO_NOTHING, verbose_name="Группа строения")

    class Meta:
        db_table = 'api_buildingtype'  # Удалены лишние кавычки
        verbose_name_plural = 'Типы строений'
        verbose_name = 'Тип строения'

    def __str__(self):
        return f"{self.building_type_name} - {self.building_type_group}"


class GeneralInformationModel(models.Model):
    WITHOUT_KITCHEN = 'без кухни'
    SEPARATE_KITCHEN = 'отдельная кухня'
    KITCHEN_LIVING_ROOM = 'кухня-гостинная'
    KITCHEN_AREA = 'кухонная зона'

    KITCHEN_CHOICES = (
        (WITHOUT_KITCHEN, 'без кухни'),
        (SEPARATE_KITCHEN, 'отдельная кухня'),
        (KITCHEN_LIVING_ROOM, 'кухня-гостинная'),
        (KITCHEN_AREA, 'кухонная зона'),
    )

    WITHOUT_REPAIR = 'без ремонта'
    RENDECORATING = 'косметический ремонт'  # Исправлено на RENDECORATING
    EURO_RENOVATION = 'евро ремонт'
    DESIGNER = 'дизайнерский'

    REPAIR_CHOICES = (
        (WITHOUT_REPAIR, 'без ремонта'),
        (RENDECORATING, 'косметический ремонт'),  # Исправлено на RENDECORATING
        (EURO_RENOVATION, 'евро ремонт'),
        (DESIGNER, 'дизайнерский'),
    )

    room_square = models.FloatField(null=True, blank=True, verbose_name="Площадь комнаты")
    floor = models.PositiveIntegerField(null=True, blank=True, verbose_name="Этаж")
    floor_in_the_house = models.PositiveIntegerField(null=True, blank=True, verbose_name="Этажей в доме")
    rooms_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Количество комнат")
    guests_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Количество гостей")
    count_sleeping_places = models.PositiveIntegerField(null=True, blank=True, verbose_name="Количество спальных мест")

    kitchen = models.CharField(
        max_length=100,  # Добавлен max_length
        choices=KITCHEN_CHOICES,
        default=WITHOUT_KITCHEN,
        verbose_name="Кухня"
    )
    room_repair = models.CharField(
        max_length=100,  # Добавлен max_length
        choices=REPAIR_CHOICES,
        default=WITHOUT_REPAIR,
        verbose_name="Ремонт комнаты"
    )

    class Meta:
        db_table = 'api_general_info'  # Удалены лишние кавычки
        verbose_name_plural = 'Общая информация'
        verbose_name = 'Общая информация'

    def __str__(self):
        return f"{self.room_square}м2 | {self.floor}/{self.floor_in_the_house} | ком {self.rooms_count} | {self.room_repair}"


class BedTypesModel(models.Model):
    """
    односпальная кровать
    двуспальная кровать
    двуспальная диван-кровать
    двуспальная широкая (king-size)
    особо широкая двуспальная (super-king-size)
    двухъярусная кровать
    диван кровать
    """
    bed_type = models.CharField(max_length=100, unique=True, verbose_name="Тип кровати")

    class Meta:
        db_table = 'api_bedtypes'  # Удалены лишние кавычки
        verbose_name_plural = 'Типы спальных мест'
        verbose_name = 'Тип спального места'

    def __str__(self):
        return self.bed_type


class BathroomAmenitiesModel(models.Model):
    """
        биде
        ванна
        гигиенический душ
        дополнительная ванная
        дополнительный туалет
        душ
        общая ванная комната
        общий туалет
        полотенца
        сауна
        тапочки
        туалетные принадлежности
        фен
        халат
        общий душ/душевая
    """
    bathroom_amenities_name = models.CharField(max_length=100, unique=True, verbose_name="Удобства ванной комнаты")

    class Meta:
        db_table = 'api_bathroomamenities'  # Удалены лишние кавычки
        verbose_name_plural = 'Типы ванной комнаты'
        verbose_name = 'Тип ванной комнаты'

    def __str__(self):
        return self.bathroom_amenities_name


class CategoriesAmenitiesModel(models.Model):
    """
    Удобства
        Популярные услуги и удобства, на которые чаще всего обращаются гости при поиске жилья. После публикации можно добавить другие
    Вид из окон
        Укажите, что можно увидеть из окон вашего объекта. В разделе «Фото» загрузите фотографии всех видов, которые вы отметили
    Кухонное оборудование
    Оснащение
    Для отдыха в помещении
    Оснащение двора
    Инфраструктура и досуг рядом
    Для детей
    """
    categories_amenities_title = models.CharField(max_length=100, unique=True, verbose_name="Название категории удобств")
    categories_amenities_description = models.TextField(null=True, blank=True, verbose_name="Описание категории удобств")

    class Meta:
        db_table = 'api_categoriesamenities'  # Удалены лишние кавычки
        verbose_name_plural = 'Категории удобств'
        verbose_name = 'Категория удобства'

    def __str__(self):
        return self.categories_amenities_title


class AmenitiesModel(models.Model):  # Amenities - удобства
    """
    """
    amenities_name = models.CharField(max_length=100, unique=True, verbose_name="Название удобства")
    amenities_description = models.CharField(max_length=100, null=True, blank=True, verbose_name="Описание удобства")
    amenities_category = models.ForeignKey(CategoriesAmenitiesModel, on_delete=models.DO_NOTHING, verbose_name="Категория удобств")

    class Meta:
        db_table = 'api_amenities'  # Удалены лишние кавычки
        verbose_name_plural = 'Удобства'
        verbose_name = 'Удобство'

    def __str__(self):
        return self.amenities_name


class PlacingRulesModel(models.Model):
    with_children = models.BooleanField(default=False, verbose_name="С детьми любого возраста")
    with_animals = models.BooleanField(default=False, verbose_name="С животными")
    smoking_is_allowed = models.BooleanField(default=False, verbose_name="Курение разрешено")
    parties_are_allowed = models.BooleanField(default=False, verbose_name="Вечеринки разрешены")
    accounting_documents = models.BooleanField(default=False, verbose_name="Предоставление документов")

    class Meta:
        db_table = 'api_placingrules'  # Удалены лишние кавычки
        verbose_name_plural = 'Правила размещения'
        verbose_name = 'Правило размещения'


class ObjectRoomModel(models.Model):
    CREDIT_CARD = 'Картой'
    CASH = 'Наличными'
    WIRE_TRANSFER = 'Перевод'

    PAYMENT_METHOD_CHOICES = [
        (CREDIT_CARD, 'Картой'),
        (CASH, 'Наличными'),
        (WIRE_TRANSFER, 'Перевод'),
    ]

    title = models.CharField(max_length=100, verbose_name="Название объекта")
    building_description = models.TextField(verbose_name="Описание объекта")
    prepayment = models.FloatField(default=0.0, verbose_name="Предоплата")
    payment_day = models.FloatField(default=0.0, verbose_name="Оплата за сутки")
    payment_method = models.CharField(
        max_length=100,  # Добавлен max_length
        choices=PAYMENT_METHOD_CHOICES,
        default=CASH,
        verbose_name="Метод оплаты"
    )
    address = models.ForeignKey(AddressModel, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Адрес")
    arrival_time = models.TimeField(default=datetime.now().strftime('%H:%M'), verbose_name="Заезд")
    departure_time = models.TimeField(default=(datetime.now() + timedelta(hours=1)).strftime('%H:%M'), verbose_name="Отъезд")
    minimum_length_of_stay = models.PositiveIntegerField(default=1, verbose_name="Минимальное количество дней заселения")
    placing_rules = models.ForeignKey(PlacingRulesModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Правила размещения")
    general_info = models.ForeignKey(GeneralInformationModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Общая информация")
    building_info = models.ForeignKey(BuildingTypeModel, on_delete=models.DO_NOTHING, verbose_name="Информация о строении")
    city = models.ForeignKey(CityModel, on_delete=models.DO_NOTHING, verbose_name="Город")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано ?")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Собственник")

    class Meta:
        db_table = 'api_objectrooms'  # Удалены лишние кавычки
        verbose_name_plural = 'Объекты'
        verbose_name = 'Объект'

    def __str__(self):
        return self.title


class FavoritesModel(models.Model):
    room_object = models.ForeignKey(ObjectRoomModel, on_delete=models.DO_NOTHING, verbose_name="Объект")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Пользователь")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = 'api_favorites'  # Удалены лишние кавычки
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = (('room_object', 'user'),)


class ReservationModel(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reserved_user', verbose_name='Жилец')
    room = models.ForeignKey(ObjectRoomModel, on_delete=models.DO_NOTHING, related_name='room', verbose_name='Комната')
    start_date = models.DateField('Заселение')
    end_date = models.DateField('Выселение')
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = 'api_reservation'  # Удалены лишние кавычки
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        unique_together = (('room', 'start_date', 'end_date'),)

    def __str__(self):
        return f'Пользователь {self.tenant}. Бронь с {self.start_date} по {self.end_date}'


class RatingModel(models.Model):
    cleanliness = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Чистота")
    conformity_to_photos = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Соответствие фото")
    timeliness_of_check_in = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Своевременность заселения")
    price_quality = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Цена-качество")
    location = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Расположение")
    quality_of_service = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Качество обслуживания")
    object_room = models.ForeignKey(ObjectRoomModel, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Объект")

    class Meta:
        db_table = 'api_ratings'  # Удалены лишние кавычки
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return f"{(self.cleanliness + self.conformity_to_photos + self.timeliness_of_check_in + self.price_quality + self.location + self.quality_of_service)/6}"


class ReviewsModel(models.Model):
    review_text = models.TextField(null=True, blank=True, verbose_name="Отзыв")
    review_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    review_updated = models.DateTimeField(auto_now_add=True, verbose_name="Дата редактирования")
    likes = models.PositiveIntegerField(default=0, verbose_name="Нравится")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Не нравится")
    room_object = models.ForeignKey(ObjectRoomModel, on_delete=models.DO_NOTHING, verbose_name="Объект")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Пользователь")
    ratings = models.ForeignKey(RatingModel, on_delete=models.CASCADE, verbose_name="Оценки")

    class Meta:
        db_table = 'api_reviews'  # Удалены лишние кавычки
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = (('room_object', 'user'),)


class ImagesModel(models.Model):
    image_path = models.CharField(verbose_name="Путь до изображения", max_length=2000)
    room_object = models.ForeignKey(ObjectRoomModel, on_delete=models.DO_NOTHING, verbose_name="Объект")

    class Meta:
        db_table = 'api_images'  # Удалены лишние кавычки
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        unique_together = (('room_object', 'image_path'),)

    def __str__(self):
        return f"Изображение для объекта {self.room_object.title}"