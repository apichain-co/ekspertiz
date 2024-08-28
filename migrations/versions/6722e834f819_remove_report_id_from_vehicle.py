from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6722e834f819'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Use batch mode to drop the report_id column
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.drop_column('report_id')

def downgrade():
    # Re-add the report_id column and foreign key constraint
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('report_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(None, 'report', ['report_id'], ['id'])
