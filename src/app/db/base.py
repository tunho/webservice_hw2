# Import all the models, so that Base has them before being
# imported by Alembic or init scripts
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.book import Book  # noqa
from app.models.order import Order  # noqa
from app.models.order_item import OrderItem  # noqa
from app.models.cart import Cart  # noqa
from app.models.cart_item import CartItem  # noqa
from app.models.review import Review  # noqa
from app.models.comment import Comment  # noqa
from app.models.favorite import Favorite  # noqa
from app.models.book_view import BookView  # noqa
from app.models.notification import Notification  # noqa
from app.models.inquiry import Inquiry  # noqa
from app.models.notice import Notice  # noqa
from app.models.log import Log  # noqa
from app.models.ranking import Ranking  # noqa
from app.models.comment_like import CommentLike  # noqa
