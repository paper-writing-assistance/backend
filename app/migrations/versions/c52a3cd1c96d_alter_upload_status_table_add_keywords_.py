"""alter upload status table add 'keywords_extracted'

Revision ID: c52a3cd1c96d
Revises: bbbbb7cfa9f0
Create Date: 2024-06-25 17:27:10.659538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = 'c52a3cd1c96d'
down_revision: Union[str, None] = 'bbbbb7cfa9f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('uploadstatus', sa.Column('keywords_extracted', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('uploadstatus', 'keywords_extracted')
    # ### end Alembic commands ###
