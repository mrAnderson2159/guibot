from src.base_controller import BaseController
from pynput.mouse import Button, Controller
from src.point import Point
from src.enums import Interval
from src.logger import get_logger

logger = get_logger(__name__)
mouse = Controller()


class MouseController(BaseController):
    @staticmethod
    def get_position() -> Point:
        """ Get the current mouse position.

        :return: Point representing the current mouse position.
        """
        position = mouse.position
        logger.debug(f"Current mouse position: {position}")
        return Point(*position)

    @classmethod
    def press(cls):
        """ Press the left mouse button. """
        cls.wait(Interval.SHORT)
        logger.info("Pressing the left mouse button.")
        mouse.press(Button.left)

    @classmethod
    def release(cls):
        """ Release the left mouse button. """
        logger.info("Releasing the left mouse button.")
        mouse.release(Button.left)
        cls.wait(Interval.INSTANT)

    @classmethod
    def click(cls, must_wait: bool = True):
        """ Click the left mouse button.

        :param must_wait: If True, it will wait for a short interval before clicking."""
        if must_wait:
            cls.wait(Interval.SHORT)
        logger.info("Clicking the left mouse button.")
        mouse.click(Button.left)

    @classmethod
    def move_by_offset(cls, x: int, y: int, slowly: bool = False, elapsed_time: float = .8, definition: int = 80):
        """ Move the mouse of x and y pixels.

        :param x: Horizontal movement in pixels.
        :param y: Vertical movement in pixels.
        :param slowly: If True, it will be simulated the movement of the pointer
        :param elapsed_time: Time in seconds to complete the movement. (Slowly must be True)
        :param definition: Number of steps to divide the movement into. A higher value means smoother movement but slower execution.
        (Slowly must be True)
        """
        if slowly:
            logger.info(f"Moving the mouse slowly to ({x}, {y}) over {elapsed_time} seconds with {definition} steps.")

            if not elapsed_time > 0 and definition > 0:
                message = (f"Elapsed time and definition must be greater than zero. "
                           f"Elapsed time: {elapsed_time}, Definition: {definition}")
                logger.error(message)
                raise ValueError(message)

            part_x = round(x / definition)
            part_y = round(y / definition)

            for _ in range(definition):
                logger.debug(f"Moving mouse by ({part_x}, {part_y})")
                mouse.move(part_x, part_y)
                logger.debug(f"Mouse position after move: {mouse.position}")
                logger.debug(f"Sleeping for {elapsed_time / definition} seconds")
                cls.wait(elapsed_time / definition)
        else:
            cls.wait(Interval.SHORT)
            logger.info(f"Moving the mouse instantly to ({x}, {y}).")
            mouse.move(x, y)

    @classmethod
    def scroll(cls, x: int, y: int):
        """ Scroll the mouse wheel

        :param x: Horizontal scroll amount (positive for right, negative for left).
        :param y: Vertical scroll amount (positive for down, negative for up).
        """
        cls.wait(Interval.SHORT)
        logger.info(f"Scrolling the mouse wheel by ({x}, {y}).")
        mouse.scroll(x, y)

    @staticmethod
    def move_to(point: Point):
        """ Move the mouse to a specific point.

        :param point: Point to move the mouse to.
        """
        logger.info(f"Moving the mouse to point: {point}")
        mouse.position = point.tuple

    @classmethod
    def click_at(cls, point: Point, wait: float = 0.2):
        """ Click at a specific point.

        :param point: Point to click at.
        :param wait: Time to wait before clicking.
        """
        logger.info(f"Preparing to click at: {point} in {wait} seconds.")
        cls.move_to(point)
        cls.wait(wait)
        cls.click(must_wait=False)

    @classmethod
    def drag_offset(cls, starting_point: Point, x: int, y: int, elapsed_time: float = .8, definition: int = 80):
        """ Drag the mouse from a starting point to a new position with a specified offset.

        :param starting_point: Point to start dragging from.
        :param x: Horizontal offset from the starting point.
        :param y: Vertical offset from the starting point.
        :param elapsed_time: Time in seconds to complete the drag.
        :param definition: Number of steps to divide the drag into. A higher value means smoother movement but slower execution.
        """
        logger.info(f"Dragging from {starting_point} to ({x}, {y}) over {elapsed_time} seconds with {definition} steps.")
        cls.move_to(starting_point)
        cls.press()
        cls.move_by_offset(x, y, slowly=True, elapsed_time=elapsed_time, definition=definition)
        cls.release()

    @classmethod
    def drag_to(cls, starting_point: Point, target_point: Point, elapsed_time: float = .8, definition: int = 80):
        """ Drag the mouse from a starting point to a target point.

        :param starting_point: Point to start dragging from.
        :param target_point: Point to drag to.
        :param elapsed_time: Time in seconds to complete the drag.
        :param definition: Number of steps to divide the drag into. A higher value means smoother movement but slower execution.
        """
        logger.info(f"Dragging from {starting_point} to {target_point} over {elapsed_time} seconds with {definition} steps.")
        x_offset = target_point.int_x - starting_point.int_x
        y_offset = target_point.int_y - starting_point.int_y
        cls.drag_offset(starting_point, x_offset, y_offset, elapsed_time=elapsed_time, definition=definition)
