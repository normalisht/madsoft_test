"""init

Revision ID: 12c00b733bd8
Revises:
Create Date: 2024-06-28 23:07:05.596512

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12c00b733bd8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'meme',
        sa.Column('filename', sa.String(length=64), nullable=False),
        sa.Column('description', sa.String(length=512), nullable=True),
        sa.Column('image_url', sa.String(length=2096), nullable=True),
        sa.Column(
            'expires_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_meme_filename'), 'meme', ['filename'], unique=True
    )
    op.create_index(op.f('ix_meme_id'), 'meme', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_meme_id'), table_name='meme')
    op.drop_index(op.f('ix_meme_filename'), table_name='meme')
    op.drop_table('meme')
    # ### end Alembic commands ###
