import asyncio
import logging
from time import sleep
from PIL import Image
import os

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    logging.debug("Я молодец")


@celery_instance.task
def resize_image(image_path: str):
    logging.debug(f"Вызывается функция resize_image с {image_path=}")
    sizes = [200, 500, 1000]
    output_folder = "src/static/images"

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)

        img_resized.save(output_path)


async def get_bookings_with_today_checkin_helper():
    logging.debug("Я ЗАПУСКАЮСЬ")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")

@celery_instance.task(name="booking_today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())