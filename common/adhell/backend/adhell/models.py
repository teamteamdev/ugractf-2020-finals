from sqlalchemy import (
    Column,
    ForeignKey,
    UniqueConstraint,
    Boolean, Date, Integer, String, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Partner(Base):
    __tablename__ = 'partner'

    id = Column(Integer, primary_key=True)
    ip = Column(String, nullable=False)
    name = Column(String, nullable=False)
    balance = Column(Integer, default=1, nullable=False)
    views = Column(Integer, default=0, nullable=False)

    banners = relationship('Banner', back_populates='owner')
    outcoming_transfers = relationship(
        'Transfer',
        foreign_keys='Transfer.sender_id',
        back_populates='sender'
    )
    incoming_transfers = relationship(
        'Transfer',
        foreign_keys='Transfer.receiver_id',
        back_populates='receiver'
    )


class Banner(Base):
    __tablename__ = 'banner'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    format = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(
        Integer,
        ForeignKey('partner.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

    owner = relationship('Partner', back_populates='banners')


class Transfer(Base):
    __tablename__ = 'transfer'

    id = Column(Integer, primary_key=True)

    sender_id = Column(
        Integer,
        ForeignKey('partner.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    receiver_id = Column(
        Integer,
        ForeignKey('partner.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    is_received = Column(Boolean, default=False, nullable=False)
    amount = Column(Integer, nullable=False)

    sender = relationship(
        'Partner',
        foreign_keys='Transfer.sender_id',
        back_populates='outcoming_transfers'
    )
    receiver = relationship(
        'Partner',
        foreign_keys='Transfer.receiver_id',
        back_populates='incoming_transfers'
    )
