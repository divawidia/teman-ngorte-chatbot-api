"""empty message

Revision ID: 7d8a3c7b6fd4
Revises: 3e7529786684
Create Date: 2022-12-04 22:16:51.095902

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d8a3c7b6fd4'
down_revision = '3e7529786684'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_msg', sa.Text(), nullable=False),
    sa.Column('bot_response', sa.Text(), nullable=False),
    sa.Column('user_timestamp', sa.DateTime(), nullable=True),
    sa.Column('bot_timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=mysql.BIGINT(display_width=20),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=mysql.BIGINT(display_width=20),
               nullable=True)

    op.drop_table('message')
    # ### end Alembic commands ###
