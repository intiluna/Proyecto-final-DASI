"""empty message

Revision ID: 97f7d2ba5cb7
Revises: c57feda6ea0a
Create Date: 2023-08-25 10:35:04.492584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97f7d2ba5cb7'
down_revision = 'c57feda6ea0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pedido_producto',
    sa.Column('pedido_id', sa.Integer(), nullable=True),
    sa.Column('producto_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ),
    sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], )
    )
    op.drop_table('lista_producto')
    op.drop_table('listas')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('listas',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('listas_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('fecha_recogida', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='listas_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='listas_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('lista_producto',
    sa.Column('lista_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('producto_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['lista_id'], ['listas.id'], name='lista_producto_lista_id_fkey'),
    sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], name='lista_producto_producto_id_fkey')
    )
    op.drop_table('pedido_producto')
    # ### end Alembic commands ###
