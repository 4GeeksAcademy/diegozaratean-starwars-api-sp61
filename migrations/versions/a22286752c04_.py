"""empty message

Revision ID: a22286752c04
Revises: ba049e49ce47
Create Date: 2024-05-08 18:03:08.098215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a22286752c04'
down_revision = 'ba049e49ce47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('videojuego', schema=None) as batch_op:
        batch_op.add_column(sa.Column('empresa_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'empresa', ['empresa_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('videojuego', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('empresa_id')

    # ### end Alembic commands ###
