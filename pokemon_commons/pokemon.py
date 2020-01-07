import typing
import enum
import decimal
import sqlalchemy
from sqlalchemy.ext import declarative
from sqlalchemy import orm
import sqlalchemy_utils

Base = declarative.declarative_base()
base_table_name = 'pokedex'

table_names = {
    'ability': f'{base_table_name}_abilities',
    'type': f'{base_table_name}_type',
    'egg_group': f'{base_table_name}_egg_group',
    'generation': f'{base_table_name}_generation',
    'region': f'{base_table_name}_region',
    'pokemon_dex': f'{base_table_name}_pokemon_dex',
    'pokemon': f'{base_table_name}_pokemon',
    'form_ability': f'{base_table_name}_form_ability',
    'form_type': f'{base_table_name}_form_type',
    'mega_stone_picture': f'{base_table_name}_mega_stone_picture',
    'form': f'{base_table_name}_form',
}


class AbilitySlot(enum.Enum):
    FIRST = 'F'
    SECOND = 'S'
    HIDDEN = 'H'
    MEGA = 'M'


class TypeSlot(enum.Enum):
    PRIMARY = 'P'
    SECONDARY = 'S'


class Ability(Base):
    __tablename__ = table_names.get('ability')
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(),
        nullable=False,
    )


class PokemonType(Base):
    __tablename__ = table_names.get('type')
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )


class EggGroup(Base):
    __tablename__ = table_names.get('egg_group')
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )


pokemon_egg_group = sqlalchemy.Table(
    f'{base_table_name}_{table_names.get("pokemon")}_{table_names.get("egg_group")}',
    Base.metadata,
    sqlalchemy.Column(
        f'{table_names.get("egg_group")}_id',
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(f'{table_names.get("egg_group")}.id'),
        primary_key=True,
    ),
    sqlalchemy.Column(
        f'{table_names.get("pokemon")}_id',
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(f'{table_names.get("pokemon")}.national_dex'),
        primary_key=True,
    ),
)


class Generation(Base):
    __tablename__ = table_names.get('generation')
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(20),
        nullable=False,
    )


class Region(Base):
    __tablename__ = table_names.get('region')
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
    __tablename__ = table_names.get('pokemon_dex')
    region_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(f'{table_names.get("region")}.id'),
        primary_key=True,
    )
    region = orm.relationship('Region', uselist=False)
    pokemon_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(f'{table_names.get("pokemon")}.national_dex'),
        primary_key=True,
    )
    regional_dex = sqlalchemy.Column(
        sqlalchemy.Integer(),
        nullable=False,
    )


class Pokemon(Base):
    __tablename__ = table_names.get('pokemon')
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
        sqlalchemy.ForeignKey(f'{table_names.get("generation")}.id'),
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
    __tablename__ = table_names.get('form_ability')
    ability_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(f'{table_names.get("ability")}.id'),
        primary_key=True,
    )
    ability = orm.relationship('Ability')
    form_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(f'{table_names.get("form")}.id'),
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
    __tablename__ = table_names.get('form_type')
    pokemon_type_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(f'{table_names.get("type")}.id'),
        primary_key=True,
    )
    pokemon_type = orm.relationship('PokemonType')
    form_id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey(f'{table_names.get("form")}.id'),
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
    __tablename__ = table_names.get('mega_stone_picture')
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
        sqlalchemy.ForeignKey(f'{table_names.get("pokemon")}.national_dex'),
    )


class Form(Base):
    __tablename__ = table_names.get('form')
    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        primary_key=True,
    )
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
        sqlalchemy.ForeignKey(f'{table_names.get("pokemon")}.national_dex'),
    )
