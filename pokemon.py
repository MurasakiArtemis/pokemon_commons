import typing
import enum
import decimal
import sqlalchemy
from sqlalchemy.ext import declarative
from sqlalchemy import orm
import sqlalchemy_utils

Base = declarative.declarative_base()


class AbilitySlot(enum.Enum):
    FIRST = 'F'
    SECOND = 'S'
    HIDDEN = 'H'
    MEGA = 'M'


class TypeSlot(enum.Enum):
    PRIMARY = 'P'
    SECONDARY = 'S'


class Ability(Base):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(),
        nullable=False,
    )


class PokemonType(Base):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )


class EggGroup(Base):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )


pokemon_egg_group = sqlalchemy.Table(
    '',
    Base.metadata,
    sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('egg_group.id'),
        primary_key=True,
    ),
    sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('pokemon.id'),
        primary_key=True,
    ),
)


class Generation(Base):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )


class Region(Base):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )
    descriptor = sqlalchemy.Column(
        sqlalchemy.String(10),
        nullable=False,
    )


class PokemonDex(Base):
    region_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('region.id'),
        primary_key=True,
    )
    region = orm.relationship('Region', uselist=False)
    pokemon_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('pokemon.id'),
        primary_key=True,
    )
    regional_dex = sqlalchemy.Column(
        sqlalchemy.Integer(),
        nullable=False,
    )


class Pokemon(Base):
    national_dex = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )
    japanese_name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )
    japanese_transliteration = sqlalchemy.Column(
        sqlalchemy.String(50),
        nullable=False,
    )
    japanese_romanized = sqlalchemy.Column(
        sqlalchemy.String(50),
        nullable=False,
    )
    regional_numbers = orm.relationship('PokemonDex')
    egg_groups = orm.relationship(
        'EggGroup',
        secondary=pokemon_egg_group,
    )
    has_mega = sqlalchemy.Column(
        sqlalchemy.Boolean(),
        nullable=False,
    )
    mega_stone_pictures = orm.relationship('MegaStonePicture')
    forms = orm.relationship('Form')
    category = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )
    hatch_time = sqlalchemy.Column(
        sqlalchemy.Integer(),
        nullable=False,
    )
    experience_yield = sqlalchemy.Column(
        sqlalchemy.Integer(),
        nullable=False,
    )
    gender_code = sqlalchemy.Column(
        sqlalchemy.Float(
            4,
            asdecimal=True,
        ),
        nullable=False,
    )
    catch_rate = sqlalchemy.Column(
        sqlalchemy.Integer(),
        nullable=False,
    )
    introduced_generation = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('generation.id'),
    )
    base_friendship = sqlalchemy.Column(
        sqlalchemy.Integer(),
        nullable=False,
    )
    url = sqlalchemy.Column(
        sqlalchemy_utils.URLType(),
        nullable=False,
    )


class FormAbility(Base):
    ability_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('ability.id'),
        primary_key=True,
    )
    ability = orm.relationship('Ability')
    form_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('form.id'),
        primary_key=True,
    )
    slot = sqlalchemy.Column(
        sqlalchemy_utils.ChoiceType([
            ('F', 'First'),
            ('S', 'Second'),
            ('H', 'Hidden'),
            ('M', 'Mega'),
        ]),
        nullable=False,
    )


class FormType(Base):
    pokemon_type_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('pokemon_type.id'),
        primary_key=True,
    )
    pokemon_type = orm.relationship('PokemonType')
    form_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('form.id'),
        primary_key=True,
    )
    slot = sqlalchemy.Column(
        sqlalchemy_utils.ChoiceType([
            ('P', 'Primary'),
            ('S', 'Secondary'),
        ]),
        nullable=False,
    )


class MegaStonePicture(Base):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )
    image_relative_link = sqlalchemy.Column(
        sqlalchemy.String(50),
        nullable=False,
    )
    pokemon_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('pokemon.id'),
    )


class Form(Base):
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )
    image_relative_link = sqlalchemy.Column(
        sqlalchemy.String(500),
        nullable=False,
    )
    sprite_relative_link = sqlalchemy.Column(
        sqlalchemy.String(500),
        nullable=False,
    )
    weight = sqlalchemy.Column(
        sqlalchemy.Float(
            2,
            asdecimal=True,
        ),
        nullable=False,
    )
    height = sqlalchemy.Column(
        sqlalchemy.Float(
            2,
            asdecimal=True,
        ),
        nullable=False,
    )
    pokemon_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('pokemon.id'),
    )
