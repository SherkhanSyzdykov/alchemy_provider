from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    String,
    BigInteger,
    ForeignKey,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from settings import settings
from .base import AbstractBaseMapper, Base


class Post(AbstractBaseMapper):
    __tablename__ = 'post'


    created_at = Column(
        DateTime(timezone=settings.USE_TIMEZONE),
        nullable=False,
        default=datetime.utcnow()
    )
    updated_at = Column(
        DateTime(timezone=settings.USE_TIMEZONE),
        onupdate=datetime.utcnow()
    )

    # uuid of user who creates this post
    created_by_uuid = Column(UUID(as_uuid=True), nullable=False)

    views = relationship('View', back_populates='post')
    likes = relationship('Like', back_populates='post')
    images = relationship('Image', back_populates='post')
    videos = relationship('Video', back_populates='post')


class Image(Base):
    """
    How many images can have a post???
    """
    __tablename__ = 'post_image'

    url = Column(String, nullable=False)

    post_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey(f'{Post.__tablename__}.{Post.uuid.name}', ondelete='CASCADE'),
        nullable=False, index=True
    )
    post = relationship('Post', back_populates='images')


class Video(Base):
    """
    How many videos can have a post???
    """
    __tablename__ = 'post_video'

    url = Column(String, nullable=False)

    post_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey(f'{Post.__tablename__}.{Post.uuid.name}',
                   ondelete='CASCADE'),
        nullable=False, index=True
    )
    post = relationship('Post', back_populates='videos')


class View(Base):
    """
    Implements view behavior of post
    """
    __tablename__ = 'post_view'

    post_uuid = Column(
        BigInteger,
        ForeignKey(
            f'{Post.__tablename__}.{Post.uuid.name}',
            ondelete='CASCADE'
        ),
        nullable=False, index=True
    )
    post = relationship('Post', back_populates='views')
    # uuid of user who views the post
    user_uuid = Column(BigInteger, nullable=False, index=True)

    __table_args__ = PrimaryKeyConstraint(
        post_uuid, user_uuid,
        'post_uuid_user_uuid_pk_constraint'
    )


class Like(Base):
    """
    Implements like behavior of post
    """
    __tablename__ = 'post_like'

    post_uuid = Column(
        BigInteger,
        ForeignKey(
            f'{Post.__tablename__}.{Post.uuid.name}',
            ondelete='CASCADE'
        ),
        nullable=False, index=True
    )
    post = relationship('Post', back_populates='likes')
    # uuid of user who views the post
    user_uuid = Column(BigInteger, nullable=False, index=True)

    __table_args__ = PrimaryKeyConstraint(
        post_uuid, user_uuid,
        'post_uuid_user_uuid_pk_constraint'
    )

